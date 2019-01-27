from flask import Flask , request, send_file

app = Flask(__name__)

@app.route("/api/chart/file")
def index():
    return send_file('site/list.html')

if __name__ == '__main__':
    app.run()
