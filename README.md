# six_degrees of Wikipedia Game - Design Specification
___
### 1. Overview (1 slide)

**Short explanation of six degrees of seperation game**

**What makes the game cool/unique/useful/valuable?**
- Streamlined version of the approach
- Stramlined procrastination
- Leaderboards
- Test your obscure knowledge

___
### 2. User Personas (2-3 slides)
( give a sense of what the user wants)

- Serial student procrastinator
- Receptionists...?
- Pub quizzers

___
### 3. Requirements (1 slide)
(MoSCoW)


- User can log in and register for an account. M
- Users can be assigned a randomly selected node source and destination. M
- Users are scored on the path they take. M
- Users can select different article nodes to traverse the network M
- Users can play a single player game M

- Users can see the ideal "route" between articles S
- Users can see a leaderboard of high scores and other player game statistics. S
- Users can view their game history. S

- User can see a visual network representation of their path. C
- Users can be assigned a predefined "mission" to complete. C

- Users can join a multiplayer game against other users. W


___
### 4. High Level System Architecture Diagram (1 slide)
![alt text](https://github.com/mcgeorgiev/six_degrees/blob/master/high_level.png "High Level Diagram")

___
### 5. ER Diagram (1 slide)
(with description of the attributes of each entity)

___
### 6. Wireframes (2-5 slides)
(to show main functionality of the system)
- Login functionality/ Home
- High Scores
- In game
- Winning
___
### 7. Walkthrough (1-2 slides)
(site map/ urls)
___


Michaels thoughts:
- Once a users is playing a game we could 

###### Socket/Event/RealTime programming:
- My first thoughts for implementing multiplayer would be to use socket programming. For example like in a chat server. Vanilla Django does not have the functionality built in, meaning for every event we would have to send a GET or POST to a server, but there are modules which can change this. 
- If we had a seperate game server we could run it with Node.js and poll it from the django app when we have sockets implemented

https://github.com/tamasgal/django-tornado
https://blog.heroku.com/in_deep_with_django_channels_the_future_of_real_time_apps_in_django

#### Links:
http://degreesofwikipedia.com/

###### Node/Network Diagram:
http://visjs.org/network_examples.html
http://sigmajs.org/


