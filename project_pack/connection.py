from .constants import (HOST,
                        USER,
                        PASSWORD,
                        DATABASE)
from .othertools import *
import csv ,json
import mysql.connector
from json import JSONDecodeError
import datetime

class ConnectionToDatabase():
    """Cu ajutorl acestei clase instantiem conexiunea la baza de date si modificam baza de date."""

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance
    
    def __init__(self):
        try:
            self.mydb = mysql.connector.connect(
                user = USER,
                host = HOST,
                password = PASSWORD,
                database = DATABASE
            )
            self.mycursor = self.mydb.cursor()
        except mysql.connector.errors.ProgrammingError:
            print(f"Baza de date {DATABASE} nu a fost inca creata! Reveniti dupa ce creati baza de date!")
            exit() 
    
    def execute_insert_query(self, query: str):
        self.mycursor.execute(query)
        self.mydb.commit()
        
    def execute_select_query(self, query: str):
        self.mycursor.execute(query)
        return self.mycursor.fetchall()
    
    def execute_update_query(self, query: str):
        self.mycursor.execute(query)
        self.mydb.commit()
    
    def execute_delete_query(self, query: str):
        self.mycursor.execute(query)
        self.mydb.commit()
    
    def add_to_database_acces(self ,file: str) -> str:
        """Adauga informatiile dintr-un fisier csv,txt sau json in baza de date.\\
        La final returnez un raspuns daca s-a reusit sau nu introducerea datelor"""
    
        # din stringul file se ia doar ce este inte ultimul caracter 'a'(cel din cuvantul Poarta) pana la punct 
        # de exemplu din ...\Poarta2.csv se ia doar cifra 2 si desigur se converteste la tipul int  
        
        file_type = file[file.rindex(".") + 1 : ]
        #Din stringul file se ia doar ce se afla dupa caracterul '.' adica tipul fisierului. \\
        #De exemplu din ...\Poarta2.csv se ia doar stringul 'csv'.
        try:
            gate = int(file[file.rindex('a') + 1 : file.rindex(".") ]) if file_type != "json" else ""
        except ValueError:
            return "Denumirea fisierului este incorecta!"
        
        if file_type == 'csv':
            with open(file,'r') as csv_file:
                content = csv.reader(csv_file)
                querys = [ ] 
                for index,line in enumerate(content):
                    if line[0].strip() != "":
                        if index != 0:
                            try:
                                id_persoana = int(line[0])
                                data = date_to_sql_format(line[1])
                                if line[2].strip()  in ['in','out']:
                                    sens = line[2].strip() 
                                else:
                                    raise ValueError
                                querys.append(f"insert into acces values(null,{id_persoana}, '{data}', '{line[2].strip()}', {gate})")
                            except ValueError:
                                return "Unele date din fisier nu sunt valide!"
                            except IndexError:
                                return "Fisierul are elemente lipsa!"  
                             
                for query in querys:
                    self.execute_insert_query(query)
            return "Datele au fost introduse cu succes!"
                                               
        elif file_type == 'txt':
            with open(file,'r') as txt_file:
                content = txt_file.readlines()
                querys = [ ]
                for line in content:
                    #verific ca fisierul sa nu aiba randuri goale 
                    if line.strip() != '':
                        #sterg spatiile golale de la final ,iau randurile excluzand caracterele de la final(';' si '\n') si apoi dau split dupa ','
                        line = line.replace(" ","")[:-2].split(",")
                        try:
                            id_persoana = int(line[0])
                            data = date_to_sql_format(line[1])
                            if line[2].strip()  in ['in','out']:
                                sens = line[2].strip() 
                            else:
                                raise ValueError
                            querys.append(f"insert into acces values(null,{id_persoana}, '{data}', '{line[2].strip()}', {gate})")
                        except ValueError:
                            return "Unele date din fisier nu sunt valide!"
                        except IndexError:
                            return "Fisierul are elemente lipsa!"
                        
                for query in querys: 
                    self.execute_insert_query(query)
            return "Datele au fost introduse cu succes!"        
        
        elif file_type == 'json':
            with open(file) as json_file:
                try:
                    content = json.load(json_file)
                    querys = [ ]
                    for intrare in content:
                        try:
                            id_persoana = int(intrare["idPersoana"])
                            data = date_to_sql_format(intrare['data'])
                            if intrare['sens'] in ['in','out']:
                                sens = intrare['sens'] 
                            else:
                                raise ValueError
                            id_poarta = int(intrare['idPoarta'])
                            querys.append(f"""insert into acces values(
                                            null,
                                            {id_persoana}, 
                                            '{data}', 
                                            '{sens}', 
                                            {id_poarta})""")
                        except ValueError:
                            return "Unele date din fisier nu sunt valide!"
                        except KeyError:
                            return "Fisierul are elemente lipsa!"       
                except JSONDecodeError:
                    return "Unele date din fisier nu sunt valide!"
                
                for query in querys:
                    self.execute_insert_query(query)  
            return "Datele au fost introduse cu succes!"
        
        else:
            return 'Nu am inregistrat acest tip de fisier!'   
    
    def add_to_database_persoane(self,*args):
        self.execute_insert_query(f"insert into persoane values(null,'{args[0]}','{args[1]}','{args[2]}',{args[3]},'{args[4]}')") 
    
    def raport_ore_lucrate(self):
        """Aceasta functie ne ajuta sa calculam numarul de ore lucrate de fiecare angajat si\\
        sa trimitem un mail managerului sau in cazul in care a lucrat mai putin de 8 ore."""
        ids_persoane = self.execute_select_query("select Id from persoane")
        data_de_lucru = datetime.datetime.now().strftime(f"%Y-%m-%d")

        for id_persoana in ids_persoane:
            id_persoana = id_persoana[0]
            date_persoana = self.execute_select_query(f"select * from persoane where id = {id_persoana}")[0]
            #Creez un obiect de tip Person
            this_person = Person(date_persoana[0],date_persoana[1],date_persoana[2],date_persoana[3],date_persoana[4],date_persoana[5])
            #selectez din baza de date doar data de azi
            table_today = f"select * from acces where Data like '%{data_de_lucru}%' "
            #selectez toate intrarile persoanei si le ordonez crescator dupa ora apoi selectez prima ora la care a intrat pe o poarta
            query_in = f"select * from ({table_today}) as today where Id_Persoana = {id_persoana} and Sens = 'in' order by Data ASC"
            
            persoana_first_entry = self.execute_select_query(query_in)

            #selectez toate iesirile persoanei si le ordonez crescator dupa ora apoi selectez ultima ora la care a iesit pe o poarta
            query_out = f"select * from ({table_today}) as today where Id_Persoana = {id_persoana} and Sens = 'out' order by Data DESC"
            persoana_last_exit = self.execute_select_query(query_out)
            
            #Verific ca nu cumva una dintre persoane sa nu se fi fost deloc la lucru in ziua respectiva si daca 
            #a lipsit de la lucru pur si simplu trec la urmatoarea persoana 
            if persoana_first_entry and persoana_last_exit:
    
                timp_la_lucru = str(persoana_last_exit[0][2] - persoana_first_entry[0][2])
                ore_lucrate = int(timp_la_lucru[0 : timp_la_lucru.index(":") ])
            
                if ore_lucrate < 8:
                    send_mail_chiulangiu(this_person,timp_la_lucru)  
    
    def cele_mai_comune_nume_si_prenume(self) -> dict:
        query = "select Nume from (select Nume,count(*) as Total from persoane group by Nume) as this group by Nume order by Total desc" 
        nume = self.execute_select_query(query)
        cele_mai_comune_nume = [nume[i][0] for i in range(0,3)]
        query = "select Prenume from (select Prenume,count(*) as Total from persoane group by Prenume) as this group by Prenume order by Total desc"
        prenume = self.execute_select_query(query)
        cele_mai_comune_prenume = [prenume[i][0] for i in range(0,3)]
        
        return {'Nume':cele_mai_comune_nume ,
                'Prenume': cele_mai_comune_prenume}
 
    def __repr__(self) :
        return f"Sunt o conexiune la baza de date {DATABASE} la adresa {hex(id(self))} !"

