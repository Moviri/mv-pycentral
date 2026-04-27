from datetime import datetime, timedelta, timezone

from pycentral.utils.url_utils import generate_url

from ..exceptions import ParameterError
import re


DEFAULT_MAX_PERIOD_DAYS = 90


def build_timestamp_filter(
    start_time=None,
    end_time=None,
    duration=None,
    fmt="rfc3339",
    max_period_days=DEFAULT_MAX_PERIOD_DAYS,
):
    """Build a formatted timestamp filter for API queries.

    Returns timestamps for filtering based on the provided parameters.

    Behavior:
        - If start_time and end_time are given, parses and converts them to the
          requested format.
        - If duration is given, computes timestamps relative to now.
                - Max supported duration defaults to 90 days and can be overridden.

    Args:
        start_time (str, optional): RFC3339 or Unix timestamp (ms or s) for start.
        end_time (str, optional): RFC3339 or Unix timestamp (ms or s) for end.
        duration (str, optional): Duration string like '3h', '2d', '1w', '1m'
            (hours, days, weeks, minutes).
        fmt (str, optional): Output format, either 'rfc3339' or 'unix'.
        max_period_days (int|float, optional): Maximum allowed duration, in days.
            Defaults to DEFAULT_MAX_PERIOD_DAYS.

    Returns:
        (tuple): A tuple of (start_time, end_time) formatted strings.

    Raises:
        ValueError: If invalid parameter combinations are provided, the maximum
            duration is invalid, or duration exceeds the configured maximum.
    """
    # --- Validation ---
    if (start_time or end_time) and duration:
        raise ValueError("Cannot specify start/end timestamps together with duration.")
    if (start_time and not end_time) or (end_time and not start_time):
        raise ValueError("Both start_time and end_time must be provided together.")
    if not duration and not (start_time and end_time):
        raise ValueError("Provide either both start_time and end_time or a duration.")
    if max_period_days is None or max_period_days <= 0:
        raise ValueError("max_period_days must be greater than 0.")

    # --- Case 1: Start + End ---
    if start_time and end_time:
        return (
            _format_timestamp(_parse_timestamp(start_time), fmt),
            _format_timestamp(_parse_timestamp(end_time), fmt),
        )

    # --- Case 2: Duration ---
    unit_map = {"w": "weeks", "d": "days", "h": "hours", "m": "minutes"}
    unit = duration[-1].lower()
    if unit not in unit_map:
        raise ValueError(
            "Duration must end with w, h, d, or m (weeks, hours, days, mins)."
        )

    delta = timedelta(**{unit_map[unit]: int(duration[:-1])})
    if delta > timedelta(days=max_period_days):
        raise ValueError(
            f"Maximum supported duration is {max_period_days} days."
        )

    now = datetime.now(timezone.utc)
    return _format_timestamp(now - delta, fmt), _format_timestamp(now, fmt)


def _parse_timestamp(ts):
    """Parse an RFC3339 string or Unix ms/s value into a UTC datetime."""
    if isinstance(ts, str):
        try:
            return datetime.fromisoformat(ts.replace("Z", "+00:00"))
        except ValueError:
            ts = float(ts)
    val = float(ts)
    if val > 1e10:
        val /= 1000
    return datetime.fromtimestamp(val, tz=timezone.utc)


def _format_timestamp(dt, fmt):
    """Format a UTC datetime as a Unix ms string or RFC3339 string."""
    if fmt == "unix":
        return str(int(dt.timestamp() * 1000))
    return dt.isoformat().replace("+00:00", "Z")


def generate_timestamp_str(
    start_time, end_time, duration, max_period_days=DEFAULT_MAX_PERIOD_DAYS
):
    """Generate a timestamp filter string for API queries.

    Args:
        start_time (str): Start timestamp.
        end_time (str): End timestamp.
        duration (str): Duration string.
        max_period_days (int|float, optional): Maximum allowed duration, in days.

    Returns:
        (str): Formatted filter string "timestamp gt <start> and timestamp lt <end>".
    """
    start_time, end_time = build_timestamp_filter(
        start_time=start_time,
        end_time=end_time,
        duration=duration,
        max_period_days=max_period_days,
    )
    return f"timestamp gt {start_time} and timestamp lt {end_time}"


