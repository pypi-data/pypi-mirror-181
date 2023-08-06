import keyboard

names: dict = dict()

class __ReturnedInput():
    def held(self, key):
        res = keyboard.is_pressed(key)
        names[key] = res
        return res

    def pressed(self, key):
        res = keyboard.is_pressed(key) and (not names[key])
        names[key] = keyboard.is_pressed(key)
        return res

def init(*args):
    for key in args:
        names[key] = keyboard.is_pressed(key)
    return __ReturnedInput()