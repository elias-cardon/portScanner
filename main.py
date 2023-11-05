# Importation des modules nécessaires
import tkinter as tk  # Module pour créer une interface graphique
from socket import *  # Module pour la communication réseau
import json  # Module pour travailler avec des fichiers JSON
from datetime import datetime  # Module pour obtenir la date et l'heure actuelles
import re  # Module pour effectuer des opérations sur les chaînes de caractères
import os  # Module pour interagir avec le système de fichiers

# Fonction pour vérifier l'état d'un port sur une cible
def conScan(tgtHost, tgtPort):
    try:
        connskt = socket(AF_INET, SOCK_STREAM)
        connskt.connect((tgtHost, tgtPort))
        result_list.insert(tk.END, f'[+] {tgtPort}/tcp open')
        connskt.close()
    except:
        result_list.insert(tk.END, f'[-] {tgtPort}/tcp closed')

# Fonction pour effectuer une analyse de ports
def portScan():
    tgtHost = host_entry.get()
    tgtPorts = port_entry.get().split(',')  # Séparation des ports saisis par l'utilisateur
    result_list.delete(0, tk.END)  # Effacer les résultats précédents

    try:
        tgtIP = gethostbyname(tgtHost)  # Obtenir l'adresse IP de la cible
    except gaierror as e:
        result_list.insert(tk.END, f'[-] Cannot resolve {tgtHost}: {e}')
        return

    try:
        tgtName = gethostbyaddr(tgtIP)  # Obtenir le nom d'hôte associé à l'adresse IP
        result_list.insert(tk.END, f'\n[+] Scan result of: {tgtName[0]}')
    except herror as e:
        result_list.insert(tk.END, f'\n[+] Scan result of: {tgtIP}')

    setdefaulttimeout(1)  # Définir le délai d'attente pour les connexions à 1 seconde
    results = []  # Liste pour stocker les résultats

    for tgtPort in tgtPorts:
        try:
            result_list.insert(tk.END, f'Scanning Port: {tgtPort}')
            conScan(tgtHost, int(tgtPort))
            results.append({"Host": tgtHost, "Port": f'{tgtPort}/tcp open'})
        except error as e:
            results.append({"Host": tgtHost, "Port": f'{tgtPort}/tcp closed: {e}'})

    # Enregistrez les résultats dans un fichier JSON avec un horodatage
    filename = 'scan_results.json'

    # Si le fichier JSON existe déjà, lisez les résultats existants
    existing_results = []
    if os.path.isfile(filename):
        with open(filename, 'r') as f:
            existing_results = json.load(f)

    # Ajoutez les nouveaux résultats aux résultats existants
    existing_results.extend(results)

    # Enregistrez les résultats mis à jour dans le fichier JSON
    with open(filename, 'w') as f:
        json.dump(existing_results, f, indent=4)
        result_list.insert(tk.END, f'\n[+] Results saved to {filename}')

# Fonction pour effacer les résultats de l'interface
def clear_results():
    result_list.delete(0, tk.END)

# Fonction pour effacer les champs de saisie de l'interface
def clear_inputs():
    host_entry.delete(0, tk.END)
    port_entry.delete(0, tk.END)

# Fonction pour gérer la fermeture de la fenêtre de l'interface
def on_closing():
    root.destroy()

# Création de la fenêtre principale de l'interface
root = tk.Tk()
root.title("Port Scanner")

# Positionnement de la fenêtre au centre de l'écran
window_width = 500
window_height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
root.geometry(f'{window_width}x{window_height}+{x}+{y}')

# Création des éléments d'interface
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

# Gestion de la fermeture de la fenêtre
root.protocol("WM_DELETE_WINDOW", on_closing)

# Démarrage de la boucle principale de l'interface
root.mainloop()
