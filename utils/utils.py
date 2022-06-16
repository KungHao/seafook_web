import json
import bcrypt
import base64
from bson.objectid import ObjectId
from bson.binary import Binary

# 從DB讀出來
def encodeImg(image):
    return base64.b64encode(image).decode()

# 存入DB
def decodeImg(image):
    return base64.b64decode(image)

def itemJson(item_name, price, discount, category, quantity, description, img):
    to_json = {
        'name': str(item_name),
        'price': int(price),
        'category': str(category),
        'discount': int(discount),
        'quantity': int(quantity),
        'description': str(description),
        'img': img
    }
    return to_json

# return byte to binary image list 
def encode_imglist(datas):
    new_datas = []
    for data in datas:
        # binary image to bytes(encode image)
        data['img'] = encodeImg(data['img'])
        new_datas.append(data)
    return new_datas
    
# password check
def check_password(input_pwd, db_pwd):
    return bcrypt.checkpw(input_pwd.encode('utf-8'), db_pwd)