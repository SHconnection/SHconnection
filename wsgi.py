from shapp import app
from flask import send_file, render_template

@app.route("/")
def chart_file():
    return render_template('list.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='2000')
