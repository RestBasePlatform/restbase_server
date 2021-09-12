SELECT "table".name AS table_list_name, "table".schema AS table_list_schema, database.id as database_list_id
FROM "table" JOIN schema ON "schema".id = "table".schema JOIN database ON database.id = "schema"."database"
WHERE database.installation = 'INSTALLATION_NAME'
