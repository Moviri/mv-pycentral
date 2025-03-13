# 1.4.1

## Notable Changes
* Support Preserve Configuration Overrides in Device Movement by @fiveghz in #43
* Version fixes by @KarthikSKumar98 in #45
* Packages that are installed along with PyCentral will have version number associated with.
  * requests - v2.31.0
  * PyYAML - v6.0.1
  * urllib3 - 2.2.2
  * certifi - 2024.7.4
## New Contributors
* @fiveghz made their first contribution in [#43](https://github.com/aruba/pycentral/pull/43)
  
Full Changelog: [v1.4...v1.4.1](https://github.com/aruba/pycentral/compare/v1.4...v1.4.1)
## Known Issues
* No known issues.





# 1.4

## Notable Changes
* Updated minimum required version of python from 3.6 to 3.8
* Add the ability to consume cluster_name as a parameter instead of base_url
* Added ability to enable and disable WLANs in Central UI Group
  * enable_wlan
  * disable_wlan
* Error handling when invalid base_url is passed
* Resolved minor bugs
  
## Known Issues
* No known issues.

Full Changelog: [v1.3...v1.4](https://github.com/aruba/pycentral/compare/v1.3...v1.4)

# 1.3

## Notable Changes
* Added MSP Module. These are some of the functions that are implemented in this module -
  *  Customer Management Functions
     *  get_customers
     *  get_all_customers
     *  create_customer
     *  update_customer
     *  delete_customer
     *  get_customer_details
     *  get_customer_id
  *  Device Management Functions
     *  get_customer_devices_and_subscriptions
     *  assign_devices_to_customers
     *  unassign_devices_from_customers
     *  unassign_all_customer_device
     *  get_msp_devices_and_subscriptions
     *  get_msp_all_devices_and_subscriptions
  *  Other Functions
     *  get_msp_id
     *  get_msp_users
     *  get_customer_users
     *  get_country_code
     *  get_country_codes_list
     *  get_msp_resources
     *  edit_msp_resources
     *  get_customers_per_group

Full Changelog: [v1.2.1...v1.3](https://github.com/aruba/pycentral/compare/v1.2.1...v1.3)

## Known Issues
* No known issues.

# 1.2.1

## Notable Changes
* Fixed bug with add_device function

## Known Issues
* No known issues.

# 1.2

## Notable Changes
* Added new Device Inventory functions - Archive Devices, Unarchive Devices, Add Devices

## Known Issues
* No known issues.

## PRs in this release
* Added device inventory functions by [@KarthikSKumar98](https://github.com/KarthikSKumar98) in [#35](https://github.com/aruba/pycentral/pull/35)
* Style linting pycentral modules by[@KarthikSKumar98](https://github.com/KarthikSKumar98) in [#36](https://github.com/aruba/pycentral/pull/36)

Full Changelog: [v1.1.1...v1.2](https://github.com/aruba/pycentral/compare/v1.1.1...v1.2)

# 1.1.1

## Notable Changes
* Updated README links

## Known Issues
* No known issues.
  
# 1.1.0

## Notable Changes
* Added APConfiguration Class to Configuration Module

## Known Issues
* No known issues.
  
# 1.0.0

## Notable Changes
* Added wait & retry logic when Aruba Central's Per-Second API rate-limit is hit
* Added log messages when Aruba Central's Per-Day API Rate-limit is exhausted
* Added new module for device_inventory APIs
* Added WLAN class to configuration module
* Merged PRs and resolved GitHub issues:
    - PR #16 : Fixing multiple devices to site bug
    - PR #19 : Added ability to associate/unassociate multiple devices to a site
    - PR #20 : Added New Device Inventory Module
    - PR #22 : Added Rate Limit Log Messages
    - PR #23 : Fixed Rate Limit Bugs
    - PR #25 : Licensing API Bug Fixes
    - PR #28, #29 : Added WLAN class to Configuration module

## Known Issues
* No known issues.
  
# 0.0.3

## Notable Changes
* Quick fix on deprecated pip module usage.
* Merged PRs and resolved GitHub issues:
    - PR #10 : remove dep on _internal function from pip module 
    - Issue #9: pip 21.3 just posted 2 days ago breaks pycentral in the config file and passed to pycentral

## Known Issues
* No known issues.
  
# 0.0.2

## Notable Changes
* Added modules for firmware_management, rapids, topology and user_management
* Major update to existing config_apsettings_from_csv.py workflow. It accepts CSV file downloaded from the Central UI group. This workflow also generates a new CSV file with failed APs. CSV file format from the previous version is not backward compatible.
* Fixes and improvement to existing modules, utilities and the documentation
* Merged PRs and resolved GitHub issues:
    - PR #6: example AP rename code always terminates with an error
    - PR #2: fix url concat in command()
    - PR #1: Added the ability for multiple Aruba Central account's in the config file and passed to pycentral

## Known Issues
* No known issues.

# 0.0.1

## Notable Changes
* This is the initial release for the Aruba Central Python SDK, sample scripts, and workflows.

## Known Issues
* No known issues.
