from ..utils.monitoring_utils import (
    execute_get,
    generate_timestamp_str,
    clean_raw_trend_data,
    merged_dict_to_sorted_list,
)
from ..exceptions import ParameterError
from concurrent.futures import ThreadPoolExecutor, as_completed

AP_LIMIT = 100
MONITOR_TYPE = "aps"


class MonitoringAPs:
    @staticmethod
    def get_all_aps(central_conn, filter_str=None, sort=None):
        """
        Retrieve all access points (APs), handling pagination.

        Args:
            central_conn (NewCentralBase): Central connection object.
            filter_str (str, optional): Optional filter expression (supported fields documented in API Reference Guide).
            sort (str, optional): Optional sort parameter (supported fields documented in API Reference Guide).

        Returns:
            (list[dict]): List of AP items.
        """
        aps = []
        total_aps = None
        next_page = 1
        while True:
            resp = MonitoringAPs.get_aps(
                central_conn,
                filter_str=filter_str,
                sort=sort,
                limit=AP_LIMIT,
                next_page=next_page,
            )
            if total_aps is None:
                total_aps = resp.get("total", 0)

            aps.extend(resp["items"])

            if len(aps) == total_aps:
                break

            next_page = resp.get("next")
            if not next_page:
                break

            next_page = int(next_page)
        return aps

    # API implementation of network-monitoring/v1alpha1/aps
    @staticmethod
    def get_aps(
        central_conn, filter_str=None, sort=None, limit=AP_LIMIT, next_page=1
    ):
        """
        Retrieve a single page of APs.

        This method makes an API call to the following endpoint - `GET network-monitoring/v1alpha1/aps`

        Args:
            central_conn (NewCentralBase): Central connection object.
            filter_str (str, optional): Optional filter expression (supported fields documented in API Reference Guide).
            sort (str, optional): Optional sort parameter (supported fields documented in API Reference Guide).
            limit (int, optional): Number of entries to return (default is 100).
            next_page (int, optional): Pagination cursor/index for next page (default is 1).

        Returns:
            (dict): API response for the aps endpoint (contains 'items', 'total', etc.).

        Raises:
            ParameterError: If limit or next_page values are invalid.
        """
        path = MONITOR_TYPE
        if limit > AP_LIMIT:
            raise ParameterError(f"limit cannot exceed {AP_LIMIT}")
        if next_page < 1:
            raise ParameterError("next_page must be 1 or greater")
        params = {
            "filter": filter_str,
            "sort": sort,
            "limit": limit,
            "next": next_page,
        }
        return execute_get(central_conn, endpoint=path, params=params)

    @staticmethod
    def get_ap_details(central_conn, serial_number):
        """
        Get details for a specific AP.

        This method makes an API call to the following endpoint - `GET network-monitoring/v1alpha1/aps/{serial_number}`

        Args:
            central_conn (NewCentralBase): Central connection object.
            serial_number (str): Serial number of the AP.

        Returns:
            (dict): API response with AP details.

        Raises:
            ParameterError: If serial_number is missing/invalid.
        """
        MonitoringAPs._validate_device_serial(serial_number=serial_number)
        path = f"{MONITOR_TYPE}/{serial_number}"
        return execute_get(central_conn, endpoint=path)

    @staticmethod
    def get_ap_stats(
        central_conn,
        serial_number,
        start_time=None,
        end_time=None,
        duration=None,
        return_raw_response=False,
    ):
        """
        Collect multiple statistics (CPU, memory, power consumption) for an AP for the specified time range. Default is to return sorted trend statistics for last 3 hours.

        Args:
            central_conn (NewCentralBase): Central connection object.
            serial_number (str): Serial number of the AP.
            start_time (int, optional): Start time (epoch seconds) for range queries.
            end_time (int, optional): End time (epoch seconds) for range queries.
            duration (str|int, optional): Duration string (e.g. '5m') or seconds for relative queries.
            return_raw_response (bool, optional): If True, return raw per-metric responses.

        Returns:
            (list|dict): If return_raw_response is True returns raw list of responses; otherwise returns merged, sorted trend statistics for the AP.

        Raises:
            ParameterError: If serial_number is missing/invalid.
            RuntimeError: If any of the parallel metric requests fail.
        """
        MonitoringAPs._validate_device_serial(serial_number)

        # dispatch the three metric calls in parallel; helper methods handle timestamp logic
        funcs = [
            MonitoringAPs.get_ap_cpu_utilization,
            MonitoringAPs.get_ap_memory_utilization,
            MonitoringAPs.get_ap_poe_utilization,
        ]

        raw_results = []
        with ThreadPoolExecutor(max_workers=3) as executor:
            future_map = {
                executor.submit(
                    func,
                    central_conn,
                    serial_number,
                    start_time,
                    end_time,
                    duration,
                ): func
                for func in funcs
            }
            for fut in as_completed(future_map):
                func = future_map[fut]
                try:
                    resp = fut.result()
                    raw_results.append(resp)
                except Exception as e:
                    # propagate the error for the caller to handle, but include which call failed
                    raise RuntimeError(
                        f"{func.__name__} metrics request failed: {e}"
                    ) from e

        if return_raw_response:
            return raw_results

        data = {}
        for resp in raw_results:
            if not isinstance(resp, dict):
                continue
            data = clean_raw_trend_data(resp, data=data)
        data = merged_dict_to_sorted_list(data)
        return data

    def get_latest_ap_stats(
        central_conn,
        serial_number,
    ):
        """
        Get the latest AP statistics (like CPU, memory, power consumption).

        Args:
            central_conn (NewCentralBase): Central connection object.
            serial_number (str): Serial number of the AP.

        Returns:
            (dict): Latest statistics for the AP, or empty dict if none exist.

        Raises:
            ParameterError: If serial_number is missing/invalid.
        """
        MonitoringAPs._validate_device_serial(serial_number)
        stats = MonitoringAPs.get_ap_stats(
            central_conn, serial_number, duration="5m"
        )
        if stats and isinstance(stats, list) and len(stats) > 0:
            return stats[-1]
        else:
            return {}

    @staticmethod
    def get_ap_cpu_utilization(
        central_conn,
        serial_number,
        start_time=None,
        end_time=None,
        duration=None,
    ):
        """
        Retrieve CPU utilization trends for an AP.

        This method makes an API call to the following endpoint - `GET network-monitoring/v1alpha1/aps/{serial_number}/cpu-utilization-trends`

        Args:
            central_conn (NewCentralBase): Central connection object.
            serial_number (str): Serial number of the AP.
            start_time (int, optional): Start time (epoch seconds) for range queries.
            end_time (int, optional): End time (epoch seconds) for range queries.
            duration (str|int, optional): Duration string or seconds for relative queries.

        Returns:
            (dict|list): API response for cpu-utilization-trends.

        Raises:
            ParameterError: If serial_number is missing/invalid.
        """
        MonitoringAPs._validate_device_serial(serial_number)
        path = f"{MONITOR_TYPE}/{serial_number}/cpu-utilization-trends"
        if start_time is None and end_time is None and duration is None:
            return execute_get(central_conn, endpoint=path)

        return execute_get(
            central_conn,
            endpoint=path,
            params={
                "filter": generate_timestamp_str(
                    start_time=start_time, end_time=end_time, duration=duration
                )
            },
        )

    @staticmethod
    def get_ap_memory_utilization(
        central_conn,
        serial_number,
        start_time=None,
        end_time=None,
        duration=None,
    ):
        """
        Retrieve memory utilization trends for an AP.

        This method makes an API call to the following endpoint -  `GET network-monitoring/v1alpha1/aps/{serial_number}/memory-utilization-trends`

        Args:
            central_conn (NewCentralBase): Central connection object.
            serial_number (str): Serial number of the AP.
            start_time (int, optional): Start time (epoch seconds) for range queries.
            end_time (int, optional): End time (epoch seconds) for range queries.
            duration (str|int, optional): Duration string or seconds for relative queries.

        Returns:
            (dict|list): API response for memory-utilization-trends.

        Raises:
            ParameterError: If serial_number is missing/invalid.
        """
        MonitoringAPs._validate_device_serial(serial_number)
        path = f"{MONITOR_TYPE}/{serial_number}/memory-utilization-trends"
        if start_time is None and end_time is None and duration is None:
            return execute_get(
                central_conn,
                endpoint=path,
            )

        return execute_get(
            central_conn,
            endpoint=path,
            params={
                "filter": generate_timestamp_str(
                    start_time=start_time, end_time=end_time, duration=duration
                )
            },
        )

    @staticmethod
    def get_ap_poe_utilization(
        central_conn,
        serial_number,
        start_time=None,
        end_time=None,
        duration=None,
    ):
        """
        Retrieve power consumption trends for an AP.

        This method makes an API call to the following endpoint - `GET network-monitoring/v1alpha1/aps/{serial_number}/power-consumption-trends`

        Args:
            central_conn (NewCentralBase): Central connection object.
            serial_number (str): Serial number of the AP.
            start_time (int, optional): Start time (epoch seconds) for range queries.
            end_time (int, optional): End time (epoch seconds) for range queries.
            duration (str|int, optional): Duration string or seconds for relative queries.

        Returns:
            (dict|list): API response for power-consumption-trends.

        Raises:
            ParameterError: If serial_number is missing/invalid.
        """
        MonitoringAPs._validate_device_serial(serial_number)
        path = f"{MONITOR_TYPE}/{serial_number}/power-consumption-trends"
        if start_time is None and end_time is None and duration is None:
            return execute_get(
                central_conn,
                endpoint=path,
            )

        return execute_get(
            central_conn,
            endpoint=path,
            params={
                "filter": generate_timestamp_str(
                    start_time=start_time, end_time=end_time, duration=duration
                )
            },
        )

    def _validate_device_serial(serial_number):
        """
        Validate AP device serial_number.

        Args:
            serial_number (str): Device serial number to validate.

        Raises:
            ParameterError: If serial_number is missing or not a string.

        Note:
            Internal SDK function
        """
        if not isinstance(serial_number, str) or not serial_number:
            raise ParameterError(
                "serial_number is required and must be a string"
            )
