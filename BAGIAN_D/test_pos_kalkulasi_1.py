import pytest
import math
# Mengimport fungsi dari file pos_kalkulasi.py
from pos_kalkulasi import hitung_total_transaksi

# ==============================================================================
# 23. UNIT TEST UNTUK SKENARIO INDIVIDU (Soal D.1)
# ==============================================================================

def test_tanpa_diskon_bukan_member():
    """3 item, harga Rp50.000, bukan member, tanpa voucher"""
    hasil = hitung_total_transaksi(jumlah_item=3, harga_satuan=50000, is_member=False, kode_voucher=None)
    assert hasil == 166500

def test_diskon_5_persen():
    """7 item, harga Rp100.000, bukan member, tanpa voucher"""
    hasil = hitung_total_transaksi(jumlah_item=7, harga_satuan=100000, is_member=False, kode_voucher=None)
    assert hasil == 738200

def test_diskon_10_persen():
    """10 item, harga Rp80.000, bukan member, tanpa voucher"""
    hasil = hitung_total_transaksi(jumlah_item=10, harga_satuan=80000, is_member=False, kode_voucher=None)
    assert hasil == 799200

def test_diskon_member():
    """5 item, harga Rp200.000, member, tanpa voucher"""
    hasil = hitung_total_transaksi(jumlah_item=5, harga_satuan=200000, is_member=True, kode_voucher=None)
    assert hasil == 1022900

def test_voucher_tidak_bisa_dengan_member():
    """5 item, harga Rp200.000, member DAN ada voucher — diskon member tidak diterapkan"""
    hasil = hitung_total_transaksi(jumlah_item=5, harga_satuan=200000, is_member=True, kode_voucher="VOUCHER_KASIR")
    assert hasil == 1054500

def test_batas_jumlah_item_minimum():
    """1 item — harus valid dan tidak raise error"""
    hasil = hitung_total_transaksi(jumlah_item=1, harga_satuan=10000, is_member=False, kode_voucher=None)
    assert hasil == 11100  # 10.000 + PPN 11% = 11.100

def test_batas_jumlah_item_maksimum():
    """999 item — harus valid dan tidak raise error"""
    # Gunakan harga kecil Rp10.000 agar tidak kena validasi batas transaksi Rp50 juta
    hasil = hitung_total_transaksi(jumlah_item=999, harga_satuan=10000, is_member=False, kode_voucher=None)
    assert hasil > 0

def test_input_nol_raise_error():
    """0 item — harus raise ValueError"""
    with pytest.raises(ValueError, match="Jumlah item tidak valid"):
        hitung_total_transaksi(jumlah_item=0, harga_satuan=50000, is_member=False, kode_voucher=None)

def test_input_negatif_raise_error():
    """Input negatif — harus raise ValueError"""
    with pytest.raises(ValueError, match="Jumlah item tidak valid"):
        hitung_total_transaksi(jumlah_item=-5, harga_satuan=50000, is_member=False, kode_voucher=None)

def test_melebihi_batas_transaksi():
    """Input yang menghasilkan total di atas Rp 50 juta — harus raise ValueError"""
    with pytest.raises(ValueError, match="Total melebihi batas maksimal transaksi"):
        # 600 item * Rp100.000 = Rp60 Juta
        # Diskon 10% -> Rp54 Juta. Ditambah PPN 11% pasti jauh di atas Rp50 Juta!
        hitung_total_transaksi(jumlah_item=600, harga_satuan=100000, is_member=False, kode_voucher=None)


# ==============================================================================
# 24. PARAMETRIZE TEST UNTUK BOUNDARY VALUES DISKON (4, 5, 9, 10)
# ==============================================================================

@pytest.mark.parametrize(
    "jumlah, harga, expected_total",
    [
        (4, 10000, 44400),   # 4 item: Tanpa diskon grosir -> 40k + 11% PPN = 44.400
        (5, 10000, 52800),   # 5 item: Diskon 5% -> 47.5k + 11% PPN = 52.725 -> Bulat 52.800
        (9, 10000, 95000),   # 9 item: Diskon 5% -> 85.5k + 11% PPN = 94.905 -> Bulat 95.000
        (10, 10000, 99900),  # 10 item: Diskon 10% -> 90k + 11% PPN = 99.900
    ]
)
def test_boundary_diskon_jumlah_item(jumlah, harga, expected_total):
    """Menguji nilai batas transisi diskon kuantitas item menggunakan parameterize"""
    hasil = hitung_total_transaksi(jumlah_item=jumlah, harga_satuan=harga, is_member=False, kode_voucher=None)
    assert hasil == expected_total
