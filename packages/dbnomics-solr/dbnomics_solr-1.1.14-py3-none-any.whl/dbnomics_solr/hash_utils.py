"""Hash utils."""

from pathlib import Path
from typing import cast

from dirhash import dirhash


def compute_dir_hash(dir_path: Path, /, *, jobs: int = 1) -> str:
    """Compute a hash for a directory in an opinionated way.

    Follows the [dirhash standard](https://github.com/andhus/dirhash).
    """
    return cast(str, dirhash(dir_path, algorithm="sha1", jobs=jobs))
