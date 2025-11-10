# (C) Copyright 2025 Hewlett Packard Enterprise Development LP.
# MIT License

versions = ["v1alpha1", "v1"]
latest = "v1alpha1"
glp_latest = "v1"

CATEGORIES = {
    "configuration": {
        "value": "network-config",
        "type": "configuration",
        "latest": "v1alpha1",
    },
    "monitoring": {
        "value": "network-monitoring",
        "type": "monitoring",
        "latest": "v1alpha1",
    },
    "troubleshooting": {
        "value": "network-troubleshooting",
        "type": "troubleshooting",
        "latest": "v1alpha1",
    },
    "subscriptions": {"value": "subscriptions", "type": "glp", "latest": "v1"},
    "user_management": {"value": "identity", "type": "glp", "latest": "v1"},
    "devices": {"value": "devices", "type": "glp", "latest": "v1"},
    "service_catalog": {
        "value": "service-catalog",
        "type": "glp",
        "latest": "v1",
    },
}


def get_prefix(category="configuration", version="latest"):
    """
    Generate URL prefix for a given category and version.

    :param category: API category name, defaults to "configuration"
    :type category: str, optional
    :param version: API version, defaults to "latest"
    :type version: str, optional
    :return: URL prefix in the format "category_value/version/"
    :rtype: str
    :raises ValueError: If category is not supported or version is invalid
    """
    if category not in CATEGORIES:
        raise ValueError(
            f"Invalid category: {category}, Supported categories: {list(CATEGORIES.keys())}"
        )
    category_value = CATEGORIES[category]["value"]
    if version == "latest":
        version = (
            latest
            if not (CATEGORIES[category]["type"] == "glp")
            else glp_latest
        )
    else:
        if version not in versions:
            raise ValueError(
                f"Invalid version: {version}. Allowed versions: {versions}"
            )
    return f"{category_value}/{version}/"


def generate_url(api_endpoint, category="configuration", version="latest"):
    """
    Generate complete API URL for a given endpoint, category, and version.

    :param api_endpoint: The API endpoint path to append to the URL
    :type api_endpoint: str
    :param category: API category name, defaults to "configuration"
    :type category: str, optional
    :param version: API version, defaults to "latest"
    :type version: str, optional
    :return: Complete API URL in the format "category[value]/version/api_endpoint"
    :rtype: str
    :raises ValueError: If category is not supported or version is invalid
    :raises TypeError: If api_endpoint is not a string
    """
    if category not in CATEGORIES:
        raise ValueError(
            f"Invalid category: {category}, Supported categories: {list(CATEGORIES.keys())}"
        )
    if api_endpoint is not None and not isinstance(api_endpoint, str):
        raise TypeError(
            f"Invalid type: {type(api_endpoint)} for api_endpoint, expected str"
        )
    category_value = CATEGORIES[category]["value"]
    if version == "latest":
        version = (
            latest
            if not (CATEGORIES[category]["type"] == "glp")
            else glp_latest
        )
    else:
        if version not in versions:
            raise ValueError(
                f"Invalid version: {version}. Allowed versions: {versions}"
            )
    return f"{category_value}/{version}/{api_endpoint}"
