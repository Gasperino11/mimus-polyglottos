def debug_formatter(input_strs: list, command: str = None) -> str:
    """
    A simple formatter to format all of the debug mode strings so they look similar.

    Params:
    - input_strs (Required) : a list of strings to list out inside of the debug mode output
    """
    
    output_str = f"```\n### DEBUG MODE OUTPUT FOR **{command}** COMMAND ###\n\n"
    
    for sub_str in input_strs:
        output_str += "  - "
        output_str += str(sub_str)
        output_str += "\n"
    
    output_str += "\n### END OF DEBUG OUTPUT ###\n```"

    return output_str

def uwu(error_str: str) -> str:
    """
    An error message formatter that adds :rotating_light: and :face_holding_back_tears: emojis to the end and beginning of the error message

    Params:
    - error_str (Required) -> A string representing the actual error message to display
    """

    uwu_string = ":rotating_light::face_holding_back_tears: UwU I made a fucky :face_holding_back_tears::rotating_light:"
    output_str = uwu_string + "\n\n" + error_str + "\n\n" + uwu_string

    return output_str

def print_help_str() -> str:

    help_str = "# AI Voice Bot Command Menu:\n"
    help_str += "> **connect**\n"
    help_str += "*Connects the bot to the voice channel of the message author*\n\n"
    help_str += "> ** disconnect **\n"
    help_str += "*Disconnects the bot from any voice channels it is connected to*\n\n"
    help_str += "> ** generate <voice> <text to generate speech from>**\n"
    help_str += "*Generates audio of the specified text in the specified voice; the text should be wrapped in double quotes*\n\n"
    help_str += "> ** list_voices **\n"
    help_str += "*Provides a list of voices with descriptions that can be used to generate audio*\n\n"
    help_str += "> ** debug **\n"
    help_str += "*Enables debug mode to print extra information on command execution out to the assigned debug channel*\n\n"
    help_str += "Typing !help will provide a list of commands and typing !help <command name> will provide a list of aliases for that command\n"

    return help_str

def print_roadmap_str() -> str:

    roadmap_str = "# AI Voice Bot Roadmap\n"
    roadmap_str += "## v0.1.0\n"
    roadmap_str += "- Initial Release\n"
    roadmap_str += "## v0.1.1\n"
    roadmap_str += "- Add more AI Voices\n"
    roadmap_str += "- Add the ability to generate and save MP3s to be played back later\n"
    roadmap_str += "## Beyond\n"
    roadmap_str += "- Add the ability to clone user voices through commands\n"
    roadmap_str += "- Add multi-language support\n"

    return roadmap_str

def print_voice_help_str() -> str:
    
    voice_help_str = "# Fequent Asked Questions\n"
    voice_help_str += "## How do I add a voice to the options?\n"
    voice_help_str += """Adding a voice is easy! All that is needed is at least 3 minutes of audio of the voice in the form of MP3s. Here are some guidelines for the audio samples:
- Make sure the speaker whose voice you are trying to clone is the lone speaker in the audio
- A wider range of emotions in the speaker audio will yield a wider range of emotions in the AI generated audio
- Background noise is okay as long as it's not overpowering the speaker's voice 
- Audio files MUST be smaller than 10 mb
- Once you've compiled your audio files, give them to me and I can add the voice to the list of available voices
"""
    voice_help_str += "## The generated audio from my custom voice is super bad! How do I make it better?\n"
    voice_help_str += """To increase the quality of your voice, do the following:
- Add more voice samples; the minimum is 3 minutes of audio spread across at least 5 voice samples but having 10 or more voice samples (regardless of length) drastically increases the quality of the generated voice
- Add more variety; if your voice samples are all in the same tone then the generated voice will always be in that tone, try to add voice samples that cover a wide range of emotions, inflections, and tones
- Use longer voice samples; although a large number of short samples can be good a longer voice sample can help the model build a basis for the voice to add variability to
- Use high quality voice samples; As mentioned above, the best samples to use are ones where the voice you're trying to clone is the only one in the audio and here is minimal or no background noise. It can also help to use audio that has been filtered and amplified (such as from a podcast or interview)
""" # this weird indentation is so the string doesn't look like shit in discord
    voice_help_str += "## How do I make the audio pause or change tone/inflection?"
    voice_help_str += "\nThe audio will take cues from the text to produce the proper tone. Use things like dashes (-) and elipses (...) for pauses and punctuation (such as ? and !) to help with tone. Adding onomatopoeias like 'uh' and 'um' can help as well."

    return voice_help_str