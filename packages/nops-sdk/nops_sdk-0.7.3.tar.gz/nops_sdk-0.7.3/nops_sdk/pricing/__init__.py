"""
This modules allows to estimate your cloud infrastructure cost changes based on input from Infrastructure
as Code (IaC) tools. This ensures that you are aware of cost changes before they occur.

It exposes the :class:`nops_sdk.pricing.CloudCost` class, which can be used
to estimate cost impact of a IaC changeset. See the documentation of the class for more.
"""
from nops_sdk.pricing.pricing import CloudCost

__all__ = ["CloudCost"]
