  <h1 align="center">SixDegrees</h1>

<p align="center">
  <img src="https://github.com/mcgeorgiev/six_degrees/blob/master/six_degrees/static/img/logo.png"/>
</p>

## Description

SixDegrees is a game based on the idea of [six degrees of seperation](https://en.wikipedia.org/wiki/Six_degrees_of_separation). The idea is that all things living or not can be connected within six steps.

## How to play

[How to play](http://sixdegrees.pythonanywhere.com/how-to-play/)
![hashids](https://github.com/mcgeorgiev/six_degrees/blob/master/six_degrees/static/img/title.gif)
* Click on new game.
* You will be presented with your start and goal articles.
* Click on the first node to reveal your next possible choices.
* Progress through the game, clicking node by node until you get to your goal!
* You can zoom in and around the graph by using your mouse wheel, or pinching on a laptop touch pad!

[Click here to play](http://sixdegrees.pythonanywhere.com/)

## Installation

#### 1. Clone repository. [How to clone a repository](https://help.github.com/articles/cloning-a-repository/)
#### 2. Enter a virtual environment.
#### 3. There are two methods. Using local hosted database or cloud hosted graph database. We recommend using the hosted version. Step 3.1 applies only to eduroam.
####  3.1. To use eduroam you must [Install neo4j](https://neo4j.com/download/) and change lines 7 - 9 in the six_degrees/six_degrees/game/graph.py to look like the follwing code:

```
def connection():
    return GraphDatabase("http://localhost:7474/db/data/", username="neo4j", password="password")
    #return GraphDatabase("http://hobby-ekngppohojekgbkepjibeaol.dbs.graphenedb.com:24789/db/data/", username="testing-user", password = "b.SIxCtcPc51R5.aaW8WZa65LdsjGgZ")

```

### Set up neo4j

+ register account
+ Change password to: ```password```
+ Run neo4j;
+ Run the population script located in: six_degrees/six_degrees/game/populate_graph.py

```
$ python populate_graph.py
```
**IMPORTANT: this script may take 40-50 minutes to populate the database!**

####    4. Run the population script located in: six_degrees/six_degrees/population_script.py

```
$ python population_script.py
```
<br />

#### 5. Install the requirements:
  
```cmd
$ pip install -r requirements.txt
```

#### 6. Run the program: six_degrees\six_degrees\manage.py

```
$ python manage.py runserver
```
<br />

#### 7. Open local host: [open](http://127.0.0.1:8000)
---


### Table of requirements:

| Package  | Version |
| ------------- | ------------- |
| beautifulsoup4  | 4.5.3  |
| Django  | 1.10.6  |
|    neo4j-driver     |    1.1.2     |
|    neo4jrestclient     |    2.1.1     |
|    py2neo     |    3.1.2    |
|    requests     |    2.4.3     |
|    wheel     |   0.24.0     |
|    django-registration-redux     |    1.4     |
|    Pillow     |   4.0.0     |

---
#### Note:
For more reliable quality rendering don’t use safari browser, the pixilation does not always render due to sigma.
