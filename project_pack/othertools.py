import smtplib ,ssl 
from smtplib import SMTPAuthenticationError as LoginError
from .constants import (sender,
                        mail_password,
                        receiver)

def date_to_sql_format(date: str) -> str:
    """Transforma data din fisiere sub o forma accepatata de sql."""
    sql_date = date.replace("T"," ")
    return sql_date[:-5]

class Person(): 
    def __init__(self, id:int, nume:str, prenume:str, companie:str, id_manager:int ,Email:str) -> None:
        self.id = id
        self.nume = nume
        self.prenume = prenume
        self.companie = companie
        self.id_manager = id_manager
        self.Email = Email
     
def send_mail_chiulangiu(person : Person ,numar_ore : int) -> None:
    subject = 'Raport chiulangiu'
    body = f"""Angajatul {person.nume} {person.prenume} cu id-ul {person.id} apartinand 
    de managerul cu id-ul {person.id_manager} a lucrat doar {numar_ore} !!!"""

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

def send_mail_log_in(cont :str) -> None:
    subject = 'Conectare'
    body = f'Adminul {cont} s-a conectat la site!'

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