from datetime import timedelta
import os
import bcrypt
import pymongo
import json
from models.models import *
from bson.json_util import dumps
from bson.objectid import ObjectId
from utils.utils import decodeImg, itemJson, encodeImg, encode_imglist, check_password
from flask import Flask, render_template, session, url_for, request, Response, redirect, url_for, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)
DB_URI = "mongodb+srv://jamesMongo:0Az82U28n2WyxNl5@clusterj.z7twq.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(DB_URI)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SECRET_KEY'] = os.urandom(23)
mydb = client['e_seafood']
prod_col = mydb['products']
user_col = mydb['users']

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = 'login'

# current_user 會來這邊找資料
@login_manager.user_loader
def user_loader(user_id):
    find_user = user_col.find_one({'_id' : ObjectId(user_id)})
    if find_user:
        user = User(id=find_user['_id'], name=find_user['name'], pwd=find_user['password'])
        return user
    return 

@login_manager.request_loader
def request_loader(request):
    find_user = user_col.find_one({'name' : request.form.get('username')})
    if find_user:
        if check_password(input_pwd=request.form['password'], db_pwd=find_user['password']):
            user = User(id=find_user['_id'], name=find_user['name'], pwd=find_user['password'])
            return user
    return

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        data = prod_col.find()
        categories = data.distinct('category')
        # 處理圖片
        data = encode_imglist(data)
    if request.method == 'POST':
        data = prod_col.find({'category': request.form['category']})
        categories = data.distinct('category')
        # 處理圖片
        data = encode_imglist(data)
    return render_template('index.html', current_user=current_user, data=data, categories=categories)

@app.route("/category", methods=['GET', 'POST'])
def category():
    if request.method == 'POST':
        data = prod_col.find({'category': request.form['category']})
        categories = data.distinct('category')
        # 處理圖片
        data = encode_imglist(data)
    return render_template('index.html', current_user=current_user, data=data, categories=categories)

@app.route("/detail", methods=['GET', 'POST'])
def detail():
    if request.method == 'POST':
        itemID = request.form['itemID']
        query = {'_id': ObjectId(itemID)}
        res = list(prod_col.find(query))
        if len(res) == 0:
            print("No image data!")
            img='ERROR'
        else:
            img = encodeImg(res[0]['img'])
    return render_template('detail.html', data=res, img=img)

@app.route('/form', methods=["POST"])
def form():
    if request.method == 'POST':
        pass
    return render_template('form.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        item_name = request.form['item_name']
        price = request.form['price']
        category = request.form['category']
        discount = request.form['discount']
        quantity = request.form['quantity']
        description = request.form['description']
        img = request.form['img']
        img = img.split('base64,')[1] # 取得base64,後面的image bytes
        data = itemJson(
            item_name=item_name, 
            price=price, 
            discount=discount, 
            category=category, 
            quantity=quantity, 
            description=description,
            img=decodeImg(img)
        )
        prod_col.insert_one(data)
    return 'success'

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request_loader(request)
        if user:
            login_user(user, remember=True)

            return redirect(url_for('index'))
        # find_user = user_col.find_one({'name' : request.form['username']})
        # if find_user:
        #     print('user:', user_loader(find_user['_id']).get_id)
        #     if check_password(input_pwd=request.form['pass'], db_pwd=find_user['password']):
        #         # session['username'] = request.form['username']
        #         user = User()
        #         user.id = find_user['_id']
        #         login_user(user)
        #         return redirect(url_for('index'))

        return '輸入帳號密碼錯誤'
    else:
        return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    # session.pop('username', None)
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        existing_user = user_col.find_one({'name' : username})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            user_col.insert_one({'name' : username, 'password' : hashpass})
            return redirect(url_for('login'))
        
        return 'That username already exists!'

    return render_template('register.html')

@app.route('/cart')
@login_required
def cart():
    return render_template('cart.html')
# @app.route('/submit', methods=['POST', 'GET'])
# def submit():
#     if request.method == 'POST':
#         user = request.form('user') # POST用此方法接收user參數
#         print('post : user => ', user)
#         return redirect(url_for('success', name=user, action='post'))
#     else:
#         user = request.args.get('user') # GET用此方法接收user參數
#         print('get : user => ', user)
#         return redirect(url_for('success', name=user, action='get'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
    