def hitung_total_transaksi(jumlah_item, harga_satuan, is_member, kode_voucher=None):
    # Baris 01: Validasi input
    if not isinstance(jumlah_item, int) or jumlah_item < 1 or jumlah_item > 999:
        raise ValueError('Jumlah item tidak valid')
    # Baris 05: Hitung subtotal
    subtotal = harga_satuan * jumlah_item
    # Baris 08: Diskon berdasarkan jumlah item
    if jumlah_item >= 10:
        diskon_jumlah = subtotal * 0.10
    elif jumlah_item >= 5:
        diskon_jumlah = subtotal * 0.05
    else:
        diskon_jumlah = 0
    # Baris 16: Setelah diskon jumlah
    total_setelah_diskon = subtotal - diskon_jumlah
    # Baris 19: Diskon member (tidak bisa digabung dengan voucher)
    if is_member and kode_voucher is None:
        diskon_member = total_setelah_diskon * 0.03
        total_setelah_diskon = total_setelah_diskon - diskon_member
    # Baris 24: Tambah PPN 11 persen
    ppn = total_setelah_diskon * 0.11
    total_dengan_ppn = total_setelah_diskon + ppn
    # Baris 28: Pembulatan ke atas ke kelipatan 100
    import math
    total_akhir = math.ceil(total_dengan_ppn / 100) * 100
    # Baris 32: Cek batas maksimal transaksi
    if total_akhir > 50000000:
        raise ValueError('Total melebihi batas maksimal transaksi')
    return total_akhir
