# Authentication

PyCentral provides a flexible authentication system allowing users to make API calls to New Central, GLP, and/or Classic Central. You only need to provide credentials for the platform(s) you want PyCentral to interact with.

## Choosing an Authentication Method

PyCentral supports two authentication methods for New Central & GLP:

| Method                                      | Best For                          | Token Expiry                                                            |
| :------------------------------------------ | :-------------------------------- | :---------------------------------------------------------------------- |
| **Client ID & Client Secret** (Recommended) | Automation & long-running scripts | Auto-renews - New tokens are generated automatically by SDK upon expiry |
| **Access Tokens**                           | Quick tests & one-time API calls  | Manually need to update token upon expiry                               |
 
If you want a hassle-free setup use **Client ID & Secret**, the SDK will automatically generate a new token whenever required. 
If you're just testing an API, using **Access Token** is fine

## New Central

**Base URL**  
   You can find your Central account's base URL from the table here:  

| Cluster                  | Base URL                               |
| :----------------------- | :------------------------------------- |
| EU-1 (eu)                | de1.api.central.arubanetworks.com      |
| EU-Central2 (eucentral2) | de2.api.central.arubanetworks.com      |
| EU-Central3 (eucentral3) | de3.api.central.arubanetworks.com      |
| US-1 (prod)              | us1.api.central.arubanetworks.com      |
| US-2 (central-prod2)     | us2.api.central.arubanetworks.com      |
| US-WEST-4 (uswest4)      | us4.api.central.arubanetworks.com      |
| US-WEST-5 (uswest5)      | us5.api.central.arubanetworks.com      |
| US-East1 (us-east-1)     | us6.api.central.arubanetworks.com      |
| Canada-1 (starman)       | ca1.api.central.arubanetworks.com      |
| APAC-1 (apac)            | in.api.central.arubanetworks.com       |
| APAC-EAST1 (apaceast)    | jp1.api.central.arubanetworks.com      |
| APAC-SOUTH1 (apacsouth)  | au1.api.central.arubanetworks.com      |
| Internal (internal)      | internal.api.central.arubanetworks.com |

Ensure you use the correct Base URL in your API calls. Using the wrong Base URL will result in failed requests.

**API Credentials** (Choose one):

- Client ID & Client Secret _(Recommended)_  
    The SDK automatically generates new tokens when they expire, so you don't have to manage them manually. Learn how to create your credentials [here](https://developer.arubanetworks.com/new-central/docs/generating-and-managing-access-tokens#create-client-credentials).
- Access Token  
    Manually, retrieve an access token. Learn how to retreive an access token [here](https://developer.arubanetworks.com/new-central/docs/generating-and-managing-access-tokens#generate-access-token). **(Tokens expire in 2 hours)**

## GLP

**No Base URL Required**   
**API Credentials** (Choose one):

- Client ID & Client Secret _(Recommended)_  
    The SDK automatically generates new tokens when they expire, so you don't have to manage them manually. Get your credentials [here](https://developer.greenlake.hpe.com/docs/greenlake/guides/public/authentication/authentication/#creating-a-personal-api-client).
- Access Token  
    Manually, retrieve an access token [here](https://developer.greenlake.hpe.com/docs/greenlake/guides/public/authentication/authentication/#generating-an-access-token)** (Tokens expire in 15 mins)**

## Classic Central

Classic Central suppports authentication methods for access tokens or generating through OAUTH APIs

**Base URL**  
   You can find your Classic Central account's base URL from the table provided within this guide [here](https://developer.arubanetworks.com/central/docs/api-oauth-access-token#table-domain-urls-for-api-gateway-access).

**API Credentials** (Choose one):

- OAUTH

    Manually, use the pycentral.workflows_utils.get_conn_from_file() function to generate new tokens when they expire. View our Classic Central guide for OAUTH Authentication with PyCentral [here](https://developer.arubanetworks.com/central/docs/python-using-api-sdk#arubacentralbase-class-requirements).

- Access Token  
    Manually, retrieve an access token. Learn how to retreive an access token [here](https://developer.arubanetworks.com/central/docs/api-gateway-creating-application-token). **(Tokens expire in 2 hours)**

## Next Steps

- [Quick Start](quickstart.md) - Start using PyCentral
- [Module Reference](../modules/base.md) - Explore modules
