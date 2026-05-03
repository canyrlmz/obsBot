# OBS Not Takip ve Telegram Bildirim Botu

Bu proje, Öğrenci Bilgi Sistemi (OBS) üzerindeki not listesini Selenium ve BeautifulSoup kullanarak belirli aralıklarla kontrol eder. Eğer mevcut notlarda bir değişiklik tespit edilirse, belirtilen Telegram hesabına anlık olarak bildirim gönderir.

## Özellikler

- Selenium tabanlı otomasyon ile dinamik iframe ve DOM kontrolü.
- BeautifulSoup ile tablo verisi ayrıştırma.
- Telegram API entegrasyonu ile anlık mesajlaşma.
- State takibi (Önceki durum ile mevcut durumu `json` formatında karşılaştırma).
- Hata durumlarında ekran görüntüsü alarak (`hata_ekrani.png`) çökme bildirimi gönderme.

## Kurulum ve Gereksinimler

Projeyi çalıştırmadan önce sisteminizde Python 3.8+ kurulu olmalıdır.

1. Repoyu klonlayın:
   ```bash
   git clone <repo-url>
   cd <repo-klasoru>
Gerekli kütüphaneleri yükleyin:

Bash

pip install requests beautifulsoup4 selenium python-dotenv
Çevre değişkenlerini (Environment Variables) yapılandırın:
Proje ana dizininde bir .env dosyası oluşturun ve içerisine aşağıdaki bilgileri kendi verilerinizle doldurun:

Kod snippet'i

TELEGRAM_BOT_TOKEN=botfather_uzerinden_aldiginiz_token
TELEGRAM_CHAT_ID=kendi_chat_id_numaraniz
BRAVE_BINARY_PATH=C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe
KONTROL_ARALIGI_SANIYE=300
Not: Eğer Brave dışında bir tarayıcı (örneğin standart Chrome) kullanacaksanız, koddaki options.binary_location kısmını kaldırabilir veya yolu Chrome'un kurulu olduğu dizine göre güncelleyebilirsiniz.

Kullanım
Terminal veya komut satırından botu başlatın:

Bash

python main.py
Otomatik olarak açılan tarayıcı penceresinden OBS sistemine manuel olarak giriş yapın.

Sol menüden Not Listesi sayfasına gidin.

Sayfa tamamen yüklendiğinde ve not tablosunu ekranda gördüğünüzde, terminale dönüp hazir yazarak Enter tuşuna basın.

Bot, .env dosyasında belirlediğiniz saniye aralığında (varsayılan: 300 saniye) sistemi kontrol etmeye başlayacaktır.

Uyarılar
.env ve notlar.json dosyalarını asla public bir depoya yüklemeyin. Projede bunu engellemek için .gitignore dosyası yapılandırılmıştır.

Bot çalışırken açılan tarayıcı penceresini kapatmayın.