def execute_get(central_conn, endpoint, params={}, version="latest"):
    """Execute a GET request to the monitoring API.

    Args:
        central_conn (NewCentralBase): Central connection object.
        endpoint (str): API endpoint path.
        params (dict, optional): Query parameters for the request.
        version (str, optional): API version to use (e.g. "v1alpha1", "v1"). Defaults to "latest".

    Returns:
        (dict): The message portion of the API response.

    Raises:
        ParameterError: If central_conn is None or endpoint is invalid.
        Exception: If the API call returns a non-200 status code.
    """
    if not central_conn:
        raise ParameterError("central_conn(Central connection) is required")

    if not endpoint or not isinstance(endpoint, str) and len(endpoint) == 0:
        raise ParameterError("endpoint is required and must be a string")

    if endpoint.startswith("/"):
        # remove leading slash if present
        endpoint = endpoint.lstrip("/")

    path = generate_url(endpoint, "monitoring", version)
    resp = central_conn.command("GET", path, api_params=params)

    if resp["code"] != 200:
        raise Exception(
            f"Error retrieving data from {path}: {resp['code']} - {resp['msg']}"
        )
    return resp["msg"]


def simplified_site_resp(site):
    """Simplify the site response structure for easier consumption.

    Args:
        site (dict): Raw site data from API response.

    Returns:
        (dict): Simplified site data with restructured health, devices, clients, and alerts.
    """
    site["health"] = _groups_to_dict(site.get("health", {}).get("groups", []))
    site["devices"] = {
        "count": site.get("devices", {}).get("count", 0),
        "health": _groups_to_dict(
            site.get("devices", {}).get("health", {}).get("groups", [])
        ),
    }
    site["clients"] = {
        "count": site.get("clients", {}).get("count", 0),
        "health": _groups_to_dict(
            site.get("clients", {}).get("health", {}).get("groups", [])
        ),
    }
    site["alerts"] = {
        "critical": site.get("alerts", {}).get("groups", [{}])[0].get("count", 0)
        if site.get("alerts", {}).get("groups")
        else 0,
        "total": site.get("alerts", {}).get("totalCount", 0),
    }
    site.pop("type", None)
    return site


def _groups_to_dict(groups_list):
    """Convert a list of group objects to a dictionary.

    Args:
        groups_list (list): List of group dictionaries with 'name' and 'value' keys.

    Returns:
        (dict): Dictionary with group names as keys and values as values.
            Defaults to {"Poor": 0, "Fair": 0, "Good": 0}.
    """
    result = {"Poor": 0, "Fair": 0, "Good": 0}
    if isinstance(groups_list, list):
        for group in groups_list:
            if isinstance(group, dict) and "name" in group and "value" in group:
                result[group["name"]] = group["value"]
    return result


def clean_switch_trend_data(raw_response):
    """Process switch trend responses into a normalized list.

    Handles all formats returned by the switch trend endpoints:
    - Top-N interface trends: ``response.items``
    - Hardware trends: ``response.switchMetrics[].samples`` with top-level ``keys``
    - Interface trends: ``response.samples`` with top-level ``keys``

    Timestamps are converted from epoch milliseconds to RFC3339 (UTC).

    Args:
        raw_response (dict): Raw response from ``execute_get`` for a switch trend endpoint.

    Returns:
        (list[dict]):
            - Top-N endpoint: ``response.items`` list as-is.
            - Hardware/interface trends: sorted list of dicts with ``timestamp`` and one
              key per metric. Hardware trends for stacked switches also include
              ``serialNumber``.
    """
    inner = raw_response.get("response", {}) if isinstance(raw_response, dict) else {}

    # Top-N interface trends: response.items
    if isinstance(inner, dict):
        items = inner.get("items")
        if isinstance(items, list):
            return items

    keys = inner.get("keys", [])
    rows = []

    # Hardware trends: switchMetrics[].samples
    for switch_metric in inner.get("switchMetrics", []):
        serial = switch_metric.get("serialNumber")
        for sample in switch_metric.get("samples", []):
            ts_ms = sample.get("timestamp")
            data = sample.get("data")
            if ts_ms is None or not data:
                continue
            ts = datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc).strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            )
            row = {"timestamp": ts}
            if serial:
                row["serialNumber"] = serial
            for k, v in zip(keys, data):
                if v is not None:
                    row[k] = v
            rows.append(row)

    # Interface trends: samples directly at response level
    if not rows:
        for sample in inner.get("samples", []):
            ts_ms = sample.get("timestamp")
            data = sample.get("data")
            if ts_ms is None or not data:
                continue
            ts = datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc).strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            )
            row = {"timestamp": ts}
            for k, v in zip(keys, data):
                if v is not None:
                    row[k] = v
            rows.append(row)

    return sorted(rows, key=lambda r: r["timestamp"])


