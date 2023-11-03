import tkinter as tk
from tkinter import ttk

def create_label_entry(parent, label_text, entry_var, is_password=False):
    frame = ttk.Frame(parent)
    label = ttk.Label(frame, text=label_text)
    label.pack(side=tk.LEFT, padx=5, pady=5)
    entry = ttk.Entry(frame, textvariable=entry_var)
    if is_password:
        entry.config(show="*")
    entry.pack(side=tk.RIGHT, padx=5, pady=5)
    frame.pack(fill=tk.X, pady=5)
    return entry
