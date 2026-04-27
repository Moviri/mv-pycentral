# MSP

The MSP module provides `MSPBase`, an extension of `NewCentralBase` designed for Managed Service Providers (MSPs). It handles MSP-level authentication and provides isolated, tenant-scoped API connections through a token-exchange flow — all without managing tokens manually.

!!! note "Unified Credentials Only"
    MSP features are available starting in PyCentral SDK `v2.0a19`.
    `MSPBase` exclusively uses `"unified"` credentials. Standalone `"glp"` or `"new_central"` entries are not supported.

## Overview

`MSPBase` builds on `NewCentralBase` and adds:

- **MSP-level GLP and New Central API calls** using a single `"unified"` credential
- **Per-tenant connections** via `get_tenant_connection()`, which exchanges the MSP token for a tenant-scoped token
- **Automatic token renewal** — when a token expires (MSP or tenant), the SDK refreshes it transparently
- **Tenant connection caching** — repeated calls with the same `tenant_workspace_id` return the same connection without re-running the token exchange

***

## Authentication

All MSP connections use a single set of `"unified"` credentials. Provide a `workspace_id` for your MSP workspace, along with your `client_id` and `client_secret`.

To also enable **New Central** API calls (e.g. for monitoring or configuration), include a `cluster_name` **or** a `base_url` for the Central cluster your MSP account is provisioned on.

```yaml title="msp_token.yaml"
unified:
  client_id: <client-id>
  client_secret: <client-secret>
  workspace_id: <workspace-id>
  cluster_name: US-WEST-5   # Optional — include to enable New Central API calls
```
***

## Basic Setup

### MSP-Level API Calls

Once you have the `msp_token.yaml` file ready, you can make MSP-level API calls to both New Central and GLP.

```python title="msp_api_calls.py"
from pycentral import MSPBase

with MSPBase(token_info="msp_token.yaml") as msp:
    # New Central API call — list MSP tenants
    response = msp.command(
            api_method="GET",
            api_path="network-msp/v1/list-tenants",
            api_params={"limit": 100, "next": 1},
    )

    if response["code"] == 200:
        tenants = response["msg"].get("items", [])
        print(f"Total tenants: {len(tenants)}")
        for tenant in tenants:
            print(f'Central Tenant ID - {tenant.get("tenantId")}, Tenant Name - {tenant.get("tenantName")}')
    else:
        print(f"Error {response['code']}: {response['msg']}")
```

!!! note "GLP-Only Mode"
    If you only need GLP API calls (e.g. listing tenants, managing subscriptions), omit `cluster_name` / `base_url` from your credentials. Only the GLP endpoint will be configured.

***

## Tenant Connections

`get_tenant_connection()` exchanges the MSP token for a tenant-scoped token and returns a connection that behaves exactly like `NewCentralBase`. Use it for all tenant-scoped API calls.

The connection is cached — calling `get_tenant_connection()` again with the same `tenant_workspace_id` returns the same object without repeating the token exchange.

!!! note "Tenant Workspace ID"
    `tenant_workspace_id` is the GLP workspace ID for the tenant. This is an ID from GLP for the tenant similar to the `workspace_id` in your MSP credentials, but scoped to the individual tenant. It can be found in the `tenantId` field of the GLP tenant list response. The SDK automatically strips dashes from the value (e.g. `"abc-def-123"` becomes `"abcdef123"`) to match GLP API requirements. This normalization is applied consistently across `get_tenant_connection()` and `close_tenant_connection()`.

### Create a Tenant Connection

You can create a tenant connection by providing either a `tenant_workspace_id` or a `tenant_name`. When using `tenant_name`, the SDK resolves it to a `tenant_workspace_id` via a GLP API call.

```python title="tenant_connection.py"
from pycentral import MSPBase

with MSPBase(token_info="msp_token.yaml") as msp:
    # Option 1: Connect by tenant workspace ID (from the GLP tenant list)
    tenant_conn = msp.get_tenant_connection(tenant_workspace_id="<tenant-workspace-id>")

    # Option 2: Connect by tenant name (resolves to workspace ID via GLP API)
    # tenant_conn = msp.get_tenant_connection(tenant_name="<tenant-name>")
```

### Tenant — New Central API Call

The tenant connection inherits the same Central base URL from the MSP credentials. Provide `cluster_name` or `base_url` in your MSP credentials to enable New Central calls.

```python title="tenant_new_central.py"
from pycentral import MSPBase

with MSPBase(token_info="account_credentials_new.yaml") as msp:
        tenant_conn = msp.get_tenant_connection(tenant_workspace_id="<tenant-workspace-id>")

        # List APs in the tenant's Central environment
        response = tenant_conn.command(
            api_method="GET",
            api_path="network-monitoring/v1/aps",
        )
        if response["code"] == 200:
            aps = response["msg"].get("items", [])
            print(f"Tenant APs: {len(aps)}")
            for ap in aps:
                print(ap.get("serialNumber"), ap.get("deviceName"), ap.get("status"))
        else:
            print(f"Error {response['code']}: {response['msg']}")
```

### Tenant — GLP API Call

Use the tenant connection to make GLP calls scoped to that tenant's workspace.

```python title="tenant_glp.py"
from pycentral import MSPBase

 with MSPBase(token_info="account_credentials_new.yaml") as msp:
    tenant_conn = msp.get_tenant_connection(tenant_name="The Wandwright Academy")

    # Specify app_name="glp" to make API call to GreenLake.
    response = tenant_conn.command(
        api_method="GET",
        api_path="audit-log/v1/logs",
        app_name="glp",
    )

    if response["code"] == 200:
        logs = response["msg"].get("items", [])
        print(f"Tenant audit logs: {len(logs)}")
        for log in logs:
            print(log.get("createdAt"), log.get("category"), log.get("user"))
    else:
        print(f"Error {response['code']}: {response['msg']}")
```

***

## Token Renewal

Token renewal is handled automatically by the SDK. No manual intervention is required.

| Scenario | What Happens |
| :--- | :--- |
| MSP token expires during an API call | SDK refreshes the MSP token using client credentials and retries |
| Tenant token expires during an API call | SDK refreshes the MSP parent token first, then re-exchanges it for a fresh tenant-scoped token, and retries |
| MSP token expires during tenant token exchange | SDK renews the MSP token and retries the exchange (up to one retry) |

***

## Managing Connections

Both `MSPBase` and tenant connections support Python's `with` statement, which ensures all HTTP clients are closed cleanly when the block exits.

```python title="manage_connections.py"
from pycentral import MSPBase

with MSPBase(token_info="msp_token.yaml") as msp:
    tenant_conn = msp.get_tenant_connection(tenant_workspace_id="<tenant-workspace-id>")

    # Use tenant_conn for API calls...

    # Optionally close a single tenant connection mid-session
    msp.close_tenant_connection(tenant_workspace_id="<tenant-workspace-id>")

# msp.close() is called automatically — closes MSP and all remaining tenant connections
```

!!! note "Manual Cleanup"
    If you're not using `with`, call `msp.close()` when done to release HTTP client resources for both the MSP connection and all cached tenant connections.

***

## Next Steps

- Explore the [Base Module Reference](base.md) for `NewCentralBase` details
- See the [Authentication Guide](../getting-started/authentication.md) for credential setup
- Explore the full catalog of Central guides on the [Developer Hub](https://developer.arubanetworks.com/new-central/docs/about)

***

## API Reference

::: pycentral.msp.msp_base.MSPBase

::: pycentral.msp.msp_base.TenantBase
