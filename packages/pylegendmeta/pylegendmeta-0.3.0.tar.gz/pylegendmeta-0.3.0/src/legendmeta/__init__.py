"""A package to access `legend-metadata <https://github.com/legend-exp/legend-metadata>`_ in Python."""

from legendmeta._version import version as __version__
from legendmeta.core import LegendMetadata
from legendmeta.jsondb import JsonDB

__all__ = ["__version__", "LegendMetadata", "JsonDB"]
