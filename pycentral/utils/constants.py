# (C) Copyright 2025 Hewlett Packard Enterprise Development LP.
# MIT License

"""
This module contains constant values used across the pycentral package.
"""

CLUSTER_BASE_URLS = {
    "EU-1": "https://ge1.api.central.arubanetworks.com",
    "EU-Central2": "https://ge2.api.central.arubanetworks.com",
    "EU-Central3": "https://ge3.api.central.arubanetworks.com",
    "US-1": "https://us1.api.central.arubanetworks.com",
    "US-2": "https://us2.api.central.arubanetworks.com",
    "US-WEST-4": "https://us4.api.central.arubanetworks.com",
    "US-WEST-5": "https://us5.api.central.arubanetworks.com",
    "US-East1": "https://us6.api.central.arubanetworks.com",
    "Canada-1": "https://cn1.api.central.arubanetworks.com",
    "APAC-1": "https://in.api.central.arubanetworks.com",
    "APAC-EAST1": "https://jp1.api.central.arubanetworks.com",
    "APAC-SOUTH1": "https://au1.api.central.arubanetworks.com",
    "Internal": "https://internal.api.central.arubanetworks.com",
}
"""Dict[str, str]: Public HPE Aruba Networking cluster names with their corresponding API Base URLs.
You can update this dictionary to add your own private cluster details.
Learn more about Base URLs: https://developer.arubanetworks.com/new-hpe-anw-central/docs/getting-started-with-rest-apis#api-gateway-base-urls
"""

SUPPORTED_CONFIG_PERSONAS = {
    "Campus Access Point": "CAMPUS_AP",
    "Micro Branch AP": "MICROBRANCH_AP",
    "Access Switch": "ACCESS_SWITCH",
    "Core Switch": "CORE_SWITCH",
    "Aggregation Switch": "AGG_SWITCH",
    "Mobility Gateway": "MOBILITY_GW",
    "Branch GW": "BRANCH_GW",
    "Bridge": "BRIDGE",
    "Hybrid NAC": "HYBRID_NAC",
}
"""Dict[str, str]: Supported device personas and their corresponding API values."""

AUTHENTICATION = {"OAUTH": "https://sso.common.cloud.hpe.com/as/token.oauth2"}
"""Dict[str, str]: Authentication endpoints for OAuth flows."""

GLP_URLS = {
    "BaseURL": "https://global.api.greenlake.hpe.com",
    "DEVICE": "devices",
    "SUBSCRIPTION": "subscriptions",
    "USER_MANAGEMENT": "users",
    "ASYNC": "async-operations",
    "SERVICE_MANAGER": "service-managers",
    "SERVICE_MANAGER_PROVISIONS": "service-manager-provisions",
    "SERVICE_MANAGER_BY_REGION": "per-region-service-managers",
}
"""Dict[str, str]: GreenLake Platform (GLP) API URLs and endpoints."""

SCOPE_URLS = {
    "SITE": "sites",
    "SITE_COLLECTION": "site-collections",
    "DEVICE": "devices",
    "DEVICE_GROUP": "device-collections",
    "ADD_SITE_TO_COLLECTION": "site-collection-add-sites",
    "REMOVE_SITE_FROM_COLLECTION": "site-collection-remove-sites",
    "HIERARCHY": "hierarchy",
    "SCOPE-MAPS": "scope-maps",
}
"""Dict[str, str]: Scope-related API URLs for site and device organization."""

__all__ = [
    "CLUSTER_BASE_URLS",
    "SUPPORTED_CONFIG_PERSONAS",
    "AUTHENTICATION",
    "GLP_URLS",
    "SCOPE_URLS",
]
