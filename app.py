from openai import OpenAI
client = OpenAI()
from pdfquery import PDFQuery

import requests
from bs4 import BeautifulSoup

word = 'dog'
url = 'https://www.google.com/search?q={0}&tbm=isch'.format(word)
content = requests.get(url).content
soup = BeautifulSoup(content,'lxml')
images = soup.findAll('img')

image = images[1]
test_str=image.replace("src=","*")
test_str=image.replace("/>","*")
re=test_str.split("*")
res=re[1]
print(res)



