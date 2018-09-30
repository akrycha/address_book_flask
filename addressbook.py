from flask import Flask, render_template, request, redirect
import sqlite3
app = Flask(__name__)


@app.route('/')
def hello():
    result = render_template('welcome.html')
    return result


@app.route('/contacts')
def contacts():
    conn = sqlite3.connect('addressbook.db')
    c = conn.cursor()
    dane = c.execute("""select * from book""")
    lista = []
    for line in dane:
        lista.append(line[1]+' '+line[2]+' '+line[3]+' '+line[4])
    return render_template('contacts.html', contacts=lista)


@app.route('/add', methods=['GET', 'POST'])
def add_contact():
    name = ''
    lastname = ''
    address = ''
    phone = ''
    if request.method == 'POST':
        name = request.form.get('imie', '')
        lastname = request.form.get('nazwisko', '')
        address = request.form.get('adres', '')
        phone = request.form.get('nrtel', '')
    conn = sqlite3.connect('addressbook.db')
    c = conn.cursor()
    if name.strip() or lastname.strip() or address.strip() or phone.strip():
        c.execute("""INSERT INTO book (name, lastname, address, phone) values (?,?,?,?)""", (name, lastname, address, phone))
        conn.commit()
        return redirect('/contacts')
    return render_template('add.html')


if __name__ == '__main__':
    app.run(debug=True)
