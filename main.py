import re


def get_db_from_schema(file_path: str) -> dict[str, set]:
    """
    How to export from SQL Server Management Studio:
    1. Right-click on the database
    2. Select Tasks -> Generate Scripts
    3. Follow the wizard to select specific tables and generate the script
    4. Save the script to a .sql file

    :param file_path: Path to the schema file
    :return: A dictionary representing the database tables and their foreign key dependencies
    """

    regex_table = re.compile(r'CREATE\s+TABLE\s+\[dbo]\.\[(?P<name>.+?)]', re.IGNORECASE)
    regex_fk = re.compile(
        r"ALTER\s+TABLE\s+\[dbo]\.\[(?P<table>[^]]+)]"
        r"(?:.(?!\bGO\b))*?"
        r"FOREIGN\s+KEY\s*\([^)]*\)"
        r"(?:.(?!\bGO\b))*?"
        r"REFERENCES\s+\[dbo]\.\[(?P<dependency>[^]]+)]",
        re.IGNORECASE | re.DOTALL
    )

    with open(file_path, 'r', encoding='utf-16') as f:
        text = f.read()

    tables = {m.group('name'): set() for m in regex_table.finditer(text)}

    for m in regex_fk.finditer(text):
        tables[m.group('table')].add(m.group('dependency'))

    return tables


def get_ordered_tables(tables: dict[str, set]) -> list:
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
            keys = keys[1:] + keys[:1]
            tables[key] = dependencies
            attempts += 1
            if attempts >= len(keys):
                raise ValueError("Circular or unresolved dependency detected on key: " + key)
    return ordered_tables


def main():
    db = get_db_from_schema('script.sql')
    ordered_tables = get_ordered_tables(db)
    for table in ordered_tables:
        print(table)


if __name__ == '__main__':
    main()
