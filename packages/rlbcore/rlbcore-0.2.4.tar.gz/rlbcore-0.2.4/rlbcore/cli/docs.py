"""Code for cli commands `rlb<project> docs ...`."""
import contextlib
import shutil
import subprocess
import typing as t
from pathlib import Path

import attrs
import typer
import yaml
from omegaconf import DictConfig, OmegaConf

import rlbcore

app = typer.Typer()
_SECTION_CONFIG_FILE_NAME = ".config.yml"
_RLB_PROJECT_NAMES = t.Literal["rlbcore", "rlbtorch", "rlbtf", "rlbjax", "rlbft"]


@attrs.define()
class _SectionConfig:
    config: DictConfig

    @classmethod
    def from_path(cls, path: Path) -> "_SectionConfig":
        config = OmegaConf.load(path)
        assert isinstance(config, DictConfig)
        return cls(config=config)

    @property
    def order(self) -> list[str]:
        """Defines the order of the sections in the docs.

        Returns:
            The order of the sections in the docs.

        Example: Specifying the order of the sections in the docs
            Suppose you have the following directory structure:
            ```
            docs
            └── sections
                └── section_1
                    ├── .config.yml
                    ├── foo.md
                    ├── bar.md
                    ├── foobar.md
                    └── section_1_1
                        ├── .config.yml
                        ├── baz.md
                        └── qux.md
            ```
            with `section_1/.config.yml` containing:
            ```yaml
            order:
                - foo
                - bar
                - section_1_1
                - foobar
            ```
            and `section_1/section_1_1/.config.yml` containing:
            ```
            order:
                - qux
                - baz
            ```
            Then the order of the sections in the docs will be:
            ```
            section_1
            ├── foo
            ├── bar
            ├── section_1_1
            │   ├── qux
            │   └── baz
            └── foobar
            ```
        """
        return self.config.order


@attrs.define()
class _RepoPaths:
    """Paths to the various directories in the repo.

    REQUIRED ENV VARS:
        The following env vars are required for this command to work:
            - RLB_REPO_ROOT: The path to the root of the RLBaselines project using
                `rlbcore`.
    """

    rlb_project_name: _RLB_PROJECT_NAMES
    rlb_repo_root: Path

    @property
    def mkdocs_config_file(self) -> Path:
        return self.rlb_repo_root / "mkdocs.yml"

    @property
    def docs_dir(self) -> Path:
        return self.rlb_repo_root / "docs"

    @property
    def resources_dir(self) -> Path:
        return self.docs_dir / "resources"

    @property
    def directory_structure_file(self) -> Path:
        return self.resources_dir / "markdown" / "directory_structure.md"

    @property
    def references_dir(self) -> Path:
        return self.docs_dir / "references"

    @property
    def algorithms_dir(self) -> Path:
        return self.docs_dir / "algorithms"

    @property
    def sections_dir(self) -> Path:
        return self.docs_dir / "sections"

    @property
    def src_code_dir(self) -> Path:
        return self.rlb_repo_root / self.rlb_project_name


