import pandas as pd
import requests
from bs4 import BeautifulSoup

def get_page(url):
    res = requests.get(url)
    if not res.ok:
        print('server responded: ', res.status_code)
    else:
        soup = BeautifulSoup(res.content, 'html.parser')
    return soup

def howTodata(soup):
  if soup.find('span', class_ ="mw-headline").text.strip() != 'Steps':
    pass
  else:
    a = [i.get_text().strip() for i in soup.find_all('div', class_ = 'step')]
    images = [i.find('img').attrs.get('data-src') for i in soup.find_all('a', class_ = 'image')]
    img_link = dict()
    steps = dict()
    for i in range(len(images)):
      img_link[i+1] = images[i]
    for i in range(len(a)):
      steps[i] = a[i]
    # for (key, value), (key1, value1) in zip(steps.items(), img_link.items()):
    #   print('Step', key1,': '+value.strip())
    #   print('Image URL: ', value1, '\n')
    total_data = pd.DataFrame({
      'Steps': a,
      'Image URL': images,
    })
    print(total_data)
    total_data.to_csv('data.csv')


def get_detail_data(soup):
    #title
    try:
      title = soup.find('h1', id="section_0").find('a').get_text()
    except:
      title = ''
    #description
    try:
      d = soup.find('div', id="mf-section-0").find('p').get_text()
    except:
      d = ''

    data  = {
      'Title': title,
      'Description': d
    }
    for key, value in data.items():
      print(key,':',value)

def main():
    url = 'https://www.wikihow.com/Increase-Concentration-Level'
    get_detail_data(get_page(url))
    howTodata(get_page(url))

if __name__ == "__main__":
    main()