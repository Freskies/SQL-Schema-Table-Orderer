import numpy as np


def get_db_from_schema(file_path: str) -> dict[str, list]:
    """
    How to export from SQL Server Management Studio:
    1. Right-click on the database
    2. Select Tasks -> Generate Scripts
    3. Follow the wizard to select specific tables and generate the script
    4. Save the script to a .sql file

    :param file_path: Path to the schema file
    :return: A dictionary representing the database tables and their foreign key dependencies
    """
    tables: dict[str, list] = {}

    # create all tables with empty dependencies
    with open(file_path, 'r', encoding='utf-16') as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip()
        if not line.startswith("CREATE TABLE"):
            continue
        parts = line.split('[')
        table_name = parts[2].split(']')[0]
        tables[table_name] = []

    # populate foreign key dependencies
    line_before_is_alter_table = False
    current_table = ""
    with open(file_path, 'r', encoding='utf-16') as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip()
        if line.startswith("ALTER TABLE") and "FOREIGN KEY" in line:
            parts = line.split('[')
            current_table = parts[2].split(']')[0]
            line_before_is_alter_table = True
            continue
        if line_before_is_alter_table:
            line_before_is_alter_table = False
            if not "REFERENCES" in line:
                continue
            parts = line.split('[')
            referenced_table = parts[2].split(']')[0]
            if current_table in tables:
                tables[current_table].append(referenced_table)

    return tables


def get_ordered_tables(tables: dict[str, list]) -> list:
    """
    Given a dictionary of tables and their foreign key dependencies,
    return a list of tables ordered such that each table appears after
    all its dependencies.
    """
    keys = list(tables.keys())
    ordered_tables: list[str] = []
    attempts = 0
    while len(tables) != 0:
        key = keys[0]
        dependencies = tables.pop(key)
        if all(dependency in ordered_tables for dependency in dependencies):
            ordered_tables.append(key)
            del keys[0]
            attempts = 0
        else:
            keys = np.roll(keys, -1).tolist()
            tables[key] = dependencies
            attempts += 1
            if attempts >= len(keys):
                raise ValueError("Circular or unresolved dependency detected")
    return ordered_tables


def main():
    db = get_db_from_schema('script.sql')
    ordered_tables = get_ordered_tables(db)
    for table in ordered_tables:
        print(table)


if __name__ == '__main__':
    main()
