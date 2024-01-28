"""
Objective: Make a little database with crypt data and with a password
Creator: XenonEGG

using: python 3.6
encoding: utf-8
"""

import os
import data_handler as dh
import tkinter as tk

_data_h = dh.data_handler("crypt.txt")
_info_file_name = "information.txt"
_current_password = ""

_bg_color = "#0061ff"

_abs_path = os.path.abspath("")
_info_file_path = f"{_abs_path}\\{_info_file_name}"


def new_account():
    password = connection_mdp_var_read.get()
    connection_mdp_var_read.set("")

    _data_h.add_new_user(password)
    _data_h.update()

    connection_new_user_var_write.set("Compte créé !")


def connect():
    global _current_password

    _current_password = connection_mdp_var_read.get()
    connection_mdp_var_read.set("")
    user_data = _data_h.get_user_data(_current_password)

    with open(_info_file_name, "w", encoding="utf-8") as file:
        file.write(user_data)
        file.close()

    account_infos_var_write.set(f"Un fichier '{_info_file_name}' vient d'être créé\n"
                                "Vous pouvez modifier son contenu\n"
                                "Avant de vous déconnecter faites 'sauvegarder'")

    connection_frame.pack_forget()
    account_frame.pack(expand=1)


def disconnect():
    global _current_password
    _current_password = ""

    if os.path.exists(_info_file_path):
        os.remove(_info_file_path)

    connection_new_user_var_write.set("Vous n'avez pas de compte ?")

    account_frame.pack_forget()
    connection_frame.pack(expand=1)


def save():
    user_data = ""

    with open(_info_file_name, "r", encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            user_data += line
        file.close()

    _data_h.set_user_data(user_data, _current_password)
    _data_h.update()

    account_infos_var_write.set("Sauvegardé !")


def on_closing():
    if os.path.exists(_info_file_path):
        os.remove(_info_file_path)
    window.quit()


"""
Création interface tkinter
"""
window = tk.Tk()

window.title("Password Handler")
window.geometry("360x280")
window.minsize(360, 280)
window.config(background=_bg_color)
window.iconbitmap("atome.ico")
window.protocol("WM_DELETE_WINDOW", on_closing)

"""
Création de la page de connection
"""
# frame.pack_forget to hide
connection_frame = tk.Frame(window, background=_bg_color)

# création button titre
connection_title_button = tk.Button(connection_frame, text="Connection", font=("courrier", 30),
                                    fg="white", bg=_bg_color, command=connect)
connection_title_button.pack()

# création label password
connection_mdp_label = tk.Label(connection_frame, text="Mot de passe", font=("courrier", 15),
                                fg="white", bg=_bg_color)
connection_mdp_label.pack()

# création entrée password
connection_mdp_var_read = tk.StringVar()
connection_mdp_entry = tk.Entry(connection_frame, textvariable=connection_mdp_var_read,
                                fg="white", bg=_bg_color)
connection_mdp_entry.pack()

# création label nouveau compte
connection_new_user_var_write = tk.StringVar()
connection_new_user_var_write.set("Vous n'avez pas de compte ?")
connection_new_user_label = tk.Label(connection_frame, textvariable=connection_new_user_var_write,
                                     bg=_bg_color, fg="#7ffe21", font=("courrier", 10))
connection_new_user_label.pack()

# création du button new_user
connection_new_user_button = tk.Button(connection_frame, text="Nouveau compte", bg=_bg_color, fg="white",
                                       font=("courrier", 10),
                                       command=new_account)
connection_new_user_button.pack()


"""
Création de la page de sauvegarde
"""
account_frame = tk.Frame(window, background=_bg_color)

# création button titre
account_save_button = tk.Button(account_frame, text="Sauvegarder", font=("courrier", 20),
                                fg="white", bg=_bg_color, command=save)
account_save_button.pack()

# création label informations
account_infos_var_write = tk.StringVar()
account_infos_var_write.set(f"Un fichier '{_info_file_name}' vient d'être créé\n"
                            "Vous pouvez modifier son contenu\n"
                            "Avant de vous déconnecter faites 'sauvegarder'")
account_infos_label = tk.Label(account_frame, textvariable=account_infos_var_write,
                               bg=_bg_color, font=("courrier", 10), fg="#7ffe21")

account_infos_label.pack()

# création button déconnexion
account_disconnect_button = tk.Button(account_frame, text="Se déconnecter", font=("courrier", 15),
                                      fg="white", bg=_bg_color, command=disconnect)
account_disconnect_button.pack()

"""
Finalisation
"""
connection_frame.pack(expand=1)
account_frame.pack_forget()
window.mainloop()
