import os

COLUMN_SEPARATOR = "|"
ROW_SEPARATOR = "\n"

class Table:
    
    def __init__(self, name, primary_key, columns):
        self.name = name
        self.primary_key = primary_key
        self.columns = columns
        self.data = []

    def _save_to_file(self):
        with open(f"{self.name}.txt", "w", encoding="utf-8") as file:
            for row in self.data:
                file.write(COLUMN_SEPARATOR.join(map(str, row)) + ROW_SEPARATOR)
    
    def load_from_file(self):
        if os.path.exists(f"{self.name}.txt"):
            with open(f"{self.name}.txt", "r", encoding="utf-8") as file:
                content = file.read().strip(ROW_SEPARATOR)
                if content:
                    self.data = [row.split(COLUMN_SEPARATOR) for row in content.split(ROW_SEPARATOR)]


    def insert(self, record):
        if len(record) != len(self.columns):
            return "Error: Record length does not match the number of columns."
        
        # Verificar si la clave primaria ya existe
        pk_value = record[self.columns.index(self.primary_key)] # Obtiene el inicio de la clave primaria
        for row in self.data:
            if row[self.columns.index(self.primary_key)] == pk_value: # Comparar si la clave primaria ya existe
                return "Error: Primary key already exists."
        
        self.data.append(record)
        self._save_to_file()
        return "Success: Record inserted."
    
    def select(self, columns=None, condition=None):
        result = []
        for row in self.data:
            if condition is None or condition(row):
                if columns is None:
                    result.append(row)
                else:
                    result.append([row[self.columns.index(col)] for col in columns])
        return result
    
    def update(self, primary_key_value, field, new_value):
        for row in self.data:
            if row[self.columns.index(self.primary_key)] == primary_key_value:
                if field not in self.columns:
                    return "Failure: Invalid field name."
                row[self.columns.index(field)] = new_value
                self._save_to_file()
                return "Success: Record updated."
        return "Failure: Primary key not found."

    def delete(self, primary_key_value):
        for row in self.data:
            if row[self.columns.index(self.primary_key)] == primary_key_value:
                self.data.remove(row)
                self._save_to_file()
                return "Success: Record deleted."
        return "Failure: Primary key not found."
