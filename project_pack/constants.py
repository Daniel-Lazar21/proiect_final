import os
# informatiile bazei de date 

# ora la care se face update-ul in formatul( "ora:minutul:secunda" ) ex : "20:00:00"
"🢃"
ORA_UPDATE = "20:00:00"
"🢁"

# numele user-ului
"🢃"
USER = "root"
"🢁"

# parola user-ului
if os.getlogin() == 'danut' :   
    with open(r'C:\Users\danut\Desktop\pythonProject1\psw.txt', 'r') as pswFile:
        PASSWORD = pswFile.readline()
else:
    #❗️ Aici introduci tu parola ta❗️
    
    "🢃"
    PASSWORD = "scrie_parola_ta" 
    "🢁"

# host-ul userului
"🢃"
HOST = "localhost"
"🢁"

# baza de date cu care se lucreaza 
"🢃"
DATABASE = "proiect_final"
"🢁"

# calea absoluta a directorului din care se iau fisierele csv sau txt si proiectul in general
"🢃"
if os.getlogin() == 'danut':
    ABSOLUTE_PATH_PROIECT = r"C:\Users\danut\Desktop\pythonProject1"
else:
   "❗️";  ABSOLUTE_PATH_PROIECT = r"pune_aici_calea_unde_se_afla_fisierul_cu_proiectul";  "❗️"
    
ABSOLUTE_PATH_INTRARI = ABSOLUTE_PATH_PROIECT + r"\proiect_final\intrari"
"🢁"

# calea de backup se deduce automat din calea de intrari
# adica iau calea de intrari pana la ultima aparitie a caracterului '\' si adaug 'backup_intrari' la acel string 
ABSOLUTE_PATH_BACKUP_INTRARI = ABSOLUTE_PATH_INTRARI[ : ABSOLUTE_PATH_INTRARI.rindex('\\') + 1] + 'backup_intrari'
# voi lua adresele de mail si cheia de acces din fisierul gmails_project.txt
with open(ABSOLUTE_PATH_PROIECT+"\proiect_final\gmails_project.txt",'r') as mails:
    content = mails.readlines()
    sender, mail_password, receiver = (content[i].replace("\n",'') for i in range(0,3))