import os
# --- Window and Layout Settings ---
FULLSCREEN = True   # Launch app in fullscreen by default
WINDOW_WIDTH = 1200 # Minimum width
WINDOW_HEIGHT = 800 # Minimum height
SIDEBAR_WIDTH = 270 # Width of the left command/notes sidebar
HELP_OVERLAY_BG = "#181830" # Help overlay panel background

# --- Color Palette ---
CONSOLE_BG = "#0a0a0a"
DISPLAY_BG = "#1a1a1a"
SIDEBAR_BG = "#13131f"
CONSOLE_FG = "#00ff00"
ACCENT_COLOR = "#00ffff"
WARNING_COLOR = "#ffcc00"
ERROR_COLOR = "#ff4040"
SUCCESS_COLOR = "#33ff66"
BUTTON_COLOR = "#333333"
ACTIVE_BUTTON_COLOR = "#555555"
SIDEBAR_FG = "#66fff6"
HELP_FG = "#fffbc4"

# --- Font Styles ---
MONOSPACE_FONT_NAME = "Consolas"
ALT_FONT_NAME = "Courier New"
TITLE_FONT_SIZE = 28
MAIN_TEXT_SIZE = 15
SMALL_TEXT_SIZE = 11
SHELL_FONT_SIZE = 13
SIDEBAR_FONT_SIZE = 13
HELP_FONT_SIZE = 15

TITLE_FONT = (MONOSPACE_FONT_NAME, TITLE_FONT_SIZE, "bold")
MAIN_FONT = (MONOSPACE_FONT_NAME, MAIN_TEXT_SIZE, "bold")
SMALL_FONT = (MONOSPACE_FONT_NAME, SMALL_TEXT_SIZE)
SHELL_FONT = (MONOSPACE_FONT_NAME, SHELL_FONT_SIZE)
SIDEBAR_FONT = (MONOSPACE_FONT_NAME, SIDEBAR_FONT_SIZE, "bold")
HELP_FONT = (ALT_FONT_NAME, HELP_FONT_SIZE)

# --- Sound File Paths ---
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
SOUNDS_DIR = os.path.join(ROOT_DIR, "sounds")

SOUND_BOOT = os.path.join(SOUNDS_DIR, "boot.mp3")
SOUND_WHIRR = os.path.join(SOUNDS_DIR, "whirr.mp3")
SOUND_GLITCH = os.path.join(SOUNDS_DIR, "glitch.mp3")
SOUND_BEEP = os.path.join(SOUNDS_DIR, "beep.mp3")
SOUND_ERROR = os.path.join(SOUNDS_DIR, "error.mp3")
SOUND_MODULE_SWITCH = os.path.join(SOUNDS_DIR, "module_switch.mp3")

# --- Command Definitions ---
COMMANDS = [
    ("start anomaly_remediation", "Start anomaly remediation game module"),
    ("view logs", "Show scrolling system diagnostic log"),
    ("view map", "Show dynamic temporal anomaly map"),
    ("back", "Return to main TARC-U shell"),
    ("help", "Show this help panel"),
    ("clear", "Clear shell/system message log"),
    ("exit", "Exit TARC-U"),
    ("reboot", "Reboot TARC-U OS"),
]

COMMAND_ALIASES = {
    "start diagnostic_viewer": "view logs",
    "start temporal_map": "view map",
    "shutdown": "exit",
}

HELP_INTRO = (
    "Welcome, Operator!\n"
    "You are in charge of resolving escalating brain rot anomalies in the timeline. "
    "Use commands (see left panel or type 'help') to switch modules, resolve events, "
    "investigate logs, and restore questionable order to history.\n\n"
    "• Start by typing a command below, or click a module in the sidebar.\n"
    "• At any time, type 'back' to return here or 'help' to view this message.\n\n"
    "Good luck - timeline integrity is, as always, questionable."
)

# --- Other UI Constants ---
LOG_MAX_LINES = 250
LOG_INFO_COLOR = CONSOLE_FG
LOG_WARN_COLOR = WARNING_COLOR
LOG_ERROR_COLOR = ERROR_COLOR

