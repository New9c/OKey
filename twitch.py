from twitch_chat_irc import twitch_chat_irc
from consts import SETTINGS
message_frames = 0
twitch_msg = ""
connection = twitch_chat_irc.TwitchChatIRC(SETTINGS["twitch_username"], SETTINGS["twitch_oauth"], True)

def show_twitch_msg(message):
    global message_frames, twitch_msg
    if message["display-name"] not in SETTINGS["twitch_ignore_names"]:
        message_frames = 90
        twitch_msg = f"{message["display-name"]}: {message["message"]}"
        print(twitch_msg)
        if len(twitch_msg)>SETTINGS["text_len"]:
            twitch_msg = f"{twitch_msg[:SETTINGS["text_len"]-6]}-[>60]"
def start():
    connection.listen(SETTINGS["which_chat_to_check"], on_message=show_twitch_msg)
def stop():
    connection.close_connection()
