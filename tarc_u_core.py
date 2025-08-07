import tkinter as tk
import sys
import os
import random

from config import (
    FULLSCREEN, WINDOW_WIDTH, WINDOW_HEIGHT, SIDEBAR_WIDTH,
    CONSOLE_BG, CONSOLE_FG, ACCENT_COLOR, WARNING_COLOR, ERROR_COLOR,
    TITLE_FONT, SHELL_FONT, SMALL_FONT, SIDEBAR_FONT, HELP_FONT,
    COMMANDS, COMMAND_ALIASES, HELP_INTRO
)
from effects import play_sound
from modules.anomaly_remediation import AnomalyRemediationModule
from modules.diagnostic_viewer import DiagnosticViewerModule
from modules.temporal_map import TemporalMapModule
from config import SOUND_ERROR, SOUND_MODULE_SWITCH


class TARC_U_Core(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window setup
        self.title("TARC-U: Temporal Anomaly Remediation & Corruption Unit")
        if FULLSCREEN:
            self.attributes("-fullscreen", True)
            # Allow toggling fullscreen off by Escape key
            self.bind("<Escape>", self._toggle_fullscreen)
        else:
            self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
            self.resizable(False, False)
        self.configure(bg=CONSOLE_BG)

        # State variables
        self.current_module_frame = None
        self.command_history = []
        self.history_index = None
        self.modules = {}

        # Session command log entries list
        self.session_log = []

        # Build UI components
        self._create_sidebar()
        self._create_main_area()
        self._create_shell_area()
        self._create_help_overlay()

        # Initialize modules (not packed yet)
        self._initialize_modules()

        # Show the shell prompt screen initially
        self.show_shell()

        # Start periodic system message updates
        self._periodic_system_message()

        # Show help overlay initially after short delay
        self.after(100, self._show_help_overlay)

    def _toggle_fullscreen(self, event=None):
        is_full = self.attributes("-fullscreen")
        self.attributes("-fullscreen", not is_full)

    def _create_sidebar(self):
        # Left sidebar frame fixed width, no resizing
        self.sidebar_frame = tk.Frame(self, bg=CONSOLE_BG, width=SIDEBAR_WIDTH)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar_frame.pack_propagate(False)  # Fix width

        # Sidebar title label
        self.sidebar_title = tk.Label(
            self.sidebar_frame, text="TARC-U COMMANDS",
            fg=CONSOLE_FG, bg=CONSOLE_BG, font=SIDEBAR_FONT
        )
        self.sidebar_title.pack(pady=10)

        # Replace Listbox with Text widget to allow wrapping and clickable commands
        self.commands_text = tk.Text(
            self.sidebar_frame, bg=CONSOLE_BG, fg=CONSOLE_FG,
            font=SMALL_FONT, bd=0, highlightthickness=0, wrap=tk.WORD,
            height=15, cursor="arrow"
        )
        self.commands_text.pack(padx=10, pady=2, fill=tk.X)

        # Insert commands with unique tags and bind click event
        self.commands_text.config(state=tk.NORMAL)
        for i, (cmd, desc) in enumerate(COMMANDS):
            tag_name = f"cmd_{i}"
            start_index = self.commands_text.index(tk.END)
            self.commands_text.insert(tk.END, f"{cmd} - {desc}\n\n")
            end_index = self.commands_text.index(tk.END)
            self.commands_text.tag_add(tag_name, start_index, end_index)
            self.commands_text.tag_bind(tag_name, "<Button-1>", self._on_command_click)
            self.commands_text.tag_bind(tag_name, "<Enter>", lambda e, t=tag_name: self.commands_text.config(cursor="hand2"))
            self.commands_text.tag_bind(tag_name, "<Leave>", lambda e: self.commands_text.config(cursor="arrow"))
            self.commands_text.tag_config(tag_name, foreground=ACCENT_COLOR)
        self.commands_text.config(state=tk.DISABLED)

        # Session log label
        self.session_log_label = tk.Label(
            self.sidebar_frame, text="SESSION LOG",
            fg=CONSOLE_FG, bg=CONSOLE_BG, font=SIDEBAR_FONT
        )
        self.session_log_label.pack(pady=(15, 5))

        # Session log listbox inside scrollframe
        self.session_log_frame = tk.Frame(self.sidebar_frame, bg=CONSOLE_BG)
        self.session_log_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)

        self.session_log_listbox = tk.Listbox(
            self.session_log_frame, bg="#121212", fg=CONSOLE_FG,
            font=("Consolas", 11), bd=0, highlightthickness=0
        )
        self.session_log_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(self.session_log_frame, orient=tk.VERTICAL, command=self.session_log_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.session_log_listbox.config(yscrollcommand=scrollbar.set)

    def _on_command_click(self, event):
        # Get mouse click position in text widget
        mouse_index = self.commands_text.index(f"@{event.x},{event.y}")

        # Identify tags at this position
        tags = self.commands_text.tag_names(mouse_index)
        cmd_tags = [t for t in tags if t.startswith("cmd_")]
        if not cmd_tags:
            return

        tag = cmd_tags[0]
        # Get text range of tag
        ranges = self.commands_text.tag_ranges(tag)
        if not ranges or len(ranges) < 2:
            return

        text_content = self.commands_text.get(ranges[0], ranges[1]).strip()
        # Extract command part before ' - '
        command = text_content.split(" - ")[0]

        # Insert command into shell input and focus
        self.shell_input.delete(0, tk.END)
        self.shell_input.insert(0, command)
        self.shell_input.focus_set()

    def _create_main_area(self):
        # Container for top bar, system message, and active module
        self.main_frame = tk.Frame(self, bg=CONSOLE_BG)
        self.main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Top bar with title and status lights
        self.top_bar = tk.Frame(self.main_frame, bg=CONSOLE_BG)
        self.top_bar.pack(fill=tk.X, pady=5, padx=10)

        self.title_label = tk.Label(
            self.top_bar, text="TARC-U OS v1.0.0 BETA",
            font=TITLE_FONT, fg=ACCENT_COLOR, bg=CONSOLE_BG
        )
        self.title_label.pack(side=tk.LEFT)

        self.status_lights_frame = tk.Frame(self.top_bar, bg=CONSOLE_BG)
        self.status_lights_frame.pack(side=tk.RIGHT)
        self.status_lights = []
        for _ in range(3):
            canvas = tk.Canvas(self.status_lights_frame, width=20, height=20, bg=CONSOLE_BG, highlightthickness=0)
            oval = canvas.create_oval(4, 4, 16, 16, fill=ERROR_COLOR, outline=ERROR_COLOR)
            canvas.pack(side=tk.LEFT, padx=3)
            self.status_lights.append((canvas, oval))

        # System message below top bar
        self.system_message_label = tk.Label(
            self.main_frame, text="System Booting...", font=SMALL_FONT,
            fg=WARNING_COLOR, bg=CONSOLE_BG, wraplength=700, justify=tk.LEFT
        )
        self.system_message_label.pack(pady=5, padx=10, anchor="w")

        # Module container frame (where loaded modules will appear)
        self.module_container = tk.Frame(self.main_frame, bg=CONSOLE_BG)
        self.module_container.pack(expand=True, fill=tk.BOTH, padx=10, pady=(0, 10))

    def _create_shell_area(self):
        # Shell input frame at bottom of main frame
        self.shell_frame = tk.Frame(self.main_frame, bg=CONSOLE_BG, bd=2, relief=tk.RIDGE)
        self.shell_frame.pack(fill=tk.X, padx=10, pady=5)

        self.shell_prompt = tk.Label(
            self.shell_frame, text="TARC-U>", font=SHELL_FONT,
            fg=CONSOLE_FG, bg=CONSOLE_BG
        )
        self.shell_prompt.pack(side=tk.LEFT, padx=5)

        self.shell_input = tk.Entry(
            self.shell_frame, font=SHELL_FONT, fg=ACCENT_COLOR,
            bg="#121212", insertbackground=ACCENT_COLOR,
            bd=0, relief=tk.FLAT
        )
        self.shell_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=3)
        self.shell_input.focus()

        self.shell_input.bind("<Return>", self._process_shell_command)
        self.shell_input.bind("<Up>", self._shell_history_back)
        self.shell_input.bind("<Down>", self._shell_history_forward)
        self.shell_input.bind("<Key>", self._reset_history_index_on_typing)

    def _create_help_overlay(self):
        # Semi-transparent fullscreen top-level for help
        self.help_overlay = tk.Toplevel(self)
        self.help_overlay.withdraw()
        self.help_overlay.overrideredirect(True)
        self.help_overlay.attributes("-topmost", True)
        self.help_overlay.config(bg="#181830")

        # Resize to match root window/screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.help_overlay.geometry(f"{screen_width}x{screen_height}+0+0")

        # Text widget for displaying help content
        self.help_text = tk.Text(
            self.help_overlay, bg="#181830", fg="#fffbc4",
            font=HELP_FONT, wrap=tk.WORD, padx=20, pady=20,
            bd=0, relief=tk.FLAT
        )
        self.help_text.pack(expand=True, fill=tk.BOTH)

        # Insert introduction and commands list
        self.help_text.insert(tk.END, HELP_INTRO + "\n\nCOMMANDS:\n")
        for cmd, desc in COMMANDS:
            self.help_text.insert(tk.END, f"- {cmd} : {desc}\n")
        self.help_text.config(state=tk.DISABLED)

        # Bind escape and click to hide help
        self.help_overlay.bind("<Escape>", lambda e: self._hide_help_overlay())
        self.help_overlay.bind("<Button-1>", lambda e: self._hide_help_overlay())

        # Hotkey '?' toggles help anywhere
        self.bind_all("?", self._toggle_help_overlay)

    def _show_help_overlay(self):
        self.help_overlay.deiconify()
        self.help_overlay.focus_set()

    def _hide_help_overlay(self):
        self.help_overlay.withdraw()
        self.focus_set()
        self.shell_input.focus_set()

    def _toggle_help_overlay(self, event=None):
        if self.help_overlay.state() == "withdrawn":
            self._show_help_overlay()
        else:
            self._hide_help_overlay()

    def _initialize_modules(self):
        # Create but don't pack modules yet
        self.modules["anomaly_remediation"] = AnomalyRemediationModule(self, self.module_container, self)
        self.modules["diagnostic_viewer"] = DiagnosticViewerModule(self, self.module_container, self)
        self.modules["temporal_map"] = TemporalMapModule(self, self.module_container, self)

    def show_module(self, module_name):
        if module_name not in self.modules:
            self.update_system_message(f"ERROR: Module '{module_name}' not found.", is_error=True)
            play_sound(SOUND_ERROR)
            return

        if self.current_module_frame:
            self.current_module_frame.pack_forget()

        self.current_module_frame = self.modules[module_name]
        self.current_module_frame.pack(expand=True, fill=tk.BOTH)
        play_sound(SOUND_MODULE_SWITCH)
        self.update_system_message(f"Module '{module_name}' loaded.")
        self.shell_input.focus_set()
        # Ensure shell frame visible on top
        self.shell_frame.lift()

        # Auto start scenario on anomaly_remediation module
        if module_name == "anomaly_remediation":
            if hasattr(self.current_module_frame, "load_scenario"):
                self.current_module_frame.load_scenario()

    def show_shell(self):
        # Hide current module, show only shell
        if self.current_module_frame:
            self.current_module_frame.pack_forget()
            self.current_module_frame = None
        self.update_system_message("TARC-U Shell ready. Type 'help' for commands.")
        self.shell_input.focus_set()

    def _process_shell_command(self, event=None):
        input_text = self.shell_input.get().strip()
        self.shell_input.delete(0, tk.END)
        if not input_text:
            return

        # Save raw input for history and session log
        self.command_history.append(input_text)
        self.history_index = None

        command = input_text.lower()
        # Map aliases
        command = COMMAND_ALIASES.get(command, command)

        response = ""
        if command in ["exit", "shutdown"]:
            response = "Shutting down TARC-U. Goodbye."
            self.update_system_message(response)
            play_sound(SOUND_ERROR)
            self.after(1000, self.destroy)
        elif command == "help":
            self._show_help_overlay()
            response = "Help overlay shown. Press Escape or click anywhere to close."
        elif command == "clear":
            self._clear_session_log()
            response = "Session log cleared."
        elif command == "back":
            self.show_shell()
            response = "Returned to main shell."
        elif command == "reboot":
            response = "Rebooting system... Stand by."
            self.update_system_message(response)
            play_sound(SOUND_ERROR)
            self.after(1000, self._perform_reboot)
        elif command.startswith("start ") or command.startswith("view "):
            mod = None
            if command.startswith("start "):
                mod = command[6:]
            elif command.startswith("view "):
                mod = command[5:]
            if mod in self.modules:
                self.show_module(mod)
                response = f"Module '{mod}' started."
            else:
                response = f"ERROR: Module '{mod}' not found."
                self.update_system_message(response, is_error=True)
                play_sound(SOUND_ERROR)
        else:
            response = f"ERROR: Unknown command '{input_text}'. Type 'help' for list."
            self.update_system_message(response, is_error=True)
            play_sound(SOUND_ERROR)

        self._append_session_log(input_text, response)

    def _append_session_log(self, command, response):
        entry = f"> {command}\n{response}"
        self.session_log.append(entry)
        # Limit to last 200 entries
        if len(self.session_log) > 200:
            self.session_log.pop(0)

        self.session_log_listbox.delete(0, tk.END)
        for line in self.session_log[-100:]:
            self.session_log_listbox.insert(tk.END, line)
        self.session_log_listbox.see(tk.END)

    def _clear_session_log(self):
        self.session_log.clear()
        self.session_log_listbox.delete(0, tk.END)

    def _shell_history_back(self, event=None):
        if not self.command_history:
            return "break"
        if self.history_index is None:
            self.history_index = len(self.command_history) - 1
        elif self.history_index > 0:
            self.history_index -= 1
        self.shell_input.delete(0, tk.END)
        self.shell_input.insert(0, self.command_history[self.history_index])
        return "break"

    def _shell_history_forward(self, event=None):
        if self.history_index is None:
            return "break"
        if self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            self.shell_input.delete(0, tk.END)
            self.shell_input.insert(0, self.command_history[self.history_index])
        else:
            self.history_index = None
            self.shell_input.delete(0, tk.END)
        return "break"

    def _reset_history_index_on_typing(self, event):
        # Only reset if event is present and keysym is not Up or Down
        if event and event.keysym not in ("Up", "Down"):
            self.history_index = None

    def update_system_message(self, message, is_error=False):
        color = ERROR_COLOR if is_error else WARNING_COLOR
        self.system_message_label.config(text=message, fg=color)

    def update_status_lights(self, status):
        color_map = {
            "initializing": [ERROR_COLOR, ERROR_COLOR, ERROR_COLOR],
            "active": [WARNING_COLOR, ERROR_COLOR, ERROR_COLOR],
            "processing": [WARNING_COLOR, WARNING_COLOR, ERROR_COLOR],
            "ready": [CONSOLE_FG, CONSOLE_FG, CONSOLE_FG],
            "error": [ERROR_COLOR, ERROR_COLOR, ERROR_COLOR],
        }
        colors = color_map.get(status, [ERROR_COLOR, ERROR_COLOR, ERROR_COLOR])
        for idx, (canvas, oval) in enumerate(self.status_lights):
            canvas.itemconfig(oval, fill=colors[idx], outline=colors[idx])

    def _periodic_system_message(self):
        # Update system message periodically unless diagnostic_viewer module active (which handles own)
        if self.current_module_frame != self.modules.get("diagnostic_viewer"):
            messages = [
                "Temporal Flux: Unstable", "Reality Coherence: 17%",
                "Warning: Paradox Imminent!", "Chroniton Levels: Fluctuating",
                "Dimensional Integrity: Compromised", "Processing Quantum Entanglement...",
                "Engaging Subspace Anomaly Dampeners...", "ERROR 404: History Not Found.",
                "Reconfiguring Chrono-Synclastic Infundibulum...", "Brain Rot Index: Critical.",
                "Event Horizon: Approaching...", "Causality Loop Detected.",
                "Historical Data Integrity: Poor.", "Time-Space Continuum: Wobbly.",
                "System operating at peak brain rot efficiency."
            ]
            self.update_system_message(random.choice(messages))
        self.after(3500, self._periodic_system_message)

    def _perform_reboot(self):
        self.update_system_message("Rebooting...")
        self.update_status_lights("initializing")
        if self.current_module_frame:
            self.current_module_frame.pack_forget()
            self.current_module_frame = None

        # Delay a moment then restart the python script
        def restart():
            python = sys.executable
            os.execl(python, python, *sys.argv)

        self.after(1000, restart)