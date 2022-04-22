def plpy_query_database(features, labels, table_name):
    columns = ", ".join(features + labels)
    return f'select {columns} from {table_name}'
