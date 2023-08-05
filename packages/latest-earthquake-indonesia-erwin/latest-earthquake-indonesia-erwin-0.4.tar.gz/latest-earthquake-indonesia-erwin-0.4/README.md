# Latest Indonesia EarthQuake
This package will get the latest earthquake from BMKG | Meteorology, Climatology, and Geophysical Agency

## HOW IT WORK?
This package will scrape from [BMKG](https://bmkg.go.id) to get latest quake happened in Indonesia.

This package will use BeautifulSoup4 and Request, to produce output in the form of JSON that is ready to be used in web or mobile application.

## HOW TO USE
```
import gempaterkini

if __name__ == '__main__':
    print('Aplikasi Utama')
    result = gempaterkini.ekstraksi_data()
    gempaterkini.tampilkan_data(result)
```

# Author
Erwin Zulfikar