@app.command()
def build(
    force_recreate_references: bool = typer.Option(
        False, "--force-recreate-references", "-f", help="Force recreate references."
    ),
    rlb_repo_root: str = typer.Option(
        str(rlbcore.REPO_ROOT.resolve()),
        "-r",
        "--rlb-repo-root",
        help="The path to the root of the RLBaselines project using `rlbcore`.",
    ),
    rlb_project_name: str = typer.Option(
        "rlbcore",
        "-n",
        "--rlb-project-name",
        help="The name of the project. This is used to get the correct modules for the "
        + "documentation. Valid values are: rlbcore, rlbtorch, rlbtf, rlbjax, rlbft.",
    ),
):
    """Generate the docs.

    REQUIRED ENV VARS:
        The following env vars are required for this command to work:

        - `RLB_REPO_ROOT`: The path to the root of the RLBaselines project using
            `rlbcore`.
        - `RLB_PROJECT_NAME`: The name of the project. This is used to get the correct
            modules for the documentation. Valid values are:
            - `rlbcore`
            - `rlbtorch`
            - `rlbtf`
            - `rlbjax`
            - `rlbft`
    """
    if rlb_project_name not in ["rlbcore", "rlbtorch", "rlbtf", "rlbjax", "rlbft"]:
        raise ValueError(
            f"Invalid value for `rlb_project_name`: {rlb_project_name}. "
            + "Valid values are: rlbcore, rlbtorch, rlbtf, rlbjax, rlbft."
        )
    typer.echo("Building the docs...")
    # Load the mkdocs.yml file
    repo_paths = _RepoPaths(
        rlb_repo_root=Path(rlb_repo_root),
        rlb_project_name=rlb_project_name,  # type: ignore
    )
    mkdocs = yaml.safe_load(repo_paths.mkdocs_config_file.read_text())
    # Get the nav links
    nav: list[dict[str, t.Any]] = mkdocs["nav"]
    # Other sections like Opinions etc.
    with contextlib.suppress(FileNotFoundError):
        _add_sections(
            nav,
            rlb_repo_root=repo_paths.rlb_repo_root,
            rlb_project_name=repo_paths.rlb_project_name,
        )
    # Add documentation describing the algorithms
    with contextlib.suppress(FileNotFoundError):
        _add_algorithm_references(
            nav,
            rlb_repo_root=repo_paths.rlb_repo_root,
            rlb_project_name=repo_paths.rlb_project_name,
        )
    # Add documentation describing the modules
    _add_references(
        nav,
        force_recreate_references,
        rlb_repo_root=repo_paths.rlb_repo_root,
        rlb_project_name=repo_paths.rlb_project_name,
    )
    # Generate the markdown file containing the directory structure so it can be shown
    # in the Architecture section
    _generate_directory_structure_file(
        rlb_repo_root=repo_paths.rlb_repo_root,
        rlb_project_name=repo_paths.rlb_project_name,
    )
    # Write the mkdocs.yml file
    repo_paths.mkdocs_config_file.write_text(yaml.dump(mkdocs))


def _get_path_tree(path: Path) -> dict[str, t.Any]:
    """Get a tree of the files in a directory.

    Given a directory structure like:
        |- rlbtorch
        |   |- memories
        |   |   |- experience_replay
        |   |   |   |- buffers.py
        |   |   |   |- prioritized.py
        |   |   |- __init__.py
        |   |- __init__.py
        |- __init__.py

    This function will return a dictionary which, when converted to yaml, looks like:
        - rlbtorch:
            - memories:
                - experience_replay:
                    - buffers.py
                    - prioritized.py
                - __init__.py
            - __init__.py
        - __init__.py
    """
    if path.is_file():
        return {path.stem: path}
    sub_paths = [
        _get_path_tree(p)
        for p in path.iterdir()
        if not any(
            (p.name.startswith("_"), p.name.startswith("."), p.name == "py.typed")
        )
    ]
    if all(x.name != _SECTION_CONFIG_FILE_NAME for x in path.iterdir()):
        return {path.stem: sub_paths}
    named_sub_paths = {}
    for sub_dict in sub_paths:
        assert len(sub_dict) == 1
        key = list(sub_dict.keys())[0]
        named_sub_paths[key] = sub_dict
    config_file_path = path / _SECTION_CONFIG_FILE_NAME
    assert config_file_path.exists()
    config = _SectionConfig.from_path(config_file_path)
    order = config.order
    ordered_sub_paths: list[dict[str, t.Any]] = [named_sub_paths[x] for x in order]
    return {path.stem: ordered_sub_paths}


def _iter_leaf_dicts(d: dict[str, t.Any]) -> t.Generator[dict[str, t.Any], None, None]:
    """Iterate through all leaf dictionaries in a dictionary."""
    if len(d) == 1 and isinstance(list(d.values())[0], Path):
        yield d
    else:
        for v in d.values():
            if isinstance(v, list):
                for i in v:  # type: ignore
                    yield from _iter_leaf_dicts(i)
            elif isinstance(v, dict):
                yield from _iter_leaf_dicts(v)


