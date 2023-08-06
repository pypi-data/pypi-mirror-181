"""CLI utils."""

__all__ = ["list_callback"]


def list_callback(values: list[str]) -> list[str]:
    """Parse comma-separated values."""

    def iter_values():
        for value in values:
            for part in value.split(","):
                yield part.strip()

    return list(iter_values())
