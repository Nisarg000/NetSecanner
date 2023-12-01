import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import subprocess
import threading
from tkinter import simpledialog

def select_interface_and_execute_command(interface):
    if interface == "ethernet":
        command = "./getmac eth"
    elif interface == "wifi":
        command = "./getmac wifi"
    else:
        return

    def execute_command():
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        for line in process.stdout:
            result_text.insert(tk.END, line)
            result_text.see(tk.END)
        process.wait()

    thread = threading.Thread(target=execute_command)
    thread.start()

def open_interface_dialog():
    dialog = tk.Toplevel(root)
    dialog.title("Select Interface")
    dialog.geometry("300x150")
    dialog.configure(bg='#3E5151')  # Dark teal background

    question_label = tk.Label(dialog, text="Which interface do you want to use?", font=('Helvetica', 14), bg='#3E5151', fg='white')  # White text
    question_label.pack(pady=10)

    ethernet_button = ttk.Button(dialog, text="Ethernet", command=lambda: handle_interface_selection("ethernet"), style="TButton")
    wifi_button = ttk.Button(dialog, text="WiFi", command=lambda: handle_interface_selection("wifi"), style="TButton")

    ethernet_button.pack(pady=10)
    wifi_button.pack(pady=10)

def handle_interface_selection(interface):
    select_interface_and_execute_command(interface)
    root.after(100, lambda: destroy_dialog(root.winfo_children()[-1]))  # Close the dialog after a short delay

def destroy_dialog(dialog):
    dialog.destroy()

# Create a themed Tk instance with the "clam" theme
root = ThemedTk(theme="clam")

root.title("Netsecanner")
root.geometry("600x400")

# Create the custom command button
custom_command_button = ttk.Button(root, text="ARP Scan", command=open_interface_dialog, style="TButton")

# Create a label with a background color and text
label = ttk.Label(root, text="Netsecanner", font=('Helvetica', 24))

# Create a text widget to display the command output
result_text = tk.Text(root, height=10, width=50, font=('Helvetica', 12), bg='white', fg='black')

# Place widgets in the window
label.pack(fill='both', pady=10)
custom_command_button.pack(pady=10)
result_text.pack()

# Create a custom style for the buttons
style = ttk.Style()
style.configure("TButton", font=('Helvetica', 12), background='#2E86AB', foreground='white')  # Custom background and text color

# Start the main event loop
root.mainloop()
