from flask import Flask
from flask import request
from flask import redirect
from flask import url_for

app = Flask(__name__)

@app.route('/api/vpf-730', methods=['GET', 'POST'])
def route():
    print(request.json)
    return {'code': 200}

@app.route('/<path:page>', methods=['GET', 'POST'])
def other(page):
    return redirect(url_for('route'))

if __name__ == '__main__':
    app.run(debug=True)
