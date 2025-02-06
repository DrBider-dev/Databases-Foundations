import os
import pickle

# Símbolos no comunes para separar columnas y filas
COLUMN_SEPARATOR = "|"
ROW_SEPARATOR = "¬"

class Table:
    def __init__(self, name, primary_key, columns):
        self.name = name
        self.primary_key = primary_key
        self.columns = columns
        self.data = []

    def insert(self, record):
        if len(record) != len(self.columns):
            return "Failure: Incorrect number of fields."
        
        # Verificar si la clave primaria ya existe
        pk_value = record[self.columns.index(self.primary_key)]
        for row in self.data:
            if row[self.columns.index(self.primary_key)] == pk_value:
                return "Failure: Primary key already exists."
        
        self.data.append(record)
        self._save_to_file()
        return "Success: Record inserted."

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

    def select(self, columns=None, condition=None):
        result = []
        for row in self.data:
            if condition is None or condition(row):
                if columns is None:
                    result.append(row)
                else:
                    result.append([row[self.columns.index(col)] for col in columns])
        return result

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

class Database:
    def __init__(self, name):
        self.name = name
        self.tables = {}
        self.metadata_file = f"{name}_metadata.pkl"
        self._load_metadata()

    def create_table(self, table_name, primary_key, columns):
        if table_name in self.tables:
            return "Failure: Table already exists."
        self.tables[table_name] = Table(table_name, primary_key, columns)
        self._save_metadata()
        return "Success: Table created."

    def _save_metadata(self):
        metadata = {table_name: (table.primary_key, table.columns) for table_name, table in self.tables.items()}
        with open(self.metadata_file, "wb") as file:
            pickle.dump(metadata, file)

    def _load_metadata(self):
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, "rb") as file:
                metadata = pickle.load(file)
                for table_name, (primary_key, columns) in metadata.items():
                    self.tables[table_name] = Table(table_name, primary_key, columns)
                    self.tables[table_name].load_from_file()

    def execute_query(self, query):
        if query.strip().upper() == "EXIT":
            return "Exiting..."
        
        parts = query.split()
        operation = parts[0].upper()
        
        if operation == "INSERT":
            table_name = parts[1]
            record = parts[2].split(",")
            return self.tables[table_name].insert(record)
        
        elif operation == "UPDATE":
            table_name = parts[1]
            primary_key_value = parts[2]
            field = parts[3]
            new_value = parts[4]
            return self.tables[table_name].update(primary_key_value, field, new_value)
        
        elif operation == "DELETE":
            table_name = parts[1]
            primary_key_value = parts[2]
            return self.tables[table_name].delete(primary_key_value)
        
        elif operation == "SELECT":
            table_name = parts[1]
            columns = parts[2].split(",") if parts[2] != "*" else None
            condition = None  # Aquí podrías implementar una condición más compleja
            return self.tables[table_name].select(columns, condition)
        
        else:
            return "Failure: Invalid query."

# Ejemplo de uso
db = Database("MyDatabase")
print(db.create_table("Users", "id", ["id", "name", "email"]))
print(db.execute_query("INSERT Users 1,John,john@example.com"))
print(db.execute_query("SELECT Users *"))