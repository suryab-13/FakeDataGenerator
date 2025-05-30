from schema_reader import get_foreign_keys, fetch_foreign_key_values, get_table_schema, get_child_tables
from data_generator import generate_fake_value
import random

def insert_fake_data(cursor, conn, table_name, schema, num_rows=10, inserted_refs=None):
    if inserted_refs is None:
        inserted_refs = {}

    print(f"\n--- Inserting into `{table_name}` ---")
   
    columns = [col[0] for col in schema if col[0].lower() != 'id']
    types = [col[1] for col in schema if col[0].lower() != 'id']


    foreign_keys = get_foreign_keys(cursor, table_name)
    foreign_key_values = {}

    for col_name, ref_table, ref_col in foreign_keys:
        cursor.execute(f"SELECT COUNT(*) FROM {ref_table}")
        count = cursor.fetchone()[0]

        if count == 0:
            print(f"No data in `{ref_table}`, populating before `{table_name}`...")
            ref_schema = get_table_schema(cursor, ref_table)
            insert_fake_data(cursor, conn, ref_table, ref_schema, num_rows, inserted_refs)

        values = fetch_foreign_key_values(cursor, ref_table, ref_col)
        foreign_key_values[col_name] = values

  
    inserted_ids = []
    for _ in range(num_rows):
        values = []
        for col, typ in zip(columns, types):
            if col in foreign_key_values:
                fk_vals = foreign_key_values[col]
                if fk_vals:
                    values.append(random.choice(fk_vals))
                else:
                    print(f" Warning: No values for foreign key column `{col}`. Inserting NULL.")
                    values.append(None)
            else:
                values.append(generate_fake_value(col, typ))

        placeholders = ', '.join(['%s'] * len(values))
        query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
        cursor.execute(query, values)
        inserted_ids.append(cursor.lastrowid)

    conn.commit()
    print(f"{num_rows} rows inserted into `{table_name}`")
    print(f"Inserted IDs for `{table_name}`: {inserted_ids}")

 
    if inserted_ids:
        cursor.execute(
            f"SELECT * FROM {table_name} WHERE id IN ({','.join(map(str, inserted_ids))})"
        )
        rows = cursor.fetchall()
        for row in rows:
            print(row)

    inserted_refs[table_name] = inserted_ids


    child_fks = get_child_tables(cursor, table_name)
    for child_table, col_name, ref_col in child_fks:
        child_schema = get_table_schema(cursor, child_table)
        child_foreign_keys = get_foreign_keys(cursor, child_table)

        fk_vals = {}
        for fk_col, ref_table, ref_column in child_foreign_keys:
            if ref_table in inserted_refs:
                fk_vals[fk_col] = inserted_refs[ref_table]
            else:
                fk_vals[fk_col] = fetch_foreign_key_values(cursor, ref_table, ref_column)

        rows = []
        for parent_id in inserted_ids:
            row = []
            for col, typ in zip([col[0] for col in child_schema], [col[1] for col in child_schema]):
                if col == col_name:
                    row.append(parent_id)
                elif col in fk_vals:
                    vals = fk_vals[col]
                    row.append(random.choice(vals) if vals else None)
                else:
                    row.append(generate_fake_value(col, typ))
            rows.append(row)

        if rows:
            placeholders = ', '.join(['%s'] * len(rows[0]))
            insert_query = f"INSERT INTO {child_table} ({', '.join([col[0] for col in child_schema])}) VALUES ({placeholders})"
            cursor.executemany(insert_query, rows)
            conn.commit()
            print(f"{len(rows)} rows inserted into child table `{child_table}`")

            try:
                fk_col_index = [col[0] for col in child_schema].index(col_name)
                fk_values = [row[fk_col_index] for row in rows]
                cursor.execute(f"SELECT * FROM {child_table} WHERE {col_name} IN ({','.join(map(str, fk_values))})")
                child_rows = cursor.fetchall()
                print(f"Verification - recently inserted rows in child table `{child_table}`:")
                for crow in child_rows:
                    print(crow)
            except Exception as e:
                print(f"Could not verify inserted rows for `{child_table}`: {e}")
