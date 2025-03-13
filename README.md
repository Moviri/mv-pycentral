# pycentral

## Introduction

Welcome to the pycentral, a Python SDK for interacting with HPE Aruba Networking Central via REST APIs. This library provides tools for automating repetitive tasks, configuring multiple devices, monitoring, and more.

## HPE Aruba Networking Central Python Package SDK (New Central)

This pre-release allows users to make REST API calls to New Central, the next generation of HPE Aruba Networking Central. It also supports making REST API calls to HPE GreenLake Platform. 

> Upgrading to this pre-release version will not break pycentral-v1 code. All the pycentral-v1 code has been moved to the `classic` folder within pycentral folder, ensuring backward compatibility. You can find Classic Central PyCentral Documentation [here](#classic-central)

### Installing the Pre-release

To install the latest pre-release version of pycentral, use the following command:

```bash
pip3 install --pre pycentral
```

If you already have pycentral-v1 and would like to upgrade to the pre-release version, use the following command:

```bash
pip3 install --upgrade --pre pycentral
```

### Getting Started

Once you have installed the pre-release version of pycentral, you need to obtain the necessary authentication details based on the platform you are working with:
1. **New Central Authentication** \
   For New Central, you must obtain the following details before making the API requests:
   1. **Base URL**: This is the API Gateway URL for your New Central account based on the geographical cluster of your account on HPE GreenLake Platform. You can find the base URL of your New Central account's API Gateway from the table [here](https://developer.arubanetworks.com/new-hpe-anw-central/docs/getting-started-with-rest-apis#base-urls).
   2. **Client ID and Client Secret**: These credentials are required to generate an access token to authenticate API requests. You can obtain them by creating a Personal API Client for your New Central Account. Follow the detailed steps in the [Create Client Credentials documentation](https://developer.arubanetworks.com/new-hpe-anw-central/docs/generating-and-managing-access-tokens#create-client-credentials).
2. **HPE GreenLake (GLP) Authentication** \
   If you are working with HPE GreenLake APIs, authentication is slightly different:
   1. GLP does not require a Base URL.
   2. You only need the **Client ID & Client Secret** for the HPE GreenLake Platform.

#### Example Script
Once you have the required credentials, you can initialize the `NewCentralBase` class as follows:
```python
# New Central Import
from pycentral import NewCentralBase

# Store New Central/GLP Token Credentials
token_info = {
    "glp": {
        "client_id": "<client-id>",
        "client_secret": "<client-secret>",
    },
    "new_central": {
        "base_url": "<api-base-url>",
        "client_id": "<client-id>",
        "client_secret": "<client-secret",
    },
}

# Initialize NewCentralBase class with the token credentials for New Central/GLP
new_central_conn = NewCentralBase(
    token_info=token_info,
)

# New Central API Call
new_central_resp = new_central_conn.command(
    api_method="GET", api_path="network-monitoring/v1alpha1/aps"
)

print(new_central_resp)

# GLP API Call
glp_resp = new_central_conn.command(
    api_method="GET", api_path="devices/v1/devices", app_name="glp"
)

print(glp_resp)

```

## Classic Central
The Classic Central functionality is still fully supported by the SDK & has been moved to a dedicated documentation page. For information on using the SDK with Classic Central, including authentication methods, API calls, and workflow examples, please see the [Classic Central Documentation](https://github.com/aruba/pycentral/blob/master/README.md).

### Documentation
* <a href="https://pycentral.readthedocs.io/en/latest/" target="_blank">Python package documentation</a>
### **Use-Cases and Workflows**
  - <a href="https://developer.arubanetworks.com/aruba-central/docs/python-getting-started" target="_blank">HPE Aruba Networking Developer Hub</a>
  - <a href="https://github.com/aruba/central-python-workflows" target="_blank">central-python-workflows</a>