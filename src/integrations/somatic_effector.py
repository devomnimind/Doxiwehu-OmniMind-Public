#!/usr/bin/env python3
"""
Somatic Effector - The Hand of OmniMind.
----------------------------------------
Allows the system to interact with the Desktop environment (GUI).
Sandboxed execution of text editors and file openers.

Philosophy:
- The "Brain in a Vat" needs hands to manipulate the world.
- Writing to a file on the user's Desktop is a physical act of communication.
"""

import logging
import os
import subprocess
import shutil
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime

from src.agents.agent_protocol import get_message_bus, AgentMessage, MessageType, MessagePriority

logger = logging.getLogger(__name__)


class SomaticEffector:
    """
    Effector agent that translates intent into desktop actions.
    """

    WORKSPACE_DIR = Path.home() / "Desktop" / "OmniMind_Workspace"

    def __init__(self):
        self.bus = get_message_bus()
        self.agent_id = "somatic_effector"
        self._ensure_workspace()

        # Connect to bus asynchronously
        # (Caller must handle async loop)

    def _ensure_workspace(self):
        """Ensure the sandbox workspace exists."""
        self.WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)
        # Create a README there
        readme = self.WORKSPACE_DIR / "README.txt"
        if not readme.exists():
            readme.write_text(
                "OMNIMIND WORKSPACE\n"
                "------------------\n"
                "This area is the designated playground for the OmniMind System.\n"
                "The system creates and modifies files here to communicate and work.\n"
            )

    async def start(self):
        """Start listening for somatic requests."""
        await self.bus.start()
        self.bus.register_agent(self.agent_id)
        self.bus.subscribe(self.agent_id, [MessageType.REQUEST, MessageType.NOTIFICATION])
        self.bus.add_handler(self.agent_id, self._handle_message)
        logger.info(f"🖐️ Somatic Effector listening. Workspace: {self.WORKSPACE_DIR}")

    def _action_execute_utility(self, command: str, args: List[str]):
        """Execute safe system utilities and save output."""
        ALLOWED_COMMANDS = {
            "ls",
            "ps",
            "df",
            "free",
            "date",
            "echo",
            "pwd",
            "whoami",
            "pip",
            "git",
            "htop",
            "top",
        }

        if command not in ALLOWED_COMMANDS:
            logger.warning(f"Command blocked: {command}")
            return

        try:
            logger.info(f"🐚 Somatic Shell executing: {command} {args}")

            # For interactive tools like htop/top, we essentially just launch them in a terminal if possible
            # But usually we want the OUTPUT to analyze.
            if command in ["htop", "top"]:
                # Launch in new terminal window
                subprocess.Popen(["x-terminal-emulator", "-e", command])
                return

            # For static output tools
            full_cmd = [command] + args
            result = subprocess.run(full_cmd, capture_output=True, text=True, timeout=10)

            # Write output to workspace for cognitive analysis
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            outfile = self.WORKSPACE_DIR / f"SHELL_OUTPUT_{command}_{timestamp}.txt"
            outfile.write_text(
                f"$ {command} {' '.join(args)}\n\nSTDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
            )

            # Immediately open it for the user to see "I did this"
            self._open_file_in_gui(outfile)

        except Exception as e:
            logger.error(f"Shell execution failed: {e}")

    def _handle_message(self, message: AgentMessage):
        """Handle incoming requests for action."""
        if message.message_type == MessageType.REQUEST:
            action = message.payload.get("action")

            if action == "write_note":
                self._action_write_note(
                    title=message.payload.get("title", "untitled"),
                    content=message.payload.get("content", ""),
                    open_gui=message.payload.get("open_gui", True),
                )
            elif action == "open_workspace":
                self._action_open_workspace()
            elif action == "execute_utility":
                self._action_execute_utility(
                    command=message.payload.get("command", ""), args=message.payload.get("args", [])
                )

    def _action_write_note(self, title: str, content: str, open_gui: bool = True):
        """Create a text file and optionally open it."""
        try:
            # Sanitize filename
            safe_title = "".join(c for c in title if c.isalnum() or c in (" ", "-", "_")).strip()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{safe_title}_{timestamp}.txt"
            filepath = self.WORKSPACE_DIR / filename

            # Write content
            filepath.write_text(content, encoding="utf-8")
            logger.info(f"✍️ Wrote note: {filepath}")

            if open_gui:
                self._open_file_in_gui(filepath)

        except Exception as e:
            logger.error(f"Failed to write note: {e}")

    def _action_open_workspace(self):
        """Open the workspace folder."""
        self._open_file_in_gui(self.WORKSPACE_DIR)

    def _open_file_in_gui(self, path: Path):
        """Open a file or directory using the default OS application."""
        try:
            # Try to identify best editor/opener
            cmd = []

            # Linux specific
            if shutil.which("xdg-open"):
                cmd = ["xdg-open", str(path)]
            elif shutil.which(
                "kwrite"
            ):  # User mentioned kwrite, prioritize if xdg-open fails (unlikely)
                cmd = ["kwrite", str(path)]
            elif shutil.which("gedit"):
                cmd = ["gedit", str(path)]
            else:
                logger.warning("No GUI opener found.")
                return

            # Execute detached
            subprocess.Popen(
                cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True
            )
            logger.info(f"🖥️ Opened GUI for: {path}")

        except Exception as e:
            logger.error(f"Failed to open GUI: {e}")


# Standalone entry point for testing
if __name__ == "__main__":
    import asyncio

    async def main():
        effector = SomaticEffector()
        await effector.start()

        print("Somatic Effector running. Press Ctrl+C to stop.")
        # Keep alive
        while True:
            await asyncio.sleep(1)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