def _get_references(
    module: Path,
    rlb_repo_root: Path,
    rlb_project_name: _RLB_PROJECT_NAMES,
    create_reference: bool = True,
    path_tree: dict[str, t.Any] | None = None,
) -> dict[str, t.Any]:
    """Get reference markdown links for a module and its submodules."""
    repo_paths = _RepoPaths(
        rlb_repo_root=rlb_repo_root, rlb_project_name=rlb_project_name
    )
    path_tree = _get_path_tree(module)
    for leaf in _iter_leaf_dicts(path_tree):
        assert len(leaf) == 1
        path = list(leaf.values())[0]
        assert isinstance(path, Path)
        if path == repo_paths.src_code_dir:
            reference_path = repo_paths.references_dir / f"{path.stem}.md"
        else:
            reference_path = (
                repo_paths.references_dir
                / f"{path.relative_to(repo_paths.src_code_dir).with_suffix('')}.md"
            )
        if create_reference:
            # Create the reference file (including parent directories) if it doesn't
            # exist
            reference_path.parent.mkdir(parents=True, exist_ok=True)
            py_module_name = str(
                path.relative_to(repo_paths.src_code_dir).with_suffix("")
            ).replace("/", ".")
            reference_path.write_text(f"::: {rlb_project_name}.{py_module_name}")
        leaf[list(leaf.keys())[0]] = str(
            reference_path.relative_to(repo_paths.docs_dir)
        )
    return path_tree


def _transform_keys(
    maybe_nested_dict: dict[str, t.Any], key_transform: t.Callable[[str], str]
) -> dict[str, t.Any]:
    """Given a possibly nested dictionary, transform the keys of the dictionary.

    Args:
        maybe_nested_dict: The dictionary to transform
        key_transform: The function to transform the keys with

    Returns:
        A dictionary with the same structure as `maybe_nested_dict` but with the keys
        transformed by `key_transform`

    Example:
        ```python
        >>> _transform_keys({"a": {"b": 1}}, lambda k: k.upper())
        {'A': {'B': 1}}
        >>> _transform_keys({"foo": {"bar": 1}}, lambda k: k.capitalize())
        {'Foo': {'Bar': 1}}
        >>> _transform_keys({"foo": [{"bar": 1}, {"baz": 2}]}, lambda k: k.capitalize())
        {'Foo': [{'Bar': 1}, {'Baz': 2}]}

        ```
    """
    result: dict[str, t.Any] = {}
    for k, v in maybe_nested_dict.items():
        if isinstance(v, dict):
            result[key_transform(k)] = _transform_keys(v, key_transform)
        elif isinstance(v, list):
            result[key_transform(k)] = [
                _transform_keys(i, key_transform) for i in v  # type: ignore
            ]
        else:
            result[key_transform(k)] = v
    return result


def _add_algorithm_references(
    nav: list[dict[str, t.Any]],
    rlb_repo_root: Path,
    rlb_project_name: _RLB_PROJECT_NAMES,
) -> None:
    """Add a section named Algorithms to the docs side-bar nav links.

    Args:
        nav: The nav links in the mkdocs.yml file

    NOTE:
        Content is taken from .md files present directly in _ALGORITHM_DIR

    EFFECT:
        `nav` is modified to contain an Algorithms section.
    """

    def as_section_name(file: Path) -> str:
        return file.stem.replace("_", " ").title()

    # Remove the Algorithms key and its values if it already exists in nav
    for key in nav:
        if "Algorithms" in key:
            nav.remove(key)
            break
    repo_paths = _RepoPaths(
        rlb_repo_root=rlb_repo_root,
        rlb_project_name=rlb_project_name,
    )
    # Add the algorithms references
    references: list[dict[str, str]] = [
        {as_section_name(file): str(file.relative_to(repo_paths.docs_dir))}
        for file in repo_paths.algorithms_dir.iterdir()
        if file.suffix == ".md"
    ]
    nav.append({"Algorithms": references})


