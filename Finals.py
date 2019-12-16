from flask import Flask, render_template, redirect, url_for, request, session
import sqlite3

app = Flask(__name__)

app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "thisisasecretkey!"


def connect_db():
    conn = sqlite3.connect('flask.db')
    return conn


def read_all_users():
    # Read all contents of first table
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM first')
    results = cur.fetchall()
    cur.close()
    return results


# end of db transaction

def read_second_table():
    # read all contents of second table
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM second')
    results = cur.fetchall()
    cur.close()
    return results


# end of db transaction


# @app.route('/' , defaults={"name":"Person"})
@app.route('/')
def index():
    # session["name"] = name
    return render_template("index.html")


@app.route('/about', defaults={"name": "client"})
@app.route('/about/<name>')
def about(name):
    if session.get("name") is None:
        return redirect(url_for("names"))
    else:
        name = session["name"]
        return render_template("about.html", about_name=name)

@app.route('/names', methods=["GET", "POST"])
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
        cur.execute('INSERT INTO first (name,hospital) VALUES (?,?)', (var_name, var_hospital))
        conn.commit()
        cur.close()

        if var_name == '':
            return redirect(url_for('unsuccessful'))
        elif var_hospital == '':
            return redirect(url_for('unsuccessful'))
        else:
            session["name"] = var_name
            return redirect(url_for('about'))


@app.route('/patient')
def patient():
    # this route will have a table from /form about common patient info
    # edit and delete button will be available here
    results = read_all_users()
    return render_template("patient.html", results=results)


@app.route('/edit', methods=['post', 'get'])
def edit():
    if request.method == 'GET':
        edit_id = request.args.get('edit')
        # Retrieve that record
        conn = connect_db()
        cur = conn.cursor()
        cur.execute('SELECT * FROM first WHERE id = ?', (edit_id))
        result = cur.fetchone()
        cur.close()
        # done

        return render_template('edit.html', result=result)
    elif request.method == 'POST':
        new_name = request.form['name']
        new_hospital = request.form['hospital']
        edit_id = request.form['id']

        if request.form['edit'] == "update":
            # Update the record
            conn = connect_db()
            cur = conn.cursor()
            cur.execute('UPDATE first SET name = ?, hospital = ? WHERE id = ?', (new_name, new_hospital, edit_id))
            conn.commit()
            cur.close()
            # end of DB transaction
        elif request.form['edit'] == "delete":
            # Delete the record
            conn = connect_db()
            cur = conn.cursor()
            cur.execute('DELETE FROM first WHERE id = ?', (edit_id))
            conn.commit()
            cur.close()
            # end of DB transaction

        results = read_all_users()
        return render_template('patient.html', results=results)


@app.route('/unsuccessful')
def unsuccessful():
    return render_template('unsuc.html')


@app.route('/records', methods=["GET", "POST"])
def records():
    if request.method == "GET":
        return render_template("records.html")
    else:
        # in this part i am extracting the values from the form
        var_pid = request.form["pid"]
        var_check = request.form["check"]
        var_complaint = request.form["complaint"]
        var_dx = request.form["dx"]
        var_tx = request.form["tx"]

        # where i save the variable to database
        conn = connect_db()
        cur = conn.cursor()
        cur.execute('INSERT INTO second (patient_id,Last_Checkup,Complaint,Diagnosis,Treatment) VALUES (?,?,?,?,?)',
                    (var_pid, var_check, var_complaint, var_dx, var_tx))
        conn.commit()
        cur.close()

        if var_pid == '':
            return redirect(url_for('unsuccessful'))
        elif var_check == '':
            return redirect(url_for('unsuccessful'))
        elif var_complaint == '':
            return redirect(url_for('unsuccessful'))
        elif var_dx == '':
            return redirect(url_for('unsuccessful'))
        elif var_tx == '':
            return redirect(url_for('unsuccessful'))
        else:
            results = read_second_table()
            return render_template('hospital.html', results=results)


@app.route('/hospital')
def hospital():
    # this route will have a table from /form about common patient info
    # edit and delete button will be available here
    results = read_second_table()
    return render_template("hospital.html", results=results)


@app.route('/edit2', methods=['post', 'get'])
def edit2():
    if request.method == 'GET':
        edit2_id = request.args.get('edit2')
        # Retrieve that record
        conn = connect_db()
        cur = conn.cursor()
        cur.execute('SELECT * FROM second WHERE id = ?', (edit2_id,))
        result = cur.fetchone()
        cur.close()
        # done
        return render_template('edit2.html', result=result)
    elif request.method == 'POST':
        new_pid = request.form['pid']
        new_check = request.form['check']
        new_complaint = request.form['complaint']
        new_dx = request.form['dx']
        new_tx = request.form['tx']
        edit2_id = request.form['id']

        if request.form['edit2'] == "update":
            # Update the record
            conn = connect_db()
            cur = conn.cursor()
            cur.execute('UPDATE second SET patient_id = ?,Last_Checkup = ?,Complaint = ?,Diagnosis = ?,Treatment =? WHERE id = ?', (new_pid, new_check, new_complaint, new_dx, new_tx, edit2_id))
            conn.commit()
            cur.close()
            # end of DB transaction
        elif request.form['edit2'] == "delete":
            # Delete the record
            conn = connect_db()
            cur = conn.cursor()
            cur.execute('DELETE FROM second WHERE id = ?', (edit2_id,))
            conn.commit()
            cur.close()
            # end of DB transaction

        results = read_second_table()
        return render_template('hospital.html', results=results)

@app.route('/logout')
def logout():
    if session.get("name") is None:
        return redirect(url_for("names"))
    else:
        session.pop("name")
        return render_template('logout.html')


if __name__ == '__main__':
    app.run()
