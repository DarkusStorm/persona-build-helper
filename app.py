from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/p3r')
def p3r():
    return render_template('p3r.html')

@app.route('/p4g')
def p4g():
    return render_template('p4g.html')

@app.route('/p5r')
def p5r():
    return render_template('p5r.html')

if __name__ == '__main__':
    app.run(debug=True)