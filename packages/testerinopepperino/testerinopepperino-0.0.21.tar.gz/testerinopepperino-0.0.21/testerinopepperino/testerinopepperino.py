from .pepperino import poop


class TesterinoPepperino:
    def __init__(self):
        self.x = 1

    def hello_world(self):
        print("hi there")
        self.x += poop()
        print(f"x is {self.x}")
