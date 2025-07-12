import csv
import os
from datetime import datetime, timedelta

PRODUK_FILE = 'produk.csv'
TRANSAKSI_FILE = 'transaksi.csv'

def load_csv(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def save_csv(filename, fieldnames, data):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

# --------------------- PRODUK ---------------------


def tampilkan_produk():
    data = load_csv(PRODUK_FILE)
    if not data:
        print("Belum ada produk.")
        return
    for d in data:
        print(f"{d['id']} | {d['nama']} | Stok: {d['stok']} | Harga: {d['harga']} | {d['deskripsi']}")

def tambah_produk():
    data = load_csv(PRODUK_FILE)
    new_id = str(len(data)+1)
    nama = input("Nama produk: ")
    stok = input("Stok: ")
    harga = input("Harga: ")
    deskripsi = input("Deskripsi: ")
    data.append({'id': new_id, 'nama': nama, 'stok': stok, 'harga': harga, 'deskripsi': deskripsi})
    save_csv(PRODUK_FILE, ['id', 'nama', 'stok', 'harga', 'deskripsi'], data)
    print("Produk berhasil ditambahkan.")

def ubah_produk():
    data = load_csv(PRODUK_FILE)
    tampilkan_produk()
    id_edit = input("ID produk yang akan diubah: ")
    for d in data:
        if d['id'] == id_edit:
            d['nama'] = input(f"Nama baru ({d['nama']}): ") or d['nama']
            d['stok'] = input(f"Stok baru ({d['stok']}): ") or d['stok']
            d['harga'] = input(f"Harga baru ({d['harga']}): ") or d['harga']
            d['deskripsi'] = input(f"Deskripsi baru ({d['deskripsi']}): ") or d['deskripsi']
            save_csv(PRODUK_FILE, ['id', 'nama', 'stok', 'harga', 'deskripsi'], data)
            print("Produk berhasil diubah.")
            return
    print("Produk tidak ditemukan.")

def hapus_produk():
    data = load_csv(PRODUK_FILE)
    tampilkan_produk()
    id_hapus = input("ID produk yang akan dihapus: ")
    data_baru = [d for d in data if d['id'] != id_hapus]
    save_csv(PRODUK_FILE, ['id', 'nama', 'stok', 'harga', 'deskripsi'], data_baru)
    print("Produk berhasil dihapus.")

# ------------------- TRANSAKSI --------------------
def tambah_transaksi(jenis):
    produk = load_csv(PRODUK_FILE)
    tampilkan_produk()
    id_pilih = input("ID produk: ")
    jumlah = int(input("Jumlah: "))
    for p in produk:
        if p['id'] == id_pilih:
            if jenis == "penjualan" and int(p['stok']) < jumlah:
                print("Stok tidak cukup!")
                return
            p['stok'] = str(int(p['stok']) + jumlah) if jenis == "pembelian" else str(int(p['stok']) - jumlah)
            save_csv(PRODUK_FILE, ['id', 'nama', 'stok', 'harga', 'deskripsi'], produk)
            transaksi = load_csv(TRANSAKSI_FILE)
            now = datetime.now().strftime("%Y-%m-%d")
            transaksi.append({
                'tanggal': now,
                'id_produk': id_pilih,
                'nama_produk': p['nama'],
                'jumlah': str(jumlah),
                'total': str(int(p['harga'])* jumlah),
                'tipe': jenis
            })
            save_csv(TRANSAKSI_FILE, ['tanggal', 'id_produk', 'nama_produk', 'jumlah', 'total', 'tipe'], transaksi)
            print(f"Transaksi {jenis} berhasil.")
            return
    print("Produk tidak ditemukan.")

# ------------------- LAPORAN ----------------------
def laporan(tipe, rentang):
    transaksi = load_csv(TRANSAKSI_FILE)
    now = datetime.now()
    if rentang == "harian":
        batas = now - timedelta(days=1)
    elif rentang == "mingguan":
        batas = now - timedelta(days=7)
    else: 
        batas = now - timedelta(days=30)

    total = 0
    print(f"\nLaporan {tipe} ({rentang})")
    for t in transaksi:
        tgl = datetime.strptime(t['tanggal'], "%Y-%m-%d")
        if t['tipe'] == tipe and tgl >= batas:
            print(f"{t['tanggal']} | {t['nama_produk']} x {t['jumlah']} = {t['total']}")
            total += int(t['total'])
    print(f"Total: {total}\n")

# --------------------- MENU -----------------------

def menu():
    while True:
        print("\n--- Menu Manajemen Toko ---")
        print("1. Lihat Produk")
        print("2. Tambah Produk")
        print("3. Ubah Produk")
        print("4. Hapus Produk")
        print("5. Transaksi Penjualan")
        print("6. Transaksi Pembelian")
        print("7. Laporan Penjualan")
        print("8. Keluar")

        pilihan = input("Pilih menu: ")
        if pilihan == '1':
            tampilkan_produk()
        elif pilihan == '2':
            tambah_produk()
        elif pilihan == '3':
            ubah_produk()
        elif pilihan == '4':
            hapus_produk()
        elif pilihan == '5':
            tambah_transaksi("penjualan")
        elif pilihan == '6':
            tambah_transaksi("pembelian")
        elif pilihan == '7':
            print("1. Harian\n2. Mingguan\n3. Bulanan")
            r = input("Pilih: ")
            rentang = {'1': 'harian', '2': 'mingguan', '3': 'bulanan'}.get(r)
            if rentang:
                laporan("penjualan", rentang)
            else:
                print("Pilihan tidak valid.")
        elif pilihan == '8':
            break
        else:
            print("Pilihan tidak valid.")

menu()