<p align="center">
  <img src="https://github.com/mcgeorgiev/six_degrees/blob/master/six_degrees/static/img/logo.png"/>
</p>
# SixDegrees

--- 

# Description

SixDegrees is a game based on the idea of [six degrees of seperation](https://en.wikipedia.org/wiki/Six_degrees_of_separation). The idea is that all things living or not can be connected within six steps.

## How to play

[Click here to play](http://sixdegrees.pythonanywhere.com/)
![hashids](https://github.com/mcgeorgiev/six_degrees/blob/master/six_degrees/static/img/title.gif)
* Click on new game.
* You will be presented with your start and goal articles.
* Click on the first node to reveal your next possible choices.
* Progress through the game, clicking node by node until you get to your goal!
* You can zoom in and around the graph by using your mouse wheel, or pinching on mac!

[Play Six Degrees Game](http://sixdegrees.pythonanywhere.com/)

## Installation

1. Clone repository. [How to clone a repository](https://help.github.com/articles/cloning-a-repository/)
2. Enter a virtual environment.
3. [Install neo4j](https://neo4j.com/download/)
3. Install the requirements:
  
```cmd
$ pip install -r requirements.txt
```
#### Set up neo4j

1. register account
2. Leave password as default: ```neo4j```
3. Run neo4j;
4. Run the population scrip located in: six_degrees\six_degrees\game\graph_populate.py

```
$ python graph_populate.py
```
<br />

5. Run the program: six_degrees\six_degrees\manage.py

```
$ python manage.py runserver
```
<br />

6. Open local host: [open](http://127.0.0.1:8000)
---


#### Table of requirements:

| Software  | Version |
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
