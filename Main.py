# digunakan untuk import modul 
from flask import Flask, render_template, request
import sqlite3 as sql

app = Flask(__name__) #definisi pertama buat main

#mendefinisikan route / rute untuk kehalaman awal
@app.route('/')
def home(): #mengembalikan halaman html dan mencari html dengan nama awal.html
    return render_template('awal.html') 

@app.route('/enternew')
def data_siswa():
    return render_template('siswa.html') #untuk mengambil halaman siswa html

@app.route('/addrec', methods=['POST', 'GET']) #untuk memanggil methods post dan get 
def addrec(): #mengambil data uang dikirimkan oleh pengguna melalui request.form  dan menyimpan variabel nama, dll
    if request.method == 'POST': #kondisi untuk memanggil methode post
        try:
            nama = request.form['nama']
            kd_MK = request.form['kd_MK']
            kelas = request.form['kelas']
            nilai = request.form['nilai']

            with sql.connect("UCP3.db") as con: #digunakan untuk menghubungkan ke database
                cur = con.cursor()

                # membuat tabel jika tabel input nilai belum ada
                cur.execute('''
                    CREATE TABLE IF NOT EXISTS InputNilai (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nama TEXT,
                        kd_MK TEXT,
                        kelas TEXT,
                        nilai TEXT
                    )
                ''')

                cur.execute('''
                    INSERT INTO InputNilai (nama, kd_MK, kelas, nilai)
                    VALUES (?, ?, ?, ?)''', (nama, kd_MK, kelas, nilai)) #memasukkan data ke dalam tabel

                con.commit()
                msg = "Data berhasil disimpan" #jika berhasil 
        except sql.Error as e:
            con.rollback() #membatalkan perubahan yang belum disimpan
            msg = f"Data tidak berhasil disimpan: {e}" #jika gagal
        finally:
            con.close()  # Pindahkan ini ke luar blok try-except
            return render_template("list.html", msg=msg) #mengembalikan halaman html

@app.route('/list') #tujuan ke dalam list database
def list(): #membuat fungsi list setelah data ditambahkan
    con = sql.connect("UCP3.db") 
    con.row_factory = sql.Row #urutan dari data

    cur = con.cursor() 
    cur.execute("SELECT * FROM InputNilai") # untuk mengambil semua data dari tabel inputnilai

    rows = cur.fetchall() #mendapatkan semua baris data
    con.close()  # Tutup koneksi setelah menggunakan

    return render_template("list.html", rows=rows) #mengembalikan halaman html dan variabel rows berisi semua baris data yang akan ditampilkan

if __name__ == '__main__': #menjalankan flask
    app.run(debug=True)
