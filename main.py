from db_config import get_connection
from schema_reader import list_tables, get_table_schema
from  PushData  import insert_fake_data

def main():
    conn = get_connection()
    cursor = conn.cursor()

    print("\nAvailable tables:")
    tables = list_tables(cursor)
    for idx, table in enumerate(tables):
        print(f"{idx + 1}. {table}")

    choice = int(input("\nSelect a table number: "))
    table_name = tables[choice - 1]

    schema = get_table_schema(cursor, table_name)

    num_rows = int(input(f"\n no of  rows to insert into `{table_name}`? "))
    insert_fake_data(cursor, conn, table_name, schema, num_rows)

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
