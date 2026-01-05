from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)

# --- CONFIGURATION ---
app.secret_key = "customic_store_99135" 
DATABASE = 'database.db'

# Database Setup
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id TEXT PRIMARY KEY,
            name TEXT,
            price REAL,
            discount INTEGER,
            category TEXT,
            image TEXT
        )
    ''')
    conn.commit()
    conn.close()

# --- 1. FRONTEND ROUTES (User Pages) ---

@app.route('/')
def home():
    # Ab Keychains.html ki jagah index.html render hoga
    return render_template('index.html')

@app.route('/keychains')
def keychains_page():
    # Agar koi /keychains par jaye tab bhi index.html dikhega
    return render_template('index.html')

@app.route('/lamp')
def lamp_page():
    return render_template('Lamp.html')

@app.route('/pen')
def pen_page():
    return render_template('Pen.html')

@app.route('/penpot')
def penpot_page():
    return render_template('Penpot.html')

@app.route('/tempset')
def tempset_page():
    return render_template('Tempset.html')

@app.route('/wallets')
def wallets_page():
    return render_template('Wallets.html')

# --- 2. ADMIN & AUTH SYSTEM ---

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/api/login-session', methods=['POST'])
def login_session():
    session['adminLoggedIn'] = True
    return jsonify({"status": "success"})

@app.route('/admin')
def admin_page():
    if not session.get('adminLoggedIn'):
        return redirect(url_for('login_page'))
    return render_template('admin.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
    (index.html)
    # return redirect(url_for('login_page'))

# --- 3. DATABASE API (Product Operations) ---

@app.route('/api/products', methods=['GET'])
def get_products():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    conn.close()
    
    products = []
    for r in rows:
        products.append({
            "id": r[0], "name": r[1], "price": r[2], 
            "discount": r[3], "category": r[4], "image": r[5]
        })
    return jsonify(products)

@app.route('/api/products', methods=['POST'])
def save_product():
    try:
        data = request.json
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("""
            REPLACE INTO products (id, name, price, discount, category, image) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, (data['id'], data['name'], data['price'], data['discount'], data['category'], data['image']))
        conn.commit()
        conn.close()
        return jsonify({"message": "Success"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/api/products/<id>', methods=['DELETE'])
def delete_product(id):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id=?", (id,))
        conn.commit()
        conn.close()
        return jsonify({"message": "Deleted"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

# --- 4. START SERVER ---
if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)