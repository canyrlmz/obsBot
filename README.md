OBS Not Takip ve Telegram Bildirim Botu
Bu bot, Karabük Üniversitesi Öğrenci Bilgi Sistemi (OBS) üzerindeki not tablosunu belirli aralıklarla kontrol eder ve yeni bir not açıklandığında veya mevcut not değiştiğinde Telegram üzerinden anlık bildirim gönderir.

Özellikler
Çift Tarayıcı Desteği: Google Chrome ve Brave Browser için optimize edilmiş ayrı betikler.

Dinamik İçerik Yönetimi: Iframe içinde gömülü olan tabloları otomatik tespit eder.

Güvenli Veri Saklama: API anahtarları ve kişisel veriler kod içinde değil, .env dosyasında tutulur.

Hata Yakalama: Çökme durumunda otomatik ekran görüntüsü alır ve Telegram üzerinden hata raporu gönderir.

State Yönetimi: Notları notlar.json dosyasında saklayarak yalnızca gerçek değişimleri bildirir.

Gereksinimler
Python 3.8 veya üzeri

Google Chrome veya Brave Browser

Telegram Bot Token ve Chat ID

Kurulum
Projeyi bilgisayarınıza indirin:

Bash

git clone <repo-url>
cd <repo-adi>
Gerekli kütüphaneleri yükleyin:

Bash

pip install requests beautifulsoup4 selenium python-dotenv
Hassas verileri yapılandırın:
Ana dizinde .env adında bir dosya oluşturun ve içeriğini şu şekilde doldurun:

Kod snippet'i

TELEGRAM_BOT_TOKEN=xxxxxxxxxx
TELEGRAM_CHAT_ID=xxxxxxxxx
# Sadece Brave kullanıcıları için (yol kurulumunuza göre değişebilir):
BRAVE_BINARY_PATH=D:\BraveSoftware\Brave-Browser\Application\brave.exe
KONTROL_ARALIGI_SANIYE=300
Kullanım
Kullandığınız tarayıcıya göre ilgili dosyayı çalıştırın:

Google Chrome Kullanıcıları
Terminale şu komutu girin:

Bash

python chrome_main.py
Açılan tarayıcıda OBS sistemine giriş yapın ve Not Listesi sayfasına gidin.

Tablo ekranda göründüğünde terminale dönüp hazir yazın.

Brave Browser Kullanıcıları
.env dosyasında BRAVE_BINARY_PATH yolunun doğru olduğundan emin olun.

Terminale şu komutu girin:

Bash

python brave_main.py
Açılan tarayıcıda OBS sistemine giriş yapın ve Not Listesi sayfasına gidin.

Tablo ekranda göründüğünde terminale dönüp hazir yazın.

Önemli Güvenlik Uyarıları
.env Dosyası: Bu dosya API anahtarlarınızı içerir. Asla GitHub veya benzeri platformlarda paylaşmayın. .gitignore dosyasında engellendiğinden emin olun.

notlar.json: İlk çalıştırmada bu dosya yoksa bot mevcut notlarınızı "referans" olarak kaydeder ve bir sonraki kontrolde bildirim göndermeye başlar.

Otomasyon Algılama: Bot, tarayıcıyı "AutomationControlled" özelliğini devre dışı bırakarak açar; ancak OBS sisteminin güvenlik politikaları değişirse manuel giriş yapmanız gerekebilir.

Dosya Yapısı
chrome_main.py: Standart Chrome kurulumları için çalışma betiği.

brave_main.py: Brave tarayıcısı kullananlar için özel binary yolu içeren betik.

notlar.json: Mevcut notların state bilgisini tutan dosya.

.env: Gizli yapılandırma ayarları.

hata_ekrani.png: Bot hata aldığında oluşan otomatik ekran görüntüsü.
