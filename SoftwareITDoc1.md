# Software Implementation and Testing Document for Group 5, Version 1.0
## Authors:
### Cameron Cornell, Nicholas Green, Joshua Kane, Tyler Mihelich
## Programming Languages:
The programming language we will be using for this project is Python.
## Platforms, APIs, Databases, and other technologies used:
For this project, we are using [Discord API](discord.com) and [NationStates API](nationstates.net)
in order to develop a discord bot that allows you to play NationStates through Discord commands
## Execution-based Functional Testing:
We performed functional testing for out Discord bot by running the commands pertaining to the bot directly in Discord.
We would run commands such as `/nation info` in order to gather information of our nation that we created in the game,
as well as basic commands like `/example` and `sync *` in order to sync new attributes to your current guild in the game.
## Execution-based Non-Functional Testing:
Due to limitations of the NationStates API, we are only able to allow for up to 50 requests for the bot within 30 seconds.
To abide by this limitation, we implemented a rate limit of 40 and a limit reached function that causes the bot
to sleep for 0.1 milliseconds whenever 40 requests is reached.
## Non-Execution-based Testing:
For non-execution-based testing, we would review and discuss the NationStates API and Discord API together
in Discord, and then study each of these APIs individually on our own time.
