FRAMES_FOR_ONE_MOVE = 60
roll = 0
ACTION_INTERVAL = 4
def face(frame):
    global roll
    if frame == 1:
        roll = (roll+1)%ACTION_INTERVAL
    if roll==0:
        return move(frame)
    return base(frame)

def base(frame) -> str:
    if frame<60-5:
        return "O u O".center(64)
    return "1 u 1".center(64)

def move(frame) -> str:
    if frame>60:
        raise ValueError("Frame is too big")
    if frame <= 8:
        return " O u O   ".center(64)
    elif frame <= 15:
        return "O u O    ".center(64)
    elif frame <= 23:
        return " O u O   ".center(64)
    elif frame <= 30:
        return "  O u O  ".center(64)
    elif frame <= 38:
        return "   O u O ".center(64)
    elif frame <= 45:
        return "    O u O".center(64)
    elif frame <= 53:
        return "   O u O ".center(64)
    return "  O u O  ".center(64)

