from datetime import datetime, timezone


def get_current_timestamp() -> str:
    """Generates a clean ISO formatted UTC timestamp string."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def format_tags_to_string(tags: list) -> str:
    return ",".join(tags)
    # syntax is "seperator".join(list) this returns a string seperated by commas


def format_string_to_tags(tags_string: str) -> list:
    return tags_string.split(",")
    # syntax is string.split("seperator") this returns a list of tags split by commas
