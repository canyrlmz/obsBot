import time
import json
import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

# .env dosyasındaki ortam değişkenlerini yükle
load_dotenv()

# --- YAPILANDIRMA ---
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
KONTROL_ARALIGI_SANIYE = int(os.getenv("KONTROL_ARALIGI_SANIYE", 300))
TABLO_CSS_SELECTOR = "#grd_not_listesi"
DATA_FILE = "notlar.json"
# -------------------

if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    raise ValueError("TELEGRAM_BOT_TOKEN veya TELEGRAM_CHAT_ID ortam değişkenleri bulunamadı. Lütfen .env dosyanızı kontrol edin.")

def telegram_bildirim_gonder(mesaj):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mesaj, "parse_mode": "Markdown"}
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Telegram bildirim başarısız: {e}")

def load_previous_grades():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    return []
                return json.loads(content)
        except json.JSONDecodeError as e:
            print(f"JSON okuma hatası: {e}")
            return []
    return []

def save_grades(grades):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(grades, f, ensure_ascii=False, indent=4)

def parse_grades_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    table = soup.find('table', id='grd_not_listesi')
    if not table:
        table = soup if soup.name == 'table' else soup.find('table')
        
    grades = []
    if not table:
        return grades

    rows = table.find_all('tr')[1:] 
    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 5:
            ders_kodu = cols[1].text.strip()
            ders_adi = cols[2].text.strip()
            notlar = cols[4].text.strip().replace('\xa0', ' ')
            
            grades.append({
                'ders_kodu': ders_kodu,
                'ders_adi': ders_adi,
                'notlar': notlar
            })
    return grades

def tabloyu_bul_ve_icine_gec(driver):
    driver.switch_to.default_content()
    try:
        element = driver.find_element(By.CSS_SELECTOR, TABLO_CSS_SELECTOR)
        return element
    except Exception as e:
        print(f"Ana içerikte tablo bulunamadı, iframeler aranıyor... Detay: {e}")

    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    for index, iframe in enumerate(iframes):
        driver.switch_to.default_content()
        try:
            driver.switch_to.frame(iframe)
            element = driver.find_element(By.CSS_SELECTOR, TABLO_CSS_SELECTOR)
            return element 
        except Exception:
            continue 
            
    driver.switch_to.default_content() 
    return None

def bot_baslat():
    options = Options()
    
    # Standart Chrome kurulumlarında binary_location belirtmeye gerek yoktur.
    # Eğer özel bir dizin (örneğin portable Chrome) kullanılıyorsa aşağıdaki satırlar aktif edilebilir:
    # custom_chrome_path = os.getenv("CHROME_BINARY_PATH")
    # if custom_chrome_path:
    #     options.binary_location = custom_chrome_path
    
    options.page_load_strategy = 'eager'
    options.add_argument("--disable-blink-features=AutomationControlled") 
    options.add_argument("--disable-extensions") 
    options.add_argument("--disable-gpu") 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=options)

    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    try:
        driver.get("https://obs.karabuk.edu.tr/")
        print("1. Tarayıcı açıldı. Sisteme manuel olarak giriş yapın.")
        print("2. Sol menüden Not Listesi sayfasına gidin ve tabloyu görün.")
        print("3. Sayfa tamamen yüklendikten sonra bu terminale gelip 'hazir' yazın ve Enter'a basın.")
        
        while input().strip().lower() != 'hazir':
            print("Hatalı giriş. Başlamak için 'hazir' yazmalısınız.")

        print("Sistem başlatılıyor... Mevcut notlar analiz ediliyor.")
        
        ilk_tur = True

        while True:
            try:
                if not ilk_tur:
                    driver.switch_to.default_content()
                    driver.refresh()
                    time.sleep(2) 
                    
                    tablo_elementi = tabloyu_bul_ve_icine_gec(driver)
                    
                    if not tablo_elementi:
                        print("Tablo ekranda yok. Navigasyon deneniyor...")
                        driver.switch_to.default_content()
                        
                        ana_menu = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, "//a[contains(normalize-space(), 'Ders ve Dönem İşlemleri')]"))
                        )
                        driver.execute_script("arguments[0].click();", ana_menu) 
                        time.sleep(1)
                        
                        alt_menu = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, "//a[contains(normalize-space(), 'Not Listesi')]"))
                        )
                        driver.execute_script("arguments[0].click();", alt_menu)
                        time.sleep(3) 
                        
                        tablo_elementi = tabloyu_bul_ve_icine_gec(driver)
                        if not tablo_elementi:
                            raise Exception("Navigasyon yapıldı ancak tablo iframe içinde dahi bulunamadı.")

                else:
                    tablo_elementi = tabloyu_bul_ve_icine_gec(driver)
                    if not tablo_elementi:
                        raise Exception("İlk başlatmada tablo ekranda bulunamadı. Lütfen notlar sayfasındayken 'hazir' yazın.")

                tablo_html = tablo_elementi.get_attribute('outerHTML')
                current_grades = parse_grades_from_html(tablo_html)
                previous_grades = load_previous_grades()

                if not previous_grades:
                    print(f"[{time.strftime('%H:%M:%S')}] İlk referans notlar JSON'a kaydedildi. İzlemeye geçildi.")
                    save_grades(current_grades)
                else:
                    degisiklik_var = False
                    for current in current_grades:
                        matching_previous = next(
                            (prev for prev in previous_grades if prev['ders_kodu'] == current['ders_kodu']), 
                            None
                        )
                        
                        if matching_previous:
                            if current['notlar'] != matching_previous['notlar']:
                                degisiklik_var = True
                                mesaj = f"📚 *{current['ders_adi']}* ({current['ders_kodu']}) NOT AÇIKLANDI!\n\n"
                                mesaj += f"Eski: `{matching_previous['notlar']}`\n"
                                mesaj += f"Yeni: `{current['notlar']}`"
                                
                                print(f"\n{mesaj}")
                                telegram_bildirim_gonder(mesaj)
                    
                    if degisiklik_var:
                        save_grades(current_grades)

                ilk_tur = False
                    
            except Exception as e:
                driver.switch_to.default_content()
                driver.save_screenshot("hata_ekrani.png")
                hata_mesaji = f"\n!!! SİSTEM ÇÖKTÜ !!!\nMevcut URL: {driver.current_url}\nKlasöre 'hata_ekrani.png' kaydedildi.\nDetay: {e}\n"
                print(hata_mesaji)
                telegram_bildirim_gonder("Bot çöktü. Klasördeki 'hata_ekrani.png' dosyasını incele.")
                break 

            print(f"[{time.strftime('%H:%M:%S')}] Kontrol tamamlandı. Bekleniyor... ({KONTROL_ARALIGI_SANIYE} saniye)")
            time.sleep(KONTROL_ARALIGI_SANIYE)

    except KeyboardInterrupt:
        print("Kullanıcı tarafından durduruldu.")
    finally:
        driver.quit()

if __name__ == "__main__":
    bot_baslat()