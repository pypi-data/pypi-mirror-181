import requests
from bs4 import BeautifulSoup

description = 'To get the latest earthquake in Indonesia from BKMG.go.id'

def ekstraksi_data():
    """
    Tanggal: 24 November 2022
    Waktu: 11:51:32 WIB
    Magnitudo: 3.8
    Kedalaman: 10 km
    Lokasi: LS=3.80 BT=128.50
    Pusat gempa: Pusat gempa berada di laut 30 km barat daya Maluku Tengah
    Dirasakan: Dirasakan (Skala MMI): I-II Ambon
    :return:
    """
    # mengambil data/konten halaman dari halaman situs bmkg.go.id
    # dan jika alamat salah/server mati maka munculkan pesan error
    try:
        content = requests.get('https://www.bmkg.go.id/')
    except (Exception,):
        return None

    # dan jika statusnya berhasil (kode 200)
    # maka tampilkan datanya menggunakan BeautifulSoup
    if content.status_code == 200:
        soup = BeautifulSoup(content.text, 'html.parser')

        # mengambil item waktu dari situs bmkg
        # dan menggunakan split itu memisahkan format
        result = soup.find('span', {'class': 'waktu'})
        result = result.text.split(', ')
        tanggal = result[0]
        waktu = result[1]

        # mengambil item lainnya dibawah class gempabumi-detail dan dibawah li (list item)
        result = soup.find('div', {'class': 'col-md-6 col-xs-6 gempabumi-detail no-padding'})
        result = result.findChildren('li')
        # hasil dari findChildren berupa array
        """
        i = 0
        for res in result:
            print(i, res)
            i = i + 1
        """
        # siapkan variabel untuk mengambil data lainnya
        i = 0
        magnitudo = None
        kedalaman = None
        ls = None
        bt = None
        lokasi = None
        dirasakan = None

        # looping data untuk membaca hasil dari scraping
        for res in result:
            if i == 1:
                magnitudo = res.text
            elif i == 2:
                kedalaman = res.text
            elif i == 3:
                koordinat = res.text.split(' - ')
                ls = koordinat[0]
                bt = koordinat[1]
            elif i == 4:
                lokasi = res.text
            elif i == 5:
                dirasakan = res.text

            i = i + 1

        # masukan datanya dalam variabel hasil
        hasil = dict()
        hasil['tanggal'] = tanggal
        hasil['waktu'] = waktu
        hasil['magnitudo'] = magnitudo
        hasil['kedalaman'] = kedalaman
        hasil['koordinat'] = {'ls': ls, 'bt': bt}
        hasil['lokasi'] = lokasi
        hasil['dirasakan'] = dirasakan
        return hasil
    else:
        return None


def tampilkan_data(result):
    # jika situs bmkg down, maka cetak pesan error
    if result is None:
        print("Tidak bisa menemukan data gempa terkini!")
        return

    # cetak hasilnya di aplikasi
    print('Gempa Terakhir berdasarkan BMKG')
    print(f"Tanggal {result['tanggal']}")
    print(f"Waktu {result['waktu']}")
    print(f"Magnitudo {result['magnitudo']}")
    print(f"Kedalaman {result['kedalaman']}")
    print(f"Koordinat LS={result['koordinat']['ls']}, BT={result['koordinat']['bt']}")
    print(f"Lokasi {result['lokasi']}")
    print(f"Dirasakan {result['dirasakan']}")


if __name__ == '__main__':
    print("Deskripsi package", description)
    result = ekstraksi_data()
    tampilkan_data(result)
