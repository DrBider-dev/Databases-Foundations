import os


COLUMN_SEPARATOR = " | "
ROW_SEPARATOR = "\n"

class Table:
    def __init__(self,db_path, name, primary_key, columns):
        self.db_path = db_path
        self.name = name
        self.primary_key = primary_key
        self.columns = columns
        self.data = []
        self.file_path = f"{self.db_path}/{self.name}.txt"

    def _save_to_file(self):
        with open(self.file_path, "w", encoding="utf-8") as file:
            for row in self.data:
                file.write(COLUMN_SEPARATOR.join(map(str, row)) + ROW_SEPARATOR)

    def load_from_file(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as file:
                content = file.read().strip(ROW_SEPARATOR)
                if content:
                    self.data = [row.split(COLUMN_SEPARATOR) for row in content.split(ROW_SEPARATOR)]

    def insert(self, record):
        if len(record) != len(self.columns):
            return "Failure: Incorrect number of fields."

        pk_value = record[self.columns.index(self.primary_key)]
        for row in self.data:
            if row[self.columns.index(self.primary_key)] == pk_value:
                return "Failure: Primary key already exists."
        
        self.data.append(record)
        self._save_to_file()
        return "Success: Record inserted."
    
    def update(self, column, new_value):
        for row in self.data:
            if column not in self.columns:
                return "Failure: Invalid Column name."
            row[self.columns.index(column)] = new_value
            self._save_to_file()
        return "Success: Records Updated."

    def update_where(self, column, new_value, key, key_value):
        for row in self.data:
            if row[self.columns.index(key)] == key_value:
                if column not in self.columns:
                    return "Failure: Invalid Column name."
                row[self.columns.index(column)] = new_value
                self._save_to_file()
                return "Success: Record updated."
        return "Failure: Primary key not found."
    
    def select_where(self,column,operator,key,key_value):
        values = []  
        for row in self.data:
            if operator == "=":
                if row[self.columns.index(key)] == key_value:
                    values .append(row[self.columns.index(column)])
            elif operator == "<":
                if row[self.columns.index(key)] < key_value:
                    values.append(row[self.columns.index(column)])
            elif operator == ">":
                if row[self.columns.index(key)] > key_value:
                    values .append(row[self.columns.index(column)])
            elif operator == "<=":
                if row[self.columns.index(key)] <= key_value:
                    values .append(row[self.columns.index(column)])
            elif operator == ">=":
                if row[self.columns.index(key)] >= key_value:
                    values .append(row[self.columns.index(column)])
            elif operator == "!=":
                if row[self.columns.index(key)] != key_value:
                    values .append(row[self.columns.index(column)])
            else:
                values.append("Failure: Invalid operator.")
        return values
    def delete(self):
        self.data[:] = []
        self._save_to_file()
        return "Success: Records Deleted."
    
    def delete_where(self, key, key_value):
        for row in self.data:
            if row[self.columns.index(key)] == key_value:
                self.data.remove(row)
                self._save_to_file()
                return "Success: Record Deleted."
        return "Failure: Record not found."

    def drop(self):
        os.remove(self.file_path)
        return "Success: Table dropped."
