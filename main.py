import os,time,datetime
from project_pack import *

myconnection = ConnectionToDatabase()
print(myconnection)
# comenzile prin sys.argv : sys.argv[2] 
             
def non_online_app():
    """Verifica in fiecare secunda daca s-au adaugat fisiere noi in directorul dat.
    La ora 20:00:00 se face calculul de ore pe ziua respectiva.
    """
    lista = os.listdir(ABSOLUTE_PATH_INTRARI)
    while True:
        changed = False
        elements_added = False
        lista_noua = os.listdir(ABSOLUTE_PATH_INTRARI)
        for element in lista_noua:
            #print(element)
            if element not in lista:
                elements_added = True
                # am luat calea absoluta a directorului intrari la care am adaugat si fisierul nou adaugat
                # apoi am apelat functia add_to_database_acces 
                file =  ABSOLUTE_PATH_INTRARI + "\\" + element
                myconnection.add_to_database_acces(file)
                # mut fisierul in directorul backup_intrari
                os.replace(file,ABSOLUTE_PATH_BACKUP_INTRARI + '\\' + element)
        if elements_added:
            changed = True
        else:
            if(len(lista_noua) < len(lista)):
                changed = True
        if changed: 
            lista = lista_noua
            print(lista)
        
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        if current_time == "21:42:10":
            myconnection.raport_ore_lucrate()
            
        time.sleep(1)
        print("mere")
        

if __name__ == '__main__':
    print(myconnection.cele_mai_comune_nume_si_prenume())
   
