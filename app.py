db_path = "./database.txt"

def create(args):
    try:
        with open(db_path, "a") as db:
            db.write(f"{args['lastname']},{args['firstname']},{args['address']},{args['phone']}\n")
        return True
    except Exception as e:
        print(f"Erreur lors de l'ajout du contact: {e}")
        return False

def search(string):
    try:
        with open(db_path, "r") as db:
            contacts = [line.strip() for line in db if line.strip()]
        return [contact for contact in contacts if string.lower() in contact.lower()]
    except Exception as e:
        print(f"Erreur lors de la recherche du contact: {e}")
        return []

def search_all():
    try:
        with open(db_path, "r") as db:
            contacts = [line.strip() for line in db if line.strip()]
        return contacts
    except Exception as e:
        print(f"Erreur lors de la lecture des contacts: {e}")
        return []

def delete(contact):
    try:
        with open(db_path, "r") as db:
            contacts = [line.strip() for line in db if line.strip()]
        contacts = [c for c in contacts if c != contact]
        with open(db_path, "w") as db:
            for contact in contacts:
                db.write(contact + "\n")
        return True
    except Exception as e:
        print(f"Erreur lors de la suppression du contact: {e}")
        return False

def sort_contacts(contacts):
    return sorted(contacts, key=lambda x: (x.split(',')[0].lower(), x.split(',')[1].lower()))

def afficher_annuaire():
    print("Nom,Prenom,Addresse,Phone")
    contacts = search_all()
    sorted_contacts = sort_contacts(contacts)
    for contact in sorted_contacts:
        print(contact)

def ajouter_contact(contact=None, save=False):
    if not contact:
        contact = {"lastname": None, "firstname": None, "address": None, "phone": None}
    lastname = get_input("Nom: ", contact["lastname"])
    firstname = get_input("Prenom: ", contact["firstname"])
    address = get_input("Addresse: ", contact["address"])
    phone = get_input("Telephone: ", contact["phone"])
    
    if not phone.isdigit():
        print("Le numéro de téléphone doit être composé de chiffres uniquement.")
        return
    
    args = {"lastname": lastname, "firstname": firstname, "address": address, "phone": phone}
    
    if save:
        click_save(args)
    else:
        print(f"{lastname},{firstname},{address},{phone}")

def click_save(args):
    verification = args["phone"]
    results = search(verification)
    if results:
        print("Le contact existe déjà.")
    else:
        success = create(args)
        if success:
            print("Contact ajouté avec succès.")
        else:
            print("Échec de l'ajout du contact.")

def rechercher_contact():
    string = input("Entrer votre recherche: ")
    contacts = search(string)
    for contact in contacts:
        print(contact)

    print("Voulez-vous..")
    print("3. Modifier ce contact")
    print("4. Supprimer ce contact")
    print("5. Retourner au menu principal")
    sub_action = int(input())
    if sub_action == 5:
        return
    elif sub_action == 4:
        supprimer_contact()
    elif sub_action == 3:
        modifier_contact()

def supprimer_contact(modify=False):
    tel = input("Entrer le numéro de téléphone complet du contact: ")
    contacts = search(tel)
    if contacts:
        contact = contacts[0]
        print(contact)
        success = delete(contact)
        if success and not modify:
            print("Le contact a été supprimé avec succès.")
        elif success and modify:
            ajouter_contact(contact=parse_contact(contact), save=True)
    else:
        print("Contact non trouvé.")

def modifier_contact():
    tel = input("Entrez le numéro de téléphone du contact à modifier: ")
    contacts = search(tel)
    if contacts:
        contact = contacts[0]
        print(f"Modifiez les informations de {contact.split(',')[0]} {contact.split(',')[1]}:")
        contact_modifie = {
            "lastname": get_input("Nom: ", contact.split(',')[0]),
            "firstname": get_input("Prenom: ", contact.split(',')[1]),
            "address": get_input("Addresse: ", contact.split(',')[2]),
            "phone": get_input("Telephone: ", contact.split(',')[3])
        }
        # Supprimer l'ancien contact
        if delete(contact):
            # Ajouter le contact modifié
            if create(contact_modifie):
                print("Contact mis à jour avec succès.")
            else:
                print("Échec de la mise à jour du contact.")
        else:
            print("Échec de la suppression du contact original.")
    else:
        print("Contact non trouvé.")

def parse_contact(contact_str):
    lastname, firstname, address, phone = contact_str.split(',')
    return {"lastname": lastname, "firstname": firstname, "address": address, "phone": phone}

def get_input(prompt, default=None):
    value = input(prompt)
    return value if value else default

def main_menu():
    while True:
        print("Entrer votre action parmi les suivantes:")
        print("1. Rechercher un contact")
        print("2. Ajouter un contact")
        print("3. Modifier un contact")
        print("0. Sortir de l'application")
        
        try:
            action = int(input())
            if action == 1:
                rechercher_contact()
            elif action == 2:
                ajouter_contact(save=True)
            elif action == 3:
                modifier_contact()
            elif action == 0:
                break
            else:
                print("Option non supportée.")
        except ValueError:
            print("Veuillez entrer un numéro valide.")

if __name__ == "__main__":
    afficher_annuaire()
    main_menu()
