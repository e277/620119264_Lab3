# ID Number: 620119264
# Lab3 - Web API

from flask import Flask, request, make_response
import mysql.connector
import csv

app = Flask(__name__)

@app.route('/customers', methods=['GET'])
def get_customers():
    try:
        conn   = mysql.connector.connect(user='root', password='mysql-25', host='127.0.0.1', database='uwi_lab3')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM customers;')
        customers_list = []
        for customer_id, gender, age, annual_income, spending_score, profession, work_experience, family_size in cursor:
            customer = {}
            customer['customer_id']        = customer_id
            customer['gender']             = gender
            customer['age']                = age
            customer['annual_income']      = annual_income
            customer['spending_score']     = spending_score
            customer['profession']         = profession
            customer['work_experience']    = work_experience
            customer['family_size']        = family_size
            customers_list.append(customer)
        cursor.close()
        conn.close()
        return make_response(customers_list, 200)
    except Exception as e:
        return make_response({'error': str(e)}, 400)


@app.route('/customer/<customer_id>', methods=['GET'])
def get_customer(customer_id):
    try:
        conn   = mysql.connector.connect(user='root', password='mysql-25', host='127.0.0.1', database='uwi_lab3')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM customers WHERE customer_id = %s;', (customer_id,))
        row      = cursor.fetchone()
        customer = {}
        if row is not None:
            customer_id, gender, age, annual_income, spending_score, profession, work_experience, family_size = row
            customer['customer_id']        = customer_id
            customer['gender']             = gender
            customer['age']                = age
            customer['annual_income']      = annual_income
            customer['spending_score']     = spending_score
            customer['profession']         = profession
            customer['work_experience']    = work_experience
            customer['family_size']        = family_size
            cursor.close()
            conn.close()
            return make_response(customer, 200)
        else:
            return make_response({'error': 'Customer Not Found'}, 404)
    except Exception as e:
        return make_response({'error': str(e)}, 400)


@app.route('/add_customer', methods=['POST'])
def create_customer():
    try:
        conn              = mysql.connector.connect(user='root', password='mysql-25', host='127.0.0.1', database='uwi_lab3')
        cursor            = conn.cursor()
        content           = request.get_json()
        customer_id       = content['customer_id']
        gender            = content['gender']
        age               = content['age']
        annual_income     = content['annual_income']
        spending_score    = content['spending_score']
        profession        = content['profession']
        work_experience   = content['work_experience']
        family_size       = content['family_size']
        sql_query = '''
        INSERT INTO 
            customers (customer_id, gender, age, annual_income, spending_score, profession, work_experience, family_size)
        VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s);
        '''
        params = (customer_id, gender, age, annual_income, spending_score, profession, work_experience, family_size)
        cursor.execute(sql_query, params)
        conn.commit()
        cursor.close()
        conn.close()
        return make_response({'message': 'Customer Created Successfully'}, 201)
    except Exception as e:
        return make_response({'error': str(e)}, 400)


@app.route('/update_profession/<customer_id>', methods=['PUT'])
def update_customer(customer_id):
    try:
        conn       = mysql.connector.connect(user='root', password='mysql-25', host='127.0.0.1', database='uwi_lab3')
        cursor     = conn.cursor()
        content    = request.get_json()
        profession = content['profession']
        sql_query  = '''
            UPDATE customers
            SET profession = %s
            WHERE customer_id = %s;
        '''
        params = (profession, customer_id)
        cursor.execute(sql_query, params)
        conn.commit()
        cursor.close()
        conn.close()
        return make_response({'message': 'Customer Profession Updated Successfully'}, 201)
    except Exception as e:
        return make_response({'error': str(e)}, 400)


@app.route('/highest_income_report', methods=['GET'])
def highest_income_report():
    try:
        conn      = mysql.connector.connect(user='root', password='mysql-25', host='127.0.0.1', database='uwi_lab3')
        cursor    = conn.cursor()
        sql_query = '''
            SELECT c.customer_id, c.profession, c.annual_income
            FROM customers c
            INNER JOIN (
                SELECT profession, MAX(annual_income) AS max_income
                FROM customers
                GROUP BY profession
            ) t ON c.profession = t.profession AND c.annual_income = t.max_income AND c.profession != '' AND t.profession != '';
        '''
        cursor.execute(sql_query)
        report = []
        for customer_id, profession, annual_income in cursor:
            report.append({
                'CustomerID': customer_id,
                'Profession': profession,
                'AnnualIncome': annual_income
            })
        cursor.close()
        conn.close()
        return make_response(report, 200)
    except Exception as e:
        return make_response({'error': str(e)}, 400)


@app.route('/total_income_report', methods=['GET'])
def total_income_report():
    try:
        conn      = mysql.connector.connect(user='root', password='mysql-25', host='127.0.0.1', database='uwi_lab3')
        cursor    = conn.cursor()
        sql_query = '''
            SELECT profession, SUM(annual_income) AS total_income
            FROM customers
            WHERE profession != '' AND profession IS NOT NULL
            GROUP BY profession
            ORDER BY total_income DESC;
        '''
        cursor.execute(sql_query)
        report = []
        for profession, total_income in cursor:
            report.append({
                'Profession': profession,
                'TotalIncome': total_income
            })
        cursor.close()
        conn.close()
        return make_response(report, 200)
    except Exception as e:
        return make_response({'error': str(e)}, 400)


@app.route('/average_work_experience', methods=['GET'])
def average_work_experience():
    try:
        conn      = mysql.connector.connect(user='root', password='mysql-25', host='127.0.0.1', database='uwi_lab3')
        cursor    = conn.cursor()
        sql_query = '''
            SELECT profession, AVG(work_experience) AS AverageExperience
            FROM customers
            WHERE annual_income > 50000 AND age < 35 AND profession != '' AND profession  IS NOT NULL
            GROUP BY profession
            ORDER BY AverageExperience DESC;
        '''
        cursor.execute(sql_query)
        report = []
        for profession, AverageExperience in cursor:
            report.append({
                'Profession': profession,
                'AverageExperience': AverageExperience
            })
        cursor.close()
        conn.close()
        return make_response(report, 200)
    except Exception as e:
        return make_response({'error': str(e)}, 400)


@app.route('/average_spending_score/<profession>', methods=['GET'])
def average_spending_score(profession):
    try:
        conn      = mysql.connector.connect(user='root', password='mysql-25', host='127.0.0.1', database='uwi_lab3')
        cursor    = conn.cursor()
        sql_query = '''
            SELECT gender, AVG(spending_score) AS AverageSpendingScore
            FROM customers
            WHERE profession = %s
            GROUP BY gender;
        '''
        cursor.execute(sql_query, (profession,))
        report = []
        for gender, AverageSpendingScore in cursor:
            report.append({
                'Gender': gender,
                'AverageSpendingScore': AverageSpendingScore
            })
        cursor.close()
        conn.close()
        return make_response(report, 200)
    except Exception as e:
        return make_response({'error': str(e)}, 400)


if __name__ == '__main__':
    app.run()
