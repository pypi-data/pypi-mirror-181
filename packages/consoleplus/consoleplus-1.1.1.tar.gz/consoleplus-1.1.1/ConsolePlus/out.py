from sys import stdout
from time import sleep
import os
class Output:

    def write(self, text, time=0.01):
        for char in text:
            stdout.write(char)
            stdout.flush()
            sleep(time)
        print()

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def write_centered(self, text, time=0.01):
        text = text.center(os.get_terminal_size().columns)
        if len(text.splitlines()) > 1:
            for line in text.splitlines():
                self.write_centered(line)
        else:
            self.write(text, time)