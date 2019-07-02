# Recommendation_Django
Python recommendation Engine. The app was implemented by Python Django framework. Live demo: [website](http://capstone.zeya.work)

## About This Project
This system chose 1619 restaurant samples which located in Wisconsin from the yelp data-set, which includes 26552 customers and 82510 reviews related to those restaurants. All of those are training data. 

The aim of this project is to develop a web application to do recommendation according to those review and rating. This system will combine machine learning rating-based algorithm such as collaborative filtering and nature language processing such as word2vec to do the prediction.

## Get Started
Use Git to clone 
```
git clone https://github.com/zeyakong/Recommendation.git
```
or download the whole project zip file.  

### Required Environment
In order to run this app, your machine must have:  
* Python 3.6 or above [website](https://www.python.org/)
* Django 2.1 or above [website](https://www.djangoproject.com/)

and load the file into your IDE.

### Download the Dataset from Yelp
This app uses yelp acdamic data set. So you must download those date set at yelp's [official website](https://www.yelp.com/dataset)    
When you finish downloading, you should unpack those file and copy business.json, reviews.json and user.json into the project root folder $XXX/DjangoTest/  
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
## Algorithms
This app uses collaborative filtering algorithm based on ratings and text reviews, which contains:  
### Similarity Calculation
* Euclidean Distance
* Cosine Similarity
* Pearson Similarity
### Natural language processing part
* word-of-bags
* TF-IDF
* Word2Vec
##### Google-News pre-trained neural network
##### gensim pre-trained neural network
* sentence2Vec / Doc2Vec
* [BERT](https://github.com/google-research/bert)

# Conclusion
the mean absolute error of text-based recommendation is better than the rating-based. The reason is the data matrix we generated is a sparse matrix, which means some restaurants don’t have too many reviews. We cannot give a precise recommendation without enough rating information. But because each review has some texts to read, the system can try to understand the text review and use this information to give more precise result. 
# Future work
* Sparse matrix problem
* Big data processing



