import ctypes
import sdl2,sdl2.ext

KEYBOARD_ARRAY_TYPE = ctypes.c_uint8 * sdl2.SDL_NUM_SCANCODES


def get_keyboard_state():
    """ Returns a pointer to the current SDL keyboard state,
    which is updated on SDL_PumpEvents. """
    raw_keystate = sdl2.keyboard.SDL_GetKeyboardState(None)
    pointer = ctypes.cast(raw_keystate, ctypes.POINTER(KEYBOARD_ARRAY_TYPE))
    return pointer.contents


sdl2.ext.init()

window = sdl2.ext.Window('Test', size=(640, 480))
window.show()

key_states = sdl2.SDL_GetKeyboardState(None)
running = True

while running:
    for event in sdl2.ext.get_events():
        if event.type == sdl2.SDL_QUIT:
            running = False
            break
    if key_states[sdl2.SDL_SCANCODE_A]:
        print('A key pressed')
    else:
        print('A key released')
    window.refresh()