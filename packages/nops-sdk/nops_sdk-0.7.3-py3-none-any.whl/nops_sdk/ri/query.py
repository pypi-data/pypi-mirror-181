from dataclasses import dataclass


@dataclass
class RIQueryParams:
    region: str
    family: str
    tenancy: str
    platform: str
