# Software Implementation and Testing Document for Group 5, Version 1.0

## Authors:
> Joshua Kane, jdk10bn, CoderJoshDK  
> Robert Whitworth, rw18cg, rwhitwo  
> Nicholas Green, njg19, dynamic-friction  
> Tyler Mihelich, tpm18b, tpm18b  
> Cameron Cornell, cc19n, cameron-cornell 

## Programming Languages:
The programming language we use for this project is Python.

## Platforms, APIs, Databases, and other technologies used:
APIs:
 * [discord.py](https://discordpy.readthedocs.io/en/latest/) - a discord bot
 * [NationStates](https://www.nationstates.net/pages/api.html) - connecting to the games DB and submitting actions to the game  

Databases:
 * [PostgreSQL](https://www.postgresql.org/)

## Execution-based Functional Testing:
We performed functional testing for our Discord bot by running the commands pertaining to the bot directly in Discord.  
We would run commands such as `/nation info` to confirm that the data requested was properly fetched. Proper display of commands and their options were also tested this way.   

## Execution-based Non-Functional Testing:
The NationStates API has its own rate limits: 50 calls/30s. Adherence to this limit has not been implemented yet. Password security was manually checked and reviewed for proper encryption. Stage is not yet implemented but, the functionality was tested in isolation.

## Non-Execution-based Testing:
Large sweeping changes require an all-hands walkthrough. Nothing (besides text related changes) is allowed to be directly pushed to main. All pull-requests have to be reviewed by the manager before merging. At least 1 other person should have a look at the code before a pull-request is made.
