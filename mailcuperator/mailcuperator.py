"""
Objective: Take every file from mails
Creator: XenonEGG

using: python 3.6
encoding: utf-8
"""

import os
import time
import string
from tkinter import *

import imaplib
import email
import webbrowser

import data_handler_not_crypted as data_handler_nc

# data base creation
_abs_path = os.path.abspath("")
_account_path = f"{_abs_path}\\account_handler"
_dh = data_handler_nc.data_handler(_account_path)

# use your email provider's IMAP server, you can look for your provider's IMAP server on Google
# or check this page: https://www.systoolsgroup.com/imap/
_imap_dictionary = {
    "yahoo": "imap.mail.yahoo.com",
    "outlook": "imap-mail.outlook.com",
    "hotmail": "imap-mail.outlook.com"
}


def clean(text, extension="", strong=True):
    text = "".join(c if c.isalnum() else "_" for c in text)
    if len(text) > 60:
        text = text[:61]
    if strong:
        to_remove = ["__utf_8_Q_", "__UTF_8_Q_", "__iso8859_15_Q_", "__windows_1258_Q_"]
        for rmv in to_remove:
            text = text.replace(rmv, "")
        # utf-8
        text = text.replace("_C3_89", "É")
        text = text.replace("_C3_A9", "é")
        text = text.replace("_C3_A8", "è")
        text = text.replace("_C3_A0", "à")
        text = text.replace("_C3_B4", "ô")
        text = text.replace("_27", "_")
        text = text.replace("_20", "")
        text = text.replace("2324", "")
        # iso8859
        text = text.replace("_E9", "é")
        text = text.replace("_EA", "è")
        text = text.replace("_E0", "à")
        text = text.replace("_5F", "")
        # window_1258
        text = text.replace("e_CC", "é")
        text = text.replace("e_EC", "è")
        while "__" in text:
            text = text.replace("__", "_")

    if len(extension) != 0:
        text = text[:-len(extension)]
    if text[-1:] == "_":
        text = text[:-1]
    return text


def get_extension(filename):
    point_not_found = True
    index = len(filename)
    while point_not_found and index > 0:
        index -= 1
        if filename[index] == ".":
            point_not_found = False

    is_letter = True
    extension = "."
    while is_letter and index < len(filename) - 1:
        index += 1
        if filename[index].isalnum():
            extension += filename[index]
        else:
            is_letter = False

    if extension != ".":
        return extension
    return None


def force_rmdir(path):
    if "folder_keeper" not in path and "files_keeper" not in path and "author_keeper" not in path:
        print(f"Le chemain d'accès : '{path}' est protégé")
        return

    try:
        os.rmdir(path)
    except:
        lib = os.listdir(path)
        for e in lib:
            e_path = f"{path}\\{e}"
            if os.path.isfile(e_path):
                os.remove(e_path)
            else:
                force_rmdir(e_path)
        os.rmdir(path)


def take_number(text):
    nums = []
    last_index = -1
    if text[0] in string.digits:
        last_index = 0
    for i in range(len(text)):
        if text[i] not in string.digits and last_index != -1:
            nums.append(int(text[last_index:i]))
            last_index = -1
        if text[i] in string.digits and last_index == -1:
            last_index = i
    return nums


def sort_list(object_list, croissant=True):
    dictio = {}
    greater = 0
    for e in object_list:
        num = take_number(e)[0]
        if num > greater:
            greater = num
        dictio[num] = e

    new_list = []
    if croissant:
        for i in range(0, greater + 1):
            try:
                new_list.append(dictio[i])
            except:
                pass
    else:
        for i in range(greater, -1, -1):
            try:
                new_list.append(dictio[i])
            except:
                pass
    return new_list


