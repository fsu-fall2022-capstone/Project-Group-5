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
We would run commands such as `/nation info` to confirm that the data requested was properly fetched. Proper display of commands and their options were also 
tested this way. We have since included the `/add_nation` command in order to bring up a login/ create a new nation button, as well as a sync function 
`@Nation States sync [~ |* | ^]` that allows for the global sync of a users nation, a copy of all global commands to the current guild then syncing, and the 
removal of guild commands. `/configure` allows you to configure your nation in the context of receiving issues and sending them to specific channels within the 
discord server. The user is able to determine when they want their issue vote to be received by their nation, between 1 and 24 hours. These issues that are sent 
to the user are sent hourly, with an image of the newspaper issue that is being addressed shown to the user when sent, along with a thread that allows the user 
to pick their option for the issue. The `/region info` command and `/wa info` command allow you to access their respective shards that are provided by the Nation States 
website in order to play the game. The shards for nation and world assembly from the website have also been implemented for the user to access through Nation States.

## Execution-based Non-Functional Testing:
The NationStates API has its own rate limits: 50 calls/30s. Password security was manually checked and reviewed for proper encryption. A gzip file taken 
directly from the Nation States API has been implemented, allowing the bot to gather information from it in order to determine options and issues for the user.
There is a slight bug with this gzip, however, being that the bot does not have enough time to gather the information from the dictionary sometimes upon load 
up. We have added tables to the PostgreSQL database in regards to storing the referenced nations, as well as creating a new table to a newly created nation. 
More tables will be made in the future. Images for the issues provided to the user have been created, but there is now way of calling for the user's nation 
issues yet.

## Non-Execution-based Testing:
Large sweeping changes require an all-hands walkthrough. Nothing (besides text related changes) is allowed to be directly pushed to main. All pull-requests have to be reviewed 
by the manager before merging. At least 1 other person should have a look at the code before a pull-request is made.
