# Software Requirements and Design Document for Group 5, Version 1.0

## Authors:
Cameron Cornell  
Nicholas Green  
Joshua Kane  
Tyler Mihelich  
Robert Whitworth

## Overview:
Our system is focused on a game that is played in discord. More specifically, it will be a discord bot that is designed to be a wrapper for the game. 
It will be similar to the original system initially proposed. The system will still be used with discord.py, but it will now also include the nation states API.
The database system being used is PostgresSQL. The user will interact with the system through discord commands. 


## Functional Requirements
(1) /nation info (Priority: High) - Provides all information related to a specific Nation.

(2) /region info (Priority: High) - Provides all information related to a specific Region.

(3) /WA Info (Priority: High) - Provides all information related to a world assembly(the worlds governing body).


## Non-functional Requirements
Nationstates API has call limits - The requirement is placed by nationstates. Exceeding 50 requests per 30 seconds limit will temporailry lock the system.
Not yet enforced/implemented.

Encryption and Decryption of nations passwords - This requirement is needed for the user to access their nation/region and prevent others from accessing nations
they are not a part of. Currently being worked on, not fully implemented yet.


## Use Case Diagram
todo

## Class Diagram
todo

## Operating Environment 
The bot instance will be run by python and the user will interact with the bot through discord.
Any users operating system that can install discord will be able to use the bot. PostgreSQL.


## Assumptions and Dependencies 
todo
