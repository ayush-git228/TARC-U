import tkinter as tk
import random

from config import (
    CONSOLE_BG, ACCENT_COLOR, WARNING_COLOR, ERROR_COLOR, CONSOLE_FG, SMALL_FONT, SIDEBAR_WIDTH, WINDOW_WIDTH, WINDOW_HEIGHT
)

class TemporalMapModule(tk.Frame):
    """
    Dynamic, glitching temporal map visualization for TARC-U.
    Nodes move smoothly with flickering color effects.
    Hovering over nodes reveals tooltip with timeline ID.
    Includes back button to return to shell.
    """

    NODE_RADIUS = 7
    NUM_NODES = 30
    LINE_FLICKER_CHANCE = 0.1
    NODE_FLICKER_CHANCE = 0.05
    ANIMATION_DELAY = 50  # ms

    def __init__(self, master_root, parent_frame, tarc_u_core_instance):
        super().__init__(parent_frame, bg=CONSOLE_BG)
        self.master_root = master_root
        self.tarc_u_core = tarc_u_core_instance

        # Canvas sized to fill available space minus sidebar
        self.canvas_width = WINDOW_WIDTH - SIDEBAR_WIDTH - 40
        self.canvas_height = WINDOW_HEIGHT - 150

        self.map_canvas = tk.Canvas(self, width=self.canvas_width,
                                    height=self.canvas_height,
                                    bg=CONSOLE_BG, highlightthickness=0)
        self.map_canvas.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

        self.nodes = []
        self.lines = []
        self.tooltip = None

        self._create_map_elements()

        # Back button to return to shell
        self.back_button = tk.Button(self, text="Back to Shell",
                                     bg="#333333", fg=CONSOLE_FG,
                                     font=SMALL_FONT, command=self._go_back)
        self.back_button.pack(pady=(5,10))

        self.map_canvas.bind("<Motion>", self._on_mouse_move)
        self.map_canvas.bind("<Leave>", self._hide_tooltip)

        self._animate_map()

    def _create_map_elements(self):
        self.nodes.clear()
        self.lines.clear()
        self.map_canvas.delete("all")

        w = self.canvas_width
        h = self.canvas_height

        for _ in range(self.NUM_NODES):
            x = random.randint(self.NODE_RADIUS + 10, w - self.NODE_RADIUS - 10)
            y = random.randint(self.NODE_RADIUS + 10, h - self.NODE_RADIUS - 10)
            color = random.choice([ACCENT_COLOR, WARNING_COLOR, CONSOLE_FG])

            node_id = self.map_canvas.create_oval(
                x - self.NODE_RADIUS, y - self.NODE_RADIUS,
                x + self.NODE_RADIUS, y + self.NODE_RADIUS,
                fill=color, outline=color
            )
            timeline_label = f"T-{random.randint(100, 999)}"
            text_id = self.map_canvas.create_text(
                x, y - 15, text=timeline_label, fill=color, font=SMALL_FONT
            )
            dx = random.uniform(-0.5, 0.5)
            dy = random.uniform(-0.5, 0.5)
            self.nodes.append({
                'x': x, 'y': y, 'color': color, 'node_id': node_id,
                'text_id': text_id, 'dx': dx, 'dy': dy, 'label': timeline_label
            })

        # Create connections (avoid self connections)
        for _ in range(self.NUM_NODES * 2):
            n1_idx = random.randint(0, self.NUM_NODES - 1)
            n2_idx = random.randint(0, self.NUM_NODES - 1)
            if n1_idx != n2_idx:
                line_id = self.map_canvas.create_line(
                    self.nodes[n1_idx]['x'], self.nodes[n1_idx]['y'],
                    self.nodes[n2_idx]['x'], self.nodes[n2_idx]['y'],
                    fill=ACCENT_COLOR, width=1, dash=(2, 2)
                )
                self.lines.append({'line_id': line_id, 'n1': n1_idx, 'n2': n2_idx})

    def _animate_map(self):
        w = self.canvas_width
        h = self.canvas_height

        for node in self.nodes:
            # Move node
            node['x'] += node['dx']
            node['y'] += node['dy']

            # Bounce edges
            if node['x'] < self.NODE_RADIUS or node['x'] > w - self.NODE_RADIUS:
                node['dx'] *= -1
            if node['y'] < self.NODE_RADIUS or node['y'] > h - self.NODE_RADIUS:
                node['dy'] *= -1

            # Update node & label position
            self.map_canvas.coords(
                node['node_id'],
                node['x'] - self.NODE_RADIUS, node['y'] - self.NODE_RADIUS,
                node['x'] + self.NODE_RADIUS, node['y'] + self.NODE_RADIUS
            )
            self.map_canvas.coords(node['text_id'], node['x'], node['y'] - 15)

            # Flicker node colors randomly
            if random.random() < self.NODE_FLICKER_CHANCE:
                flicker_color = random.choice([node['color'], WARNING_COLOR, ERROR_COLOR])
                self.map_canvas.itemconfig(node['node_id'], fill=flicker_color, outline=flicker_color)
                self.map_canvas.itemconfig(node['text_id'], fill=flicker_color)
            else:
                self.map_canvas.itemconfig(node['node_id'], fill=node['color'], outline=node['color'])
                self.map_canvas.itemconfig(node['text_id'], fill=node['color'])

        # Update lines
        for line in self.lines:
            n1 = self.nodes[line['n1']]
            n2 = self.nodes[line['n2']]
            self.map_canvas.coords(line['line_id'], n1['x'], n1['y'], n2['x'], n2['y'])

            if random.random() < self.LINE_FLICKER_CHANCE:
                flicker_color = random.choice([ACCENT_COLOR, WARNING_COLOR, ERROR_COLOR])
                self.map_canvas.itemconfig(line['line_id'], fill=flicker_color)
            else:
                self.map_canvas.itemconfig(line['line_id'], fill=ACCENT_COLOR)

        self.after(self.ANIMATION_DELAY, self._animate_map)

    def _on_mouse_move(self, event):
        # Show tooltip if hovering over a node
        x, y = event.x, event.y
        # Check proximity for each node
        for node in self.nodes:
            dx = x - node['x']
            dy = y - node['y']
            dist_sq = dx * dx + dy * dy
            if dist_sq <= (self.NODE_RADIUS + 5) ** 2:
                self._show_tooltip(node['label'], x, y)
                return
        self._hide_tooltip()

    def _show_tooltip(self, text, x, y):
        if self.tooltip is None:
            self.tooltip = self.map_canvas.create_text(x + 10, y + 10, text=text,
                                                       fill=ACCENT_COLOR,
                                                       font=SMALL_FONT,
                                                       anchor="nw",
                                                       tags="tooltip")
        else:
            self.map_canvas.coords(self.tooltip, x + 10, y + 10)
            self.map_canvas.itemconfig(self.tooltip, text=text)
        # Raise tooltip to front
        self.map_canvas.tag_raise("tooltip")

    def _hide_tooltip(self, event=None):
        if self.tooltip is not None:
            self.map_canvas.delete(self.tooltip)
            self.tooltip = None

    def _go_back(self):
        self.tarc_u_core.show_shell()
