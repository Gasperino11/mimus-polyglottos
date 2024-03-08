# mimus-polyglottos aka The Mockingbird Bot

Repository for all the code associated with *The Mockingbird Bot*; a discord bot capable of generating speech from text and playing it in a voice channel.

## Documentation

I'll update this later with actual documentation... maybe.

## Trello

Here is a trello board I use to help me keep track of the project: https://trello.com/b/wUB8sHSg/mockingbird-bot

## Contributing

Right now there are no contributors except me - if you would like to contribute I may consider it on special cases but otherwise feel free to fork this repo and make your own version.

## Running the bot

For right now I am not going to make this bot generally available. If you want to run it you'll need a few things:

- Discord API Token
- Elevenlabs API Token
- Python 3+ installed along with the discord and elevenlabs python libraries installed.

After this you'll also need to update the common.py file under the voice_generator folder with your list of voices as you will not have access to the ones I have created.

Last thing; I developed this on a Windows machine so some of the file paths may be formatted for the Windows file system. If you're running this on MacOS or Linux, you may need to make some code changes. I will not help you with these code changes so don't ask. :grinning: