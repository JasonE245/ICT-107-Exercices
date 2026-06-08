from os import environ
from web3 import Web3
from dotenv import load_dotenv
load_dotenv()

import json
import hashlib

# ==========================================================
# CONFIGURATION
# ==========================================================

# URL RPC de la blockchain privée CPNV
RPC_URL = "http://10.229.43.182:8545/"

# Adresse du compte expéditeur
SENDER_ADDRESS = "0x9b0e179F5F15B712736AFA377b7DF212b8936896"

# Clé privée (⚠ À améliorer !)
PRIVATE_KEY = environ.get("PRIVATE_KEY")

# Montant à envoyer (en ETH)
AMOUNT_TO_SEND = 0.01

# ==========================================================
# CONNEXION À LA BLOCKCHAIN
# ==========================================================

w3 = Web3(Web3.HTTPProvider(RPC_URL))

if w3.is_connected():
    print("Connecte a la blockchain")
else:
    print("Connexion echouee")
    exit()

# ==========================================================
# LECTURE DES ADRESSES
# ==========================================================

def lire_adresses(fichier):
    adresses = []
    with open(fichier, "r") as f:
        for ligne in f:
            adresse = ligne.strip()
            if w3.is_address(adresse):
                adresses.append(adresse)
    return adresses

# ==========================================================
# AFFICHER LES SOLDES
# ==========================================================

def afficher_soldes(adresses):
    for adresse in adresses:
        balance_wei = w3.eth.get_balance(adresse)
        balance_eth = w3.from_wei(balance_wei, 'ether')
        print(f"{adresse} : {balance_eth} ETH")

# ==========================================================
# ENVOI DE TRANSACTION
# ==========================================================

def envoyer_eth(destinataire, montant_eth, nonce):
    transaction = {
        "nonce": nonce,
        "to": destinataire,
        "value": w3.to_wei(montant_eth, 'ether'),
        "gas": 2100000,
        "gasPrice": w3.eth.gas_price,
        "chainId": w3.eth.chain_id
    }
    signed_tx = w3.eth.account.sign_transaction(transaction, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    return tx_hash.hex()

# ==========================================================
# ENVOI DE METADONNEES
# ==========================================================

def envoyer_metadonnees(url, file_hash):
    metadata = json.dumps({"url": url, "sha256": file_hash})
    data_hex = "0x" + metadata.encode('utf-8').hex()

    nonce = w3.eth.get_transaction_count(SENDER_ADDRESS)
    transaction = {
        "nonce": nonce,
        "to": "0x0000000000000000000000000000000000000000",
        "value": 0,
        "gas": 200000,
        "gasPrice": w3.to_wei('20', 'gwei'),
        "chainId": w3.eth.chain_id,
        "data": data_hex
    }
    signed_tx = w3.eth.account.sign_transaction(transaction, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    return tx_hash.hex()

# ==========================================================
# PROGRAMME PRINCIPAL
# ==========================================================

def main():
    adresses = lire_adresses("adresses.txt")

    print("\n=== Soldes avant envoi ===")
    afficher_soldes(adresses)

    nonce = w3.eth.get_transaction_count(SENDER_ADDRESS)

    print("\n=== Envoi des transactions ===")

    for adresse in adresses:
        try:
            tx_hash = envoyer_eth(adresse, AMOUNT_TO_SEND, nonce)
            print(f"Transaction envoyee vers {adresse}")
            print(f"Hash : {tx_hash}")
            nonce += 1
        except Exception as e:
            print(f"Erreur : {e}")

    print("\n=== Soldes apres envoi ===")
    afficher_soldes(adresses)

    # Envoi de metadonnees
    print("\n=== Ecriture de metadonnees ===")
    path = input("Chemin de votre fichier PDF (Enter pour ignorer): ").strip()
    if path:
        try:
            with open(path, 'rb') as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
            print(f"Hash SHA-256 : {file_hash}")
            url = input("URL publique du fichier: ")
            tx_hash = envoyer_metadonnees(url, file_hash)
            print(f"Metadonnees envoyees ! tx_hash : {tx_hash}")
        except FileNotFoundError:
            print("Fichier introuvable")
        except Exception as e:
            print(f"Erreur : {e}")


if __name__ == "__main__":
    main()