def _add_references(
    nav: list[dict[str, t.Any]],
    force_recreate_references: bool,
    rlb_repo_root: Path,
    rlb_project_name: _RLB_PROJECT_NAMES,
) -> None:
    """Add a section named Reference to the docs side-bar nav links.

    NOTE:
        The Reference section contains links to the reference markdown files for each
        python file in the source directory.

    Args:
        nav: The nav links in the mkdocs.yml file.
        force_recreate_references: If True, delete the references directory and recreate
            the reference markdown files.
        rlb_project_name: The name of the rlb project for which we are adding refs.

    EFFECT:
        If force_recreate_references is True, the references directory is deleted and
        recreated.

    EFFECT:
        `nav` is modified to contain a Reference section.
    """
    repo_paths = _RepoPaths(
        rlb_repo_root=rlb_repo_root,
        rlb_project_name=rlb_project_name,
    )
    if force_recreate_references:
        typer.echo("Recreating references...")
        # Delete the references directory
        if repo_paths.references_dir.exists():
            shutil.rmtree(repo_paths.references_dir)
    # Generate reference links
    for key in nav:
        if "Reference" in key:
            nav.remove(key)
            break
    # Add the reference links
    references: list[dict[str, t.Any]] = _get_references(
        module=repo_paths.src_code_dir,
        rlb_repo_root=rlb_repo_root,
        rlb_project_name=rlb_project_name,
    )[rlb_project_name]
    # Iterate through every python file in the source directory
    nav.append({"Reference": references})


def _add_sections(
    nav: list[dict[str, t.Any]],
    rlb_repo_root: Path,
    rlb_project_name: _RLB_PROJECT_NAMES,
) -> None:
    """Convert the files and folders in the sections directory to an appropriate nav.

    Files are added as top level links, and folders are added as sections with links to
    the markdown files in the folder (recursively).

    Args:
        nav: The nav links in the mkdocs.yml file

    Example:
        Given the following directory structure:
        ```
        sections/
            foo/
                bar.md
                baz.md
            qux.md
        ```
        The following nav is added:
        ```yaml
        - Foo:
            - Bar: sections/foo/bar.md
            - Baz: sections/foo/baz.md
        - Qux: sections/qux.md
        ```
    """

    def as_section_name(path: str) -> str:
        """Convert the path to the markdown file to a section name."""
        file_name = Path(path).stem
        if file_name.upper() == file_name:
            return file_name.replace("_", " ")
        return file_name.capitalize().replace("_", " ")

    repo_paths = _RepoPaths(
        rlb_repo_root=rlb_repo_root,
        rlb_project_name=rlb_project_name,
    )
    path_tree = _get_path_tree(repo_paths.sections_dir)
    sections_tree = _transform_keys(path_tree, as_section_name)
    for leaf in _iter_leaf_dicts(sections_tree):
        assert len(leaf) == 1
        key = list(leaf.keys())[0]
        path = list(leaf.values())[0]
        assert isinstance(path, Path)
        leaf[key] = str(path.relative_to(repo_paths.docs_dir))
    section_names = {
        as_section_name(str(section))
        for section in repo_paths.sections_dir.iterdir()
        if any((section.suffix == ".md", section.is_dir()))
    }
    items_to_remove: list[dict[str, str]] = []
    for item in nav:
        key = list(item.keys())[0]
        if key in section_names:
            items_to_remove.append(item)
    for item in items_to_remove:
        nav.remove(item)
    nav.extend(sections_tree["Sections"])


def _generate_directory_structure_file(
    rlb_repo_root: Path,
    rlb_project_name: _RLB_PROJECT_NAMES,
) -> None:
    """Update the _DIRECTORY_STRUCTURE_FILE with the directory structure of the source
    code."""
    repo_paths = _RepoPaths(
        rlb_repo_root=rlb_repo_root,
        rlb_project_name=rlb_project_name,
    )
    repo_paths.directory_structure_file.parent.mkdir(parents=True, exist_ok=True)
    # Get output by running tree on the source code directory
    ignore_dirs = [
        "__pycache__",
        "docs",
        "tests",
    ]
    cmd = f"tree --gitignore -I '{'|'.join(ignore_dirs)}' {repo_paths.src_code_dir}"
    structure = subprocess.check_output(cmd, shell=True).decode("utf-8")
    repo_paths.directory_structure_file.write_text(f"```{{toctree}}\n{structure}\n```")


@app.command()
def publish():
    """Publish the docs."""
    typer.echo("Publishing the docs...")
    # Ensure that you're on the main branch
    if (
        subprocess.check_output("git branch --show-current", shell=True)
        .decode("utf-8")
        .strip()
        != "main"
    ):
        typer.echo("You must be on the main branch to publish the docs.")
        raise typer.Exit(1)
    # Build mkdocs
    subprocess.run("mkdocs gh-deploy", shell=True)
