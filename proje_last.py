from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def driver_maker():
    chrome_options=Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.deepl.com/tr/translator")
    return driver

driver=driver_maker()

# cevirilecek dosyanın ve cevirinin yazılmasını ıstedıgın konumları ayarla asagıda

with open(r"C:\Users\Hayri^\Desktop\cevirilecekmetinler\sexx.txt", "r", encoding="utf-8") as f, \
        open(r"C:\Users\Hayri^\Desktop\cevirilmismetinler\pat.txt", "w", encoding="utf-8") as w:
    buffer_size = 750
    son = ""

    while True:
        #cevirilecek metin dosyasını okuyup ceviriye gonderilmeye uygun sekılde ayrıstırır
        data = f.read(buffer_size)
        if "." in data:
            bas = data.rsplit(".", 1)[0]
            post_to_trnslt = son + bas
            son = data.rsplit(".", 1)[1]
        else:
            post_to_trnslt = data
        if not data:
            break

        #işlem sırasında ortaya cıkabilen staleelement  nointeractableelement ve
        #ınvalıdelementsstate exceptionlarına karşı bekleme
        #süreleriyle önlem alınsada paslanan datanın çevirisinin bi şekilde gerçekleştirilemediği durumlar için
        #4 deneme hakkı tanıdım
        for i in range(4):
            #deepl ceviri sayfasındaki metin kutusunu tespit eder
            try:
                text_box = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div[contenteditable='true'][role='textbox']"))
                )
                # metin kutusuna cevirilecek datayı paslar
                text_box.send_keys(post_to_trnslt)

                time.sleep(1.5)

                #html den metinleri iceren elemetleri toplar
                elements = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".--l.--r.sentence_highlight"))
                )
                # elementlerden cevirilmis kısmı iceren son yarısının textini dosyaya yazar(abi orjinal metnin ve cevirilmis
                # metnin sınıf degerleri aynı oldugu ıcın ıkısını de ıceren elementlerı topluyor son yarısı turkce onları aldım
                for element in elements[int(len(elements) / 2):]:
                    w.write(element.text)

                try:
                    text_box.clear()
                except Exception:
                    pass

                break

            except Exception:
                driver.quit()
                driver=driver_maker()
                continue

        #burda deneme hakları biterse mevcut datanın çevirilemediğini ve sonraki adıma geçileceğini bildiriyor
        if i == 3:
            print("bu parçaçığın çeviri işlemi gerçekleştirilemedi,program sonraki parçacıklarla devam edecektir")

driver.quit()
print("işlem bitti")
















