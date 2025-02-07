import os
import Database

class Main:

    def run():
        db = None
        while True:
            query = input("Enter your query: ")
            if query.strip().upper() == "EXIT":
                print("Exiting...")
                break
            if (db is None and query.strip().upper().startswith("CREATE DATABASE")) or query.strip().upper().startswith("CREATE DATABASE"):
                db_name = query.split()[2]
                if not os.path.exists(f"./{db_name}/metadata.pkl"):
                    db = Database.Database(db_name)
                    print(f"Database {db_name} created.")
                    continue
                print(f"Database {db_name} already exists.")
                    
            
            elif (db is None and query.strip().upper().startswith("USE")) or query.strip().upper().startswith("USE"):
                db_name = query.split()[1]
                if not os.path.exists(f"./{db_name}/metadata.pkl"):
                    print(f"Failure: Database {db_name} doesn't exist.")
                else:
                    db = Database.Database(db_name)
                    print(f"Using database {db_name}.")
                
            elif query.strip().upper().startswith("DROP DATABASE"):
                db_name = query.split()[2]
                if os.path.exists(f"./{db_name}/metadata.pkl"):
                    os.system(f"rm -rf ./{db_name}")
                    print(f"Database {db_name} dropped.")
                else:
                    print(f"Failure: Database {db_name} doesn't exist.")

            elif db is not None:
                result = db.execute_query(query)
                print(result)
            else:
                print("No database selected. Please create a database first.")

    if __name__ == "__main__":
        run()
