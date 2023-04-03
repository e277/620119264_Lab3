# ID Number: 620119264
# Lab3 - Generate SQL File
# Execute this script to load the data in the csv file into sql file named insert_data.sql
import csv

csv_file = open('Customers.csv', 'r')

csv_reader = csv.reader(csv_file)

sql_file = open('insert_data.sql', 'w')

# sql_file.write('INSERT INTO customers(customer_id, gender, age, annual_income, spending_score, profession, work_experience, family_size) VALUES \n')

next(csv_reader, None)
for line in csv_reader:
    # obtain the values from the csv file, put string values in single quotes
    customer_id        = line[0] if line[0] != '' else 'NULL'
    gender             = "'" + line[1] + "'" if line[1] != '' else 'NULL'
    age                = line[2] if line[2] != '' else 'NULL'
    annual_income      = line[3] if line[3] != '' else 'NULL'
    spending_score     = line[4] if line[4] != '' else 'NULL'
    profession         = "'" + line[5] + "'" if line[5] != '' else 'NULL'
    work_experience    = line[6] if line[6] != '' else 'NULL'
    family_size        = line[7] if line[7] != '' else 'NULL'
    
    sql_file.write('INSERT INTO customers (customer_id, gender, age, annual_income, spending_score, profession, work_experience, family_size) VALUES \
        (' + customer_id + ', ' + gender + ', ' + age + ', ' + annual_income + ', ' + spending_score + ', ' + profession + ', ' + work_experience + ', ' + family_size + ');\n')


csv_file.close()
sql_file.close()
