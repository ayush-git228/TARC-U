import tkinter as tk
import random

from tarc_u_core import TARC_U_Core
from effects import play_sound
from config import CONSOLE_BG, CONSOLE_FG, ACCENT_COLOR, WARNING_COLOR, SHELL_FONT, TITLE_FONT, SOUND_BOOT

def run_boot_sequence(root, boot_canvas, boot_text_id):
    # Simulates a system boot-up sequence on a Tkinter canvas.
    
    play_sound(SOUND_BOOT)

    boot_messages = [
        "Initializing Temporal Anomaly Remediation & Corruption Unit (TARC-U)...",
        "Checking temporal conduits...",
        "Establishing causality protocols...",
        "Loading historical anomaly database...",
        "Verifying reality coherence checksums...",
        "Engaging Chroniton Particle Generators...",
        "Calibrating temporal displacement fields...",
        "WARNING: Brain Rot Index at critical levels. Proceed with caution.",
        "System ready. Awaiting operator commands."
    ]

    def update_boot_text(index=0):
        if index < len(boot_messages):
            # Update text progressively
            current_text = "\n".join(boot_messages[:index+1])
            boot_canvas.itemconfig(boot_text_id, text=current_text)
            boot_canvas.update_idletasks()
            root.after(random.randint(400, 800), update_boot_text, index + 1)
        else:
            # Start fade out after messages done
            fade_out_boot_screen(root, 1.0)

    def fade_out_boot_screen(window, alpha):
        alpha -= 0.05
        if alpha <= 0:
            # After fade-out completes, destroy boot window and start main app
            window.destroy()
            launch_main_app()
            return
        window.wm_attributes("-alpha", alpha)
        window.after(50, fade_out_boot_screen, window, alpha)

    # Setup the boot canvas display
    boot_canvas.config(bg=CONSOLE_BG)
    boot_canvas.delete("all")

    w = boot_canvas.winfo_width()
    # Title texts at top center
    boot_canvas.create_text(w / 2, 50, text="TARC-U", font=TITLE_FONT, fill=ACCENT_COLOR, justify=tk.CENTER)
    boot_canvas.create_text(w / 2, 100, text="Temporal Anomaly Remediation & Corruption Unit", font=SHELL_FONT, fill=WARNING_COLOR, justify=tk.CENTER)
    boot_canvas.create_text(w / 2, 150, text="v3.1.4 BETA", font=SHELL_FONT, fill=CONSOLE_FG, justify=tk.CENTER)

    # Text box for boot messages starting empty, left-aligned below titles
    boot_text_id = boot_canvas.create_text(
        50, 200, anchor="nw", text="", font=SHELL_FONT, fill=CONSOLE_FG, width=w - 100
    )
    update_boot_text()


def launch_main_app():
    # Create and start the main TARC-U application in fullscreen.
    
    app = TARC_U_Core()
    app.attributes("-fullscreen", True)
   
    app.bind("<Escape>", lambda e: app.attributes("-fullscreen", False))
    app.mainloop()


def main():
    # Boot window setup
    boot_root = tk.Tk()
    boot_root.overrideredirect(True)  # No decorations
    width, height = 800, 600
    screen_width = boot_root.winfo_screenwidth()
    screen_height = boot_root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    boot_root.geometry(f"{width}x{height}+{x}+{y}")
    boot_root.config(bg=CONSOLE_BG)
    boot_root.attributes("-topmost", True)
    boot_root.wm_attributes("-alpha", 1.0)  # Fully opaque

    boot_canvas = tk.Canvas(boot_root, width=width, height=height,
                           bg=CONSOLE_BG, highlightthickness=0)
    boot_canvas.pack(expand=True, fill='both')

    # Wait for the canvas to be ready before creating text item
    boot_root.update_idletasks()

    # Create the text item to be updated by run_boot_sequence
    boot_text_id = boot_canvas.create_text(
        50, 200, anchor="nw", text="", font=SHELL_FONT,
        fill=CONSOLE_FG, width=width - 100
    )

    # Pass the created text id to update text progressively in boot sequence
    run_boot_sequence(boot_root, boot_canvas, boot_text_id)

    boot_root.mainloop()


if __name__ == "__main__":
    main()