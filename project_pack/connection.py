from .constants import (HOST,
                        USER,
                        PASSWORD,
                        DATABASE)
from .othertools import *
import csv ,json
import mysql.connector

class ConnectionToDatabase():
    """Cu ajutorl acestei clase instantiem conexiunea la baza de date si modificam baza de date."""

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
    
    def execute_insert_query(self, query: str):
        self.mycursor.execute(query)
        self.mydb.commit()
        
    def execute_select_query(self, query: str):
        self.mycursor.execute(query)
        return self.mycursor.fetchall()
    
    def execute_update_query(self, query: str):
        self.execute_insert_query(query)
    
    def add_to_database_acces(self ,file: str):
        """Adauga informatiile dintr-un fisier csv sau txt in baza de date."""
    
        # din stringul file se ia doar ce este inte ultimul caracter 'a'(cel din cuvantul Poarta) pana la punct 
        # de exemplu din ...\Poarta2.csv se ia doar cifra 2 si desigur se converteste la tipul int  
        
        gate = int(file[file.rindex('a') + 1 : file.index('.') ])
        
        if file_type(file) == 'csv':
            with open(file,'r') as csv_file:
                content = csv.reader(csv_file)
                for index,line in enumerate(content):
                    if line[0].strip() != "":
                        #adaug in baza de date inforamtiile si de la Sens sterg spatiile goale pentu a nu avea probleme mai tarziu 🢃
                        if index != 0:
                            new_query = f"insert into acces values(null,{line[0]}, '{date_to_sql_format(line[1])}', '{line[2].strip()}', {gate})"
                            self.execute_insert_query(new_query)                     
        elif file_type(file) == 'txt':
            with open(file,'r') as txt_file:
                content = txt_file.readlines()
                for line in content:
                    #verific ca fisierul sa nu aiba randuri goale 
                    if line.strip() != '':
                        #sterg spatiile golale de la final ,iau randurile excluzand caracterele de la final(';' si '\n') si apoi dau split dupa ','
                        line = line.replace(" ","")[:-2].split(",")
                        #adaug in baza de date informatille
                        new_query = f"insert into acces values(null,{line[0]}, '{date_to_sql_format(line[1])}', '{line[2]}', {gate})"
                        self.execute_insert_query(new_query)
        elif file_type(file) == 'json':
            with open(file) as json_file:
                content = json.load(json_file)
                #pot face si varianta in care apar mai multe dictionare in json dar pe moment las asa!
                new_query = f"""insert into acces values(
                    null,
                    {content['idPersoana']}, 
                    '{date_to_sql_format(content['data'])}', 
                    '{content['sens']}', 
                    {content['idPoarta']})"""
                self.execute_insert_query(new_query)
        else:
            print('Nu am inregistrat acest tip de fisier')   
    
    def add_to_database_persoane(self,*args):
        self.execute_insert_query(f"insert into persoane values(null,'{args[0]}','{args[1]}','{args[2]}',{args[3]},'{args[4]}')") 
    
    def raport_ore_lucrate(self):
        """Aceasta functie ne ajuta sa calculam numarul de ore lucrate de fiecare angajat si\\
        sa trimitem un mail managerului sau in cazul in care a lucrat mai putin de 8 ore."""
        ids_persoane = self.execute_select_query("select Id from persoane")
        data_de_lucru = '2023-05-21'#datetime.datetime.now().strftime("%Y-%m-%d")

        for id_persoana in ids_persoane:
            id_persoana = id_persoana[0]
            date_persoana = self.execute_select_query(f"select * from persoane where id = {id_persoana}")[0]
            #Creez un obiect de tip Person
            this_person = Person(date_persoana[0],date_persoana[1],date_persoana[2],date_persoana[3],date_persoana[4],date_persoana[5])
            #selectez din baza de date doar data de azi
            table_today = f"select * from acces where Data like '%{data_de_lucru}%' "
            #selectez toate intrarile persoanei si le ordonez crescator dupa ora apoi selectez prima ora la care a intrat pe o poarta
            query_in = f"select * from ({table_today}) as today where Id_Persoana = {id_persoana} and Sens = 'in' order by Data ASC"
            persoana_first_entry = self.execute_select_query(query_in)[0][2]
            #selectez toate iesirile persoanei si le ordonez crescator dupa ora apoi selectez ultima ora la care a iesit pe o poarta
            query_out = f"select * from ({table_today}) as today where Id_Persoana = {id_persoana} and Sens = 'out' order by Data ASC"
            persoana_last_exit = self.execute_select_query(query_out)[-1][2]
            
            timp_la_lucru = str(persoana_last_exit - persoana_first_entry)
            ore_lucrate = int(timp_la_lucru[0 : timp_la_lucru.index(":") ])
        
            if ore_lucrate < 8:
                send_mail(this_person,ore_lucrate)  
    
    def cele_mai_comune_nume_si_prenume(self):
        query = "select Nume from (select Nume,count(*) as Total from persoane group by Nume) as this group by Nume order by Total desc" 
        cele_mai_comune_nume = [self.execute_select_query(query)[i][0] for i in range(0,3)]
        query = "select Prenume from (select Prenume,count(*) as Total from persoane group by Prenume) as this group by Prenume order by Total desc"
        cele_mai_comune_prenume = [self.execute_select_query(query)[i][0] for i in range(0,3)]
        
        return {'Nume':cele_mai_comune_nume ,
                'Prenume': cele_mai_comune_prenume}
    #def   
    def __repr__(self) :
        return f"Sunt o conexiune la baza de date {DATABASE} la adresa {hex(id(self))} !"

