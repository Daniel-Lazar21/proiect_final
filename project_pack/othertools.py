
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
        