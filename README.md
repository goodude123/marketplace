# Stock Exchange

Stock Exchange is a web application created to display information about currencies and to operate on them in a basic way.

[Page Link](http://stock-exchange-mm.herokuapp.com/)

### Features
For users:
- currency converter
- currency valuation charts
- buy, sell options and own pocket for logged users

For owners:
- possibility to randomly generate currency values

### Future improves
- many currencies displayed on one chart
- more complicated actions on currencies

### Technologies
- Django
- BeautifulSoup4
- requests
- apscheduler
- djangorestframework

### Usage
## Project installation
- git clone http://github.com/michal-mietus/exchange
- cd stock-exchange
- python3 manage migrate

## Commands
- scrap --initial
  Should be called first, it collects all primary data about
  currencies like their names, abbrevations etc. and also
  current valuations.

- scrap --update
  This command scraps and save to database only current valuations with date of scraping.

- random
  Saves random generated currency values with current date to database.
