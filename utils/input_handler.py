# input_handler.py
import platform

if platform.system() == "Darwin":  # macOS
    from pynput import keyboard as pynput_keyboard

    _pressed_keys = set()

    def _on_press(key):
        try:
            _pressed_keys.add(key.char.lower())
        except AttributeError:
            if key == pynput_keyboard.Key.up:
                _pressed_keys.add('up')
            elif key == pynput_keyboard.Key.down:
                _pressed_keys.add('down')
            elif key == pynput_keyboard.Key.enter:
                _pressed_keys.add('enter')

    def _on_release(key):
        try:
            _pressed_keys.discard(key.char.lower())
        except AttributeError:
            if key == pynput_keyboard.Key.up:
                _pressed_keys.discard('up')
            elif key == pynput_keyboard.Key.down:
                _pressed_keys.discard('down')
            elif key == pynput_keyboard.Key.enter:
                _pressed_keys.discard('enter')
        if key == pynput_keyboard.Key.esc:
            return False  # stop listener

    listener = pynput_keyboard.Listener(on_press=_on_press, on_release=_on_release)
    listener.start()

    def is_pressed(key_str):
        return key_str.lower() in _pressed_keys

else:  # Assume Windows/Linux
    import readchar