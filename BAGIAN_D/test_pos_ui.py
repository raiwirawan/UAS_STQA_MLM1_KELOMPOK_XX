from playwright.sync_api import Page, expect


BASE_URL = "http://localhost:3000/pos-kasir.html"


# =====================================================
# PAGE OBJECT MODEL
# =====================================================

class KasirPage:

    def __init__(self, page: Page):
        self.page = page

    def buka(self):
        self.page.goto(BASE_URL)

    def tambah_produk(self, kode, qty):
        self.page.fill("#kode-produk", kode)
        self.page.fill("#jumlah-item", str(qty))
        self.page.click("#tombol-tambah")

    def pilih_tunai(self):
        self.page.click("#metode-tunai")

    def pilih_kartu(self):
        self.page.click("#metode-kartu")

    def isi_uang(self, nominal):
        self.page.fill("#uang-tunai", str(nominal))

    def isi_pin(self, pin):
        self.page.fill("#pin-kartu", pin)

    def bayar(self):
        self.page.click("#tombol-bayar")


# =====================================================
# TC01
# Tambah item valid
# =====================================================

def test_tambah_item_valid(page: Page):
    page.goto(BASE_URL)

    page.fill("#kode-produk", "BV123456")
    page.fill("#jumlah-item", "3")
    page.click("#tombol-tambah")

    expect(page.locator("#success-produk")).to_be_visible()

    expect(page.locator("#success-produk-text")).to_contain_text(
        "berhasil ditambahkan"
    )


# =====================================================
# TC02
# Format kode produk salah
# =====================================================

def test_format_kode_produk_salah(page: Page):
    page.goto(BASE_URL)

    page.fill("#kode-produk", "ABC")
    page.fill("#jumlah-item", "1")
    page.click("#tombol-tambah")

    expect(page.locator("#error-produk")).to_be_visible()

    expect(page.locator("#error-produk-text")).to_contain_text(
        "Format kode produk tidak valid"
    )


# =====================================================
# TC03
# Produk tidak ditemukan
# =====================================================

def test_produk_tidak_ditemukan(page: Page):
    page.goto(BASE_URL)

    page.fill("#kode-produk", "ZZ999999")
    page.fill("#jumlah-item", "1")
    page.click("#tombol-tambah")

    expect(page.locator("#error-produk")).to_be_visible()

    expect(page.locator("#error-produk-text")).to_contain_text(
        "tidak ditemukan"
    )


# =====================================================
# TC04
# Diskon qty 5%
# =====================================================

def test_diskon_qty_5_persen(page: Page):
    page.goto(BASE_URL)

    page.fill("#kode-produk", "BV123456")
    page.fill("#jumlah-item", "5")
    page.click("#tombol-tambah")

    expect(page.locator(".badge-diskon")).to_be_visible()

    expect(page.locator(".badge-diskon")).to_contain_text(
        "-5%"
    )


# =====================================================
# TC05
# Voucher expired
# =====================================================

def test_voucher_expired(page: Page):
    page.goto(BASE_URL)

    page.fill("#kode-voucher", "OLDVOUCH")
    page.click("#tombol-voucher")

    expect(page.locator("#error-voucher")).to_be_visible()


# =====================================================
# TC06
# Voucher + member tidak boleh digabung
# =====================================================

def test_voucher_dan_member_tidak_boleh_bersamaan(page: Page):
    page.goto(BASE_URL)

    # checkbox hidden, aktifkan via JavaScript
    page.evaluate("""
        document.getElementById('toggle-member').checked = true;
        hitungUlang();
    """)

    page.fill("#kode-voucher", "SAVE5RIB")
    page.click("#tombol-voucher")

    expect(page.locator("#error-voucher")).to_be_visible()

    expect(page.locator("#error-voucher-text")).to_contain_text(
        "diskon member"
    )


# =====================================================
# TC07
# Pembayaran tunai berhasil
# =====================================================

def test_pembayaran_tunai_berhasil(page: Page):
    page.goto(BASE_URL)

    page.fill("#kode-produk", "BV123456")
    page.fill("#jumlah-item", "2")
    page.click("#tombol-tambah")

    page.click("#metode-tunai")

    page.fill("#uang-tunai", "100000")

    page.click("#tombol-bayar")

    expect(page.locator("#overlay-struk")).to_be_visible()


# =====================================================
# TC08
# PIN kartu salah
# =====================================================

def test_pin_kartu_salah(page: Page):
    page.goto(BASE_URL)

    page.fill("#kode-produk", "BV123456")
    page.fill("#jumlah-item", "1")
    page.click("#tombol-tambah")

    page.click("#metode-kartu")

    page.fill("#pin-kartu", "000000")

    page.click("#tombol-bayar")

    expect(page.locator("#error-kartu")).to_be_visible()

    expect(page.locator("#error-kartu-text")).to_contain_text(
        "PIN kartu salah"
    )


# =====================================================
# TC09
# Tombol bayar disabled saat keranjang kosong
# =====================================================

def test_tombol_bayar_disabled_saat_keranjang_kosong(page: Page):
    page.goto(BASE_URL)

    expect(page.locator("#tombol-bayar")).to_be_disabled()


# =====================================================
# TC10
# Batal transaksi mengosongkan keranjang
# =====================================================

def test_batal_transaksi(page: Page):
    page.goto(BASE_URL)

    page.fill("#kode-produk", "BV123456")
    page.fill("#jumlah-item", "2")
    page.click("#tombol-tambah")

    page.click("#tombol-batal")

    expect(page.locator("#display-total")).to_have_text("Rp 0")

    expect(page.locator("#status-jumlah-item")).to_have_text("0")


# =====================================================
# POM TEST
# =====================================================

def test_pom_tambah_produk(page: Page):
    kasir = KasirPage(page)

    kasir.buka()
    kasir.tambah_produk("BV123456", 2)

    expect(page.locator("#success-produk")).to_be_visible()


def test_pom_pembayaran_tunai(page: Page):
    kasir = KasirPage(page)

    kasir.buka()

    kasir.tambah_produk("BV123456", 2)

    kasir.pilih_tunai()

    kasir.isi_uang(100000)

    kasir.bayar()

    expect(page.locator("#overlay-struk")).to_be_visible()