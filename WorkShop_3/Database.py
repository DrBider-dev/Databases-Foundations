import os
import pickle
import Table

class Database:


    def __init__(self, name):
        self.name = name
        self.db_path = f"./{name}"
        self.tables = {}
        self.metadata_file = f"{self.db_path}/metadata.pkl"
        os.makedirs(self.db_path, exist_ok=True)
        self._load_metadata()
        self._save_metadata()

    def create_table(self, table_name, primary_key, columns):
        if table_name in self.tables:
            return "Failure: Table already exists."
        self.tables[table_name] = Table.Table(self.db_path, table_name, primary_key, columns)
        self.tables[table_name]._save_to_file()
        self._save_metadata()
        return "Success: Table created."

    def _save_metadata(self):
        metadata = {}
        for table_name, table in self.tables.items():
            metadata[table_name] = (table.primary_key, table.columns)
        with open(self.metadata_file, "wb") as file:
            pickle.dump(metadata, file)

    def _load_metadata(self):
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, "rb") as file:
                metadata = pickle.load(file)
                for table_name, (primary_key, columns) in metadata.items():
                    self.tables[table_name] = Table.Table(self.name, table_name, primary_key, columns)
                    self.tables[table_name].load_from_file()


    def execute_query(self, query):
        if query.strip().upper() == "EXIT":
            return "Exiting..."
        
        parts = query.split()
        operation = parts[0].upper()
                
        if operation == "CREATE" and parts[1].upper() == "TABLE":
            if len(parts) < 5:
                return "Failure: Invalid query."
            table_name = parts[2]
            primary_key = parts[3]
            columns = parts[4].split(",")
            if "," not in parts[4]:
                return f"Failure: Values must be comma-separated. Did you mean: CREATE TABLE {table_name} {primary_key} {','.join(parts[4:])}?"
            if primary_key not in columns:
                return "Failure: Primary key must be one of the columns."
            return self.create_table(table_name, primary_key, columns)
        
        elif operation == "INSERT" and parts[1].upper() == "INTO":
            if len(parts) < 4:
                return "Failure: Invalid query."
            table_name = parts[2]
            if table_name not in self.tables:
                return f"Failure: Table {table_name} doesn't exist."
            if len(parts[3].split(",")) != len(self.tables[table_name].columns):
                return "Failure: Incorrect number of fields."
            if "," not in parts[3]:
                return f"Failure: Values must be comma-separated. Did you mean: INSERT INTO {table_name} {','.join(parts[3:])}?"
            
            record = parts[3].split(",")
            return self.tables[table_name].insert(record)
        
        
        elif operation == "UPDATE" and parts[2].upper() == "SET":
            table_name = parts[1]
            column = parts[3]
            new_value = parts[5].strip("'")
            
            if len(parts) > 6 and parts[6] and parts[6].upper() == "WHERE":
                if len(parts) < 9:
                    return "Failure: Invalid query."
                key = parts[7]
                key_value = parts[9].strip("'")
                return self.tables[table_name].update_where(column, new_value, key, key_value)
            
            return self.tables[table_name].update(column, new_value)
        
        elif operation == "DELETE" and parts[1].upper() == "FROM":
            table_name = parts[2]

            if len(parts) > 3 and parts[3] and parts[3].upper() == "WHERE":
                if len(parts) < 5:
                    return "Failure: Invalid query."
                key = parts[4]
                key_value = parts[6].strip("'")
                return self.tables[table_name].delete_where(key, key_value)
            return self.tables[table_name].delete()
        
        elif operation == "DROP" and parts[1].upper() == "TABLE":
            table_name = parts[2]
            if table_name in self.tables:
                self.tables[table_name].drop()
                del self.tables[table_name]
                self._save_metadata()
                return f"Success: Table {table_name} dropped."
            return "Failure: Table doesn't exist."
        
        elif operation == "SELECT" and parts[2].upper() == "FROM":
            column = parts[1]
            table_name = parts[3]
            if table_name not in self.tables:
                return f"Failure: Table {table_name} doesn't exist."
            elif column == "*":
                for row in self.tables[table_name].data:
                    return "|".join(str(data) for data in row)

            elif len(parts) == 4:
                for row in self.tables[table_name].data:
                    return row[self.tables[table_name].columns.index(column)]
                    
            elif len(parts) > 4 and parts[4].upper() == "WHERE":
                if len(parts) < 8:
                    return "Failure: Invalid query."
                key = parts[5]
                operator = parts[6]
                key_value = parts[7]
                values = self.tables[table_name].select_where(column,operator,key, key_value)
                return values
        else:
            return "Failure: Invalid query."