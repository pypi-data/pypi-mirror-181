import atexit
import logging
import os
import shutil
import sys
from typing import Dict, List, Tuple

from mkapi import utils
from mkapi.core.module import Module, get_module

logger = logging.getLogger("mkdocs")


def create_nav(config, global_filters):
    nav = config["nav"]
    docs_dir = config["docs_dir"]
    config_dir = os.path.dirname(config["config_file_path"])
    abs_api_paths = []
    for page in nav:
        if isinstance(page, dict):
            for key, value in page.items():
                if isinstance(value, str) and value.startswith("mkapi/"):
                    page[key], abs_api_paths_ = collect(
                        value, docs_dir, config_dir, global_filters
                    )
                    abs_api_paths.extend(abs_api_paths_)
    return config, abs_api_paths


def collect(path: str, docs_dir: str, config_dir, global_filters) -> Tuple[list, list]:
    _, api_path, *paths, package_path = path.split("/")
    abs_api_path = os.path.join(docs_dir, api_path)
    if os.path.exists(abs_api_path):
        logger.error(f"[MkApi] {abs_api_path} exists: Delete manually for safety.")
        sys.exit(1)
    os.mkdir(abs_api_path)
    os.mkdir(os.path.join(abs_api_path, "source"))
    atexit.register(lambda path=abs_api_path: rmtree(path))

    root = os.path.join(config_dir, *paths)
    if root not in sys.path:
        sys.path.insert(0, root)

    package_path, filters = utils.split_filters(package_path)
    filters = utils.update_filters(global_filters, filters)

    module = get_module(package_path)
    nav = []
    abs_api_paths = []

    def add_to_nav(entry_name, package_parts, is_package):
        package_parts = package_parts.split(".")
        if is_package:
            page_file = "index.md"
        else:
            page_file = f"{entry_name}.md"
        relative_file_path = os.path.join("api", *package_parts, page_file)

        if is_package:
            new_entry = {entry_name: [relative_file_path]}
        else:
            new_entry = {entry_name: relative_file_path}

        # now find the right place to put it into nav
        location = nav
        for package in package_parts:
            for entry in location:
                if isinstance(entry, str):
                    # index.md file
                    continue
                l = entry.get(package)
                if l is not None:
                    location = l
                    break
        location.append(new_entry)

    # Not the most efficient but easiest to implement because the ordering returned is all over the place
    # meaning; it is not certain that we get Package_A -> Package_A.moduleA -> Package_A.moduleB
    # it can very well be Package_A -> Package_B.moduleA

    # create all package folders + index.md files first
    for m in module:
        if m.object.kind != "package":
            continue
        page_file = 'index.md'
        path_with_package = os.path.join(abs_api_path, m.object.id.replace(".", "/"))
        os.makedirs(path_with_package)

        abs_file_path = os.path.join(path_with_package, page_file)
        abs_api_paths.append(abs_file_path)
        create_page(abs_file_path, m, filters)
        add_to_nav(m.object.name, m.object.id, is_package=True)

    # now process remaining files
    for m in module:
        if m.object.kind == "package":
            continue

        page_file = m.object.name + ".md"
        path_with_package = os.path.join(abs_api_path, m.parent.object.id.replace(".", "/"))  # parent.object.id
        abs_file_path = os.path.join(path_with_package, page_file)
        abs_api_paths.append(abs_file_path)
        create_page(abs_file_path, m, filters)
        add_to_nav(m.object.name, m.parent.object.id, is_package=False)

    return nav, abs_api_paths


def create_page(path: str, module: Module, filters: List[str]):
    with open(path, "w") as f:
        f.write(module.get_markdown(filters))
    if module.object.name == 'neo3':
        warning = r"""!!! Bug

        The generator for the API Reference does not correctly display `Sequence` and `Optional`s.
        We're hoping to find a solution to this. Please check the source code for now. Sorry for the inconvenience.
                """
        with open(path, "r+") as f:
            lines = f.readlines()
            lines.insert(1, warning)
            f.seek(0)
            f.writelines(lines)


def create_source_page(path: str, module: Module, filters: List[str]):
    filters_str = "|".join(filters)
    with open(path, "w") as f:
        f.write(f"# ![mkapi]({module.object.id}|code|{filters_str})")


def rmtree(path: str):
    if not os.path.exists(path):
        return
    try:
        shutil.rmtree(path)
    except PermissionError:
        logger.warning(f"[MkApi] Couldn't delete directory: {path}")
