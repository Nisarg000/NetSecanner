import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import subprocess
import threading
from tkinter import simpledialog

def select_interface_and_execute_command(interface):
    if interface == "ethernet":
        command = "bash getmac eth"
    elif interface == "wifi":
        command = "bash getmac wifi"
    else:
        return

    def execute_command():
        clear_output()
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

        for line in process.stdout:
            result_text.insert(tk.END, line)
            result_text.see(tk.END)
            root.update()  # Update the GUI to show real-time output

    thread = threading.Thread(target=execute_command)
    thread.start()

def open_interface_dialog():
    clear_output()
    dialog = tk.Toplevel(root)
    dialog.title("Select Interface")
    dialog.geometry("400x250")  # Increased dialog size
    dialog.configure(bg='#3E5151')  # Dark teal background

    question_label = tk.Label(dialog, text="Which interface do you want to use?", font=('Helvetica', 18), bg='#3E5151', fg='white')  # Larger font
    question_label.pack(pady=20)  # Increased padding

    ethernet_button = ttk.Button(dialog, text="Ethernet", command=lambda: handle_interface_selection("ethernet"), style="TButton")
    wifi_button = ttk.Button(dialog, text="WiFi", command=lambda: handle_interface_selection("wifi"), style="TButton")

    ethernet_button.pack(pady=10)
    wifi_button.pack(pady=10)

def handle_interface_selection(interface):
    select_interface_and_execute_command(interface)
    root.after(100, lambda: destroy_dialog(root.winfo_children()[-1]))  # Close the dialog after a short delay

def destroy_dialog(dialog):
    dialog.destroy()

def execute_command_with_timer(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    clear_output()

    for line in process.stdout:
        result_text.insert(tk.END, line)
        result_text.see(tk.END)
        root.update()  # Update the GUI to show real-time output

    process.wait()

def clear_output():
    result_text.delete(1.0, tk.END)

def open_port_scan_dialog():
    ip_and_ports = simpledialog.askstring("Port Scan", "Enter IP address or hostname and port range (e.g., 192.168.1.1 80-100):")
    if ip_and_ports:
        command = f"python3 portscan.py {ip_and_ports}"
        execute_command_with_timer(command)

def open_ping_scan_dialog():
    clear_output()
    ip_range = simpledialog.askstring("Ping Scan", "Enter IP range, list, or single IP (e.g., 192.168.1.1-10,192.168.1.20,192.168.1.30):")
    if ip_range:
        command = f"python3 pingscan.py {ip_range}"
        execute_command_with_timer(command)

# Create a themed Tk instance with the "clam" theme
root = ThemedTk(theme="clam")

root.title("Netsecanner")
root.geometry("800x600")  # Increased default size

# Create the custom command button
custom_command_button = ttk.Button(root, text="ARP Scan", command=open_interface_dialog, style="TButton")

# Create a Port Scan button
port_scan_button = ttk.Button(root, text="Port Scan", command=open_port_scan_dialog, style="TButton")

# Create a Ping Scan button
ping_scan_button = ttk.Button(root, text="Ping Scan", command=open_ping_scan_dialog, style="TButton")

# Create a label with a background color and text
label = ttk.Label(root, text="Netsecanner", font=('Helvetica', 32))  # Larger font

# Create a text widget to display the command output
result_text = tk.Text(root, height=15, width=70, font=('Helvetica', 18), bg='white', fg='black')  # Larger size and font

# Place widgets in the window
label.pack(fill='both', pady=20)  # Increased padding
custom_command_button.pack(pady=15)  # Increased padding
port_scan_button.pack(pady=15)  # Increased padding
ping_scan_button.pack(pady=15)  # Increased padding
result_text.pack(pady=15)  # Increased padding

# Create a custom style for the buttons
style = ttk.Style()
style.configure("TButton", font=('Helvetica', 18), background='#2E86AB', foreground='white')  # Custom background and text color

# Start the main event loop
root.mainloop()
