from .constants import *
import mysql.connector

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
