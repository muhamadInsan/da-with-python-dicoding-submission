# diCommerce Dashboard
A dashboard to visualize the e-commerce public datasets. The dashboard was created to fulfill the requirements submitted at the [dicoding.com](https://www.dicoding.com/academies/555/corridor) courses.

## What information will you get from the dashboard

 - Visualize the states and cities of the customer
 - Product categories with the largest order
 - Score review of each of the product categories
 - Visualize of order statuses
 - Visualize of RFM (Recency, Frequency, Monetary) analysis 

## Prerequisite
- [Python (pandas, jupyter, plotly)](https://docs.python.org/)
- [Streamlit (installation, deployment)](https://docs.streamlit.io/)
- [Containerize (Docker)](https://docs.docker.com/)
- Extract, Transform, Load (ETL)

## How to run
### Clone Source Code
Clone source code from [github](https://www.github.com)
```
$ mkdir app
$ clone https://github.com/muhamadInsan/da-with-python-dicoding-submission.git
$ cd app
```
### Setup Environment
I use pip to set up my environment (env), please use set up env that makes you easier.
For windows:
```
$ pyhton -m venv <env-name>
$ <env-name>\scripts\activate
```
For Unix/Linux
```
$ pyhton3 -m venv <env-name>
$ source <env-name>/bin/activate
```
### Run App
```
$ docker-compose up
```
Enjoy !!
#

Written by me with [StackEdit](https://stackedit.io/).
