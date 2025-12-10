# Troubleshooting

This documentation provides an overview of the troubleshooting capabilities available in the PyCentral SDK. It lists the supported troubleshooting tests for different device types (APs, AOS-CX, AOS-S, Gateway), and maps each test to the corresponding method in the `Troubleshooting` class. Use this as a reference to identify which troubleshooting functions are available for your device and how to invoke them programmatically.

| Test Name                       | Method Name | APs | AOS-CX | AOS-S | Gateway |
|----------------------------------|-------------------------------|-----|--------|-------|---------|
| **AAA Authentication Test**     | -                             | `aaa_aps_test` | `aaa_cx_test` | ❌ | ❌ |
| **Cable Test**                  | `cable_test`                  | ❌  | ✅     | ✅    | ❌     |
| **Disconnect All Clients**      | `disconnect_all_clients`      | ❌  | ❌     | ❌    | ✅     |
| **Disconnect All Users**        | `disconnect_all_users`        | ✅  | ❌     | ❌    | ❌     |
| **Disconnect Users by SSID**    | `disconnect_all_users_ssid`   | ✅  | ❌     | ❌    | ❌     |
| **Disconnect Client by MAC**    | `disconnect_client_mac_addr`  | ❌  | ❌     | ❌    | ✅     |
| **Disconnect User by MAC**      | `disconnect_user_mac_addr`    | ✅  | ❌     | ❌    | ❌     |
| **HTTP Test**                   | `http_test`                   | ✅  | ✅     | ✅    | ✅      |
| **HTTPS Test**                  | -                             | `https_aps_test` | `https_cx_test` | ❌ | `https_gateways_test` |
| **iPerf Performance Test**      | `iperf_test`                  | ❌  | ❌     | ❌    | ✅     |
| **Locate Device (LED Blink)**   | `locate_device`               | ✅  | ✅     | ✅    | ✅      |
| **NSLookup Test**               | `nslookup_test`               | ✅  | ❌     | ❌    | ❌     |
| **Ping Test**               | -               | `ping_aps_test`  | `ping_cx_test`  | `ping_aoss_test`    | `ping_gateways_test`     |
| **PoE Bounce Test**             | `poe_bounce_test`             | ❌  | ✅     | ✅    | ✅     |
| **Port Bounce Test**            | `port_bounce_test`            | ❌  | ✅     | ✅    | ✅     |
| **Reboot Device**               | `reboot_device`               | ✅  | ✅     | ✅    | ✅      |
| **ARP Table Retrieval**         | `retrieve_arp_table_test`     | ✅  | ❌     | ✅    | ✅     |
| **Speed Test**                  | `speedtest_test`              | ✅  | ❌     | ❌    | ❌     |
| **TCP Test**                    | `tcp_test`                    | ✅  | ❌     | ❌    | ❌     |
| **Traceroute Test**             | -             | `traceroute_aps_test` | `traceroute_cx_test`     | `traceroute_aoss_test`    | `traceroute_gateways_test`      |
| **List Show Commands**          | `list_show_commands`          | ✅  | ✅     | ✅    | ✅     |
| **Run Show Command**            | `run_show_command`            | ✅  | ✅     | ✅    | ✅     |
| **List Active Tasks**           | `list_active_tasks`           | ✅  | ✅     | ✅    | ✅     |

**Legend:**  

- ✅ = Supported with the method named in the "Method Name" column
- ❌ = Not supported

For device-specific implementations (HTTPS Test, Ping Test), the specific method name is shown in the device column in the table above.

::: pycentral.troubleshooting.troubleshooting
