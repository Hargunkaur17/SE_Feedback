import time
import csv
import pandas as pd
import mysql.connector

# MySQL database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'forms_data'
}

# Path to the CSV file
csv_file_path = 'C:\\xampp\\mysql\\data\\forms_data\\Sample data.csv'

def update_database(connection, cursor):
    with open('C:\\xampp\\mysql\\data\\forms_data\\Sample data.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        for row in csv_reader:
            # Assuming Student_Name is the column used to identify records
            student_name = row['Student_Name']
            Satisfaction_Rating_Distribution = row['Satisfaction Rating Distribution']
            
            # Update the MySQL table using the identified student_name
            update_query = f"UPDATE feedback_form SET Satisfaction_Rating_Distribution = {Satisfaction_Rating_Distribution} WHERE Student_Name = '{student_name}'"
            cursor.execute(update_query)
            connection.commit()

def insert_data(connection, cursor):
    df = pd.read_csv('C:\\xampp\\mysql\\data\\forms_data\\Sample data.csv')

    cols = df.columns.tolist()
    for i in range(df.shape[0]):
        select_query = f"SELECT student_name FROM feedback_form WHERE student_name like '{df[cols[0]].loc[i]}'"
        cursor.execute(select_query)
        print("abcd", type(cursor.fetchone()), cursor.fetchone())
        if type(cursor.fetchone()) is tuple:
            continue
        else:
            print("1",f"{df[cols[0]].loc[i]}")
            insert_query = f"INSERT INTO feedback_form VALUES ('{df[cols[0]].loc[i]}', '{df[cols[1]].loc[i]}', '{df[cols[2]].loc[i]}', '{df[cols[3]].loc[i]}', '{df[cols[4]].loc[i]}', '{df[cols[5]].loc[i]}')"
            cursor.execute(insert_query)
            connection.commit()

def main():
    try:
        # Establish MySQL connection
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        
        # # Update the database with data from the CSV file
        # update_database(connection, cursor)

        insert_data(connection, cursor)
        
        # Close the MySQL connection
        cursor.close()
        connection.close()
        
        print("Database updated.")
        
    except Exception as e:
        print("Error:", e)
        
      

if __name__ == '__main__':
    main()