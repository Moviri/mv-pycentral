# Quick Start
With authentication set-up, let's see how to use PyCentral to interact with New Central.

!!! note "Authentication"
    This guide assumes you already have your API credentials ready. For help obtaining credentials, see the [Authentication Guide](authentication.md).

## Basic Setup
Before running a script, create a `token.yaml`. This file provides the authentication credentials required by the SDK to make API calls to New Central.
You will need to populate it with the required credentials as follows:

```yaml title="token.yaml"
new_central:
  base_url: <api-base-url>
  client_id: <client-id>
  client_secret: <client-secret>
```



### Example: Python Script to Get Devices

The python script below demonstrates:

1. Loading API Client Credentials from [`token.yaml`](doc:pycentral-quickstart-guide#prerequisites) file. 
2. Initialize the PyCentral SDK's connection to New Central
3. Fetch a list of devices from New Central

Once you have the `token.yaml` file ready, you can run the following Python script:

```python title="get_devices.py"
import os
from pycentral import NewCentralBase

# Validate token file exists
token_file = "token.yaml"
if not os.path.exists(token_file):
    raise FileNotFoundError(
        f"Token file '{token_file}' not found. Please provide a valid token file."
    )

# Initialize NewCentralBase class with the token credentials for New Central/GLP
new_central_conn = NewCentralBase(token_info=token_file)

# New Central API Call
new_central_resp = new_central_conn.command(
    api_method="GET", api_path="network-monitoring/v1/devices"
)

# Check response status and print results or error message
if new_central_resp["code"] == 200:
    print(new_central_resp["msg"])
else:
    print(f"Error - Response code {new_central_resp['code']}")
    print(new_central_resp["msg"])

```

### Running the Script

Save the code above as `get_devices.py` then execute it using:

```
python get_devices.py
```

If successful, you'll see a list of devices retrieved from New Central.

***

The above example serves as a foundation for writing your own custom scripts. As you explore [more API endpoints](https://developer.arubanetworks.com/new-central/reference/) , you can extend this approach to automate tasks, gather monitoring statistics, or integrate with your existing tools. The PyCentral SDK is designed to help you script confidently and build workflows that fit your specific needs.

## Next Steps

- Explore the [Modules Reference](../modules/base.md)
- Explore our full catalog of Central guides on our [Developer Hub](https://developer.arubanetworks.com/new-central/docs/about)
- Explore other python workflows on our [GitHub](https://github.com/aruba/central-python-workflows)
