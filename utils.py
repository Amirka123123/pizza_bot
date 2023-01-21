class MenuStack():

    def __init__(self, default_menu):
        self.elements = list()
        self.default_menu = default_menu

    def push(self, element):
        self.elements.append(element)

    def pop(self):
        if len(self.elements) == 0:
            return self.default_menu

        popped_element = self.elements[-1]
        del self.elements[-1]
        return popped_element

    def __str__(self):
        return str(self.elements)


if __name__ == '__main__':
    my_stack = MenuStack()
    my_stack.push(3)
    my_stack.push(5)
    my_stack.push(-1)
    print(my_stack.elements)
    popped = my_stack.pop()
    print("Popped element:", popped)
    print(my_stack.elements)