class Person:
    # defines a set of attributes about a student

    def __init__(self, name, hair_colour, height):
        # passed in parameter is equal to self . name
        self.name = name
        self.hair_colour = hair_colour
        self.height = height

    def print_name(self,some_detail):
        print(self.name + " known as : " + some_detail)

    def print_hair_colour(self):
        print(self.hair_colour)

    def print_height(self):
        print(self.height)