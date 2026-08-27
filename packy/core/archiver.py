"""Define archive format and compression option enumerations.

Copyright 2023-present, Marie-Neige Chapel and Joseph Garnier
All rights reserved.

See LICENSE.md file for more information.
"""

# Standard library
from enum import IntEnum, auto, unique
from typing import override


###############################################################################
class Archiver:
    """Group archive format and compression option enumerations."""

    ###########################################################################
    @unique
    class Format(IntEnum):
        """Represent the available archive formats."""

        ZIP = 0
        TAR = auto()
        BZ2 = auto()
        TBZ = auto()
        GZ = auto()
        TGZ = auto()
        LZMA = auto()
        TLZ = auto()
        XZ = auto()

        # ---------------------------------------------------------------------
        @override
        def __repr__(self) -> str:
            cls_name = self.__class__.__name__
            return f"{cls_name}.{self.name}(name={self.name!r}, value={int(self.value)!r})"

        # ---------------------------------------------------------------------
        @override
        def __str__(self) -> str:
            cls_name = self.__class__.__name__
            return f"{cls_name}.{self.name}({int(self.value)})"

        # ---------------------------------------------------------------------
        @override
        def __format__(self, format_spec: str) -> str:
            return format(str(self), format_spec)

    ###########################################################################
    @unique
    class CompressionMethod(IntEnum):
        """Represent the available compression methods."""

        DEFLATE = 0
        STORE = auto()
        OPTIMAL = auto()

        # ---------------------------------------------------------------------
        @override
        def __repr__(self) -> str:
            cls_name = self.__class__.__name__
            return f"{cls_name}.{self.name}(name={self.name!r}, value={int(self.value)!r})"

        # ---------------------------------------------------------------------
        @override
        def __str__(self) -> str:
            cls_name = self.__class__.__name__
            return f"{cls_name}.{self.name}({int(self.value)})"

        # ---------------------------------------------------------------------
        @override
        def __format__(self, format_spec: str) -> str:
            return format(str(self), format_spec)

    ###########################################################################
    @unique
    class CompressionLevel(IntEnum):
        """Represent the available compression levels."""

        NORMAL = 0
        MAXIMUM = auto()
        FAST = auto()
        FASTEST = auto()

        # ---------------------------------------------------------------------
        @override
        def __repr__(self) -> str:
            cls_name = self.__class__.__name__
            return f"{cls_name}.{self.name}(name={self.name!r}, value={int(self.value)!r})"

        # ---------------------------------------------------------------------
        @override
        def __str__(self) -> str:
            cls_name = self.__class__.__name__
            return f"{cls_name}.{self.name}({int(self.value)})"

        # ---------------------------------------------------------------------
        @override
        def __format__(self, format_spec: str) -> str:
            return format(str(self), format_spec)
