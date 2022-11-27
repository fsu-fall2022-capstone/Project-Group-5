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

(4) Add nation (Priority: High) - Adds a user made nation.

(5) Remove nation (Priority: Medium) - Remove nation from the discord server it is currently in.

(6) Login (Priority: High) - Login to an existing Nationstates Nation. Authenticate and check againt Nationstates API for correct credentials. Only need to login once to use nation for future.

(7) Logout (Priority: Medium) - Logout of nation the discord server is currently logged in to.

(8) Configure (Priority: High) - Configure nation to choose what channel issues are sent to. Also used to configure how long the timeframe for issues is.

(9) Create issues (Priority: High) - Creates a random issue and provides variable amounts of options for the users of the Nationstates system.

(10) View issues (Priority: High) - Formats the issues from xml into a more readable format for the users.

(11) Vote on issues (Priority: High) - Allows the users to vote on issue options to decide what the nation will choose. 

## Non-functional Requirements
Nationstates API has call limits - The requirement is placed by nationstates. Exceeding 50 requests per 30 seconds limit will temporarily lock the system.
Not yet enforced/implemented.

Encryption and Decryption of nations passwords - This requirement is needed for the user to access their nation/region and prevent others from accessing nations
they are not a part of. Currently being worked on, not fully implemented yet.


## Use Case Diagram
Basic uses cases implemented at the moment along with their relation with the user.  
![ucase inc 2](https://user-images.githubusercontent.com/72528884/204110148-41b8bd66-544d-401b-8f23-59518866a3a2.png)


## Class Diagram
Sequence Diagram:

![sequence diagram without configure](https://user-images.githubusercontent.com/72528884/204078360-6f2adbcb-a538-4671-820b-7af4f73b0c8c.jpg)

  
Class Diagram:  
![inc2classdiagram](https://user-images.githubusercontent.com/72528884/203927568-9a5e07f1-b05a-49db-a8ef-b97f2efca40e.jpg)

## Operating Environment 
The bot instance will be run by python and the user will interact with the bot through discord.
Any users operating system that can install discord will be able to use the bot. PostgreSQL.  
The bot could be hosted on any VPS with python. 


## Assumptions and Dependencies 
We are using multiple third party wrappers. If the discord API changed, which it has in the past, it could cause issues for the longevity of our project. 
A similar idea is shared with the discord.py wrapper. We are dependent on the nationstates API to remain consistent so that calls and information stored will
remain working.
