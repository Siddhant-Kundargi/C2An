from flask import Flask, abort
import C2AnApi

app = Flask(__name__)

app.register_blueprint(C2AnApi.auth, url_prefix='/auth')

@app.route('/<inputString>')
def index(inputString):
    abort(404)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
 