from __future__ import annotations

import sys

import loguru


def _format(record: loguru.Record) -> str:
    source = "{file}:{line}".format(**record)
    record["extra"]["source"] = source[-16:]
    return (
        "<green>{time:HH:mm:ss.SSS}</green>"
        " | "
        "<level>{level:^8}</level>"
        " | "
        "<cyan>{extra[source]:>16}</cyan>"
        " | "
        "<level>{message}</level>"
        "\n"
    )


logger = loguru.logger
logger.remove()
logger.add(sys.stderr, format=_format)
