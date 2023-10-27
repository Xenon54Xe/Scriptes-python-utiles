
import os


abs_path = os.getcwd()

mdp_folder_name = "mdp_handler.txt"
mdp_crypt_folder_name = "mdp_crypt_handler.txt"

if not os.path.isfile(mdp_crypt_folder_name):
    folder = open(mdp_crypt_folder_name, "x")
    folder.close()


crypt_string = ""
with open(mdp_crypt_folder_name, "r") as crypt_folder:
    for i in crypt_folder.readlines():
        crypt_string += i
    crypt_folder.close()

print(crypt_string)
