from flask import Flask,url_for, send_from_directory, render_template, request
import csv

{
#testing to implement for a larger database .ie. multiple classes
# import pymongo
# Replace 'mongodb://localhost:27017/' with your MongoDB connection string
# client = pymongo.MongoClient("mongodb://localhost:27017/")
# db = client["mydatabase"]
# collection = db["mycollection"]
}

app = Flask(__name__,static_folder="static")

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory("static",filename)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        enrollNo = request.form['enrollNo']
        class_no = request.form['class_no']
        with open('data.csv', 'a', newline='') as csvfile:
            fieldnames = ['Enroll No', 'Class']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'Enroll No': enrollNo, 'Class': class_no})
        return 'Data received successfully!'
    else:
        return render_template('index.html',script_url=url_for('static', filename='script.js'))

if __name__ == '__main__':
    app.run(debug=True,port=8930)
