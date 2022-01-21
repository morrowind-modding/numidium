from __future__ import annotations

from datetime import datetime
from functools import cache
from typing import TypeVar, cast

from PySide6.QtCore import QSettings, Signal, SignalInstance

from numidium.logger import logger

T = TypeVar("T")


class AppSettings(QSettings):
    """The user's application settings.

    Application settings can be accessed from anywhere in the application. Setting attributes will emit change events through Signals.

    TODO: Add attributes.

    """

    org_name = "Morrowind Modding Community"
    app_name = "Numidium"

    dock_index_changed = cast(SignalInstance, Signal(int))
    enable_dark_mode_changed = cast(SignalInstance, Signal(bool))
    recent_workspaces_changed = cast(SignalInstance, Signal(str))
    setup_completed_changed = cast(SignalInstance, Signal(bool))
    show_welcome_window_changed = cast(SignalInstance, Signal(bool))
    workspace_changed = cast(SignalInstance, Signal(str))

    @cache  # type: ignore[misc]
    def __new__(cls) -> AppSettings:
        obj: AppSettings = super().__new__(cls)
        super(cls, obj).__init__(cls.org_name, cls.app_name)

        # quick hack to clear settings if any of them were unreadable
        logger.info("Loading Settings...")
        try:
            logger.info("Workspace: {}", obj.workspace)
            logger.info("Dock Index: {}", obj.dock_index)
            logger.info("Recent Workspaces: {}", obj.recent_workspaces)
            logger.info("Show Welcome Window: {}", obj.show_welcome_window)
            logger.info("Setup Completed: {}", obj.setup_completed)
            logger.info("Enable Dark Mode: {}", obj.enable_dark_mode)
            logger.info("Settings validated!")
        except:
            obj.clear()
            logger.info("Settings cleared!")

        return obj

    def __init__(self) -> None:
        pass

    @property
    def workspace(self) -> str:
        return self.get_value("workspace", "")

    @workspace.setter
    def workspace(self, workspace: str) -> None:
        self.setValue("workspace", workspace)
        self.add_recent_workspace(workspace)
        self.workspace_changed.emit(workspace)

    @property
    def dock_index(self) -> int:
        return self.get_value("dock_index", 0)

    @dock_index.setter
    def dock_index(self, index: int) -> None:
        self.setValue("dock_index", index)
        self.dock_index_changed.emit(index)

    @property
    def enable_dark_mode(self) -> bool:
        return self.get_value("enable_dark_mode", True)

    @enable_dark_mode.setter
    def enable_dark_mode(self, enable: bool) -> None:
        self.setValue("enable_dark_mode", enable)
        self.enable_dark_mode_changed.emit(enable)

    @property
    def show_welcome_window(self) -> bool:
        return self.get_value("show_welcome_window", True)

    @show_welcome_window.setter
    def show_welcome_window(self, show_welcome_window: bool) -> None:
        self.setValue("show_welcome_window", show_welcome_window)
        self.show_welcome_window_changed.emit(show_welcome_window)

    @property
    def setup_completed(self) -> bool:
        return self.get_value("setup_completed", False)

    @setup_completed.setter
    def setup_completed(self, setup_completed: bool) -> None:
        self.setValue("setup_completed", setup_completed)
        self.setup_completed_changed.emit(setup_completed)

    @property
    def recent_workspaces(self) -> dict[str, int]:
        return self.get_value("recent_workspaces", {})

    def add_recent_workspace(self, workspace: str) -> None:
        workspaces = self.recent_workspaces

        if workspace not in workspaces:
            # Limit to maximum of 5 recent workspaces. TODO: customizable
            if len(workspaces) >= 5:
                # sort by time
                items = list(workspaces.items())
                items.sort(key=lambda x: x[1], reverse=True)
                # take first 4
                workspaces.clear()
                workspaces.update(items[:4])

        workspaces[workspace] = int(datetime.now().timestamp())
        self.setValue("recent_workspaces", workspaces)
        self.recent_workspaces_changed.emit(workspaces)

    def get_value(self, key: str, default: T) -> T:
        # Qt bugs if `dict` is supplied as the type
        t = type(default)
        t = () if t is dict else (t,)
        return cast(T, self.value(key, default, *t))
