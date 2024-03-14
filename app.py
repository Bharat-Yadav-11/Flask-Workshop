from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient

mongodb_uri = "mongodb+srv://bharat:zrDZNUm3dGePeZQQ@cluster0.6lcmris.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

mongodb_client = MongoClient(mongodb_uri)

mongodb_database = mongodb_client['main']

# mongodb_database["user"].insert_one({"name": "Bharat", "age": 20,})

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'

# @app.route('/')
# def hello_world():
#     return "Hello World"

# @app.route('/about')
# def about():
#     return 'About Us'

# @app.route('/greet/<username>')
# def greet(username):
#     return f"Hello {username}"


@app.route('/')
def task():
    if 'tasks' not in session:
        session['tasks'] =[]

    return render_template('index.html', tasks=session['tasks'])

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == "POST":
        name = request.form['task']
        session['tasks'] += [name]
        return redirect(url_for('task'), code=302)
    return render_template("add.html")
  

@app.route('/delete/<index>')
def delete(index):
    index = int(index)-1
    session['tasks'] = session['tasks'][:int(index)] + session['tasks'][int(index)+1:]
    return redirect(url_for('task'), code=302)

@app.route('/register', methods=['GET', 'POST'])
def sign_up():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        if mongodb_database["user"].find_one({"email" : email}):
            return "User already exists"
        else:
            mongodb_database["user"].insert_one({"name": name, "email": email, "password": password})
            return "User created successfully"
    return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if "logged_in" not in session:
        return redirect(url_for('sign_up'), code=302)
    
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        user = mongodb_database["user"].find_one({"email" : email, "password": password})
        if user:
            session['logged_in'] = True
            return "Logged in successfully"
        else:
            return "Invalid credentials"
    return render_template("login.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0')



