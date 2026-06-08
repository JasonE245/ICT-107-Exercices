"""
Script de génération de hashes
"""
import hashlib
def generate_hash(password):
    """Génère un hash avec l'algorithme spécifié"""
    pwd_bytes = password.encode('utf-8')
    return hashlib.sha256(pwd_bytes).hexdigest()


while True:
    choix = input("Tapez:\n[1] Hachage d'un texte saisi \n[2] Hachage d'un fichier texte existant \nQue choisissez vous : ")
    if choix == '1':
        data = input("Entrer une donnée: ")
        generated_hash = generate_hash(data)
        print(generated_hash+"\n")
    elif choix == '2':
        path = input("Entrer le chemin de votre fichier: ")
        with open(path, 'rb') as file:
            file_bytes = file.read()
        generated_hash = hashlib.sha256(file_bytes).hexdigest()
        print(generated_hash + "\n")
    else:
        print("Choix invalide\n")

    while True:
        # Bonus - sauvegarde du hash
        sauvegarde = input("Sauvegarde (T/F): ")
        if sauvegarde == 'T' or sauvegarde == 't' or sauvegarde == 'True' or sauvegarde == 'true':
            try:
                with open('sauvegarde_hashes.txt', 'a', encoding="utf-8") as file:
                    file.write("- "+generated_hash+"\n")

            except:
                print("Fichier introuvable\n")
            else:
                print("Votre hash a donc été stocké !\n")
                break
        elif sauvegarde == 'F' or sauvegarde == 'f' or sauvegarde == 'False' or sauvegarde == 'false':
            print("Votre hash n'a donc pas été stocké !\n")
            break
        else:
            print("Choix invalide\n")