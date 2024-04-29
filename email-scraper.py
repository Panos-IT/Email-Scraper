from bs4 import BeautifulSoup
import requests
import requests.exceptions
import urllib.parse
from collections import deque
import re

# Request the target URL to scan from the user.
# Solicita al usuario la URL objetivo para escanear.
# Ζητάμε από τον χρήστη το URL που θέλει να σκανάρει.
# 请求用户输入要扫描的目标网址。
user_url = str(input('[+] Enter Target URL To Scan: '))

# Request the maximum number of URLs to scan from the user.
# Solicita al usuario el número máximo de URLs para escanear.
# Ζητάμε από τον χρήστη το πόσα URLs θέλει να σκανάρει.
# 请求用户输入要扫描的URL最大数量。
max_urls = int(input('[+] Enter Maximum Number of URLs to Scan: '))

# Initialize the URL deque with the given URL.
# Inicializa la cola de URLs con la URL dada.
# Αρχικοποιούμε την λίστα με τα URLs με το δοθέν URL.
# 使用给定的URL初始化URL双端队列。
urls = deque([user_url])

scraped_urls = set()
emails = set()

count = 0
try:
    while len(urls):
        count += 1
        if count == max_urls:
            break
        url = urls.popleft()
        scraped_urls.add(url)

        parts = urllib.parse.urlsplit(url)
        base_url = '{0.scheme}://{0.netloc}'.format(parts)

        path = url[:url.rfind('/')+1] if '/' in parts.path else url

        print('[%d] Processing %s' % (count, url))
        
        try:
            response = requests.get(url)
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            continue
        except requests.exceptions.InvalidURL:
            print("Invalid URL:", url)
            continue

        new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
        emails.update(new_emails)

        soup = BeautifulSoup(response.text, features="lxml")

        for anchor in soup.find_all("a"):
            link = anchor.attrs['href'] if 'href' in anchor.attrs else ''
            if link.startswith('/'):
                link = base_url + link
            elif not link.startswith('http'):
                link = path + link
            if not link in urls and not link in scraped_urls:
                urls.append(link)
except KeyboardInterrupt:
    print('[-] Closing!')

for mail in emails:
    print(mail)

# Instead of the last loop that prints emails, we add code to write them to a file.
# En lugar del último bucle que imprime los correos electrónicos, agregamos código para escribirlos en un archivo.
# Αντί για τον τελευταίο βρόχο που εκτυπώνει τα emails, προσθέτουμε κώδικα για εγγραφή σε αρχείο.
# 代替最后一个循环打印电子邮件，我们添加代码将它们写入文件。
with open('emails.txt', 'w') as f:
    for mail in emails:
        f.write(mail + '\n')

print("Emails extracted successfully and saved to 'emails.txt' file.")
