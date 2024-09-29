import tkinter as tk
from tkinter import filedialog, scrolledtext
import subprocess
import threading

print("Developed By https://t.me/micr0softstore")

# Initialize variables to store the paths
ap_path = ""
bl_path = ""
csc_path = ""
cp_path = ""
home_path = ""


# Function to open file dialog and update corresponding textbox and path variable
def select_file(entry, path_var):
    filepath = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])  # Allow all file types
    if filepath:
        entry.config(state=tk.NORMAL)  # Unlock the textbox to insert file path
        entry.delete(0, tk.END)        # Clear the previous text
        entry.insert(0, filepath)      # Insert the new file path
        entry.config(state=tk.DISABLED)  # Lock the textbox again
        path_var.set(filepath)         # Update the variable with selected file path

# Function to output text in the terminal (read-only text area)
def terminal_output(text):
    terminal.config(state=tk.NORMAL)  # Unlock terminal to write
    terminal.insert(tk.END, text)     # Insert new text at the end
    terminal.see(tk.END)              # Scroll to the end for real-time updates
    terminal.config(state=tk.DISABLED)  # Lock terminal to make it read-only

# Function to run a command in the background and update terminal in real-time
def run_command(command):
    # This function will run in a separate thread
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)

    # Read output line by line and display it in the terminal
    for line in process.stdout:
        terminal_output(line)

    # Handle any error messages (optional)
    for line in process.stderr:
        terminal_output(line)

# Function to be triggered by the Start button (for demo: running "ping google.com")
def flash():
    # Retrieve the paths from the textboxes and save them to variables
    global ap_path, bl_path, csc_path, cp_path
    ap_path = entries[0].get()
    bl_path = entries[1].get()
    csc_path = entries[2].get()
    cp_path = entries[3].get()
    home_path = entries[4].get()

    nand_erase_state = nand_erase_var.get()

    root_cmd = "./odin4 "
    if ap_path != "":
        root_cmd = f'{root_cmd}-a "{ap_path}" ' 
    if bl_path != "":
        root_cmd = f'{root_cmd}-b "{bl_path}" '
    if csc_path != "":
        root_cmd = f'{root_cmd}-s "{csc_path}" '
    if cp_path != "":
        root_cmd = f'{root_cmd}-c "{cp_path}" '
    if home_path != "":
        root_cmd = f'{root_cmd}-u "{home_path}" '
    if str(nand_erase_state) == "1":
        root_cmd = f'{root_cmd}-e '

    command = f"{root_cmd}"
    
    threading.Thread(target=run_command, args=(command,)).start()

# Function to exit the application
def exit_app():
    root.destroy()

def redownload_d():
    command = f"./odin4 --redownload"
    terminal_output("Rebooting to download mode...\n")
    threading.Thread(target=run_command, args=(command,)).start()

def restrat_d():
    command = f"./odin4 --reboot"
    terminal_output("Rebooting to system...\n")
    threading.Thread(target=run_command, args=(command,)).start()

# Function to check the device state and update the label (you'll write the logic here)
def check_device_state():
    command = "./odin4 -l"
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
    value = str(result.stdout)
    if value != "":
        state_d = True 
    else:
        state_d = False
    
    if state_d:
        device_status_label.config(text="Device: Connected")
    else:
        device_status_label.config(text="Device: Disconnected")

# Function to show the Main menu layout
def show_main():
    # Hide Settings and Device State widgets
    nand_erase_checkbutton.grid_forget()
    redownload_btn.grid_forget()
    reboot_btn.grid_forget()
    device_status_label.grid_forget()
    refresh_btn.grid_forget()

    # Show Main widgets (file selectors)
    for i in range(len(entries)):
        labels[i].grid(row=i, column=0, padx=10, pady=5)
        entries[i].grid(row=i, column=1, padx=10, pady=5)
        buttons[i].grid(row=i, column=2, padx=10, pady=5)

# Function to show the Settings menu layout
def show_settings():
    # Hide Main and Device State widgets
    for i in range(len(entries)):
        labels[i].grid_forget()
        entries[i].grid_forget()
        buttons[i].grid_forget()
    device_status_label.grid_forget()
    refresh_btn.grid_forget()

    # Show Settings widgets
    nand_erase_checkbutton.grid(row=0, column=0, padx=10, pady=5)
    redownload_btn.grid(row=1, column=0, padx=10, pady=5)
    reboot_btn.grid(row=1, column=1, padx=10, pady=5)

# Function to show the Device State layout
def show_device_state():
    # Hide Main and Settings widgets
    for i in range(len(entries)):
        labels[i].grid_forget()
        entries[i].grid_forget()
        buttons[i].grid_forget()
    nand_erase_checkbutton.grid_forget()
    redownload_btn.grid_forget()
    reboot_btn.grid_forget()

    # Show Device State widgets
    device_status_label.grid(row=0, column=0, padx=10, pady=5)
    refresh_btn.grid(row=1, column=0, padx=10, pady=5)

# Create main window
root = tk.Tk()
root.title("Odin4 - Linux")

# Define the layout of labels, textboxes, and buttons for the Main menu
label_names = ["AP:", "BL:", "CSC:", "CP:", "HOME:"]
entries = []
labels = []
buttons = []
variables = []

for i, label_name in enumerate(label_names):
    # Create a label
    lbl = tk.Label(root, text=label_name)
    lbl.grid(row=i, column=0, padx=10, pady=5)
    labels.append(lbl)

    # Create a locked entry (textbox)
    entry = tk.Entry(root, width=50, state=tk.DISABLED)
    entry.grid(row=i, column=1, padx=10, pady=5)
    entries.append(entry)

    # Create a variable to store the selected file path
    path_var = tk.StringVar()
    variables.append(path_var)

    # Create a 'Select' button
    select_btn = tk.Button(root, text="Select", command=lambda e=entry, v=path_var: select_file(e, v))
    select_btn.grid(row=i, column=2, padx=10, pady=5)
    buttons.append(select_btn)

# Create a read-only scrolled text area for terminal output
terminal = scrolledtext.ScrolledText(root, width=70, height=10, state=tk.DISABLED, wrap=tk.WORD)
terminal.grid(row=len(label_names), column=0, columnspan=3, padx=10, pady=10)

# Create a Start button at the bottom
start_btn = tk.Button(root, text="Start", command=flash)
start_btn.grid(row=len(label_names) + 2, column=1, pady=10)

# Create an Exit button at the bottom
exit_btn = tk.Button(root, text="Exit", command=exit_app)
exit_btn.grid(row=len(label_names) + 2, column=2, pady=10)

# Create Settings widgets (check box and buttons)
nand_erase_var = tk.IntVar()
nand_erase_checkbutton = tk.Checkbutton(root, text="Nand Erase", variable=nand_erase_var)

redownload_btn = tk.Button(root, text="Redownload (If possible)", command=redownload_d)
reboot_btn = tk.Button(root, text="Reboot", command=restrat_d)

# Create Device State widgets (label and refresh button)
device_status_label = tk.Label(root, text="Device: Disconnected")
refresh_btn = tk.Button(root, text="Refresh", command=check_device_state)

# Create a menu bar with three options: Main, Settings, and Device State
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Add "Main", "Settings", and "Device State" to the menu
menu_bar.add_command(label="Main", command=show_main)
menu_bar.add_command(label="Settings", command=show_settings)
menu_bar.add_command(label="Device State", command=show_device_state)

# Show Main menu by default
show_main()

# Start the Tkinter event loop
root.mainloop()
