import tkinter as tk
import random
import math
import time

from config import (
    WINDOW_WIDTH, CONSOLE_BG, DISPLAY_BG, CONSOLE_FG, ACCENT_COLOR,
    WARNING_COLOR, ERROR_COLOR, BUTTON_COLOR, ACTIVE_BUTTON_COLOR,
    MAIN_FONT, SMALL_FONT, SOUND_WHIRR, SOUND_GLITCH, SOUND_BEEP, SOUND_ERROR
)
from data.curated_scenarios import CURATED_BRAIN_ROT_SCENARIOS
from data.historical_elements import (
    HISTORICAL_FIGURES, ABSURD_ACTIONS, RANDOM_OBJECTS, HISTORICAL_ERAS_EVENTS,
    PROCEDURAL_RESPONSES, NEW_INVENTIONS, RANDOM_CONCEPTS, RANDOM_DISCOVERIES
)
from effects import glitch_text, play_sound


class AnomalyRemediationModule(tk.Frame):
    """
    Main game module for TARC-U, handling historical brain rot anomaly scenarios.
    Supports curated and procedural scenario generation.
    """
    def __init__(self, master_root, parent_frame, tarc_u_core_instance):
        super().__init__(parent_frame, bg=CONSOLE_BG)
        self.master_root = master_root
        self.tarc_u_core = tarc_u_core_instance

        self.current_scenario_data = None
        self.choice_buttons = []
        self.buttons_enabled = False
        self.current_scenario_text_id = None
        self.current_response_text_id = None

        self._create_widgets()
        self.load_scenario()

    def _create_widgets(self):
        # Display canvas for prompts and responses
        self.display_canvas = tk.Canvas(
            self, width=WINDOW_WIDTH - 100, height=320,
            bg=DISPLAY_BG, highlightbackground=ACCENT_COLOR, highlightthickness=2
        )
        self.display_canvas.pack(pady=10)

        self.display_canvas.create_text(
            (WINDOW_WIDTH - 100) // 2, 160,
            text="Awaiting Anomaly...",
            fill=CONSOLE_FG, font=MAIN_FONT, justify=tk.CENTER, width=(WINDOW_WIDTH - 120)
        )

        # Control panel frame below display
        control_frame = tk.Frame(self, bg=CONSOLE_BG)
        control_frame.pack(pady=10, fill=tk.X)

        # Chrono-Flux Dial Canvas
        self.dial_canvas = tk.Canvas(
            control_frame, width=120, height=120,
            bg=CONSOLE_BG, highlightbackground=ACCENT_COLOR, highlightthickness=1
        )
        self.dial_canvas.grid(row=0, column=0, padx=20, pady=5, sticky="n")
        self.dial_canvas.create_oval(10, 10, 110, 110, outline=ACCENT_COLOR, width=2)
        self.dial_needle = self.dial_canvas.create_line(
            60, 60, 60, 20, fill=ERROR_COLOR, width=3, arrow=tk.LAST
        )
        self.dial_canvas.create_text(60, 60, text="FLUX", fill=ACCENT_COLOR, font=SMALL_FONT)
        self.dial_canvas.bind("<Button-1>", self._spin_dial_and_load_scenario)
        dial_label = tk.Label(
            control_frame, text="Chrono-Flux Dial\n(Click to Distort)",
            font=SMALL_FONT, fg=CONSOLE_FG, bg=CONSOLE_BG, justify=tk.CENTER
        )
        dial_label.grid(row=1, column=0, padx=20, pady=5)

        # Buttons for choices A, B, C
        buttons_frame = tk.Frame(control_frame, bg=CONSOLE_BG)
        buttons_frame.grid(row=0, column=1, rowspan=2, padx=20)

        button_texts = [
            '[A] Initiate Temporal Shift',
            '[B] Engage Reality Override',
            '[C] Activate Paradox Protocol'
        ]

        for idx, text in enumerate(button_texts):
            btn = tk.Button(
                buttons_frame, text=text, font=MAIN_FONT,
                fg=CONSOLE_FG, bg=BUTTON_COLOR, activebackground=ACTIVE_BUTTON_COLOR,
                activeforeground=ACCENT_COLOR, relief=tk.RAISED, bd=3,
                command=lambda choice=chr(65 + idx): self.process_choice(choice)
            )
            btn.pack(pady=6, fill=tk.X)
            self.choice_buttons.append(btn)

        self._set_buttons_state(False)

    def _set_buttons_state(self, enabled: bool):
        self.buttons_enabled = enabled
        for btn in self.choice_buttons:
            btn.config(state=tk.NORMAL if enabled else tk.DISABLED,
                       bg=BUTTON_COLOR if enabled else "#222222")

    def _spin_dial_and_load_scenario(self, event=None):
        if self.buttons_enabled:
            return  # Ignore if buttons are active, means already loaded/scenario running

        play_sound(SOUND_WHIRR)
        for _ in range(5):
            angle = random.randint(0, 360)
            x_end = 60 + 40 * math.cos(math.radians(angle))
            y_end = 60 - 40 * math.sin(math.radians(angle))
            self.dial_canvas.coords(self.dial_needle, 60, 60, x_end, y_end)
            self.master_root.update_idletasks()
            time.sleep(0.05)

        self.load_scenario()

    def _generate_procedural_anomaly(self):
        figure = random.choice(HISTORICAL_FIGURES)
        action = random.choice(ABSURD_ACTIONS)
        obj = random.choice(RANDOM_OBJECTS)
        event = random.choice(HISTORICAL_ERAS_EVENTS)

        prompt_template = (
            "You find {figure} {action} with {object} during {event}. What do you do?\n\n"
            "[A] Initiate Temporal Shift\n"
            "[B] Engage Reality Override\n"
            "[C] Activate Paradox Protocol"
        )
        prompt = prompt_template.format(figure=figure, action=action, object=obj, event=event)

        responses = []
        for _ in range(3):
            response_template = random.choice(PROCEDURAL_RESPONSES)
            new_invention = random.choice(NEW_INVENTIONS)
            random_concept = random.choice(RANDOM_CONCEPTS)
            random_discovery = random.choice(RANDOM_DISCOVERIES)

            response = response_template.format(
                figure=figure,
                action=action,
                object=obj,
                event=event,
                new_invention=new_invention,
                random_concept=random_concept,
                random_discovery=random_discovery
            )
            responses.append(response)

        return (prompt, responses)

    def load_scenario(self):
        self.display_canvas.delete("all")
        self.tarc_u_core.update_status_lights("active")
        self._set_buttons_state(True)

        # 30% chance to show curated scenario if available, else procedural
        if CURATED_BRAIN_ROT_SCENARIOS and random.random() < 0.3:
            self.current_scenario_data = random.choice(CURATED_BRAIN_ROT_SCENARIOS)
        else:
            self.current_scenario_data = self._generate_procedural_anomaly()

        prompt_text, _ = self.current_scenario_data
        self.current_scenario_text_id = self.display_canvas.create_text(
            (WINDOW_WIDTH - 100) // 2, 160,
            text=prompt_text, fill=CONSOLE_FG,
            font=MAIN_FONT, justify=tk.CENTER, width=(WINDOW_WIDTH - 120)
        )
        glitch_text(self.master_root, self.display_canvas, self.current_scenario_text_id)
        self.tarc_u_core.update_system_message("Temporal Anomaly Detected!")

    def process_choice(self, choice_letter):
        if not self.buttons_enabled:
            return

        play_sound(SOUND_BEEP)
        self._set_buttons_state(False)
        self.tarc_u_core.update_status_lights("processing")
        self.tarc_u_core.update_system_message(f"Processing choice: {choice_letter}...")

        if self.current_scenario_data:
            _, responses = self.current_scenario_data
            idx = {'A': 0, 'B': 1, 'C': 2}.get(choice_letter.upper(), 0)
            response_text = responses[idx]

            self.display_canvas.delete("all")
            self.current_response_text_id = self.display_canvas.create_text(
                (WINDOW_WIDTH - 100) // 2, 160,
                text=f"--- Reality Warps ---\n\n{response_text}\n\n--- End of Distortion ---",
                fill=ACCENT_COLOR, font=MAIN_FONT, justify=tk.CENTER, width=(WINDOW_WIDTH - 120)
            )
            glitch_text(self.master_root, self.display_canvas, self.current_response_text_id, color_change=True)
            play_sound(SOUND_GLITCH)

            self.tarc_u_core.update_status_lights("ready")
            self.tarc_u_core.update_system_message("Anomaly resolved. Click dial for next.")
        else:
            self.display_canvas.delete("all")
            self.display_canvas.create_text(
                (WINDOW_WIDTH - 100) // 2, 160,
                text="ERROR: No active anomaly data.",
                fill=ERROR_COLOR, font=MAIN_FONT, justify=tk.CENTER, width=(WINDOW_WIDTH - 120)
            )
            play_sound(SOUND_ERROR)
            self.tarc_u_core.update_status_lights("error")
            self.tarc_u_core.update_system_message("CRITICAL ERROR: Data integrity compromised.")
