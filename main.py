import tkinter as tk
from socket import *

def conScan(tgtHost, tgtPort):
    try:
        connskt = socket(AF_INET, SOCK_STREAM)
        connskt.connect((tgtHost, tgtPort))
        result_list.insert(tk.END, f'[+] {tgtPort}/tcp open')
        connskt.close()
    except:
        result_list.insert(tk.END, f'[-] {tgtPort}/tcp closed')

def portScan():
    tgtHost = host_entry.get()
    tgtPorts = port_entry.get().split(',')
    result_list.delete(0, tk.END)
    try:
        tgtIP = gethostbyname(tgtHost)
    except:
        result_list.insert(tk.END, f'[-] Cannot resolve {tgtHost}')
        return

    try:
        tgtName = gethostbyaddr(tgtIP)
        result_list.insert(tk.END, f'\n[+] Scan result of: {tgtName[0]}')
    except:
        result_list.insert(tk.END, f'\n[+] Scan result of: {tgtIP}')

    setdefaulttimeout(1)
    for tgtPort in tgtPorts:
        result_list.insert(tk.END, f'Scanning Port: {tgtPort}')
        conScan(tgtHost, int(tgtPort))

def clear_results():
    result_list.delete(0, tk.END)

def clear_inputs():
    host_entry.delete(0, tk.END)
    port_entry.delete(0, tk.END)

def on_closing():
    root.destroy()

root = tk.Tk()
root.title("Port Scanner")

window_width = 500
window_height = 400

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

root.geometry(f'{window_width}x{window_height}+{x}+{y}')

host_label = tk.Label(root, text="Target Host (IP or Hostname):")
host_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')

host_entry = tk.Entry(root)
host_entry.grid(row=0, column=1, padx=10, pady=10)

port_label = tk.Label(root, text="Target Ports (comma separated):")
port_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')

port_entry = tk.Entry(root)
port_entry.grid(row=1, column=1, padx=10, pady=10)

scan_button = tk.Button(root, text="Scan Ports", command=portScan)
clear_results_button = tk.Button(root, text="Clear Results", command=clear_results)
clear_inputs_button = tk.Button(root, text="Clear Inputs", command=clear_inputs)

scan_button.grid(row=2, column=0, padx=10, pady=10)
clear_results_button.grid(row=2, column=1, padx=10, pady=10)
clear_inputs_button.grid(row=2, column=2, padx=10, pady=10)

result_list = tk.Listbox(root, height=15, width=70)
result_list.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
