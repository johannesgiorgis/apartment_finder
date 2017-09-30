from bs4 import BeautifulSoup
import requests
import sys

'''
link:
https://code.tutsplus.com/tutorials/scraping-webpages-in-python-with-beautiful-soup-the-basics--cms-28211
'''

def get_neighborhoods():

    sites = [
        'http://vanmag.com/best-of-the-city/vancouvers-best-and-worst-places-to-live/', 
        'https://www.airbnb.com/things-to-do/vancouver/sightseeing/neighborhood'
    ]
    web_page = 'https://www.airbnb.com/things-to-do/vancouver/sightseeing/neighborhood'

    req = requests.get(web_page)
    soup = BeautifulSoup(req.text, "lxml")
    print(soup.title)
    print(soup.title.name)
    print(soup.title.string)

    #print(dir(soup))
    for sub_heading in soup.find_all('h3'):
        print(sub_heading.text)


def get_skytrain_stations():
    web_page = 'https://en.wikipedia.org/wiki/List_of_Vancouver_SkyTrain_stations'

    req = requests.get(web_page)
    soup = BeautifulSoup(req.text, 'lxml')
    print(soup.title)
    print(soup.title.string)

    #for r in soup.find_all('table'):
    #    print(dir(r))
    #    print(r.text)
        #break

    stations = []
    table = soup.find('table', attrs={'class': 'wikitable sortable'})
    rows = table.findAll('tr')
    print('Rows:', len(rows))   
    for row in rows[1:]:
        #print(row)
        col = row.findAll('td')
        print(col[0].text)
        stations.append(col[0].text)

    print('Got {} stations:'.format(len(stations)))
    print(stations)

        #for td in cols:
        #    print(td.text)
        #print(type(cols), len(cols))
        #print(dir(cols))
        #print(cols[0])
    #print(rows)
    #print(dir(rows))
    #print(table)
    #print(dir(table))
    #rows = table.findAll('tr')


def main():
    #get_neighborhoods()
    get_skytrain_stations()


if __name__ == '__main__':
    main()

