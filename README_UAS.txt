================================================================================
  README — UAS STQA (Software Testing & Quality Assurance)
  Kelompok 1 | MLM1
================================================================================

NAMA ANGGOTA KELOMPOK:
  1. I Gede Nakamanda Candra Putra     (2301010015)
  2. Farrel Nazwa Diaz Ersyad          (2301010017)
  3. I Made Rai Adi Wirawan            (2301010020)
  4. Lutfi Prasetyo                    (2301010039)

--------------------------------------------------------------------------------
DESKRIPSI PROYEK
--------------------------------------------------------------------------------

Proyek ini adalah hasil UAS mata kuliah Software Testing & Quality Assurance (STQA).
Proyek terdiri dari pengujian sebuah Aplikasi POS (Point of Sale) kasir berbasis web
milik "PT Maju Bersama". Pengujian mencakup unit testing, integration testing, dan
UI testing menggunakan framework Pytest dan Playwright.

--------------------------------------------------------------------------------
STRUKTUR DIREKTORI
--------------------------------------------------------------------------------

UAS_STQA_MLM1_KELOMPOK_1/
│
├── pos-kasir.html          → Aplikasi web POS kasir (front-end utama)
├── laporan_uas.html        → Laporan hasil pengujian (output pytest-html)
├── README_UAS.txt          → File ini
│
├── BAGIAN_A_B_C_E/         → Jawaban soal essay (Bagian A, B, C, E)
│   └── Jawaban_Essay_*.docx
│
├── BAGIAN_C/               → Kode fungsi kalkulasi POS (versi awal/referensi)
│   └── pos_kalkulasi.py
│
└── BAGIAN_D/               → Implementasi pengujian lengkap (unit + UI)
    ├── pos_kalkulasi.py         → Fungsi logika bisnis kalkulasi transaksi
    ├── test_pos_kalkulasi.py    → Unit test untuk fungsi kalkulasi
    ├── test_pos_ui.py           → UI test dengan Playwright (Page Object Model)
    ├── pytest.ini               → Konfigurasi pytest
    ├── laporan_uas.html         → Laporan hasil test (pytest-html)
    └── screenshot_playwright_PASSED.png  → Bukti screenshot test berhasil

--------------------------------------------------------------------------------
APLIKASI YANG DIUJI: pos-kasir.html
--------------------------------------------------------------------------------

Aplikasi POS kasir berbasis web dengan fitur:
  - Pencarian produk berdasarkan kode produk (format: 2 huruf + 6 angka, cth: BV123456)
  - Keranjang belanja (tambah, hapus item)
  - Diskon kuantitas otomatis:
      * Beli >= 5 item  → diskon 5%
      * Beli >= 10 item → diskon 10%
  - Diskon member 3% (tidak bisa digabung dengan voucher)
  - Input kode voucher
  - Perhitungan PPN 11%
  - Pembulatan total ke atas ke kelipatan Rp 100
  - Batas maksimal transaksi: Rp 50.000.000
  - Metode pembayaran: Tunai atau Kartu (dengan PIN 6 digit)
  - Cetak struk setelah pembayaran berhasil

--------------------------------------------------------------------------------
FUNGSI KALKULASI: pos_kalkulasi.py
--------------------------------------------------------------------------------

Fungsi utama: hitung_total_transaksi(jumlah_item, harga_satuan, is_member, kode_voucher)

Alur perhitungan:
  1. Validasi jumlah item (harus integer, antara 1–999)
  2. Hitung subtotal = harga_satuan × jumlah_item
  3. Terapkan diskon kuantitas (5% atau 10%)
  4. Terapkan diskon member 3% jika is_member=True DAN tidak ada voucher
  5. Tambahkan PPN 11%
  6. Bulatkan ke atas ke kelipatan 100
  7. Validasi total tidak melebihi Rp 50.000.000

--------------------------------------------------------------------------------
PENGUJIAN: BAGIAN D
--------------------------------------------------------------------------------

A. UNIT TEST (test_pos_kalkulasi.py) — Pytest
   Total: 14 test case (10 individual + 4 parameterize boundary values)

   Skenario yang diuji:
   - Transaksi tanpa diskon (bukan member)
   - Diskon kuantitas 5% (>= 5 item)
   - Diskon kuantitas 10% (>= 10 item)
   - Diskon member 3%
   - Aturan: voucher + member tidak bisa bersamaan
   - Batas minimum item (1 item) — harus valid
   - Batas maksimum item (999 item) — harus valid
   - Input nol (0 item) — harus raise ValueError
   - Input negatif — harus raise ValueError
   - Transaksi melebihi Rp 50 juta — harus raise ValueError
   - Boundary value analysis: item 4, 5, 9, 10 (transisi diskon)

B. UI TEST (test_pos_ui.py) — Pytest + Playwright
   Total: 12 test case (10 TC biasa + 2 TC menggunakan Page Object Model)

   Skenario yang diuji:
   - TC01: Tambah item dengan kode valid → sukses
   - TC02: Format kode produk salah → tampil pesan error
   - TC03: Kode produk tidak ditemukan → tampil pesan error
   - TC04: Diskon qty 5% muncul di UI saat beli >= 5 item
   - TC05: Voucher expired → tampil pesan error
   - TC06: Voucher + member bersamaan → ditolak
   - TC07: Pembayaran tunai berhasil → struk muncul
   - TC08: PIN kartu salah → tampil pesan error
   - TC09: Tombol bayar disabled saat keranjang kosong
   - TC10: Batal transaksi → keranjang dikosongkan
   - POM-01: Tambah produk via Page Object Model
   - POM-02: Pembayaran tunai via Page Object Model

C. KONFIGURASI (pytest.ini)
   - Base URL : http://localhost:3000
   - Mode     : verbose (--headed), browser tampil saat test berjalan
   - Tool     : pytest-html v4.2.0 untuk generate laporan HTML

D. HASIL PENGUJIAN
   - Semua test case PASSED (dibuktikan dengan screenshot_playwright_PASSED.png
     dan laporan_uas.html)
   - Environment: Python 3.12.6, Windows 11, Playwright 0.8.0

--------------------------------------------------------------------------------
CARA MENJALANKAN PENGUJIAN (BAGIAN D)
--------------------------------------------------------------------------------

1. Pastikan server lokal berjalan di http://localhost:3000
   (contoh: jalankan `npx serve .` atau server HTTP sederhana)

2. Install dependencies:
   pip install pytest pytest-html pytest-playwright
   playwright install

3. Jalankan semua test:
   cd BAGIAN_D
   pytest --html=laporan_uas.html

4. Untuk unit test saja:
   pytest test_pos_kalkulasi.py -v

5. Untuk UI test saja:
   pytest test_pos_ui.py -v --headed

================================================================================
