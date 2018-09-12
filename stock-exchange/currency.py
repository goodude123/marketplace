from request_handle import simple_get
from bs4 import BeautifulSoup
from datetime import datetime

class Currency:
    """ Simple currency class """

    def __init__(self, name, value, code, course, date):
        self.name = name
        self.value = value
        self.code = code
        self.course = course
        self.date = date
        

class Data:
    """ All scrapped data class """

    def __init__(self):
        """ Create empty data object """

        self.url = 'https://www.nbp.pl/home.aspx?f=/kursy/kursya.html'
        self.currencies = []


    def get_bs4(self):
        """ Creates bs4 html code model """

        raw_html = simple_get(self.url)
        bs4_html = BeautifulSoup(raw_html, 'html.parser')

        return bs4_html


    def get_currencies(self):
        """ Finds data in bs4 html, get contents and creates Currency models"""

        html = self.get_bs4()
        for table in html.findAll('table'):

            # find correct table
            if table.parent.get('id') == 'article':

                # iterate through table rows
                for tr in table.findAll('tr')[3:38]:
                    tds = tr.findAll('td')[:3]
                    args = []

                    # unpack content from table data
                    args.append(tds[0].contents[0]) # currency name
                    args.extend(tds[1].contents[0].split()) # unit and abbr
                    args.append(float(tds[2].contents[0].replace(',', '.'))) # rate
                    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S') # date
                    args.append(str(date)) 

                    self.currencies.append(Currency(*args))
                    
                    

if __name__ == '__main__':
    obj = Data()
    obj.get_currencies()
    for obj in obj.currencies:
        print(obj.name, obj.value, obj.code, obj.course, obj.date)
        
