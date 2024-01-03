import os,time,csv,datetime
import smtplib ,ssl 
from project_pack import *

from smtplib import SMTPAuthenticationError as LoginError

myconnection = ConnectionToDatabase()

# comenzile prin sys.argv : sys.argv[2] 
             
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

def raport_ore_lucrate(connection : ConnectionToDatabase):
    """Aceasta functie ne ajuta sa calculam numarul de ore lucrate de fiecare angajat si\\
    sa trimitem un mail managerului sau in cazul in care a lucrat mai putin de 8 ore."""
    ids_persoane = connection.execute_select_query("select Id from persoane")
    data_de_lucru = '2023-05-21'#datetime.datetime.now().strftime("%Y-%m-%d")

    for id_persoana in ids_persoane:
        id_persoana = id_persoana[0]
        date_persoana = myconnection.execute_select_query(f"select * from persoane where id = {id_persoana}")[0]
        #Creez un obiect de tip Person
        this_person = Person(date_persoana[0],date_persoana[1],date_persoana[2],date_persoana[3],date_persoana[4],date_persoana[5])
        #selectez din baza de date doar data de azi
        table_today = f"select * from acces where Data like '%{data_de_lucru}%' "
        #selectez toate intrarile persoanei si le ordonez crescator dupa ora apoi selectez prima ora la care a intrat pe o poarta
        query_in = f"select * from ({table_today}) as today where Id_Persoana = {id_persoana} and Sens = 'in' order by Data ASC"
        persoana_first_entry = myconnection.execute_select_query(query_in)[0][2]
        #selectez toate iesirile persoanei si le ordonez crescator dupa ora apoi selectez ultima ora la care a iesit pe o poarta
        query_out = f"select * from ({table_today}) as today where Id_Persoana = {id_persoana} and Sens = 'out' order by Data ASC"
        persoana_last_exit = myconnection.execute_select_query(query_out)[-1][2]
        
        timp_la_lucru = str(persoana_last_exit - persoana_first_entry)
        ore_lucrate = int(timp_la_lucru[0 : timp_la_lucru.index(":") ])
    
        if ore_lucrate < 8:
            send_mail(this_person,ore_lucrate)
            

def send_mail(person : Person ,numar_ore : int):
    subject = 'Raport chiulangiu'
    body = f'Angajatul {person.nume} {person.prenume} cu id-ul {person.id} apartinand de managerul cu id-ul {person.id_manager} a lucrat doar {numar_ore} ore!!!'

    message = f"""
            From: {sender}
            To: {receiver}
            Subject: {subject}\n
            {body}
            """

    context = ssl.create_default_context()
    server = smtplib.SMTP("smtp.gmail.com", 587)

    server.starttls(context = context)

    try:
        server.login(sender, mail_password)
        print("Logged in...")
        server.sendmail(sender, receiver, message)
        print("Mail sent successfully!")
        server.quit()
    except LoginError as e:
        print(e)
        print("Ceva nu a mers bine")
         
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
        if current_time == "21:42:10":
            raport_ore_lucrate(myconnection)
        
        onilne_app_flask_run()
            
        time.sleep(1)
        print("mere")

if __name__ == '__main__':
    update()
   
