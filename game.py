import tkinter as tk

class DFAGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🌸 Escape the Magical Palace (DFA Simulator) 🌸")
        self.root.geometry("820x560")  # Widened window to fit the history panel nicely
        self.root.configure(bg="#FFF0F5")  # Lavender Blush Background

        # 1. Initialize the FSM State and History Tracker
        self.current_state = "q0"
        self.move_history = []  # List to store strings of every step taken

        # Theme Color Palette
        self.colors = {
            "main_bg": "#FFF0F5",       # Soft pastel pink/white
            "card_bg": "#FFFFFF",       # Pure white for text boxes
            "text_dark": "#4A2E35",     # Deep berry for readable text
            "pink_accent": "#FF69B4",   # Hot Pink for primary buttons
            "purple_accent": "#D8BFD8", # Thistle Purple for states
            "state_bg": "#FFE4E1",      # Misty Rose
            "win_green": "#C1E1C1",     # Soft pastel mint green
            "lose_red": "#FFB7B2",      # Soft pastel coral red
            "log_bg": "#FAFAFA"         # Light off-white for the history tracker
        }

        # Room Data mapped to DFA States
        self.room_data = {
            "q0": {
                "title": "🎀 State q0: The Dressing Room 🎀",
                "desc": "You wake up in a locked pastel dressing room.\nThe vanity mirror is sparkling. The only heavy glass door is to the NORTH.",
            },
            "q1": {
                "title": "✨ State q1: The Grand Ballroom ✨",
                "desc": "You are surrounded by fairy lights and crystal chandeliers.\nThere is a glowing hallway to the EAST,\nand your dressing room is back to the SOUTH.",
            },
            "q2": {
                "title": "🏰 State q2: The Royal Courtyard 🏰",
                "desc": "Oh no, you hear palace guards approaching your way!\nA massive golden exit gate stands right to the NORTH.",
            },
            "q_win": {
                "title": "👑 State q_win: Freedom! (ACCEPT STATE) 👑",
                "desc": "The starlight hits your face! You successfully navigated the state machine and escaped the palace safely!",
            },
            "q_lose": {
                "title": "💔 State q_lose: Caught! (TRAP STATE) 💔",
                "desc": "Oops! You stepped into a trap room or got spotted by guards.\nThe DFA reached a dead state. Game Over, bestie.",
            }
        }

        # --- LAYOUT FRAMES ---
        # Left Panel (For the Game Controls)
        self.left_frame = tk.Frame(root, bg=self.colors["main_bg"])
        self.left_frame.pack(side="left", fill="both", expand=True, padx=20)

        # Right Panel (For the Live History Tracker)
        self.right_frame = tk.LabelFrame(root, text=" 📜 DFA Transition History Log 📜 ", fg=self.colors["text_dark"], bg=self.colors["main_bg"], font=("Segoe UI", 11, "bold"), padx=10, pady=10)
        self.right_frame.pack(side="right", fill="both", padx=20, pady=20)

        # 2. Build the Left UI Components (Game Content)
        self.title_label = tk.Label(self.left_frame, text="", font=("Segoe UI", 16, "bold"), fg=self.colors["text_dark"], bg=self.colors["main_bg"])
        self.title_label.pack(pady=15)

        self.desc_label = tk.Label(self.left_frame, text="", font=("Segoe UI", 11), fg=self.colors["text_dark"], bg=self.colors["card_bg"], 
                                   width=45, height=5, relief="flat", highlightbackground=self.colors["purple_accent"], highlightthickness=2, justify="center", wraplength=360)
        self.desc_label.pack(pady=10)

        self.state_frame = tk.Frame(self.left_frame, bg=self.colors["state_bg"], padx=15, pady=8, highlightbackground=self.colors["pink_accent"], highlightthickness=1)
        self.state_frame.pack(pady=10)
        
        self.state_label = tk.Label(self.state_frame, text="", font=("Courier New", 12, "bold"), fg=self.colors["text_dark"], bg=self.colors["state_bg"])
        self.state_label.pack()

        self.banner_label = tk.Label(self.left_frame, text="", font=("Segoe UI", 11, "bold"), width=42, height=2, relief="solid", bd=1)
        self.banner_label.pack(pady=5)
        self.banner_label.pack_forget()

        # Directional Controls
        self.control_frame = tk.LabelFrame(self.left_frame, text=" 💕 Make Your Next Move 💕 ", fg=self.colors["text_dark"], bg=self.colors["main_bg"], font=("Segoe UI", 10, "italic"), padx=15, pady=15)
        self.control_frame.pack(pady=10)

        btn_style = {"width": 10, "bg": self.colors["pink_accent"], "fg": "white", "font": ("Segoe UI", 9, "bold"), "relief": "flat", "activebackground": "#FF1493"}
        
        self.btn_north = tk.Button(self.control_frame, text="🌸 NORTH", command=lambda: self.move("north"), **btn_style)
        self.btn_west  = tk.Button(self.control_frame, text="🌸 WEST",  command=lambda: self.move("west"),  **btn_style)
        self.btn_east  = tk.Button(self.control_frame, text="EAST 🌸",  command=lambda: self.move("east"),  **btn_style)
        self.btn_south = tk.Button(self.control_frame, text="🌸 SOUTH", command=lambda: self.move("south"), **btn_style)

        self.btn_north.grid(row=0, column=1, pady=5)
        self.btn_west.grid(row=1, column=0, padx=5)
        self.btn_east.grid(row=1, column=2, padx=5)
        self.btn_south.grid(row=2, column=1, pady=5)

        self.btn_reset = tk.Button(self.left_frame, text="✨ Play Again / Reset DFA ✨", command=self.reset_game, 
                                   width=25, bg="#4A2E35", fg="white", font=("Segoe UI", 11, "bold"), relief="flat", activebackground="#FF69B4")
        self.btn_reset.pack(pady=10)
        self.btn_reset.pack_forget()

        # 3. Build the Right UI Components (The History Tracker Display)
        self.history_listbox = tk.Listbox(self.right_frame, width=38, height=22, font=("Courier New", 10), bg=self.colors["log_bg"], fg=self.colors["text_dark"], relief="flat", highlightbackground=self.colors["purple_accent"], highlightthickness=1)
        self.history_listbox.pack(side="left", fill="both", expand=True)
        
        # Scrollbar for long loop histories
        self.scrollbar = tk.Scrollbar(self.right_frame, orient="vertical", command=self.history_listbox.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.history_listbox.config(yscrollcommand=self.scrollbar.set)

        # Insert placeholder instruction in history box
        self.history_listbox.insert(tk.END, " Machine initialized.")
        self.history_listbox.insert(tk.END, " Waiting for token input... ")
        self.history_listbox.insert(tk.END, "-------------------------------------")

        # Refresh screen to show starting state
        self.update_ui()

    def update_ui(self):
        """Redraws text and color elements based on current DFA state"""
        data = self.room_data[self.current_state]
        
        self.title_label.config(text=data["title"])
        self.desc_label.config(text=data["desc"])
        self.state_label.config(text=f" Palace State: [{self.current_state.upper()}] ")

        # Check if we hit an End State
        if self.current_state in ["q_win", "q_lose"]:
            for btn in [self.btn_north, self.btn_south, self.btn_east, self.btn_west]:
                btn.config(state="disabled", bg="#E0E0E0")

            self.banner_label.pack(pady=5) 
            self.btn_reset.pack(pady=10)
            
            self.history_listbox.insert(tk.END, "-------------------------------------")
            
            if self.current_state == "q_win":
                self.desc_label.config(bg=self.colors["win_green"])
                self.banner_label.config(text="🎉 INPUT ACCEPTED! YOU WIN! 🎉", bg=self.colors["win_green"], fg="#1E4620")
                self.history_listbox.insert(tk.END, " STATUS: String Accepted! ✅")
            else:
                self.desc_label.config(bg=self.colors["lose_red"])
                self.banner_label.config(text="❌ INPUT REJECTED! GAME OVER! ❌", bg=self.colors["lose_red"], fg="#721C24")
                self.history_listbox.insert(tk.END, " STATUS: String Rejected! ❌")
                
            self.history_listbox.insert(tk.END, f" Final Path Size: {len(self.move_history)} moves.")
            self.history_listbox.see(tk.END) # Auto-scroll to the bottom

    def move(self, direction):
        """Processes state transitions and appends logs to our tracker box"""
        old_state = self.current_state

        if self.current_state == "q0":
            if direction == "north": self.current_state = "q1"
            else: self.current_state = "q_lose"
                
        elif self.current_state == "q1":
            if direction == "east": self.current_state = "q2"
            elif direction == "south": self.current_state = "q0"
            else: self.current_state = "q_lose"
                
        elif self.current_state == "q2":
            if direction == "north": self.current_state = "q_win"
            else: self.current_state = "q_lose"

        # Log the transition to memory arrays and onto the UI Panel tracker
        move_num = len(self.move_history) + 1
        log_entry = f" {move_num}. Input: {direction.upper()}"
        state_entry = f"    ({old_state.upper()} -> {self.current_state.upper()})"
        
        self.move_history.append((direction, old_state, self.current_state))
        
        # Display nicely inside our right-side log box
        self.history_listbox.insert(tk.END, log_entry)
        self.history_listbox.insert(tk.END, state_entry)
        self.history_listbox.see(tk.END)  # Automatically shifts view to focus on the latest step

        self.update_ui()

    def reset_game(self):
        """Wipes the history log clean and loops the machine back to state q0"""
        self.current_state = "q0"
        self.move_history = []  # Clear history list
        
        # Clear UI components
        self.banner_label.pack_forget()
        self.btn_reset.pack_forget()
        self.desc_label.config(bg=self.colors["card_bg"])
        
        # Wipe the history log listbox and re-insert the starting notes
        self.history_listbox.delete(0, tk.END)
        self.history_listbox.insert(tk.END, " Machine Reset. New Test Running.")
        self.history_listbox.insert(tk.END, " Waiting for token input... ")
        self.history_listbox.insert(tk.END, "-------------------------------------")
        
        # Reactivate movement controls
        for btn in [self.btn_north, self.btn_south, self.btn_east, self.btn_west]:
            btn.config(state="normal", bg=self.colors["pink_accent"])
        
        self.update_ui()

if __name__ == "__main__":
    root = tk.Tk()
    app = DFAGameGUI(root)
    root.mainloop()