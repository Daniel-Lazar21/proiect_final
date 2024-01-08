from flask import Flask, render_template, request 
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

myconnection = ConnectionToDatabase()
print(myconnection)
app = Flask(__name__)

#am creat o functie cu ajutorul careia pot extrage date dintr un formular 
def extract(html_var: str ,var_type = "") -> str:
   if var_type =="file":
      return request.files[html_var] if var_type =="file" else request.form[html_var]
  
@app.route('/')
def home():
   return render_template('index.html')

@app.route('/', methods=["GET", "POST"])     
def get_information():
   empty_value = False
   
   if request.method == "POST":
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
      else:
         print(info)
         
   if not empty_value: 
      myconnection.add_to_database_persoane(nume ,prenume ,companie ,id_manager ,email)        
      empty_value = not empty_value

   #aici iau continutul fisierului introdus in formular si creez un fisier in directorul backup intrari in care 
   #pun informatiile din fisierul introdus in formlular.Codul e conceput in asa fel incat fisierul se va suprascrie
   #de fiecare data
   try :
      new_file_content = json.load(sent_file)
      new_file = ABSOLUTE_PATH_BACKUP_INTRARI +"\\"+ "Poarta3.json"
      with open(new_file,'w') as online_file:
         json.dump(new_file_content,online_file)
      
      myconnection.add_to_database_acces(new_file)
   except JSONDecodeError:
      print("Ceva nu a mers bine")
   
   return home()
   
def onilne_flask_app():
   app.run(debug = True)

onilne_flask_app() 
# contionua cu requesturile pe flask si fa cumva sa bagi asta la tine in aplicatie ca o sa fie nevoie 