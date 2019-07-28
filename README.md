# Instructions to use and test womenmentors.co
Hi! Welcome to womenmentors.co! The mission of this website is to enable women in STEM fields to grow and develop. This will enable more diversity and more representation of women in tech.  

The tech stack of womenmentors.co is : 
1) Vue.js, JavaScript, Bootstrap 4, HTML and CSS for front-end
2) Python with libraries Flask, Jinja, tweepy, nltk at the back-end
3) Heroku for hosting the site, CloudFlare for SSL protection, and NameCheap for domain registration. 
4) PostgreSQL and Firebase for databases
5) Twitter API and Microsoft Face API 
6) Git for version control 

## Testing via Local Script `unit_tests.py`
If you just want to use it as a product, just go to womenmentors.co. For testing and running it locally, follow these steps: 
1) First `git clone` this repository women-mentors in your local computer
1) Create virtual environment (using say `pyenv` ) and run it
2) Run `pip install -r requirements.txt` - this will install requirements 
3) Install PostgreSQL 11 (I used it with v2.2.4) from https://postgresapp.com
4) Type `$psql` and then create database using`create database test` and then type `exit`
5) Run `nosetests unit_tests.py` - it will run unit tests locally 

## Running Locally
To run locally run`python run.py` and go to [127.0.0.1:5000](127.0.0.1:5000)

Hope you can find a mentor of your own!

### Credits:
A lot of the work done here was possible through amazing tutorials available online:

Flask Tutorial: https://coreyms.com/development/python/python-flask-tutorials-full-series

Vue JS Tutorial: https://www.youtube.com/playlist?list=PL4cUxeGkcC9gQcYgjhBoeQH7wiAyZNrYa

Bootstrap: W3Schools https://www.w3schools.com/bootstrap4/default.asp
           PluralSight https://www.pluralsight.com/courses/code-school-blasting-off-with-bootstrap
