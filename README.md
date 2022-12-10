# Nation States

# A discord bot designed to be a wrapper for the online game [nationstates](nationstates.net). 

## How to use
Run the command `add_nation` and follow the prompt to assign a nation to a server. You can then configure that nation. Afterwards, you the bot will send new issues to the server. The members can vote on how the nation should respond and after enough time passes, the bot will pass the voted for legislation. Changes in the game state will be expressed to through the bot.   
You can also get data about a specific nation, region, and world assembly.

## Implemented Commands
 * nation
    * info \<nation> [shard]
 * region
    * info \<region> [shard]
 * wa
    * info \<General Assembly | Security Council> [shard]
 * add_nation
 * remove_nation
 * configure

## Personal Hosting

[Install wand](https://docs.wand-py.org/en/0.6.10/guide/install.html#install-imagemagick)
```cmd
$ pip3 install -r requirements.txt
```

Next, create a `.env` file and fill it with the secretes. The needed secretes are `TOKEN` and `ENCRYPTION_KEY`. The others are optional.
