import random
import time
import os
import sys
import threading

from config import CONSOLE_FG, ACCENT_COLOR, WARNING_COLOR, ERROR_COLOR

# Sound Setup using pygame
try:
    import pygame
    pygame.mixer.init()
    SOUND_ENABLED = True
except ImportError:
    print("Warning: 'pygame' library not found. Sound effects will be disabled.")
    print("To enable sound, install it: pip install pygame")
    SOUND_ENABLED = False
    pygame = None  # <- Fixes 'possibly unbound' warning


def glitch_text(master_root, canvas, item_id, color_change=False, count=0, max_glitches=5, delay=50):
    if count < max_glitches:
        original_color = canvas.itemcget(item_id, 'fill')
        original_coords = canvas.coords(item_id)

        canvas.coords(item_id, original_coords[0] + random.randint(-2, 2),
                      original_coords[1] + random.randint(-2, 2))

        if color_change:
            canvas.itemconfig(item_id, fill=random.choice([WARNING_COLOR, ERROR_COLOR, ACCENT_COLOR]))
        else:
            canvas.itemconfig(item_id, fill=random.choice([CONSOLE_FG, ACCENT_COLOR]))

        master_root.after(delay, glitch_text, master_root, canvas, item_id, color_change, count + 1, max_glitches, delay)
    else:
        canvas.itemconfig(item_id, fill=CONSOLE_FG if not color_change else ACCENT_COLOR)


def _play_sound_thread(full_path):
    if pygame:
        try:
            sound = pygame.mixer.Sound(full_path)
            sound.play()
        except Exception as e:
            print(f"Error playing sound '{full_path}': {e}")


def play_sound(sound_file_path):
    # Plays a sound file using pygame in a non-blocking thread.

    if SOUND_ENABLED and pygame:
        base_path = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(os.path.dirname(base_path), sound_file_path)

        if os.path.exists(full_path):
            threading.Thread(target=_play_sound_thread, args=(full_path,), daemon=True).start()
        else:
            print(f"Sound file not found: {full_path}")
