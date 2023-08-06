import pkg_resources
from prettytable import PrettyTable


def _get_pkg_license(pkg):
    try:
        lines = pkg.get_metadata_lines("METADATA")
    except Exception:
        lines = pkg.get_metadata_lines("PKG-INFO")

    for line in lines:
        if line.startswith("License:"):
            return line[9:]
    return "(License not found)"


def _get_pkg_home_page(pkg):
    try:
        lines = pkg.get_metadata_lines("METADATA")
    except Exception:
        lines = pkg.get_metadata_lines("PKG-INFO")

    for line in lines:
        if line.startswith("Home-page:"):
            return line[11:]
    return "(Homepage not found)"


def get_py_deps(package_name: str) -> PrettyTable:
    """Print all dependencies which are required with their licenses and home page."""
    pkg_requires = pkg_resources.working_set.by_key[package_name].requires()
    table = PrettyTable(["Package", "License", "Url"])

    for pkg in sorted(pkg_resources.working_set, key=lambda x: str(x).lower()):
        if pkg.project_name in [pkg.project_name for pkg in pkg_requires]:
            table.add_row((str(pkg), _get_pkg_license(pkg), _get_pkg_home_page(pkg)))

    return table
