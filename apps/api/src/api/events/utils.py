import httpx


def get_location_from_ip(ip_address: str) -> tuple[str, str]:
    """
    Fetches the country and city for a given IP address using ip-api.com.
    Returns a tuple of (country, city).
    """
    if not ip_address or ip_address in ("127.0.0.1", "::1", "localhost"):
        return "Unknown", "Unknown"

    try:
        response = httpx.get(f"http://ip-api.com/json/{ip_address}", timeout=2.0)
        response.raise_for_status()
        data = response.json()

        if data.get("status") == "success":
            return data.get("country", "Unknown"), data.get("city", "Unknown")
    except Exception:
        pass

    return "Unknown", "Unknown"
