import keyboard
import tkinter as tk
from tkinter import ttk

# Key mapping templates
TEMPLATES = {
    "FNF": {'1': 'left', '2': 'down', '3': 'up', '4': 'right'},
    "osu!mania 4k": {'1': 'd', '2': 'f', '3': 'j', '4': 'k'}
}

class RemapperApp:
    def __init__(self, root):
        self.root = root
        self.active = False
        self.current_mappings = TEMPLATES["FNF"].copy()
        
        # Setup GUI
        self.setup_gui()
        self.setup_keyboard()
        
    def setup_gui(self):
        self.root.title("Mania Key Remapper")
        
        # Template selection
        self.template_var = tk.StringVar()
        ttk.Label(self.root, text="Template:").grid(row=0, column=0, padx=5, pady=5)
        self.template_dropdown = ttk.Combobox(self.root, textvariable=self.template_var,
                                            values=["FNF", "osu!mania 4k", "Custom"])
        self.template_dropdown.grid(row=0, column=1, columnspan=3, padx=5, pady=5)
        self.template_dropdown.bind("<<ComboboxSelected>>", self.on_template_select)
        self.template_dropdown.current(0)
        
        # Key entry fields
        self.entry_vars = [tk.StringVar() for _ in range(4)]
        for i in range(4):
            ttk.Label(self.root, text=f"Key {i+1}:").grid(row=i+1, column=0, padx=5, pady=5)
            entry = ttk.Entry(self.root, textvariable=self.entry_vars[i], width=10)
            entry.grid(row=i+1, column=1, padx=5, pady=5)
            self.entry_vars[i].trace_add("write", self.on_entry_change)
            self.entry_vars[i].set(self.current_mappings[str(i+1)])
        
        # Toggle button
        self.toggle_button = tk.Button(self.root, text="Start", command=self.toggle_active,
                                     bg="red", width=15)
        self.toggle_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
        
        # Status label
        self.status_label = ttk.Label(self.root, text="Status: Inactive")
        self.status_label.grid(row=5, column=2, columnspan=2, padx=5, pady=5)
        
    def setup_keyboard(self):
        # Register key handlers
        for num in ['1', '2', '3', '4']:
            keyboard.on_press_key(num, lambda e, n=num: self.handle_key(e, n), suppress=False)
        
        # Register toggle hotkey
        keyboard.add_hotkey('ctrl+shift+t', lambda: self.root.after(0, self.toggle_active))
    
    def handle_key(self, event, num):
        if self.active:
            target = self.current_mappings.get(num)
            if target:
                keyboard.send(target)
                return False  # Suppress original key
        return True
    
    def on_template_select(self, event):
        selected = self.template_var.get()
        if selected in TEMPLATES:
            self.current_mappings = TEMPLATES[selected].copy()
            for i in range(4):
                self.entry_vars[i].set(self.current_mappings[str(i+1)])
    
    def on_entry_change(self, *args):
        try:
            new_mappings = {
                '1': self.entry_vars[0].get().strip(),
                '2': self.entry_vars[1].get().strip(),
                '3': self.entry_vars[2].get().strip(),
                '4': self.entry_vars[3].get().strip()
            }
            self.current_mappings = new_mappings
            self.template_var.set("Custom")
        except Exception as e:
            pass
    
    def toggle_active(self):
        self.active = not self.active
        if self.active:
            self.toggle_button.config(text="Stop", bg="green")
            self.status_label.config(text="Status: Active")
        else:
            self.toggle_button.config(text="Start", bg="red")
            self.status_label.config(text="Status: Inactive")

if __name__ == "__main__":
    root = tk.Tk()
    app = RemapperApp(root)
    root.mainloop()
