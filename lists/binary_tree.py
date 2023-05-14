class node:
    def __init__(self, data):
        self.data = data
        self.right_node = None
        self.left_node = None

    def append(self, data):
        if data == self.data:
            return
        if data > self.data:
            if self.right_node == None:
                self.right_node = node(data)
            else:
                self.right_node.append(data)
        else:
            if self.left_node == None:
                self.left_node = node(data)
            else:
                self.left_node.append(data)

    def search(self, data):
        if data == self.data:
            return True
        elif data < self.data:
            if self.left_node == None:
                return False
            else:
                self.left_node.search(data)
        else:
            if self.right_node == None:
                return False
            else:
                self.right_node.search(data)


class binary_tree:
    def __init__(self, data):
        self.first_node = node(data)

    def append(self, data):
        self.first_node.append(data)
