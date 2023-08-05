import pkg_resources


def _get_version():
    return pkg_resources.get_distribution("nops-sdk").version.replace(".", "").lstrip("0")
