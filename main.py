from constants import * 
import mysql.connector
import os,time,sys,csv

class ConnectionToDatabase():

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance
    
    def __init__(self):
        self.mydb = mysql.connector.connect(
            user = USER,
            host = HOST,
            password = PASSWORD,
            database = DATABASE
        )
        self.mycursor = self.mydb.cursor()
    
    def execute_insert_query(self, query):
        self.mycursor.execute(query)
        self.mydb.commit()
        
    def execute_select_query(self, query):
        self.mycursor.execute(query)
        return self.mycursor.fetchall()
    
    def execute_update_query(self, query):
        self.execute_insert_query(query)
    
    def __repr__(self) :
        return f"Sunt o conexiune la baza de date {DATABASE} la adresa {hex(id(self))} !"

myconnection = ConnectionToDatabase()

PATH_TO_DIR = "proiect_final\intrari"#sys.argv[2] 

 
def date_to_sql_format(date :str) -> str:
    """Transforma data din fisiere sub o forma accepatata de sql."""
    sql_date = ''
    for char in date:
        if char == "T":
            sql_date += " "
        elif char == "Z":
            sql_date += ""
        else :
            sql_date += char       
    return sql_date[:-4]
            
def add_to_database(file: str):
    """Adauga informatiile dintr-un fisier csv sau txt in baza de date."""
    file_type = file[file.index(".") + 1 :]
    gate = int(file[file.rindex('a') + 1 : file.index('.') ])
    
    if file_type == 'csv':
        with open(file,'r') as csv_file:
            content = csv.reader(csv_file)
            for index,line in enumerate(content):
                if line[0].strip() != "":
                    print(line)
                    #adaug in baza de date inforamtiile si de la Sens sterg spatiile goale pentu a nu avea probleme mai tarziu
                    if index != 0:
                        new_query = f"insert into acces values(null,{line[0]}, '{date_to_sql_format(line[1])}', '{line[2].strip()}', {gate})"
                        myconnection.execute_insert_query(new_query)                     
    elif file_type == 'txt':
        with open(file,'r') as txt_file:
            content = txt_file.readlines()
            for line in content:
                #verific ca fisierul sa nu aiba randuri goale 
                if line.strip() != '':
                    #sterg spatiile golale de la final ,iau randurile excluzand caracterele de la final(';' si '\n') si apoi dau split dupa ','
                    line = line.replace(" ","")[:-2].split(",")
                    #adaug in baza de date informatille
                    print(line)
                    new_query = f"insert into acces values(null,{line[0]}, '{date_to_sql_format(line[1])}', '{line[2]}', {gate})"
                    myconnection.execute_insert_query(new_query)
    
    
    
def check_for_new_files():
    """Verifica in fiecare secunda daca s-au adaugat fisiere noi in directorul dat"""
 
    lista = os.listdir(PATH_TO_DIR)
    while True:
        changed = False
        elements_added = False
        lista_noua = os.listdir(PATH_TO_DIR)
        for element in lista_noua:
            if element not in lista:
                elements_added = True
                #print("adaug")
                break
        if elements_added:
            changed = True
            print("adaugat")
        else:
            if(len(lista_noua) < len(lista)):
                #print("sters")
                changed = True
        if changed: 
            #print(lista_noua)
            lista = lista_noua
        time.sleep(1)
'2023-05-22T14:23:42.153Z'
add_to_database("proiect_final\intrari\Poarta1.txt")
add_to_database("proiect_final\intrari\Poarta2.csv")

#print(date_to_sql_format('2023-05-22T14:23:42.153Z'))
# if __name__ == '__main__':
#     check_for_new_files()      

