from flask import Flask,  render_template, redirect, url_for, request, g
import sqlite3
app = Flask(__name__)

app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "thisisasecretkey!"

def connect_db():
    conn = sqlite3.connect('flask.db')
    return conn

def read_all_users():
    # Read all contents of user table
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM primary')
    results = cur.fetchall()
    cur.close()
    #end of db transaction

    return results

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

#@app.route('/names')
#def names():
#def form(): #this route will have a form to fill up for common patient info
    #will link to SQlite, Method: Post8
    #name = request.args.get('name')
    #location = request.args.get('location')
#    return render_template("names.html")
@app.route('/names', methods=["GET","POST"])
def names():
    if request.method == "GET":
        return render_template("names.html")
    else:
        # in this part i am extracting the values from the form
        var_name = request.form["name"]
        var_hospital = request.form["hospital"]

        ####
        ####This is where i save the variable to database
        conn = connect_db()
        cur = conn.cursor()
        cur.execute('INSERT INTO primary (name,hospital) VALUES (?,?)', (var_name,var_hospital))
        conn.commit()
        cur.close()

#@app.route('/patient')
#def patient():
    # this route will have a table from /form about common patient info
    #edit and delete button will be available here

#@app.route('/history')
#def history():
    #this route will have a form about patient's medical history, allergies, medications,etcc
    # will link to SQlite, Method: Post

#@app.route('/records')
#def records():
    #this app will contain a table with patient's medical records from /history
    #edit and delete will be available here

if __name__ == '__main__':
    app.run()