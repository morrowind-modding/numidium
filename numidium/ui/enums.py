from typing import TYPE_CHECKING

from PySide6.QtCore import Qt

if not TYPE_CHECKING:
    AlignmentFlag = Qt.AlignmentFlag
    ItemDataRole = Qt.ItemDataRole
else:
    from enum import IntEnum

    class AlignmentFlag(IntEnum, Qt.Alignment):
        AlignLeading = Qt.AlignLeading
        AlignLeft = Qt.AlignLeft
        AlignRight = Qt.AlignRight
        AlignTrailing = Qt.AlignTrailing
        AlignHCenter = Qt.AlignHCenter
        AlignJustify = Qt.AlignJustify
        AlignAbsolute = Qt.AlignAbsolute
        AlignHorizontal_Mask = Qt.AlignHorizontal_Mask
        AlignTop = Qt.AlignTop
        AlignBottom = Qt.AlignBottom
        AlignVCenter = Qt.AlignVCenter
        AlignCenter = Qt.AlignCenter
        AlignBaseline = Qt.AlignBaseline
        AlignVertical_Mask = Qt.AlignVertical_Mask

    class ItemDataRole(IntEnum):
        DisplayRole = Qt.DisplayRole
        DecorationRole = Qt.DecorationRole
        EditRole = Qt.EditRole
        ToolTipRole = Qt.ToolTipRole
        StatusTipRole = Qt.StatusTipRole
        WhatsThisRole = Qt.WhatsThisRole
        FontRole = Qt.FontRole
        TextAlignmentRole = Qt.TextAlignmentRole
        BackgroundRole = Qt.BackgroundRole
        ForegroundRole = Qt.ForegroundRole
        CheckStateRole = Qt.CheckStateRole
        AccessibleTextRole = Qt.AccessibleTextRole
        AccessibleDescriptionRole = Qt.AccessibleDescriptionRole
        SizeHintRole = Qt.SizeHintRole
        InitialSortOrderRole = Qt.InitialSortOrderRole
        DisplayPropertyRole = Qt.DisplayPropertyRole
        DecorationPropertyRole = Qt.DecorationPropertyRole
        ToolTipPropertyRole = Qt.ToolTipPropertyRole
        StatusTipPropertyRole = Qt.StatusTipPropertyRole
        WhatsThisPropertyRole = Qt.WhatsThisPropertyRole
        UserRole = Qt.UserRole
