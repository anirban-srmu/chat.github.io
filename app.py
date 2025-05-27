from flask import Flask,render_template,redirect,url_for,request,flash
from flask_socketio import SocketIO,send
from flask_login import LoginManager,UserMixin, login_user,login_required,current_user,logout_user
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'

socketio = SocketIO(app)
login_manager= LoginManager(app)
bcrypt = Bcrypt(app)

user_db = {}

class User(UserMixin):
    def __init__(self,username):
        self.id = username

@login_manager.user_loader
def load_user(username):
    if username in user_db:
        return User(username)
    return None

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = bcrypt.generate_password_hash(request.form['password'])
        if username in user_db:
            flash("User already exists","danger")
        else:
            user_db[username] = {'password':password}
            flash("registration sucessful! Please now login","sucsess")
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = user_db.get(username)

        if user and bcrypt.check_password_hash(user['password'],password):
            login_user(User(username))
            return redirect(url_for('chat'))
        else:
            flash("Invalid credential", "danger")
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/chat')
@login_required
def chat():
    return render_template('chat.html',username=current_user.id)

@socketio.on('message')
def handle_message(msg):
    print(f"Received Message: {msg}")
    send({'msg':msg['msg'],'user':msg['user']},broadcast= True)


if __name__ =='__main__':
    socketio.run(app,debug = True)