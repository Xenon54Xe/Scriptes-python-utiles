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
    if "folder_keeper" not in path and "files_keeper" not in path:
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

    if type(nb_mail_to_fetch) != int or nb_mail_to_fetch < 0:
        print("La valeur du nombre de mail à traiter n'est pas correcte !")
        return

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

    typ, mail_count, file_count = main(user_email, user_mdp_app, folder_target, imap_server, time.time())

    if typ == "Erase":
        data_connection_save(user_email, "")
        select_frame("email")
    elif typ == "OK":
        print("=" * 100)
        data_connection_save(user_email, user_mdp_app)
        print("Un fichier folder_keeper a été créé, il contient tous les fichiers rangés dans des dossiers\n"
              "portant le nom des mails où ils ont étés trouvés.\n"
              "Un fichier files_keeper a été créé, il contient tous les fichiers trouvés dans les mails,\n"
              "s'il existe des fichiers avec le même nom, le plus récent a été conservé.\n")

        print(f"{mail_count} mails ont étés traités et {file_count} fichiers ont étés téléchargés.")


def main(user_email, user_mdp, folder_target, imap_server, start_time: float):
    # create an IMAP4 class with SSL
    mail = imaplib.IMAP4_SSL(imap_server)
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

    folder_keeper_path = f"{_abs_path}\\folder_keeper"
    if os.path.exists(folder_keeper_path):
        force_rmdir(folder_keeper_path)
    os.mkdir(folder_keeper_path)

    # Recherche des emails
    typ, data = mail.search(None, 'ALL')  # Récupérer tous les emails
    mail_indexes = data[0].split()
    if len(mail_indexes) == 0:
        print(f"Il n'y a pas de mail à traiter dans {folder_target}")
        return "Empty", 0, 0

    mail_count = int(mail_indexes[-1])
    increment = 0
    # Parcourir tous les emails récupérés dans l'odre du plus récent au plus vieux
    for index in range(mail_count, 0, -1):
        increment += 1
        typ, msg_data = mail.fetch(str(index), '(RFC822)')
        raw_email = msg_data[0][1]
        email_message = email.message_from_bytes(raw_email)

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

                folder_path = f"{folder_keeper_path}\\{increment}_{subject}"
                if not os.path.exists(folder_path):
                    os.mkdir(folder_path)
                filepath = f"{folder_path}\\{filename}"
                open(filepath, 'wb').write(part.get_payload(decode=True))
        if increment in [5, mail_count // 3, mail_count // 2, mail_count // 1.2]:
            current_time = time.time()
            delta_time = current_time - start_time
            achieved = increment / mail_count
            speed = achieved / delta_time
            remaining = 1 - achieved
            time_remaining, unity = format_time(remaining / speed)
            print(f"Il reste {time_remaining} {unity}")
            print("{:.0f}%".format(achieved * 100))

    # close and logout
    mail.close()
    mail.logout()

    folders = os.listdir(folder_keeper_path)
    folders = sort_list(folders, False)

    files_keeper_path = f"{_abs_path}\\files_keeper"
    if os.path.exists(files_keeper_path):
        force_rmdir(files_keeper_path)
    os.mkdir(files_keeper_path)

    file_count = 0
    for folder in folders:
        folder_path = f"{folder_keeper_path}\\{folder}"
        lib = os.listdir(folder_path)
        for file in lib:
            file_count += 1
            source_file = f"{folder_path}\\{file}"
            destination_file = f"{files_keeper_path}\\{file}"

            with open(source_file, 'rb') as src:
                # Lire le contenu du fichier source
                contenu = src.read()

                # Ouvrir le fichier cible en mode écriture binaire ('wb' pour écriture binaire)
                with open(destination_file, 'wb') as dest:
                    # Écrire le contenu dans le fichier cible
                    dest.write(contenu)

    return "OK", mail_count, file_count


"""
Configuration de la fenêtre
"""
window = Tk()

window.title("Mailcuperator")
window.geometry("400x200")
window.minsize(400, 200)
window.iconbitmap("atome.ico")
window.protocol("WM_DELETE_WINDOW", on_quit)


"""
Logique window
"""


def select_frame(frame_name):
    """
    frame_name: email, mdp, recup
    """
    frame_names = ["email", "mdp", "recup"]
    if frame_name not in frame_names:
        raise Exception("Le nom de frame spécifié n'est pas correct")

    frame_email.pack_forget()
    frame_mdp_app.pack_forget()
    frame_recup.pack_forget()

    if frame_name == frame_names[0]:
        frame_email.pack()
    elif frame_name == frame_names[1]:
        frame_mdp_app.pack()
    elif frame_name == frame_names[2]:
        frame_recup.pack()


def validate_email():
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


def validate_mdp():
    user_mdp_app = user_mdp_app_value.get()
    if len(user_mdp_app) == 0:
        print("Le mot de passe ne doit pas être vide !")
        return

    select_frame("recup")


"""
Frames (pages)
"""
frame_email = Frame(window)
frame_mdp_app = Frame(window)
frame_recup = Frame(window)


"""
Elements de frame_email (page email)
"""

# label email
label_user_email = Label(frame_email, text="Email", fg="blue")
label_user_email.pack()

# entrée email
user_email_value = StringVar()
user_email_value.set("")
entry_user_email = Entry(frame_email, textvariable=user_email_value, width=30)
entry_user_email.pack()

# bouton de validation email
button_mdp_app = Button(frame_email, text="Valider", command=validate_email, fg="red")
button_mdp_app.pack()

frame_email.pack()


"""
Elements dans frame_mdp (page mdp)
"""

# label mdp
label_user_mdp_app = Label(frame_mdp_app, text="Mot de passe d'application (cliquez pour avoir "
                                               "des explications)", fg="blue")
label_user_mdp_app.bind("<Button-1>", lambda *args: webbrowser.open("https://fr.aide.yahoo.com/kb/SLN15241.html"))
label_user_mdp_app.pack()

# entrée mdp
user_mdp_app_value = StringVar()
user_mdp_app_value.set("")
entry_user_mdp_app = Entry(frame_mdp_app, textvariable=user_mdp_app_value, width=30)
entry_user_mdp_app.pack()

# bouton de validation mdp
button_mdp_app = Button(frame_mdp_app, text="Valider", command=validate_mdp, fg="red")
button_mdp_app.pack()


"""
Elements dans frame_recup (page recup)
"""

# label folder_target
label_folder_target = Label(frame_recup, text="\n"
                            "Nom du dossier où sont les mails à extraire.\n"
                            "Vous avez plusieurs dossier dans votre boîte mail:\n"
                            "Boîte de réception, Spam, et d'autres que "
                            "vous avez vous-même créés", fg="blue")
label_folder_target.pack()

# entrée folder_target
box_target_value = StringVar()
box_target_value.set("")
entry_box_target = Entry(frame_recup, textvariable=box_target_value, width=30)
entry_box_target.pack()

# label nombre de mail à traiter
label_nb_mail_to_fetch = Label(frame_recup, text="Nombre de mail à traiter en partant du plus récent "
                                                 "(0 pour tous les traiter)", fg="blue")
label_nb_mail_to_fetch.pack()

# entry nombre de mail à traiter
nb_mail_to_fetch_value = IntVar()
nb_mail_to_fetch_value.set(0)
entry_nb_mail_to_fetch = Entry(frame_recup, textvariable=nb_mail_to_fetch_value, width=30)
entry_nb_mail_to_fetch.pack()

# bouton de validation pour le téléchargement
button_download = Button(frame_recup, text="Télécharger les fichiers", command=start, fg="red")
button_download.pack()


"""
Finalization
"""
window.mainloop()
