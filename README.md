# Discord Text Spacer Bot

A simple discord bot that inserts spaces between letters in words.

Since this bot isn't hosted anywhere, if you would like to use it, you'll have to setup the bot as your own, which requires
going through some setup on Discord's side. Below is a guide to get you started
(Make sure that the bot has access to all Message related permissions!):

https://www.ionos.com/digitalguide/server/know-how/creating-discord-bot/

Or you can try this guide after following the below steps:
https://www.youtube.com/watch?v=SRV_4C9aEqM

And the bot's user ID is: ```1179924526788788244```, which you'll need.

You'll also need Python, git, and some kind of text editor installed on your computer.


Once you do that, you'll want to go ahead and clone the repo:

```git clone https://github.com/Thnderbread/discordbot```

Open up the folder where the repo was cloned, and create a file called `.env` Write the following:

BOT_TOKEN=[YOUR BOT T0KEN HERE (without the brackets.)]

Save it. Once that's done, the following in your text editor or command line:

```pip install -r requirements.txt```
```python main.py```

Then, go back to your Discord server and add the bot, if you haven't done so from the earlier tutorial already.

# Bot usage

The bot responds to the ``$spacify`` command. After inputting that, type anything you want! For example:

```$spacify Hello there!```

Outputs:

``H e l l o t h e r e !``

You can use braces {} to ignore certain words:

```$spacify Hello {there!}```

Outputs:

``H e l l o there!``

Discord emotes and emojis are preserved as well!

```$spacify Thumbs up! 👍```

Outpus:

``T h u m b s u p ! 👍``

# Notes

- Make sure to include a space between any words and emotes or emojis. They may not render correctly if this is not done.
- This bot will only have access to the emotes in your server! If the bot doesn't have access to an emote in the message it's processing,
      It may appear like this : `<a:Emote_name:01234567890123456789>` or like this: `:emote_name:`. This is how emotes look under the Discord hood!
- Type ```$help``` or ```$help spacify``` to get a rundown of the bot usage.
