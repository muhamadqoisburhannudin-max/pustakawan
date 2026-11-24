import sqlite3


def get_db_connection():
    conn = sqlite3.connect('pustaka.db')
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()

    # Tabel Buku
    conn.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            provider TEXT NOT NULL,
            status TEXT DEFAULT 'Tersedia'
        )
    ''')

    # Tabel Peminjaman
    conn.execute('''
        CREATE TABLE IF NOT EXISTS borrowings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER,
            borrower_name TEXT NOT NULL,
            FOREIGN KEY (book_id) REFERENCES books (id)
        )
    ''')

    conn.commit()
    conn.close()
    print("Database SQLite 'pustaka.db' berhasil diinisialisasi.")


if __name__ == '__main__':
    init_db()