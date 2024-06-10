from flask import Flask


app = Flask(__name__)


@app.route('/')
def index_view():
    return 'Main page'


if __name__ == '__main__':
    app.run()
