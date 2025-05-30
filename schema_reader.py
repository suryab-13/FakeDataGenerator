def get_table_schema(cursor, table_name):
    cursor.execute("""
        SELECT COLUMN_NAME, COLUMN_TYPE 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = %s
    """, (table_name,))
    return cursor.fetchall()

def list_tables(cursor):
    cursor.execute("SHOW TABLES")
    return [row[0] for row in cursor.fetchall()]

def get_foreign_keys(cursor, table_name):
    cursor.execute("""
        SELECT COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
        FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
        WHERE TABLE_SCHEMA = DATABASE()
        AND TABLE_NAME = %s 
        AND REFERENCED_TABLE_NAME IS NOT NULL
    """, (table_name,))
    return cursor.fetchall()

def fetch_foreign_key_values(cursor, referenced_table, referenced_column):
    cursor.execute(f"SELECT {referenced_column} FROM {referenced_table}")
    return [row[0] for row in cursor.fetchall()]


def get_child_tables(cursor, table_name):
    cursor.execute("""
        SELECT TABLE_NAME, COLUMN_NAME, REFERENCED_COLUMN_NAME
        FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
        WHERE REFERENCED_TABLE_NAME = %s AND TABLE_SCHEMA = DATABASE()
    """, (table_name,))
    return cursor.fetchall()

