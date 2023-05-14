class node:
    def __init__(self,data):
        self.data = data
        self.next_nodes = []

    def size(self):
        count = 1
        for node in self.next_nodes:
            count += node.size()
        return count

    def search(self,data):
        if self.data == data:
            return True
        else : 
            result = False
        for N in self.next_nodes:
            result = result or N.search(data)
        return result

class tree:
  def __init__(self, data):
    self.first_node = node(data)

  def size(self):
    return self.first_node.size()

  def search(self, data):
    return self.first_node.search(data)