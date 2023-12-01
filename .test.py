import tkinter as tk
import subprocess
import threading

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
    dialog.configure(bg='black')

    question_label = tk.Label(dialog, text="Which interface do you want to use?", font=('Helvetica', 14), bg='black', fg='white')
    question_label.pack(pady=10)

    ethernet_button = tk.Button(dialog, text="Ethernet", command=lambda: handle_interface_selection("ethernet"), font=('Helvetica', 12), fg='black', bg='gray')
    wifi_button = tk.Button(dialog, text="WiFi", command=lambda: handle_interface_selection("wifi"), font=('Helvetica', 12), fg='black', bg='gray')

    ethernet_button.pack(pady=10)
    wifi_button.pack(pady=10)

def handle_interface_selection(interface):
    select_interface_and_execute_command(interface)
    root.after(100, lambda: destroy_dialog(root.winfo_children()[-1]))  # Close the dialog after a short delay

def destroy_dialog(dialog):
    dialog.destroy()

root = tk.Tk()
root.title("Netsec Mapper")
root.configure(bg='black')

# Create the custom command button
custom_command_button = tk.Button(root, text="ARP Scan", command=open_interface_dialog, font=('Helvetica', 12), fg='black', bg='gray')

# Create a label with a background color and text
label = tk.Label(root, text="Netsec Mapper", font=('Helvetica', 24), bg='black', fg='white', padx=20, pady=10)

# Create a text widget to display the command output
result_text = tk.Text(root, height=10, width=50, font=('Helvetica', 12), bg='black', fg='white')

# Place widgets in the window
label.pack(fill='both')
custom_command_button.pack(pady=10)
result_text.pack()

# Start the main event loop
root.mainloop()
