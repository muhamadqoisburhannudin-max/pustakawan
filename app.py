from flask import Flask, render_template, request, redirect, url_for
import db

app = Flask(__name__)

# Jalankan inisiasi DB secara otomatis
db.init_db()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/wisatawan', methods=['GET', 'POST'])
def wisatawan():
    conn = db.get_db_connection()
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        provider = request.form['provider']

        # Tambah buku baru dari wisatawan
        conn.execute('INSERT INTO books (title, author, provider) VALUES (?, ?, ?)',
                     (title, author, provider))
        conn.commit()
        return redirect(url_for('wisatawan'))

    # Ambil semua buku yang pernah ditambahkan
    books = conn.execute('SELECT * FROM books ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('wisatawan.html', books=books)


@app.route('/peminjam', methods=['GET', 'POST'])
def peminjam():
    conn = db.get_db_connection()
    if request.method == 'POST':
        book_id = request.form['book_id']
        borrower_name = request.form['borrower_name']

        # Ubah status buku menjadi Dipinjam
        conn.execute('UPDATE books SET status = ? WHERE id = ?', ('Dipinjam', book_id))
        # Catat data peminjam
        conn.execute('INSERT INTO borrowings (book_id, borrower_name) VALUES (?, ?)',
                     (book_id, borrower_name))
        conn.commit()
        return redirect(url_for('peminjam'))

    # Tampilkan hanya buku yang masih tersedia
    available_books = conn.execute("SELECT * FROM books WHERE status = 'Tersedia'").fetchall()
    conn.close()
    return render_template('peminjam.html', books=available_books)


if __name__ == '__main__':
    app.run(debug=True)
    from flask import Flask, render_template, request, redirect, url_for, flash
    import db

    app = Flask(__name__)
    # Secret key wajib ada untuk menggunakan fitur flash message Flask
    app.secret_key = 'pustaka_wisata_rahasia_key'

    db.init_db()


    @app.route('/')
    def index():
        return render_template('index.html')


    @app.route('/wisatawan', methods=['GET', 'POST'])
    def wisatawan():
        conn = db.get_db_connection()
        if request.method == 'POST':
            title = request.form['title']
            author = request.form['author']
            provider = request.form['provider']

            conn.execute('INSERT INTO books (title, author, provider) VALUES (?, ?, ?)',
                         (title, author, provider))
            conn.commit()

            # Kirim notifikasi sukses
            flash('Buku berhasil disumbangkan! Terima kasih.', 'success')
            return redirect(url_for('wisatawan'))

        books = conn.execute('SELECT * FROM books ORDER BY id DESC').fetchall()
        conn.close()
        return render_template('wisatawan.html', books=books)


    @app.route('/peminjam', methods=['GET', 'POST'])
    def peminjam():
        conn = db.get_db_connection()
        if request.method == 'POST':
            book_id = request.form['book_id']
            borrower_name = request.form['borrower_name']

            conn.execute('UPDATE books SET status = ? WHERE id = ?', ('Dipinjam', book_id))
            conn.execute('INSERT INTO borrowings (book_id, borrower_name) VALUES (?, ?)',
                         (book_id, borrower_name))
            conn.commit()

            # Kirim notifikasi sukses
            flash(f'Selamat membaca, {borrower_name}! Buku berhasil dipinjam.', 'success')
            return redirect(url_for('peminjam'))

        available_books = conn.execute("SELECT * FROM books WHERE status = 'Tersedia'").fetchall()
        conn.close()
        return render_template('peminjam.html', books=available_books)


    if __name__ == '__main__':
        app.run(debug=True)

