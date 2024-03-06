from flask import Flask, render_template, request ,redirect
from sys import path
from json import JSONDecodeError
#DE TINUT MINTE !!! daca nu poti importa pachete e posibil ca directorul in care lucrezi sa nu recunoasca path-ul directorului in care se afla
# pachetul in cazul meu "proiect_final"!!!
#Ce se intampla la linia urmatoare si de ce am facut asa?
path.append('c:\\Users\\danut\\Desktop\\pythonProject1\\proiect_final\\')
#raspuns : practic ce se intampla aici este factul ca eu nu as putea importa din pachetul project_pack deoarece el se afla in directorul
#"proiect_final" care nu este recunoscut de sys(Terminal) iar eu ce fac adaug path-ul ca si argument in sys 
from project_pack.constants import ABSOLUTE_PATH_BACKUP_INTRARI
from project_pack.connection import *
from project_pack.othertools import send_mail_log_in

myconnection = ConnectionToDatabase()
print(myconnection)
app = Flask(__name__)

#am creat o functie cu ajutorul careia pot extrage date dintr un formular 
def extract(html_var: str ,var_type = "") -> str:
   return request.files[html_var] if var_type =="file" else request.form[html_var]
   
def get_statistics_as_dict(connection:ConnectionToDatabase):
   return connection.cele_mai_comune_nume_si_prenume()
   #se face ca dictionar tot ce tine de statistici

@app.route('/',methods=['GET','POST'])
def login():
   admins_info = myconnection.execute_select_query("Select * from admins")
   info = " "
   if request.method == "POST":
      log_mail = extract('login_mail')
      log_psw = extract('login_psw')
      for admin in admins_info:
         if log_mail != admin[1] or log_psw != admin[2]:
            info = "Mail or password incorrect!"
         else:
            send_mail_log_in(admin[1])
            return redirect('/stats')

   return render_template('login_user.html',my_info = info)

@app.route('/stats')
def home(message=''):
   _stats_ = get_statistics_as_dict(myconnection)
   return render_template('index.html',stats = _stats_,my_message = message)

@app.route('/stats', methods=["POST"])     
def get_information():
   empty_value = False
   message = ''

   print(request.form)
   nume = extract('Nume')
   prenume = extract('Prenume')
   companie = extract('Companie')
   try:
      id_manager = int(extract('Id_Manager'))
   except (ValueError,TypeError):
      id_manager = extract('Id_Manager')
       
   email = extract('Email')
   sent_file = extract('Fisier','file')
   
   #verific daca in formular s-au trimis toate datele in mod corect altfel nu le ia in calcul   
   for info in (nume ,prenume ,companie ,id_manager ,email):
      if str(info).strip() =='' or info == None:
         empty_value = True

   if not sent_file:   
      if not empty_value: 
         myconnection.add_to_database_persoane(nume ,prenume ,companie ,id_manager ,email)        
         message = "Datele au fost introduse cu succes!"
      else:
         message = 'Va rog completati toate campurile!'
   else:
      #aici iau continutul fisierului introdus in formular si creez un fisier in directorul backup intrari in care 
      #pun informatiile din fisierul introdus in formlular.Codul e conceput in asa fel incat fisierul se va suprascrie
      #de fiecare data
      try :
         new_file_content = json.load(sent_file)
         new_file = ABSOLUTE_PATH_BACKUP_INTRARI +"\\"+ "Poarta3_backup.json"
         with open(new_file,'w') as online_file:
            json.dump(new_file_content,online_file)
         
         message = myconnection.add_to_database_acces(new_file)
      except UnicodeDecodeError:
         message = "Formatul fisierului nu este acceptat"
      except JSONDecodeError:
         message = "Formatul fisierului nu este corect!"
      
   
   return home(message)

if __name__ == "__main__":
   app.run(debug = True)
