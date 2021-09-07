SELECT table_list.name AS table_list_name, table_list.schema AS table_list_schema, database_list.id as database_list_id
FROM table_list JOIN schema_list ON schema_list.id = table_list.schema JOIN database_list ON database_list.id = schema_list."database"
WHERE database_list.installation = 'INSTALLATION_NAME'
