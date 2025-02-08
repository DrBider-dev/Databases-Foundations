# UDSQL - A Simple DBMS

## Project Overview
UDSQL is a lightweight, file-based database management system (DBMS) developed as part of the Databases Foundations course (Workshop No. 3). This project provides basic database functionalities such as inserting, updating, deleting, and selecting data using a simple command-line interface.

## Features
- Stores tables as individual files
- Uses the `pickle` module to manage database metadata.
- Supports basic SQL-like operations:
  - `INSERT` to add records.
  - `UPDATE` to modify existing records.
  - `DELETE` to remove records.
  - `SELECT` with basic projection and selection using logical operators.

## Installation & Usage
1. Clone the repository:
   ```bash
   git clone https://github.com/DrBider-dev/Databases-Foundations.git
   cd Databases-Foundations/WorkShop_3
   ```
2. Run the application:
   ```bash
   python3 main.py
   ```
3. Enter commands in the CLI interface. Type `EXIT` to quit.

## Possible Operations
Here are some example queries that users can do in the application:

- Create a Database:
    ```
    CREATE DATABASE UDsql
    ```
- Create a Table:
    ```
    CREATE TABLE user id id,name,age  # id will be the table's primary_key 
    ```
- Insert a new record:
    ```
    INSERT INTO user 1,pepe,20
    ```
- Update a record:
    ```
    UPDATE user SET name = 'pepa' WHERE age = 20
    ```
- Select something:
    ```
    SELECT name FROM user WHERE id = 1
    ```
- Drop table:
    ```
    DROP TABLE user
    ```
- Drop database:
    ```
    DROP DATABASE UDsql
    ```

## File Structure
- `main.py`: Entry point of the application.
- `Database.py`: Contains the `Database` class which handles the core database operations.
- `Table.py`: Contains the `Table` class which handles individual table operations.
- `{Database Name}/`: Directory where table files are stored.
- `{Database Name}/metadata.pkl`: Stores database schema information.
- `{Database Name}/{Table Name}.txt`: Stores the table information.
- `README.md`: Documentation for the project.

## Authors
This repository is being developed by students from the Universidad Distrital Francisco Jose de Caldas for their Database Fundamentals course in the Systems Engineering program.
- [Brayan Estiven Aguirre Aristizabal - 20231020156](https://github.com/DrBider-dev)
- [Marlon Yecid Riveros Guio - 20231020208](https://github.com/Drack678?tab=overview&from=2024-09-01&to=2024-09-15)