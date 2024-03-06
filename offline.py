import os,time,datetime
from project_pack import (ConnectionToDatabase,
                          ABSOLUTE_PATH_INTRARI,
                          ABSOLUTE_PATH_BACKUP_INTRARI,
                          ORA_UPDATE)

myconnection = ConnectionToDatabase()
print(myconnection)

def offline_app(myconnection:ConnectionToDatabase) -> None:
    """Verifica in fiecare secunda daca s-au adaugat fisiere noi in directorul dat.
    La ora 20:00:00 se face calculul de ore pe ziua respectiva.
    """
    lista = os.listdir(ABSOLUTE_PATH_INTRARI)
    while True:
        changed = False
        elements_added = False
        lista_noua = os.listdir(ABSOLUTE_PATH_INTRARI)
        for element in lista_noua:

            if element not in lista:
                elements_added = True
                # am luat calea absoluta a directorului intrari la care am adaugat si fisierul nou adaugat
                # apoi am apelat functia add_to_database_acces 
                file =  ABSOLUTE_PATH_INTRARI + "\\" + element
                #verific daca pot introduce datele cu succes in baza de date 
                respone = myconnection.add_to_database_acces(file)
                new_name_for_file = element[:element.index(".")] + "_backup" + element[element.index("."):]
                if respone == "Datele au fost introduse cu succes!":
                # mut fisierul in directorul backup_intrari
                    os.replace(file,ABSOLUTE_PATH_BACKUP_INTRARI + '\\' + new_name_for_file )

        if elements_added:
            changed = True
        else:
            if(len(lista_noua) < len(lista)):
                changed = True
        if changed: 
            lista = lista_noua
            print(lista)
        
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        if current_time == ORA_UPDATE:
            myconnection.raport_ore_lucrate()
            
        time.sleep(1)
        print("checking...")

if __name__ == '__main__':
    offline_app(myconnection)
