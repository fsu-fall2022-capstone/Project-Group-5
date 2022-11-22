# Software Requirements and Design Document for Group 5, Version 1.0

## Authors:
> Joshua Kane, jdk10bn, CoderJoshDK  
> Robert Whitworth, rw18cg, rwhitwo  
> Nicholas Green, njg19, dynamic-friction  
> Tyler Mihelich, tpm18b, tpm18b  
> Cameron Cornell, cc19n, cameron-cornell 

## Overview:
Our system is focused on a game that is played in discord. More specifically, it will be a discord bot that is designed to be a wrapper for the game. 
It will be similar to the original system initially proposed. The system will still be used with discord.py, but it will now also include the nation states API.
The database system being used is PostgresSQL. The user will interact with the system through discord commands. 


## Functional Requirements
(1) /nation info (Priority: High) - Provides all information related to a specific Nation.

(2) /region info (Priority: High) - Provides all information related to a specific Region.

(3) /WA Info (Priority: High) - Provides all information related to a world assembly(the worlds governing body).


## Non-functional Requirements
Nationstates API has call limits - The requirement is placed by nationstates. Exceeding 50 requests per 30 seconds limit will temporarily lock the system.
Not yet enforced/implemented.

Encryption and Decryption of nations passwords - This requirement is needed for the user to access their nation/region and prevent others from accessing nations
they are not a part of. Currently being worked on, not fully implemented yet.


## Use Case Diagram
Basic uses cases implemented at the moment along with their relation with the user.  
![image](https://user-images.githubusercontent.com/72528884/197101853-2461ab8a-c372-407a-b2f3-598d105ed8db.png)


## Class Diagram
Sequence Diagram:

![image](https://user-images.githubusercontent.com/72528884/197253511-99552700-2fb8-493a-8997-ed752f955b3b.png)
  
Class Diagram:  
![image](https://user-images.githubusercontent.com/72528884/197253154-32e79f9e-6557-46d2-b372-81e8d4c95185.png)



## Operating Environment 
The bot instance will be run by python and the user will interact with the bot through discord.
Any users operating system that can install discord will be able to use the bot. PostgreSQL.  
The bot could be hosted on any VPS with python. 


## Assumptions and Dependencies 
We are using multiple third party wrappers. If the discord API changed, which it has in the past, it could cause issues for the longevity of our project. 
A similar idea is shared with the discord.py wrapper. We are dependent on the nationstates API to remain consistent so that calls and information stored will
remain working.