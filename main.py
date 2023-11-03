import tkinter as tk
from socket import *

def conScan(tgtHost, tgtPort):
    try:
        connskt = socket(AF_INET, SOCK_STREAM)
        connskt.connect((tgtHost, tgtPort))
        result_text.insert(tk.END, f'[+] {tgtPort}/tcp open\n')
        connskt.close()
    except:
        result_text.insert(tk.END, f'[-] {tgtPort}/tcp closed\n')

def portScan():
    tgtHost = host_entry.get()
    tgtPorts = port_entry.get().split(',')
    result_text.delete(1.0, tk.END)
    try:
        tgtIP = gethostbyname(tgtHost)
    except:
        result_text.insert(tk.END, f'[-] Cannot resolve {tgtHost}\n')
        return

    try:
        tgtName = gethostbyaddr(tgtIP)
        result_text.insert(tk.END, f'\n[+] Scan result of: {tgtName[0]}\n')
    except:
        result_text.insert(tk.END, f'\n[+] Scan result of: {tgtIP}\n')

    setdefaulttimeout(1)
    for tgtPort in tgtPorts:
        result_text.insert(tk.END, f'Scanning Port: {tgtPort}\n')
        conScan(tgtHost, int(tgtPort))

def on_closing():
    root.destroy()

root = tk.Tk()
root.title("Port Scanner")

# Calcul des dimensions de la fenêtre
window_width = 400
window_height = 400

# Obtenir les dimensions de l'écran
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculer la position pour centrer la fenêtre
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

# Définir les dimensions de la fenêtre et la positionner au centre
root.geometry(f'{window_width}x{window_height}+{x}+{y}')

host_label = tk.Label(root, text="Target Host (IP or Hostname):")
host_label.pack()

host_entry = tk.Entry(root)
host_entry.pack()

port_label = tk.Label(root, text="Target Ports (comma separated):")
port_label.pack()

port_entry = tk.Entry(root)
port_entry.pack()

scan_button = tk.Button(root, text="Scan Ports", command=portScan)
scan_button.pack()

result_text = tk.Text(root, height=15, width=50)
result_text.pack()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
