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

**Base URL or Cluster Name (Choose one)**
Identifies your Central Account's API gateway. Both options function identically. Use whichever is convenient:

- Base URL
    Base of the URL for requests to your Central API Gateway. For instructions on how to locate your Base URL, see [Finding Your Base URL in Central](https://developer.arubanetworks.com/new-central/docs/getting-started-with-rest-apis#finding-your-base-url).
- Cluster Name
    Name of the cluster where your account is provisioned. A table detailing all cluster names can be found [here](https://developer.arubanetworks.com/new-central/docs/getting-started-with-rest-apis#api-gateway-base-urls).


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