def clean_raw_trend_data(raw_results, data=None):
    """Clean and restructure raw trend data from API response.

    Args:
        raw_results (dict): Raw trend data containing 'graph' with 'keys' and 'samples'.
        data (dict, optional): Existing data dictionary to append to.

    Returns:
        (dict): Dictionary with timestamps as keys and metric values as nested dictionaries.
    """
    if data is None:
        data = {}
    graph = raw_results.get("graph", {}) or {}
    keys = graph.get("keys", []) or []
    samples = graph.get("samples", []) or []

    for s in samples:
        ts = s.get("timestamp")
        if not ts:
            continue
        vals = s.get("data")
        if isinstance(vals, (list, tuple)):
            for k, v in zip(keys, vals):
                data.setdefault(ts, {})[k] = v
        else:
            target_key = keys[0] if keys else None
            if target_key:
                data.setdefault(ts, {})[target_key] = vals
            else:
                # fallback to a generic key if none provided
                data.setdefault(ts, {})["value"] = vals
    return data


def merged_dict_to_sorted_list(merged):
    """Convert a merged dictionary to a sorted list of timestamped entries.

    Args:
        merged (dict): Dictionary with timestamps as keys.

    Returns:
        (list): Sorted list of dictionaries with 'timestamp' key and all associated values.
    """
    # try strict RFC3339 parsing (Z -> +00:00), fallback to lexicographic
    try:
        keys = sorted(
            merged.keys(),
            key=lambda t: datetime.fromisoformat(t.replace("Z", "+00:00")),
        )
    except Exception:
        keys = sorted(merged.keys())
    return [{"timestamp": ts, **merged[ts]} for ts in keys]


def _validate_mac_address(mac):
    """
    Validate a MAC address string and return True if valid.
    Accepts the format AA:BB:CC:DD:EE:FF

    Args:
        mac (str): MAC address string to validate.

    Returns:
        (bool): True if the MAC address is valid.

    Raises:
        ParameterError: If mac is missing or does not match the expected format.

    Note:
        Internal SDK function
    """
    _MAC_PATTERN = re.compile(r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$")
    if not mac:
        raise ParameterError("MAC address is required")
    if not isinstance(mac, str) or not _MAC_PATTERN.match(mac):
        raise ParameterError(
            f"Invalid MAC address format: '{mac}'. Expected format: AA:BB:CC:DD:EE:FF"
        )
    return True


def validate_device_serial(serial_number):
    """
    Validate device serial number.

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


def validate_central_conn_and_serial(central_conn, serial_number):
    """
    Validate central connection and device serial number.

    Args:
        central_conn (NewCentralBase): Central connection object (required).
        serial_number (str): Device serial number (required).

    Raises:
        ParameterError: If central_conn is None or serial_number is missing/invalid.

    Note:
        Internal SDK function
    """
    if central_conn is None:
        raise ParameterError("central_conn is required")
    if not isinstance(serial_number, str) or not serial_number:
        raise ParameterError(
            "serial_number is required and must be a string"
        )
