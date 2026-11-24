from flask import Flask, render_template
from data.database import init_db
from models.party_member import PartyMember

app = Flask(__name__)

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/p3r')
def p3r():
    membros = PartyMember.buscar_por_jogo('p3r')
    builds = [PartyMember.buscar_build_completa(m['id']) for m in membros]
    return render_template('p3r.html')

@app.route('/p4g')
def p4g():
    return render_template('p4g.html')

@app.route('/p5r')
def p5r():
    return render_template('p5r.html')

if __name__ == '__main__':
    app.run(debug=True)