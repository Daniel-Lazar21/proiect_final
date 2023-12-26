from constants import * 
import mysql.connector
import os,time,sys,csv,datetime

class ConnectionToDatabase():
    """Cu ajutorl acestei clase instantiem conexiunea cu baza de date"""

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

class Person():
    def __init__(self,nume,prenume,companie,id_manager,Email):
        self.nume = nume
        self.prenume = prenume
        self.companie = companie
        self.id_manager = id_manager
        self.Email = Email
     
    
myconnection = ConnectionToDatabase()

# comenzile prin sys.argv : sys.argv[2] 
 
def date_to_sql_format(date: str) -> str:
    """Transforma data din fisiere sub o forma accepatata de sql."""
    sql_date = date.replace("T"," ")
    sql_date = sql_date[:-5]     
    return sql_date
            
def add_to_database(file: str, connection: ConnectionToDatabase):
    """Adauga informatiile dintr-un fisier csv sau txt in baza de date."""
    # din stringul file se ia doar ce se afla dupa caracterul'.' adica tipul fisierului 
    # de exemplu din ...\Poarta2.csv se ia doar stringul 'csv'
    file_type = file[file.index(".") + 1 : ]
    # din stringul file se ia doar ce este inte ultimul caracter 'a'(cel dein cuvantul Poarta) pana la punct 
    # de exemplu din ...\Poarta2.csv se ia doar cifra 2 si desigur se converteste la tipul int  
    gate = int(file[file.rindex('a') + 1 : file.index('.') ])
    
    if file_type == 'csv':
        with open(file,'r') as csv_file:
            content = csv.reader(csv_file)
            for index,line in enumerate(content):
                if line[0].strip() != "":
                    #adaug in baza de date inforamtiile si de la Sens sterg spatiile goale pentu a nu avea probleme mai tarziu 🢃
                    if index != 0:
                        new_query = f"insert into acces values(null,{line[0]}, '{date_to_sql_format(line[1])}', '{line[2].strip()}', {gate})"
                        connection.execute_insert_query(new_query)                     
    elif file_type == 'txt':
        with open(file,'r') as txt_file:
            content = txt_file.readlines()
            for line in content:
                #verific ca fisierul sa nu aiba randuri goale 
                if line.strip() != '':
                    #sterg spatiile golale de la final ,iau randurile excluzand caracterele de la final(';' si '\n') si apoi dau split dupa ','
                    line = line.replace(" ","")[:-2].split(",")
                    #adaug in baza de date informatille
                    new_query = f"insert into acces values(null,{line[0]}, '{date_to_sql_format(line[1])}', '{line[2]}', {gate})"
                    connection.execute_insert_query(new_query)

def calcul_ore_lucrate(connection : ConnectionToDatabase):
    ids_persoane = connection.execute_select_query("select Id from persoane")
    data_de_lucru = '2023-05-21'#datetime.datetime.now().strftime("%Y-%m-%d")
    print(data_de_lucru)
    print(ids_persoane)
    for id_persoana in ids_persoane:
        id_persoana = id_persoana[0]
        date_persoana = myconnection.execute_select_query(f"select * from persoane where id = {id_persoana}")[0]
        print(date_persoana)
        #this_person = Person()
        table_today = f"select * from acces where Data like '%{data_de_lucru}%' "
        query_in = f"select * from ({table_today}) as today where Id_Persoana = {id_persoana} and Sens = 'in' "
        persoana_first_entry = myconnection.execute_select_query(query_in)[0][2]
        query_out = f"select * from ({table_today}) as today where Id_Persoana = {id_persoana} and Sens = 'out' "
        persoana_last_exit = myconnection.execute_select_query(query_out)[-1][2]
        
        timp_la_lucru = str(persoana_last_exit - persoana_first_entry)
        print(timp_la_lucru)
        ore_lucrate = int(timp_la_lucru[0 : timp_la_lucru.index(":") ])
    
        
        if ore_lucrate < 8:
            print("CHIULANGIU")
        
    
  
def update():
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
                # am luat calea absouta a directorului intrari la care am adaugat si fisierul nou adaugat
                # apoi am apelat functia add_to_database 
                file =  ABSOLUTE_PATH_INTRARI + "\\" + element
                add_to_database(file, myconnection)
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
        time.sleep(1)
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        if current_time == ORA_UPDATE:
            calcul_ore_lucrate(myconnection)
            

        time.sleep(1)
# add_to_database("proiect_final\intrari\Poarta1.txt",myconnection)
# add_to_database("proiect_final\intrari\Poarta2.csv",myconnection)

# print(date_to_sql_format('2023-05-22T14:23:42.153Z'))
if __name__ == '__main__':
    calcul_ore_lucrate(myconnection)      

