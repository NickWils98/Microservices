from sre_constants import SUCCESS
from flask import Flask, render_template, redirect, request, url_for
import requests

app = Flask(__name__)

ALLOWED_HOSTS = ['login', 'localhost', 'friend', 'group', 'search']
# The Username & Password of the currently logged-in User
username = None
password = None

session_data = dict()

def save_to_session(key, value):
    """
    @brief Save a key, value pair to the global session object.
    """
    session_data[key] = value

def load_from_session(key):
    """
    @brief load (and pop) the value associated with the given key from the global session object.
    """
    return session_data.pop(key) if key in session_data else None  # Pop to ensure that it is only used once

@app.route("/")
def main_page():
    return render_template('main.html', username=username, password=password)

@app.route("/catalogue")
def catalogue():
    # ================================
    # FEATURE 4 (catalogue)
    #
    # fetch a list of movies from the microservice
    # microservice returns a (python) list of movie strings
    # ================================
    try:
        movies = requests.get("http://search:8004/api/movielist").json()["response"]
    except:
        movies = []

    return render_template('catalogue.html', username=username, password=password, movies=movies)

@app.route("/login")
def login_page():

    success = load_from_session('success')
    return render_template('login.html', username=username, password=password, success=success)

@app.route("/login", methods=['POST'])
def actual_login():
    req_username, req_password = request.form['username'], request.form['password']

    # ================================
    # FEATURE 1 (login)
    #
    # send the username and password to the microservice
    # microservice returns True if correct combination, False if otherwise.
    # ================================

    data = {'username':req_username, 'password':req_password}
    try:
        success = requests.get("http://login:8001/api/login", json=data).json()["response"]
    except:
        success = False
    save_to_session('success', success)
    if success:
        global username, password
        
        username = req_username
        password = req_password

    return redirect('/login')

@app.route("/register")
def register_page():
    success = load_from_session('success')
    return render_template('register.html', username=username, password=password, success=success)

@app.route("/register", methods=['POST'])
def actual_register():

    req_username, req_password = request.form['username'], request.form['password']

    # ================================
    # FEATURE 1 (register)
    #
    # send the username and password to the microservice
    # microservice returns True if username is available, False if otherwise.
    # ================================

    data = {'username': req_username, 'password': req_password}
    try:
        success = requests.post("http://login:8001/api/register", json=data).json()["response"]
    except:
        success = False
    

    save_to_session('success', success)

    if success:
        global username, password

        username = req_username
        password = req_password

    return redirect('/register')


@app.route("/friends")
def friends():
    success = load_from_session('success')
    return render_template('friends.html', username=username, password=password, success=success)

@app.route("/add_friend", methods=['POST'])
def add_friend():
    global username

    friend_username = request.form['username']
    # ==============================
    # FEATURE 2
    #
    # send the username of the current user and the username of the added friend to the microservice
    # microservice returns True if the friend request is successful (the friend exists & is not already friends), False if otherwise
    # ==============================


    data = {'username': username}
    
    data["friendname"] = friend_username
    try:
        success = requests.post("http://friend:8002/api/friend", json=data).json()["response"]
    except:
        success = False

    save_to_session('success', success)

    return redirect('/friends')

@app.route("/groups")
def groups():

    create_success = load_from_session('create_success')
    add_success = load_from_session('add_success')
    return render_template('groups.html', username=username, password=password, create_success=create_success, add_success=add_success)

@app.route('/create_group', methods=['POST'])
def create_group():
    global username
    # ==============================
    # FEATURE 8
    #
    # send the groupname to the microservice
    # microservice returns True if the group creation is succesful (the group with this name doesn't exist already), False if otherwise
    # ==============================

    groupname = request.form['groupname']

    data = {'username':username}
    data["groupname"] = groupname
    try:
        success = requests.post("http://group:8003/api/group", json=data).json()["response"]
    except:
        success = False
    
    save_to_session('create_success', success)

    return redirect('/groups')


@app.route('/add_friend_to_group', methods=['POST'])
def add_friend_to_group():
    global username
    # ==============================
    # FEATURE 9
    #
    # send the groupname, username, friendname to the microservice
    # microservice returns True if the action is succesful (you are friends, the group exists & you are in the group), False if otherwise
    # ==============================
    groupname, friend_username = request.form['groupname'], request.form['friendname']

    
    data = {'username':username}
    data["groupname"] = groupname
    data["friend_username"] = friend_username
    try:
        success = requests.post("http://group:8003/api/group_user", json=data).json()["response"]
    except:
        success = False
    save_to_session('add_success', success)
    return redirect('/groups')

@app.route("/logout")
def logout():
    global username, password

    username = None
    password = None
    return redirect('/')

app.run(host="0.0.0.0",port=5000)