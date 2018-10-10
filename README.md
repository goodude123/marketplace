# marketplace
Marketplace/stock-exchange

Currency base project.

This project is about web site where you can check currency rates (mainly for PLN currency).
You can here check actually and past courses, see tables with most popular currencies, convert them,
check their rate history, diagrams rate in time and many more.

Running:
  python manage.py runserver --noreload 
  (--noreload flag is by apscheduler)

It uses exterior libraries/modules:
  - Django
  - BeautifulSoup4
  - requests
  - apscheduler
  

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