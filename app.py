import os

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)

app = Flask(__name__)


@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
   name = request.form.get('name')

   if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))


if __name__ == '__main__':
   app.run()

#2
#g
# from flask import Flask, render_template, request, redirect, url_for
# import pandas as pd
# import os
# from werkzeug.utils import secure_filename

# app = Flask(__name__)

# # Configuration
# app.config['UPLOAD_FOLDER'] = 'static/images'  # Ensure this directory exists
# app.config['CSV_FILE'] = 'people.csv'
# data = pd.read_csv(app.config['CSV_FILE'])  # Load the data
# data['Picture'].fillna('', inplace=True)  # Ensure no null values in the Picture column
# data['Salary'] = pd.to_numeric(data['Salary'], errors='coerce')  # Convert salary to numeric, handling errors

# # Ensure the upload directory exists
# os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/search', methods=['GET', 'POST'])
# def search():
#     if request.method == 'POST':
#         name_query = request.form['name']
#         if name_query:
#             # Search for the name in the dataframe
#             result = data[data['Name'].str.lower() == name_query.lower()]
#             if not result.empty:
#                 picture = result.iloc[0]['Picture']
#                 return render_template('result.html', picture=picture, name=name_query)
#             else:
#                 return render_template('index1.html', message="No name found.") #changing search to index1
#         else:
#             return render_template('index1.html', message="Please enter a name.")
#     return render_template('index1.html')

# @app.route('/low_salary')
# def low_salary():
#     # Filter entries with salary less than 99000
#     filtered_data = data[data['Salary'] < 99000]
#     # Ensure we have valid picture filenames
#     pictures = filtered_data['Picture'].dropna().tolist()
#     return render_template('low_salary.html', pictures=pictures)

# @app.route('/update_or_add_picture', methods=['GET', 'POST'])
# def update_or_add_picture():
#     global data
#     message = ''
#     if request.method == 'POST':
#         name_query = request.form['name'].strip().lower()
#         file = request.files['file']
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             if filename:  # Check if filename is not empty
#                 file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

#                 # Check if the entry exists
#                 existing_record = data[data['Name'].str.lower() == name_query]
#                 if not existing_record.empty:
#                     # Delete the old picture if it exists
#                     old_filename = existing_record['Picture'].iloc[0]
#                     if old_filename:
#                         old_file_path = os.path.join(app.config['UPLOAD_FOLDER'], old_filename)
#                         if os.path.exists(old_file_path):
#                             os.remove(old_file_path)

#                 # Save the new file
#                 file.save(file_path)

#                 # Update or add the record
#                 if not existing_record.empty:
#                     data.loc[data['Name'].str.lower() == name_query, 'Picture'] = filename
#                 else:
#                     # Add new entry if name does not exist
#                     new_entry = {'Name': name_query.capitalize(), 'Picture': filename, 'Keywords': ''}
#                     data = data.append(new_entry, ignore_index=True)

#                 # Save changes back to CSV
#                 data.to_csv(app.config['CSV_FILE'], index=False)
#                 message = 'Picture updated or added successfully for "{}".'.format(name_query.capitalize())
#             else:
#                 message = 'No valid filename provided.'
#         else:
#             message = 'Invalid file or file not provided.'
#     return render_template('update_or_add_picture.html', message=message)

# @app.route('/remove_entry', methods=['GET', 'POST'])
# def remove_entry():
#     global data
#     message = ''
#     if request.method == 'POST':
#         name_query = request.form['name'].strip().lower()
#         # Find if the entry exists
#         existing_record = data[data['Name'].str.lower() == name_query]
#         if not existing_record.empty:
#             # Delete the picture if it exists
#             old_filename = existing_record['Picture'].iloc[0]
#             if old_filename:
#                 old_file_path = os.path.join(app.config['UPLOAD_FOLDER'], old_filename)
#                 if os.path.exists(old_file_path):
#                     os.remove(old_file_path)
#             # Remove the data entry
#             data = data[data['Name'].str.lower() != name_query]
#             data.to_csv(app.config['CSV_FILE'], index=False)
#             message = 'The entry for "{}" was removed successfully.'.format(name_query.capitalize())
#         else:
#             message = 'Error: No entry found for the name "{}".'.format(name_query.capitalize())
#     return render_template('remove_entry.html', message=message)

# @app.route('/update_keywords', methods=['GET', 'POST'])
# def update_keywords():
#     message = ''
#     if request.method == 'POST':
#         name_query = request.form['name'].strip().lower()
#         new_keywords = request.form['keywords'].strip()
#         # Check if the entry exists
#         if name_query in data['Name'].str.lower().values:
#             # Update the keywords for the given name
#             data.loc[data['Name'].str.lower() == name_query, 'Keywords'] = new_keywords
#             # Save changes back to CSV
#             data.to_csv(app.config['CSV_FILE'], index=False)
#             message = 'Keywords updated successfully for "{}".'.format(name_query.capitalize())
#         else:
#             message = 'Error: No entry found for the name "{}".'.format(name_query.capitalize())
#     return render_template('update_keywords.html', message=message)

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

# if __name__ == '__main__':
#     app.run(debug=True)
