# marketplace
Marketplace/stock-exchange

Currency base project.

This project is about web site where you can check currency rates (mainly for PLN currency).
You can here check actually and past courses, see tables with most popular currencies, convert them,
check their rate history, diagrams rate in time and many more.


It uses exterior libraries/modules:
  - Django
  - BeautifulSoup4
  - requests
  - apscheduler
  - djangorestframework
  
Repository download:
  git clone https://github.com/goodude123/marketplace.git
  
Environment installation:
  - python3 -m venv /path/to/new/virtual/environment
  - source /path/to/new/virtual/environment/bin/activate
  - pip3 install django
  - pip3 install bs4
  - pip3 install requests
  - pip3 install APScheduler
  - pip3 install djangorestframework

Running:
  python manage.py runserver --noreload 
  (--noreload flag is by apscheduler)

  

Django-admin custom commands:
  ./manage.py scrap (
    --new      scrap constant currency data like: name, abbreviation, unit of course
    --update   scrap courses and dates
  )
  
  ./manage.py random (
    creates random course and save it with current date
  )


Actions I had to do on server:
  - allow server host
  - replace static JavaScript files with CDN (they didn't work)
  - remove apscheduler (threads had been disabled)
  - enable venv before install outside packages
