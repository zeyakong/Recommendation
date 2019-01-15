# Recommendation_Django
Python recommendation Engine. The app uses Python Django framework to implement. 

## About This Project
This system chose 1619 restaurant samples which located in Wisconsin from the yelp data-set, which includes 26552 customers and 82510 reviews related to those restaurants. All of those are training data. 

The aim of this project is to develop a web application to do recommendation according to the those review and rating. This system will combine machine learning rating analysis and nature language processing to do the prediction.

## Get Started
Use git to clone 
```
git clone https://github.com/zeyakong/Recommendation_Django.git
```
or download the whole project zip file.  

### Required Environment
In order to run this app, your machine must have:  
* Python 3.6 or above [website](https://www.python.org/)
* Django 2.1 or above [website](https://www.djangoproject.com/)

and load the file into your IDE.

### Download the Dataset from Yelp
This app uses yelp acdamic data set. So you must download those date set at yelp's [official website](https://www.yelp.com/dataset)    
When you finiseh download, you should unpack those file and copy business.json, reviews.json and user.json into the project root folder $XXX/DjangoTest/  
### Load Data
This project uses Django default SQLite DB. In order to run this app with correct data. You should manually load the json data from what you downloaded before.  
Because those data cannot be loaded directly into Django SQLite DB, you have to execute the load python file when you are in the Django environment.
So, open the terminal and go to the project root path, try to execute:
```
$ Python manage.py shell
```
When you open your Django command line, and you can see the Django version number, which means now you can run Python file with the Django environment. So, try to run those file by the following order:
```
import loadbusi
import loadreview
import loaduser
import loaddata
```
Now you can run the Django server and go to you loaclhost to start the app!



