import httpx

__all__ = ["measure_response_time"]


def measure_response_time(url: str) -> float:
    """
    Measure the response time of the GET request to the given URL.
    """
    r = httpx.get(url)
    return r.elapsed.total_seconds()
