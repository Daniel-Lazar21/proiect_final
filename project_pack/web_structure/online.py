from flask import Flask, render_template, request
from sys import path

#DE TINUT MINTE !!! daca nu poti importa pachete e posibil ca directorul in care lucrezi sa nu recunoasca path-ul directorului in care se afla
# pachetul in cazul meu "proiect_final"!!!
#Ce se intampla la linia urmatoare si de ce am facut asa?
path.append('c:\\Users\\danut\\Desktop\\pythonProject1\\proiect_final\\')
#raspuns : practic ce se intampla aici este factul ca eu nu as putea importa din pachetul project_pack deoarece el se afla in directorul
#"proiect_final" care nu este recunoscut de sys(Terminal) iar eu ce fac adaug path-ul ca si argument in sys 

from project_pack.connection import *

myconnection = ConnectionToDatabase()

app = Flask(__name__)

#myconnection = connection.ConnectionToDatabase()

def extract(html_var: str) -> str:
   return request.form[html_var]

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/', methods=["GET", "POST"])     
def get_information():
   if request.method == "POST":
      nume = extract('Nume')
      prenume = extract('Prenume')
      companie = extract('Companie')
      id_manager = int(extract('Id_Manager'))
      email = extract('Email')
      json_file = extract('Fisier')
            
   myconnection.execute_insert_query(f"insert into persoane values(null,'{nume}','{prenume}','{companie}',{id_manager},'{email}')")

   return home()
   
def onilne_app_flask_run():
   app.run(debug = True)
   
# contionua cu requesturile pe flask si fa cumva sa bagi asta la tine in aplicatie ca o sa fie nevoie 