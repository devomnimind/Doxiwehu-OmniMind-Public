from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

import dbus  # type: ignore[import-untyped]

logger = logging.getLogger(__name__)


class DBusSessionController:
    _ACTION_MAP = {
        "play": "Play",
        "pause": "Pause",
        "playpause": "PlayPause",
        "next": "Next",
        "previous": "Previous",
        "stop": "Stop",
    }

    def __init__(self, bus: Optional[Any] = None) -> None:
        self._bus = bus or dbus.SessionBus()

    def control_media_player(
        self, action: str, player_bus_name: str = "org.mpris.MediaPlayer2.vlc"
    ) -> Dict[str, Any]:
        action_key = action.lower().strip()
        method_name = self._ACTION_MAP.get(action_key)
        if not method_name:
            return {"success": False, "error": f"Unsupported action {action}"}
        try:
            proxy = self._bus.get_object(player_bus_name, "/org/mpris/MediaPlayer2")
            interface = dbus.Interface(proxy, "org.mpris.MediaPlayer2.Player")
            getattr(interface, method_name)()
            return {
                "success": True,
                "player": player_bus_name,
                "action": action_key,
            }
        except dbus.DBusException as exc:
            logger.warning(
                "Failed to control media player %s: %s", player_bus_name, exc
            )
            return {"success": False, "error": str(exc)}
        except AttributeError as exc:
            return {"success": False, "error": str(exc)}

    def list_media_players(self) -> List[str]:
        try:
            proxy = self._bus.get_object(
                "org.freedesktop.DBus", "/org/freedesktop/DBus"
            )
            interface = dbus.Interface(proxy, "org.freedesktop.DBus")
            names = interface.ListNames()
            return [n for n in names if n.startswith("org.mpris.MediaPlayer2.")]
        except dbus.DBusException as exc:
            logger.debug("Unable to list media players: %s", exc)
            return []


class DBusSystemController:
    _NETWORK_STATES = {
        0: "UNKNOWN",
        10: "ASLEEP",
        20: "DISCONNECTED",
        30: "DISCONNECTING",
        40: "CONNECTING",
        50: "CONNECTED_LOCAL",
        60: "CONNECTED_SITE",
        70: "CONNECTED_GLOBAL",
    }
    _CONNECTIVITY = {
        0: "UNKNOWN",
        1: "NONE",
        2: "PORTAL",
        3: "LIMITED",
        4: "FULL",
    }

    def __init__(self, bus: Optional[Any] = None) -> None:
        self._bus = bus or dbus.SystemBus()

    def get_network_status(self) -> Dict[str, Any]:
        try:
            proxy = self._bus.get_object(
                "org.freedesktop.NetworkManager", "/org/freedesktop/NetworkManager"
            )
            props = dbus.Interface(proxy, "org.freedesktop.DBus.Properties")
            state = int(props.Get("org.freedesktop.NetworkManager", "State"))
            connectivity = int(
                props.Get("org.freedesktop.NetworkManager", "Connectivity")
            )
            connections = props.Get(
                "org.freedesktop.NetworkManager", "ActiveConnections"
            )
            return {
                "state": self._NETWORK_STATES.get(state, "UNKNOWN"),
                "connectivity": self._CONNECTIVITY.get(connectivity, "UNKNOWN"),
                "active_connections": len(connections) if connections else 0,
            }
        except dbus.DBusException as exc:
            logger.debug("NetworkManager query failed: %s", exc)
            return {"error": str(exc)}

    def get_power_status(self) -> Dict[str, Any]:
        try:
            proxy = self._bus.get_object(
                "org.freedesktop.UPower", "/org/freedesktop/UPower"
            )
            props = dbus.Interface(proxy, "org.freedesktop.DBus.Properties")
            on_battery = bool(props.Get("org.freedesktop.UPower", "OnBattery"))
            percentage = float(props.Get("org.freedesktop.UPower", "Percentage"))
            return {"on_battery": on_battery, "percentage": percentage}
        except dbus.DBusException as exc:
            logger.debug("UPower query failed: %s", exc)
            return {"error": str(exc)}
