Sainsburys Calorie counter tool
-------------------------------

Basically webscrapper which creates a pie chart representing the calorie distribution of items in a Sainsburys recept pdf.

Dockerized application which adds Selenium standalone for navigating the Sainsburys UK website to get calorie information of each item in the reciept.

To Run
------
Put your Sainsburys receipt in the app folder
clone the repo
run sudo docker-compose build
sudo docker-compose up

pie chart will be generated in the end in app folder


TBD
---

Improve speed through use of parellelization. Currently delays have been added between steps to avoid identification of selenium by the website.
This slows down the execution.


