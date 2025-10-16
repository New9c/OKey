import consts

FRAMES_FOR_ONE_MOVE = 60
roll = 0

def face(frame: int, mouse_clicked: bool = False, talking: bool = False):
    global roll
    if talking:
        return "O  O".center(consts.TEXT_LEN)
    if frame == 1:
        roll = (roll+1)%consts.ACTION_INTERVAL
    if roll==0:
        return move(frame, mouse_clicked)
    return base(frame, mouse_clicked)

def base(frame: int, mouse_clicked: bool = False) -> str:
    if mouse_clicked:
        return "󰆿 u 󰆿".center(consts.TEXT_LEN)
    if frame<60-5:
        return "O u O".center(consts.TEXT_LEN)
    return "I u I".center(consts.TEXT_LEN)

def move(frame: int, mouse_clicked: bool = False) -> str:
    eye = '󰆿' if mouse_clicked else 'O'
    look = f"{eye} u {eye}"
    if frame>60:
        raise ValueError("Frame is too big")
    if frame <= 8:
        return f" {look}   ".center(consts.TEXT_LEN)
    elif frame <= 15:
        return f"{look}    ".center(consts.TEXT_LEN)
    elif frame <= 23:
        return f" {look}   ".center(consts.TEXT_LEN)
    elif frame <= 30:
        return f"  {look}  ".center(consts.TEXT_LEN)
    elif frame <= 38:
        return f"   {look} ".center(consts.TEXT_LEN)
    elif frame <= 45:
        return f"    {look}".center(consts.TEXT_LEN)
    elif frame <= 53:
        return f"   {look} ".center(consts.TEXT_LEN)
    return f"  {look}  ".center(consts.TEXT_LEN)

