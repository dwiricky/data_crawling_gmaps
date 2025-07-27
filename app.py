from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# Setup Chrome
options = Options()
options.add_argument('--headless')
# options.add_argument('--disable-gpu')
# options.add_argument('--window-size=1920x1080')
driver = webdriver.Chrome(options=options)

# Daftar URL yang ingin di-scrape
urls = [
"https://www.google.com/maps/place/Danau+Toba/@2.611404,98.5062874,10z/data=!4m8!3m7!1s0x3031de07a843b6ad:0xc018edffa69c0d05!8m2!3d2.7860786!4d98.6160674!9m1!1b1!16zL20vMDRuNGY?entry=ttu&g_ep=EgoyMDI1MDYyMy4yIKXMDSoASAFQAw%3D%3D"
"https://www.google.com/maps/place/Bukit+Holbung+Samosir/@2.5303677,98.6953207,17z/data=!4m8!3m7!1s0x3031da4bba9d523f:0xf1e39423315c1cfc!8m2!3d2.5303623!4d98.6978956!9m1!1b1!16s%2Fg%2F11fyx7qq1b?entry=ttu&g_ep=EgoyMDI1MDYyMy4yIKXMDSoASAFQAw%3D%3D"
"https://www.google.com/maps/place/Puncak+Huta+Ginjang/@2.3148037,98.970669,17z/data=!4m8!3m7!1s0x302e1b004ec44d39:0x4b9efd3592a526fc!8m2!3d2.3148412!4d98.9710016!9m1!1b1!16s%2Fg%2F11cs1kl5y2?entry=ttu&g_ep=EgoyMDI1MDYyMy4yIKXMDSoASAFQAw%3D%3D"
"https://www.google.com/maps/place/Pulau+Samosir/@2.5944389,98.2470688,10z/data=!4m8!3m7!1s0x3031e8022c23c201:0x9e185a1f1c3da745!8m2!3d2.6273112!4d98.7922018!9m1!1b1!16zL20vMDJqZHl0?entry=ttu&g_ep=EgoyMDI1MDYyMy4yIKXMDSoASAFQAw%3D%3D"
"https://www.google.com/maps/place/Desa+Wisata+Tomok+Parsaoran/@2.6518037,98.8584802,17z/data=!4m8!3m7!1s0x3031e9ba15354255:0xc2c6218271f054a5!8m2!3d2.6517983!4d98.8610551!9m1!1b1!16s%2Fg%2F11mvlmmp9f?entry=ttu&g_ep=EgoyMDI1MDYyMy4yIKXMDSoASAFQAw%3D%3D"
"https://www.google.com/maps/place/Museum+Batak+T.B.+Silalahi+Center/@2.3332099,99.0458419,17z/data=!4m8!3m7!1s0x30314bcb41946ac1:0xb21059a51abb5794!8m2!3d2.3332045!4d99.0484168!9m1!1b1!16s%2Fg%2F1hg0b0v7s?entry=ttu&g_ep=EgoyMDI1MDYyMy4yIKXMDSoASAFQAw%3D%3D"
"https://www.google.com/maps/place/Air+Terjun+Sipisopiso/@2.9164927,98.5169289,17z/data=!4m8!3m7!1s0x3031ad70b69431e9:0x8d2b0d8b4069f47f!8m2!3d2.9164873!4d98.5195038!9m1!1b1!16s%2Fg%2F11c1g6qdhc?entry=ttu&g_ep=EgoyMDI1MDYyMy4yIKXMDSoASAFQAw%3D%3D"
"https://www.google.com/maps/place/Bukit+Sibeabea/@2.5506755,98.6710138,17z/data=!4m8!3m7!1s0x3031db06803ec9f5:0xc95cb1fb76492ad6!8m2!3d2.5506701!4d98.6735887!9m1!1b1!16s%2Fg%2F11rgg_wcd1?entry=ttu&g_ep=EgoyMDI1MDYyMy4yIKXMDSoASAFQAw%3D%3D"
]

# Fungsi untuk melakukan scraping pada satu URL
def scrape_reviews(url):
    driver.get(url)
    time.sleep(5)

    # Klik tombol More Reviews jika ada
    try:
        more_reviews = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Ulasan lainnya') or contains(text(), 'More reviews')]/ancestor::button"))
        )
        more_reviews.click()
        print(f"[INFO] Klik tombol More reviews untuk {url}.")
        time.sleep(3)
    except:
        print(f"[INFO] Tidak ada tombol More reviews di {url}.")

    # Loop scroll berdasarkan elemen terakhir
    reviews_data = []
    seen_reviews = set()
    scroll_attempt = 0
    max_scroll_attempts = 200
    print(f"[INFO] Mulai scroll untuk {url}...")

    while scroll_attempt < max_scroll_attempts and len(reviews_data) < 50:
        # Ambil semua container review
        review_containers = driver.find_elements(By.CSS_SELECTOR, 'div.jftiEf')

        for container in review_containers:
            try:
                username = container.find_element(By.CLASS_NAME, 'd4r55').text.strip()
            except:
                username = 'Unknown'

            try:
                review = container.find_element(By.CLASS_NAME, 'wiI7pd').text.strip()
            except:
                review = ''

            try:
                rating_element = container.find_element(By.CLASS_NAME, 'kvMYJc')
                rating = rating_element.get_attribute('aria-label').split()[0]  # contoh: "2 stars"
            except:
                rating = 'Unknown'

            # Cek duplikat review
            unique_key = (username, review)
            if review and unique_key not in seen_reviews:
                seen_reviews.add(unique_key)
                reviews_data.append({
                    'user': username,
                    'review': review,
                    'rating': rating
                })

        # Scroll ke bawah dengan elemen terakhir
        if review_containers:
            driver.execute_script("arguments[0].scrollIntoView();", review_containers[-1])
        else:
            print(f"[INFO] Tidak ada container review ditemukan untuk {url}.")
            break

        print(f"[INFO] Total ulasan terkumpul untuk {url}: {len(reviews_data)}")
        time.sleep(2)
        scroll_attempt += 1

        if len(reviews_data) >= 50:
            print(f"[INFO] Sudah mencapai 50 ulasan untuk {url}, berhenti scrolling.")
            break

    # Cetak hasil
    print(f"\n=== Hasil Ulasan untuk {url} ===")
    for i, item in enumerate(reviews_data[:50], 1):
        print(f"{i}. User: {item['user']}")
        print(f"   Rating: {item['rating']}")
        print(f"   Review: {item['review']}\n")

    # Simpan ke CSV
    df = pd.DataFrame(reviews_data)
    file_name = f"ulasan_{url.split('/')[-1].split('?')[0]}.xlsx"
    df.to_excel(file_name, index=False)
    print(f"[INFO] Data berhasil disimpan ke '{file_name}'.")

# Loop untuk memproses banyak URL
for url in urls:
    scrape_reviews(url)

driver.quit()
