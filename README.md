# TARC-U: Temporal Anomaly Remediation & Corruption Unit

TARC-U is a Python Tkinter application that simulates a procedural, "brain rot" time anomaly remediation game/UI.  
The app features a command shell, multiple interactive modules, and a persistent sidebar with commands and session logs. It blends themes with procedural scenario generation for engaging gameplay.

---

<img width="1920" height="1080" alt="ss-upload-1" src="https://github.com/user-attachments/assets/9d0f9b49-92f9-4486-8362-f082911d1709" />

---

<img width="1920" height="1080" alt="ss-upload-2" src="https://github.com/user-attachments/assets/0ed3223c-da32-4148-bca8-69df28412132" />

---

## Features

- Fullscreen responsive UI with sidebar command list and session logs
- Interactive command shell with command history and aliases
- Multiple modules including:
  - Anomaly Remediation (procedurally generated and curated historical scenario interactions)
  - Diagnostic Viewer (live log view with filters and pause/resume)
  - Temporal Map (dynamic animated timeline visualization)
- Toggleable help overlay with command reference and introductory text
- Immersive system status display and color-coded status lights
- Sound effects integrated for UI actions and feedback
- Smooth transitions between modules and shell prompt

---

## Why Use TARC-U?

Perfect "brain rot" entertainment app. Provides quick sessions with amusing historical and anomaly-themed scenarios, replayability, and a unique retro-futuristic terminal aesthetic.

---

## Installation

1. Clone the repository.

2. Create a Python 3 virtual environment and activate it:
   
    python3 -m venv venv
    source venv/bin/activate # macOS/Linux
    venv\Scripts\activate # Windows

3. Install dependencies:

    pip install -r requirements.txt

4. Run the app:

    python main.py

    Click on screen that appears

---

## Dependencies

- Python 3.8 or later
- `tkinter` (usually included in Python installations)
- `pygame` for sound playback

---

## Notes

- Sound files should be placed in the `sounds/` folder as per the paths defined in `config.py`.
- The app relies mainly on Tkinter for GUI and Pygame for sound.
- The project aims to be modular and easily extensible.

---
