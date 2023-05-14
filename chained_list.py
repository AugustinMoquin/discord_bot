

class List_chained:
    def __init__(self, first_data):
        self.first_node = Node(None, None, first_data)
        self.last_node = self.first_node
        self.length = 1

    def view(self, index):
        current_node = self.first_node
        i = 0
        while i < index:
            current_node = current_node.following_node
            i += 1
        return current_node.data

    def view_from(self, user):
        current_node = self.first_node
        i = 0
        while current_node.data.user != user:
            current_node = current_node.following_node
        return current_node.data

    def get(self, index):
        current_node = self.first_node
        i = 0
        while i < index:
            current_node = current_node.following_node
            i += 1
        return current_node

    def get_from(self, user):
        current_node = self.first_node
        i = 0
        while current_node.data.user != user:
            current_node = current_node.following_node
        return current_node

    def append(self, data):
        old_last_node = self.last_node
        new_last_node = Node(old_last_node, None, data)
        old_last_node.following_node = new_last_node
        self.last_node = new_last_node
        self.last_node.previous_node = old_last_node
        self.length += 1

    def size(self):
        return self.length

    def clear(self, first_data):
        current_node = self.first_node
        while current_node.following_node is not None:
            current_node = current_node.following_node
            del current_node.previous_node
        del current_node
        self.first_node = Node(None, None, first_data)
        self.last_node = self.first_node
        self.length = 1
        return


class List_chained_sorted:
    def __init__(self, data):
        self.first_node = Node(data)
        self.last_node = self.first_node

    def add_data(self, data):
        N = Node(data)
        if data < self.first_node.data:
            N.next_node = self.first_node
            self.first_node = N
            return

        if data > self.last_node.data:
            self.last_node.next_node = N
            self.last_node = N
            return

        current_node = self.first_node
        while current_node.next_node.data < data:
            current_node = current_node.next_node

        N.next_node = current_node.next_node
        current_node.next_node = N


class Stack:
    def __init__(self, data):
        self.last_node = Node(data)

    def push(self, data):
        N = Node(data)
        N.next_node = self.last_node
        self.lest_node = N

    def pop(self):
        data = self.last_node.data
        self.last_node = self.last_node.next_node
        return data

    def size(self):
        pass

    def peek(self):
        pass


class Node:
    def __init__(self, previous_node, following_node, data):
        self.previous_node = previous_node
        self.following_node = following_node
        self.data = data
