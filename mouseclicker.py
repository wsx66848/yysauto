from pymouse import PyMouse
import sys
import keyboard



key = "z"

def main():
    global key
    if len(sys.argv) > 1:
        key = sys.argv[1]
    mouse = PyMouse()


    def click(e):
        position = mouse.position()
        mouse.click(position[0], position[1], n=1)

    keyboard.on_press_key(key, click)
    keyboard.wait('e')

if __name__ == "__main__":
    main()
        
    