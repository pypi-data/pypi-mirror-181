import pkg_resources
from pkg_resources import DistributionNotFound


def _get_version():
    try:
        return pkg_resources.get_distribution("nops-sdk").version.replace(".", "").lstrip("0")
    except DistributionNotFound:
        return "0"
