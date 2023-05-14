

class list_chained:
    def __init__(self, first_data):
        self.first_node = Node(first_data)
        self.last_node = self.first_node
        self.size = 1

    def append(self,data):
        self.last_node.next_node = Node(data)
        self.last_node = self.last_node.next_node
        self.size += 1
    
    def insert_first(self, data):
        current_node = Node(data)
        current_node.next_node = self.first_node
        self.first_node = current_node
    
    def size(self):
        return self.size
    
    def insert(self, data, index):
        current_node = Node(data)
        i = 1
        while index > i :
             current_node = current_node.next_node
             i += 1
        new_node = Node(data)
        new_node.next_node = current_node.next_node
        current_node.next_node = new_node
      
    def seeData(self):
        current_node = self.first_node
        index = 0
        f = open("myData.txt", "x")
        while(current_node.next_node != None):
              print(current_node.data)
              current_node = current_node.next_node
              index += 1
              
        
        
        
 
class list_chained_sorted : 
  def __init__(self,data):
    self.first_node = Node(data)
    self.last_node = self.first_node

  def add_data(self,data):
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
    while current_node.next_node.data < data :
      current_node = current_node.next_node

    N.next_node = current_node.next_node
    current_node.next_node = N
    
    
class Stack :
    def __init__(self,data):
        self.last_node = Node(data)

    def push(self,data):
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
  def __init__(self,data):
    self.data = data
    self.previous_node = None
    self.next_node = None
    
