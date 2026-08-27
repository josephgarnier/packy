"""Translation helpers for Qt internationalization.

Copyright 2023-present, Marie-Neige Chapel and Joseph Garnier
All rights reserved.

See LICENSE.md file for more information.
"""

# Third-party
from PySide6.QtCore import QT_TR_NOOP, QT_TRANSLATE_NOOP

# Standard library
from typing import cast


# -----------------------------------------------------------------------------
def PACKY_TR_NOOP(text: str) -> str:  # noqa: N802
    """Marks a string for translation without translating it immediately.

    Args:
        text (str): The source text to mark for translation.

    Returns:
        str: The marked text, usable with Qt translation tools.
    """
    return cast("str", QT_TR_NOOP(text))


# -----------------------------------------------------------------------------
def PACKY_TRANSLATE_NOOP(context: str, text: str) -> str:  # noqa: N802
    """Marks a string with a specific context for deferred translation.

    Args:
        context (str): The translation context.
        text (str): The source text to mark for translation.

    Returns:
        str: The marked text associated with the given context.
    """
    return cast("str", QT_TRANSLATE_NOOP(context, text))
