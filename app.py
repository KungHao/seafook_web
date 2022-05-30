from unicodedata import name
from flask import Flask, render_template, url_for, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def hello():
    # return "Hello, World!"
    return render_template('index.html')

@app.route('/submit', methods=['POST', 'GET'])
def submit():
    if request.method == 'POST':
        user = request.form('user') # POST用此方法接收user參數
        print('post : user => ', user)
        return redirect(url_for('success', name=user, action='post'))
    else:
        user = request.args.get('user') # GET用此方法接收user參數
        print('get : user => ', user)
        return redirect(url_for('success', name=user, action='get'))

@app.route('/success/<action>/<name>')
def success(name, action):
    return '{} : Welcome {} ~ !!!'.format(action, name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)