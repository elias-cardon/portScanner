from socket import *

def conScan(tgtHost, tgtPort):
    try:
        # Crée un objet de socket avec la famille d'adresses IPv4 et le type de socket en mode flux
        connskt = socket(AF_INET, SOCK_STREAM)
        # Tente de se connecter à l'adresse IP ou au nom d'hôte et au numéro de port spécifiés
        connskt.connect((tgtHost, tgtPort))
        # Affiche un message indiquant que le port est ouvert si la connexion réussit
        print('[+]%d/tcp open' % tgtPort)
        # Ferme la connexion
        connskt.close()
    except:
        # Affiche un message indiquant que le port est fermé si la connexion échoue
        print('[-]%d/tcp closed' % tgtPort)

def portScan(tgtHost, tgtPorts):
    try:
        # Obtient l'adresse IP de la cible en utilisant son nom d'hôte
        tgtIP = gethostbyname(tgtHost)
    except:
        # Affiche un message d'erreur si l'adresse IP de la cible ne peut pas être résolue
        print('[-] Cannot resolve %s ' % tgtHost)
        return

    try:
        # Obtient le nom d'hôte associé à l'adresse IP
        tgtName = gethostbyaddr(tgtIP)
        # Affiche le nom d'hôte si disponible
        print('\n[+] Scan result of: %s' % tgtName[0])
    except:
        # Affiche l'adresse IP si le nom d'hôte n'est pas disponible
        print('\n[+] Scan result of: %s' % tgtIP)

    # Configure le temps d'attente pour les connexions à 1 seconde
    setdefaulttimeout(1)

    for tgtPort in tgtPorts:
        # Affiche un message indiquant le port en cours de numérisation
        print('Scanning Port: %d' % tgtPort)
        # Appelle la fonction conScan pour scanner le port en cours
        conScan(tgtHost, int(tgtPort))

if __name__ == '__main__':
    # Appelle la fonction portScan pour scanner les ports 80 et 22 de la machine cible 'google.com'
    portScan('google.com', [80, 22])
