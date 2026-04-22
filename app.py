from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('inventario.db')
    conn.row_factory = sqlite3.Row
    return conn

# Crear DB si no existe
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    ''')
    conn.close()

init_db()

# LISTAR
@app.route('/')
def index():
    buscar = request.args.get('buscar')

    conn = get_db_connection()

    if buscar:
        productos = conn.execute(
            "SELECT * FROM productos WHERE nombre LIKE ? OR categoria LIKE ?",
            ('%' + buscar + '%', '%' + buscar + '%')
        ).fetchall()
    else:
        productos = conn.execute('SELECT * FROM productos').fetchall()

    conn.close()
    return render_template('index.html', productos=productos)

# CREAR
@app.route('/crear', methods=('GET', 'POST'))
def crear():
    if request.method == 'POST':
        nombre = request.form['nombre']
        categoria = request.form['categoria']
        precio = request.form['precio']
        stock = request.form['stock']

        conn = get_db_connection()
        conn.execute('INSERT INTO productos (nombre, categoria, precio, stock) VALUES (?, ?, ?, ?)',
                     (nombre, categoria, precio, stock))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('crear.html')

# EDITAR
@app.route('/editar/<int:id>', methods=('GET', 'POST'))
def editar(id):
    conn = get_db_connection()
    producto = conn.execute('SELECT * FROM productos WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        nombre = request.form['nombre']
        categoria = request.form['categoria']
        precio = request.form['precio']
        stock = request.form['stock']

        conn.execute('UPDATE productos SET nombre=?, categoria=?, precio=?, stock=? WHERE id=?',
                     (nombre, categoria, precio, stock, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('editar.html', producto=producto)

# ELIMINAR
@app.route('/eliminar/<int:id>')
def eliminar(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM productos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)