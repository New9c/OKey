from consts import SETTINGS

SETTINGS["face_animation"].sort()
FRAMES_FOR_ONE_MOVE = SETTINGS["face_animation"][-1][0]
pointer = 0

def face(frame: int, mouse_clicked: bool = False, talking: bool = False):
    """
    Return the proper face to display
    params:
        frame (int): The frame (1~inf)
        mouse_clicked (int): Whether the mouse is clicked
        talking (bool): Whether the person is talking
    """
    global pointer
    eye = SETTINGS["face_click_eye"] if mouse_clicked else SETTINGS["face_normal_eye"]
    mouth = SETTINGS["face_talking_mouth"] if talking else SETTINGS["face_normal_mouth"]
    if SETTINGS["face_animation"][pointer][0]<frame:
        pointer += 1
    res = __replacer(SETTINGS["face_animation"][pointer][1], eye, mouth)
    if frame == FRAMES_FOR_ONE_MOVE:
        pointer = 0
    return res

def __replacer(face_string: str, eye: str, mouth: str) -> str:
    s = ""
    for c in face_string:
        if c == 'e':
            s += eye
        elif c == 'm':
            s += mouth
        else:
            s += c
    return s.center(SETTINGS["text_len"])


