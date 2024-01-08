import smtplib ,ssl 
from smtplib import SMTPAuthenticationError as LoginError
from .constants import (sender,
                        mail_password,
                        receiver)

def file_type(file : str) -> str:
    """Din stringul file se ia doar ce se afla dupa caracterul '.' adica tipul fisierului. \\
        De exemplu din ...\Poarta2.csv se ia doar stringul 'csv'."""
    return file[file.index(".") + 1 : ]

def date_to_sql_format(date: str) -> str:
    """Transforma data din fisiere sub o forma accepatata de sql."""
    sql_date = date.replace("T"," ")
    sql_date = sql_date[:-5]     
    return sql_date

class Person():
    def __init__(self, id:int, nume:str, prenume:str, companie:str, id_manager:int ,Email:str):
        self.id = id
        self.nume = nume
        self.prenume = prenume
        self.companie = companie
        self.id_manager = id_manager
        self.Email = Email
        
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

