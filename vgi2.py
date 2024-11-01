import tkinter as tk
from tkinter import messagebox, simpledialog
from dataclasses import dataclass
import sqlite3

# Define data structures
@dataclass
class User:
    name: str
    phone: str
    location: str

@dataclass
class Need:
    water: bool = False
    food: bool = False
    medical_supplies: bool = False
    shelter: bool = False
    other: str = ''

# Enhanced register user function
def register_user() -> User:
    name = simpledialog.askstring("Input", "Enter your name:")
    phone = simpledialog.askstring("Input", "Enter your phone number:")

    if not name or not phone:
        messagebox.showwarning("Warning", "All fields are required!")
        return None

    location = select_location()
    return User(name=name, phone=phone, location=location)

# Enhanced location selection with modern design
def select_location() -> str:
    location_window = tk.Toplevel()
    location_window.title("Select Supply Station Location")
    location_window.geometry("360x280")
    location_window.config(bg='#FAFAFA')

    locations = ["Station A", "Station B", "Station C"]
    selected_location = tk.StringVar(value=locations[0])

    label = tk.Label(location_window, text="Choose a Supply Gathering Station:", font=("Segoe UI", 13, 'bold'), bg="#FAFAFA", fg="#333")
    label.pack(pady=15)

    for location in locations:
        radio = tk.Radiobutton(location_window, text=location, variable=selected_location, value=location,
                               bg="#FAFAFA", font=("Segoe UI", 11), fg="#5F6368", activebackground="#E0E0E0",
                               indicatoron=0, padx=10, pady=5, relief="ridge", borderwidth=1, width=15, cursor="hand2")
        radio.pack(anchor="w", padx=30, pady=2)

    def confirm_selection():
        location_window.destroy()

    confirm_button = tk.Button(location_window, text="Confirm", command=confirm_selection,
                               font=("Segoe UI", 12, "bold"), bg="#4CAF50", fg="white", relief="flat", padx=10, pady=6, cursor="hand2")
    confirm_button.pack(pady=25)

    location_window.wait_window()
    return selected_location.get()

# Collection of needs with pop-up dialogs
def collect_needs() -> Need:
    water = messagebox.askyesno("Needs", "Do you need water?")
    food = messagebox.askyesno("Needs", "Do you need food?")
    medical_supplies = messagebox.askyesno("Needs", "Do you need medical supplies?")
    shelter = messagebox.askyesno("Needs", "Do you need shelter?")
    other = simpledialog.askstring("Input", "Any other specific needs?")
    return Need(water=water, food=food, medical_supplies=medical_supplies, shelter=shelter, other=other)

# Database functions
def submit_request(user: User, needs: Need):
    if user:
        conn = sqlite3.connect('requests.db')
        c = conn.cursor()
        
        c.execute('INSERT INTO user (name, phone, location) VALUES (?, ?, ?)', (user.name, user.phone, user.location))
        user_id = c.lastrowid
        
        c.execute('''
            INSERT INTO need (user_id, water, food, medical_supplies, shelter, other)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, needs.water, needs.food, needs.medical_supplies, needs.shelter, needs.other))
        
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Success", "Your request has been submitted successfully.")
    else:
        messagebox.showerror("Error", "User information is missing!")

# Main application with enhanced layout and colors
def main():
    root = tk.Tk()
    root.title("Post-Earthquake Needs Management System")
    root.geometry("550x400")
    root.configure(bg="#FAFAFA")

    # Title label with rounded border
    title_frame = tk.Frame(root, bg="#3B5998", bd=0, highlightthickness=0)
    title_frame.pack(fill="x", pady=(20, 10))

    title_label = tk.Label(title_frame, text="Post-Earthquake Needs Management", font=('Segoe UI', 16, 'bold'),
                           bg="#3B5998", fg="white", padx=15, pady=10)
    title_label.pack(fill="x", padx=20, pady=5)

    # Frame for buttons with modern style
    button_frame = tk.Frame(root, bg="#FAFAFA")
    button_frame.pack(pady=40)

    # Register button with sleek design
    register_button = tk.Button(button_frame, text="Register & Submit Needs",
                                command=lambda: submit_request(register_user(), collect_needs()), font=("Segoe UI", 12, "bold"),
                                bg="#4CAF50", fg="white", relief="flat", padx=20, pady=8, borderwidth=0, cursor="hand2")
    register_button.pack(pady=10)

    # Exit button with modern styling
    exit_button = tk.Button(button_frame, text="Exit", command=root.quit,
                            font=("Segoe UI", 12, "bold"), bg="#b71c1c", fg="white", relief="flat", padx=20, pady=8, borderwidth=0, cursor="hand2")
    exit_button.pack(pady=10)

    # Version label at the bottom
    version_label = tk.Label(root, text="Demo Version | Created by Mobin Zehtabi Aslkhiabani", font=('Segoe UI', 9, 'italic'),
                             bg="#FAFAFA", fg="#7F8C8D")
    version_label.pack(side="bottom", pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
