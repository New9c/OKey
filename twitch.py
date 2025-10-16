from twitch_chat_irc import twitch_chat_irc
import consts
message_frames = 0
twitch_msg = ""
connection = twitch_chat_irc.TwitchChatIRC()

def show_twitch_msg(message):
    global message_frames, twitch_msg
    if message["display-name"]!="a username":
        message_frames = 90
        twitch_msg = f"{message["display-name"]}: {message["message"]}"
        print(twitch_msg)
        if len(twitch_msg)>consts.TEXT_LEN:
            twitch_msg = f"{twitch_msg[:consts.TEXT_LEN-6]}-[>60]"
def start():
    connection.listen('DaNew9c', on_message=show_twitch_msg)
def stop():
    connection.close_connection()
