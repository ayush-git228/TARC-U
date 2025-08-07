import tkinter as tk
from tkinter import ttk
import random
import time

from config import (
    CONSOLE_BG, CONSOLE_FG, WARNING_COLOR, ERROR_COLOR, ACCENT_COLOR, SHELL_FONT, SMALL_FONT, 
    BUTTON_COLOR, ACTIVE_BUTTON_COLOR
)

class DiagnosticViewerModule(tk.Frame):
    """
    Enhanced diagnostic log viewer for TARC-U system.
    Features:
    - Continuously scrolling log messages (simulated)
    - Pause/Play control
    - Filter by severity: INFO, WARN, ERROR, CRIT, DEBUG
    - Simple search input to filter displayed logs
    - Clear log button
    """
    def __init__(self, master_root, parent_frame, tarc_u_core_instance):
        super().__init__(parent_frame, bg=CONSOLE_BG)
        self.master_root = master_root
        self.tarc_u_core = tarc_u_core_instance

        self.paused = False
        self.severity_filter = tk.StringVar(value="ALL")
        self.search_query = tk.StringVar()

        # Store all log messages (tuples: (timestamp, severity, text))
        self.all_logs = []

        self._create_widgets()

        self._simulate_log_messages()
    
    def _create_widgets(self):
        # Controls frame: filter + search + pause/clear buttons
        controls_frame = tk.Frame(self, bg=CONSOLE_BG)
        controls_frame.pack(fill=tk.X, padx=10, pady=(5,2))

        # Severity filter
        tk.Label(controls_frame, text="Filter severity:", fg=CONSOLE_FG, bg=CONSOLE_BG, font=SMALL_FONT).pack(side=tk.LEFT, padx=(0,5))
        severity_options = ["ALL", "INFO", "WARN", "WARNING", "ERROR", "CRIT", "DEBUG"]
        self.severity_combobox = ttk.Combobox(controls_frame, values=severity_options,
                                              textvariable=self.severity_filter, width=8, state='readonly', font=SMALL_FONT)
        self.severity_combobox.pack(side=tk.LEFT)
        self.severity_combobox.bind("<<ComboboxSelected>>", lambda e: self._refresh_displayed_logs())

        # Search box
        tk.Label(controls_frame, text="Search:", fg=CONSOLE_FG, bg=CONSOLE_BG, font=SMALL_FONT).pack(side=tk.LEFT, padx=(15,5))
        self.search_entry = tk.Entry(controls_frame, textvariable=self.search_query, width=20, font=SMALL_FONT)
        self.search_entry.pack(side=tk.LEFT, padx=(0,5))
        self.search_entry.bind("<KeyRelease>", lambda e: self._refresh_displayed_logs())

        # Pause/Play button
        self.pause_button = tk.Button(controls_frame, text="Pause", command=self._toggle_pause,
                                      font=SMALL_FONT, bg=BUTTON_COLOR, fg=CONSOLE_FG, activebackground=ACTIVE_BUTTON_COLOR)
        self.pause_button.pack(side=tk.LEFT, padx=10)

        # Clear log button
        clear_button = tk.Button(controls_frame, text="Clear Logs", command=self._clear_logs,
                                 font=SMALL_FONT, bg=BUTTON_COLOR, fg=CONSOLE_FG, activebackground=ACTIVE_BUTTON_COLOR)
        clear_button.pack(side=tk.LEFT)

        # Log display: ScrolledText-like with a scrollbar
        text_frame = tk.Frame(self, bg=CONSOLE_BG)
        text_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=(0,10))

        self.log_text = tk.Text(text_frame, bg="#121212", fg=CONSOLE_FG, font=("Consolas", 12),
                                state='disabled', wrap='word', insertbackground=ACCENT_COLOR)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)

    def _toggle_pause(self):
        self.paused = not self.paused
        self.pause_button.config(text="Resume" if self.paused else "Pause")
        if not self.paused:
            self._refresh_displayed_logs()

    def _clear_logs(self):
        self.all_logs.clear()
        self._refresh_displayed_logs()

    def _simulate_log_messages(self):
        if not self.paused:
            # Simulate a new log entry
            message, severity = self._random_log_entry()
            timestamp = time.strftime("%H:%M:%S")
            self.all_logs.append((timestamp, severity, message))
            # Limit max logs to prevent memory bloat
            if len(self.all_logs) > 1000:
                self.all_logs.pop(0)
            self._append_log_to_display(timestamp, severity, message)

        # Schedule next log message between 1 and 3 seconds
        self.master_root.after(random.randint(1000, 3000), self._simulate_log_messages)

    def _random_log_entry(self):
        # Randomly pick a severity weighted roughly
        severities = ["INFO"]*20 + ["WARN"]*8 + ["ERROR"]*5 + ["CRIT"]*2 + ["DEBUG"]*10
        severity = random.choice(severities)
        messages = {
            "INFO": [
                "Temporal Flux Capacitor operating nominally.",
                "Chroniton particle emission stable.",
                "Subspace anomaly dampeners engaged.",
                "System diagnostics complete. All green.",
                "Initiating timeline defragmentation protocol."
            ],
            "WARN": [
                "Reality coherence index dropped slightly.",
                "Historical anomaly detected: minor timeline divergence.",
                "Corrupted data stream in sector 7G being repaired.",
                "Temporary paradox detected; localized reality shift.",
                "Brain rot index rising in localized region."
            ],
            "ERROR": [
                "Paradox imminent: conflicting temporal events detected.",
                "Data stream corruption critical in historic records.",
                "Core temperature rising due to excessive timeline stress.",
                "Module malfunction: Temporal displacement field unstable.",
                "System integrity compromised: Initiating fallback protocols."
            ],
            "CRIT": [
                "Reality fracture detected: Awaiting emergency re-assembly.",
                "Causality violation critical: Multiple realities intersecting.",
                "Temporal shield failure imminent: Prepare for lockdown.",
                "Timeline divergence escalating: Evacuate non-essential personnel."
            ],
            "DEBUG": [
                "User input received: 'Initiate chaos sequence.'",
                "Simulating alternate reality stress tests.",
                "Recalibrating chrono-synclastic infundibulum.",
                "Logging memory buffer state: nominal.",
                "Patch check complete: No conflicts found."
            ]
        }
        msg = random.choice(messages.get(severity, ["Unknown event logged."]))
        return msg, severity

    def _append_log_to_display(self, timestamp, severity, message):
        # Append log message if it passes current filter and search
        if not self._passes_filter(severity, message):
            return
        self.log_text.config(state='normal')

        color = {
            "INFO": CONSOLE_FG,
            "WARN": WARNING_COLOR,
            "WARNING": WARNING_COLOR,
            "ERROR": ERROR_COLOR,
            "CRIT": ERROR_COLOR,
            "DEBUG": ACCENT_COLOR
        }.get(severity, CONSOLE_FG)

        self.log_text.insert(tk.END, f"[{timestamp}] [{severity}] {message}\n", severity)
        self.log_text.tag_configure(severity, foreground=color)
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')

    def _passes_filter(self, severity, message):
        # Check severity filter
        filt = self.severity_filter.get().upper()
        if filt != "ALL" and severity.upper() != filt:
            return False
        # Check search query
        q = self.search_query.get().lower()
        if q and q not in message.lower() and q not in severity.lower():
            return False
        return True

    def _refresh_displayed_logs(self):
        # Refresh complete display based on filter and search
        self.log_text.config(state='normal')
        self.log_text.delete('1.0', tk.END)

        for (timestamp, severity, message) in self.all_logs:
            if self._passes_filter(severity, message):
                color = {
                    "INFO": CONSOLE_FG,
                    "WARN": WARNING_COLOR,
                    "WARNING": WARNING_COLOR,
                    "ERROR": ERROR_COLOR,
                    "CRIT": ERROR_COLOR,
                    "DEBUG": ACCENT_COLOR
                }.get(severity, CONSOLE_FG)
                self.log_text.insert(tk.END, f"[{timestamp}] [{severity}] {message}\n", severity)
                self.log_text.tag_configure(severity, foreground=color)

        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')