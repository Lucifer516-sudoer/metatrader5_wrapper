from datetime import UTC, datetime


def unix_to_datetime(timestamp: int) -> datetime:
    return datetime.fromtimestamp(timestamp, tz=UTC)
