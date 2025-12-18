# SQL Schema Table Orderer

A small Python utility that parses a SQL Server schema export and prints tables in an order where each table appears after its foreign\-key dependencies. Useful for generating ordered table creation or data import sequences.

## Requirements
1. Python 3.10+  
2. `numpy` package

Install dependency on Windows:
```powershell
python -m pip install numpy
```

## Usage
1. Export your database schema from SQL Server Management Studio (SSMS) to a `.sql
2. Place the exported file as `script.sql` in the same directory as `main.py`.
3. Run the script:
```powershell
python main.py
```
4. The ordered list of tables will be printed to the console.

## How to Export Schema from SSMS
1. Open SQL Server Management Studio (SSMS).
2. Connect to your database server.
3. Right-click on the database you want to export.
4. Select "Tasks" > "Generate Scripts".
5. Follow the wizard to select the database objects you want to script (choose "Tables").
6. In the "Set Scripting Options" step, choose to save the script to a
7. Finish the wizard to generate the SQL script file.
8. Rename the generated file to `script.sql` and place it in the same directory as `main.py`.