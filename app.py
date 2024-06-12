# import os

# from flask import (Flask, redirect, render_template, request,
#                    send_from_directory, url_for)

# app = Flask(__name__)


# @app.route('/')
# def index():
#    print('Request for index page received')
#    return render_template('index.html')

# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(app.root_path, 'static'),
#                                'favicon.ico', mimetype='image/vnd.microsoft.icon')

# @app.route('/hello', methods=['POST'])
# def hello():
#    name = request.form.get('name')

#    if name:
#        print('Request for hello page received with name=%s' % name)
#        return render_template('hello.html', name = name)
#    else:
#        print('Request for hello page received with no name or blank name -- redirecting')
#        return redirect(url_for('index'))


# if __name__ == '__main__':
#    app.run()

#2
# conn = pymssql.connect(host ='sinong.database.windows.net' ,user="sinong" ,password ="Azhar@123" ,data)
# cur = conn.cursor()

# LOAD DATA INFILE 'C:\Users\Lenovo\Desktop\sem 3 summer\ccbd\assignment 2\data.csv'
# INTO TABLE earthquake1
# FIELDS TERMINATED BY ',' 
# OPTIONALLY ENCLOSED BY '"'
# LINES TERMINATED BY '\n'
# IGNORE 1 ROWS
# (time, latitude, longitude, depth, mag, magType, nst, dmin, rms, net, id, updated, place, type, horizontal_error, depth_error, magError, magNst, status, locationSource, magSource);



import pandas as pd
import pyodbc
print("drivers name", pyodbc.drivers())
# Function to establish connection
def connect_to_db():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=ccbd_server.database.windows.net;'
        'DATABASE=db1;'
        'UID=ccbd;'
        'PWD=Azhar@123'
    )
    return conn

# Function to create the table
def create_table():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'EarthquakeData')
        BEGIN
            CREATE TABLE EarthquakeData (
                time DATETIME,
                latitude FLOAT,
                longitude FLOAT,
                depth FLOAT,
                mag FLOAT,
                magType VARCHAR(10),
                nst INT,
                gap FLOAT,
                dmin FLOAT,
                rms FLOAT,
                net VARCHAR(10),
                id VARCHAR(50),
                updated DATETIME,
                place VARCHAR(255),
                type VARCHAR(50),
                horizontalError FLOAT,
                depthError FLOAT,
                magError FLOAT,
                magNst INT,
                status VARCHAR(50),
                locationSource VARCHAR(50),
                magSource VARCHAR(50)
            );
        END
    """)
    conn.commit()
    cursor.close()
    conn.close()


# Function to read CSV and load data
def load_data_to_db(file_path):
    # Modify this line to read only the first 5 rows
    data = pd.read_csv(file_path, nrows=5)
    conn = connect_to_db()
    cursor = conn.cursor()

    # Assuming you have a table named 'EarthquakeData'
    # and columns named exactly as in the CSV header
    for index, row in data.iterrows():
        cursor.execute("""
            INSERT INTO EarthquakeData (time, latitude, longitude, depth, mag, magType, nst, gap, dmin, rms, net, id, updated, place, type, horizontalError, depthError, magError, magNst, status, locationSource, magSource)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, 
            row['time'], row['latitude'], row['longitude'], row['depth'], row['mag'], row['magType'],
            row['nst'], row['gap'], row['dmin'], row['rms'], row['net'], row['id'],
            row['updated'], row['place'], row['type'], row['horizontalError'], row['depthError'],
            row['magError'], row['magNst'], row['status'], row['locationSource'], row['magSource']
        )
        conn.commit()  # commit after each row, or you can optimize by committing after multiple rows

    cursor.close()
    conn.close()

# Path to your CSV file
csv_file_path = 'C:\Users\Lenovo\Desktop\github_files\Asg02\data.csv'
load_data_to_db(csv_file_path)

