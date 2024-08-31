1. Database Architecture. Use the file  database_schema.sql` to define the DB Architecture. 
Execute the SQL file using a SQLite command-line tool or any SQL client connected to your database.
   ```
   expenses.db < database_schema.sql 
   ```
1. Create exhaustive list of categories, subcategories, and products formatted for SQL insertions. Save this content into a .sql file (e.g., `master_data.sql`) and run it to populate your database with the initial data. 
Run the SQL File: Execute the SQL file using a SQLite command-line tool or any SQL client connected to your database. This command assumes you are using SQLite and expenses.db is your database file.
```
sqlite3 expenses.db < master_data.sql
```

Use the curl command
```
curl "http://127.0.0.1:5000/product/category_subcategory?product_name=Milk"
```