def format_time(cur_time):
    """
    cur_time need to be in seconds
    """
    if cur_time > 3600:
        return "{:.0f}".format(cur_time // 3600), "hour"
    if cur_time > 60:
        return "{:.0f}".format(cur_time // 60), "min"
    return "{:.0f}".format(cur_time), "sec"


def data_connection_save(user_mail, user_mdp):
    _dh.set_user_data(user_mail, user_mdp)


def get_mdp_app(user_mail):
    return _dh.get_user_data(user_mail)


def on_quit():
    _dh.update()
    window.quit()


def start():
    # vérifications
    user_email = user_email_value.get()
    user_mdp_app = user_mdp_app_value.get()
    folder_target = box_target_value.get()
    nb_mail_to_fetch = nb_mail_to_fetch_value.get()
    if folder_target == "":
        print("Sélectionnez un dossier à traiter...")
        return

    if not issubclass(type(nb_mail_to_fetch), int) or nb_mail_to_fetch < 0:
        print("La valeur du nombre de mail à traiter n'est pas correcte !")
        return

    # ajout du triage
    sorting = []
    if sorting_all_in_same_folder.get() == 1:
        sorting.append("all_in_same")
    if sorting_author_value.get() == 1:
        sorting.append("author")

    # traitement du mail
    mail_box = user_email.split("@")[1].split(".")[0]
    try:
        imap_server = _imap_dictionary[mail_box]
    except:
        print("Votre boîte mail n'est pas encore traitable par mailcuperator, "
              "ou alors faites attention à la syntaxe")
        return

    print("Téléchargement en cours...\n"
          "Cette opération peut prendre plusieurs minutes, "
          "cela dépend de la taille de votre boite mail à extraire...")
    print("=" * 100)

    typ, mail_count, file_count = main(imap_server, user_email, user_mdp_app, folder_target,
                                       nb_mail_to_fetch, time.time(), sorting)

    if typ in ["Empty", "OK"]:
        data_connection_save(user_email, user_mdp_app)
    if typ == "Erase":
        data_connection_save(user_email, "")
        select_frame("email")

    if typ == "OK":
        print("=" * 100)
        print("Un fichier folder_keeper a été créé, il contient tous les fichiers rangés dans des dossiers\n"
              "portant le nom des mails où ils ont étés trouvés.\n"
              "Un fichier files_keeper a été créé, il contient tous les fichiers trouvés dans les mails,\n"
              "s'il existe des fichiers avec le même nom, le plus récent a été conservé.\n")

        print(f"{mail_count} mails ont étés traités et {file_count} fichiers ont étés téléchargés.")


def main(imap_server, user_email, user_mdp, folder_target, nb_mail_to_fetch, start_time: float, sorting: list):
    """
    Les différents mode de triage sont : author
    """
    # create an IMAP4 class with SSL
    try:
        mail = imaplib.IMAP4_SSL(imap_server)
    except:
        print("Il semblerait que vous soyez hors connexion...")
        return "Connection", 0, 0
    # authenticate
    try:
        mail.login(user_email, user_mdp)
    except:
        print("Mail ou mot de passe invalide ! Essayez de recommencer.")
        return "Erase", 0, 0

    try:
        mail.select(folder_target)
    except:
        print("Dossier introuvable...\n"
              "Essayez de créer un dossier avec un nom sans accents, sans caractères spéciaux et "
              "sans espaces et mettez tous les mails que vous voulez extraire dedans. (les caractères "
              "spéciaux ne sont pas supportés pour accéder à une catégorie spécifique dans votre boîte mail)")
        return "Folder", 0, 0

    # Recherche des emails
    try:
        typ, data = mail.search(None, 'ALL')  # Récupérer tous les emails
    except:
        print("Le dossier renseigné n'est pas bon, essayez avec la bonne orthographe")
        return "Folder", 0, 0
    mail_indexes = data[0].split()
    if len(mail_indexes) == 0:
        print(f"Il n'y a pas de mail à traiter dans {folder_target}")
        return "Empty", 0, 0

    # Création du dossier qui va contenir tous les mails pendant le traitement
    folder_keeper_path = f"{_abs_path}\\folder_keeper"
    if os.path.exists(folder_keeper_path):
        force_rmdir(folder_keeper_path)
    os.mkdir(folder_keeper_path)

    mail_count = int(mail_indexes[-1])
    mail_stop = 0
    if nb_mail_to_fetch != 0:
        mail_stop = mail_count - nb_mail_to_fetch
    total_mail = mail_count - mail_stop

    increment = 0
    # Parcourir tous les emails récupérés dans l'odre du plus récent au plus vieux (mail_count > mail_stop)
    for index in range(mail_count, mail_stop, -1):
        increment += 1
        typ, msg_data = mail.fetch(str(index), '(RFC822)')
        raw_email = msg_data[0][1]
        try:
            email_message = email.message_from_bytes(raw_email)
        except:
            print(f"Mailcupérator n'a pas réussi à ouvrir le {increment}ème mail.")
            continue

        # Récupérer l'auteur (expéditeur) et le titre (sujet) de l'email
        sender = email_message['From']
        subject = clean(email_message['Subject'])

        for part in email_message.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue

            filename = part.get_filename()
            if filename:
                extension = get_extension(filename)
                if extension is None:
                    print(f"Mailcuperator n'arrive pas à télécharger un ficher du mail '{subject}' de '{sender}'")
                    continue
                filename = clean(filename, extension)
                filename = filename + extension

                folder_path = f"{folder_keeper_path}\\{increment}_{subject}_author_{clean(sender)}"
                if not os.path.exists(folder_path):
                    os.mkdir(folder_path)
                filepath = f"{folder_path}\\{filename}"
                open(filepath, 'wb').write(part.get_payload(decode=True))
        if increment == 3 or increment % 10 == 0:
            current_time = time.time()
            delta_time = current_time - start_time
            achieved = increment / total_mail
            speed = achieved / delta_time
            remaining = 1 - achieved
            time_remaining, unity = format_time(remaining / speed)
            print(f"Il reste {time_remaining} {unity}")
            print("{:.0f}%".format(achieved * 100))

    # close and logout
    mail.close()
    mail.logout()

    folders = os.listdir(folder_keeper_path)
    # Rangement des dossiers dans l'ordre du plus vieux au plus récent
    folders = sort_list(folders, False)

    """
    Mettre tous les fichiers dans le même dossier
    """
    # Création du dossier qui va contenir tous les fichiers
    files_keeper_path = f"{_abs_path}\\files_keeper"
    if os.path.exists(files_keeper_path):
        force_rmdir(files_keeper_path)

    if "all_in_same" in sorting:
        os.mkdir(files_keeper_path)

        # Ajout des fichiers, les plus vieux sont écrasés par les plus récents
        for folder in folders:
            folder_path = f"{folder_keeper_path}\\{folder}"
            lib = os.listdir(folder_path)
            for file in lib:
                source_file = f"{folder_path}\\{file}"
                destination_file = f"{files_keeper_path}\\{file}"

                with open(source_file, 'rb') as src:
                    # Lire le contenu du fichier source
                    contenu = src.read()

                    # Ouvrir le fichier cible en mode écriture binaire ('wb' pour écriture binaire)
                    with open(destination_file, 'wb') as dest:
                        # Écrire le contenu dans le fichier cible
                        dest.write(contenu)

    """
    Ranger les dossiers par auteur
    """
    # Création du dossier qui va contenir tous les mails rangés par auteur
    author_keeper_path = f"{_abs_path}\\author_keeper"
    if os.path.exists(author_keeper_path):
        force_rmdir(author_keeper_path)

    if "author" in sorting:
        os.mkdir(author_keeper_path)

        for folder in folders:
            folder_path = f"{folder_keeper_path}\\{folder}"
            sender = folder.split("author_")[-1]
            folder_target = f"{author_keeper_path}\\{sender}"

            if not os.path.exists(folder_target):
                os.mkdir(folder_target)

            lib = os.listdir(folder_path)
            for file in lib:
                source_file = f"{folder_path}\\{file}"
                destination_file = f"{folder_target}\\{file}"

                with open(source_file, 'rb') as src:
                    # Lire le contenu du fichier source
                    contenu = src.read()

                    # Ouvrir le fichier cible en mode écriture binaire ('wb' pour écriture binaire)
                    with open(destination_file, 'wb') as dest:
                        # Écrire le contenu dans le fichier cible
                        dest.write(contenu)

    file_count = 0
    for folder in folders:
        folder_path = f"{folder_keeper_path}\\{folder}"
        lib = os.listdir(folder_path)
        file_count += len(lib)

    return "OK", total_mail, file_count


"""
Configuration de la fenêtre
"""

window_bg_color = "#0CA8D6"
frame_bg_color = "#da7eff"
label_bg_color = "#29fff5"
button_bg_color = "#ffc829"

window = Tk()

window.title("Mailcuperator")
window.geometry("450x300")
window.minsize(450, 300)
window.iconbitmap("atome.ico")
window.configure(bg=window_bg_color)

window.protocol("WM_DELETE_WINDOW", on_quit)


"""
Logique window
"""
current_frame = None  # Allow to track in what window the user is


def select_frame(frame_name):
    """
    frame_name: email, mdp, recup
    """
    global current_frame

    frame_names = ["email", "mdp", "recup"]
    if frame_name not in frame_names:
        raise Exception("Le nom de frame spécifié n'est pas correct")

    frame_email.pack_forget()
    frame_mdp_app.pack_forget()
    frame_recuperation.pack_forget()

    if frame_name == frame_names[0]:
        frame_email.pack(expand=True)
    elif frame_name == frame_names[1]:
        frame_mdp_app.pack(expand=True)
    elif frame_name == frame_names[2]:
        frame_recuperation.pack(expand=True)

    current_frame = frame_name


def validate():
    global current_frame

    if current_frame == "email":
        user_email = user_email_value.get()
        parts = user_email.split("@")
        if len(parts) != 2:
            print("L'email n'est pas valide")
            return

        try:
            mdp = get_mdp_app(user_email)
            if mdp != "":
                user_mdp_app_value.set(mdp)
                select_frame("recup")
            else:
                select_frame("mdp")
        except:
            select_frame("mdp")

    elif current_frame == "mdp":
        user_mdp_app = user_mdp_app_value.get()
        if len(user_mdp_app) == 0:
            print("Le mot de passe ne doit pas être vide !")
            return

        select_frame("recup")

    elif current_frame == "recup":
        start()


"""
Frames (pages)
"""
frame_email = Frame(window)
frame_email.configure(bg=frame_bg_color, borderwidth=2, relief="raised")

frame_mdp_app = Frame(window)
frame_mdp_app.configure(bg=frame_bg_color, borderwidth=2, relief="raised")

frame_recuperation = Frame(window)
frame_recuperation.configure(bg=frame_bg_color, borderwidth=2, relief="raised")


"""
Elements de frame_email (page email)
"""

# label email
label_user_email = Label(frame_email, text="Email", fg="blue")
label_user_email.configure(bg=label_bg_color)
label_user_email.pack(padx=5, pady=5)

# entrée email
user_email_value = StringVar()
user_email_value.set("")
entry_user_email = Entry(frame_email, textvariable=user_email_value, width=30)
entry_user_email.pack(padx=5)

# bouton de validation email
button_mdp_app = Button(frame_email, text="Valider", command=validate, fg="red")
button_mdp_app.configure(bg=button_bg_color)
button_mdp_app.pack(padx=5, pady=5)


"""
Elements dans frame_mdp (page mdp)
"""

# label mdp
label_user_mdp_app = Label(frame_mdp_app, text="Mot de passe d'application (cliquez pour avoir "
                                               "des explications)", fg="blue")
label_user_mdp_app.bind("<Button-1>", lambda *args: webbrowser.open("https://fr.aide.yahoo.com/kb/SLN15241.html"))
label_user_mdp_app.configure(bg=label_bg_color)
label_user_mdp_app.pack(padx=5, pady=5)

# entrée mdp
user_mdp_app_value = StringVar()
user_mdp_app_value.set("")
entry_user_mdp_app = Entry(frame_mdp_app, textvariable=user_mdp_app_value, width=30)
entry_user_mdp_app.pack(padx=5)

# bouton de validation mdp
button_mdp_app = Button(frame_mdp_app, text="Valider", command=validate, fg="red")
button_mdp_app.configure(bg=button_bg_color)
button_mdp_app.pack(padx=5, pady=5)


"""
Elements dans frame_recup (page recup)
"""

# label folder_target
label_folder_target = Label(frame_recuperation, text="Vous avez plusieurs dossier dans votre boîte mail:\n"
                            "Boîte de réception, Spam, et d'autres que "
                            "vous avez vous-même créés.\n"
                            "Nom du dossier où sont les mails à extraire:", fg="blue")
label_folder_target.configure(bg=label_bg_color)
label_folder_target.pack(padx=5, pady=5)

# entrée folder_target
box_target_value = StringVar()
box_target_value.set("")
entry_box_target = Entry(frame_recuperation, textvariable=box_target_value, width=30)
entry_box_target.pack(padx=5)

# label nombre de mail à traiter
label_nb_mail_to_fetch = Label(frame_recuperation, text="Nombre de mail à traiter en partant du plus récent "
                                                        "(0 pour tous les traiter)", fg="blue")
label_nb_mail_to_fetch.configure(bg=label_bg_color)
label_nb_mail_to_fetch.pack(padx=5, pady=5)

# entry nombre de mail à traiter
nb_mail_to_fetch_value = IntVar()
nb_mail_to_fetch_value.set(0)
entry_nb_mail_to_fetch = Entry(frame_recuperation, textvariable=nb_mail_to_fetch_value, width=30)
entry_nb_mail_to_fetch.pack(padx=5)

# label sorte de triage
label_sorting = Label(frame_recuperation, text="Triage des mails par:", fg="blue")
label_sorting.configure(bg=label_bg_color)
label_sorting.pack(padx=5, pady=5)

# checkbutton selection tout dans le même
sorting_all_in_same_folder = IntVar()
checkbutton_sorting_all_in_same = Checkbutton(frame_recuperation, variable=sorting_all_in_same_folder,
                                              text="All in one", height=2, width=10)
checkbutton_sorting_all_in_same.configure(bg=frame_bg_color)
checkbutton_sorting_all_in_same.pack(padx=5)

# checkbutton selection auteur
sorting_author_value = IntVar()
checkbutton_sorting_author = Checkbutton(frame_recuperation, variable=sorting_author_value, text="Auteur", height=2, width=10)
checkbutton_sorting_author.configure(bg=frame_bg_color)
checkbutton_sorting_author.pack(padx=5)

# bouton de validation pour le téléchargement
button_download = Button(frame_recuperation, text="Télécharger les fichiers", command=validate, fg="red")
button_download.configure(bg=button_bg_color)
button_download.pack(padx=5, pady=5)


"""
Logique des touches
"""
window.bind("<Return>", lambda *args: validate())

"""
Finalization
"""
select_frame("email")
window.mainloop()
