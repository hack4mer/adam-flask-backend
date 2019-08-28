from flask import Flask,jsonify,request
from flask_cors import CORS, cross_origin
from flask import render_template
from flaskext.mysql import MySQL
import time
import datetime

app = Flask(__name__)
#DB SETUP
#SHOULD RATHER USER MODELS AND NOT DIRECT QUETRIES
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'greatness'
app.config['MYSQL_DATABASE_DB'] = 'adam'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route("/")
def hello():
        return render_template("welcome.html")

@app.route("/api/saveGreeting",methods=['POST'])
@cross_origin() #Should be limited to whitelisted domains/origins
def saveGreeting():

        conn = mysql.connect()
        cursor =conn.cursor()

        #form data
        greeting = request.form['greeting']
        name = request.form['name']
        ts = float(request.form['timestamp'])/1000

        error = None

        if not greeting :
            error = "Enter greeting"
        elif not name:
            error = "Enter name"
        elif not ts:
            error = "Invalid form data"

        if error:
            return jsonify({"status":"error", "data": error})

        #data validated
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

        insert_data = "INSERT INTO greetings(greeting,name,saved_on) VALUES (%s,%s,%s)"
        cursor.execute(insert_data,(greeting,name,timestamp))
        conn.commit()
        cursor.close()

        ts_now = time.time()
        timestamp_now = datetime.datetime.fromtimestamp(ts_now).strftime('%Y-%m-%d %H:%M:%S')

        #An API should usually return json
        return jsonify({"status":"success", "data": greeting+" "+name+", You called at "+timestamp+". My time is actually "+timestamp_now+", the difference is  "+str(round(ts_now-ts,2))+" seconds"})

if __name__ == "__main__":
    app.run(debug=True)