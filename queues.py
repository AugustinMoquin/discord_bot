class Node:
    def __init__(self, previous_node, following_node, data):
        self.previous_node = previous_node
        self.following_node = following_node
        self.data = data

# class Node {
    
#     private int data;
#     private Node next_node;

#     public Node(int data)
#     {
#         this.data = data;
#         this.next_node = null;
#     }

# }

class Queue:
  def __init__(self,data):
    self.first_node = Node(data)
    self.size = 1

  def __str__(self):
    txt = str(self.first_node.data)

    current_node = self.first_node
    while current_node.next_node != None:
      current_node = current_node.next_node
      txt += str(current_node.data)
    
    return txt

  def push(self,data):
    if self.first_node == None:
      self.first_node = Node(data)
      return

    current_node = self.first_node
    while current_node.next_node != None:
      current_node = current_node.next_node

    current_node.next_node = Node(data)
    self.size += 1

  def pop(self):
    temp_data = self.first_node.data
    self.first_node = self.first_node.next_node
    return temp_data

  def peek(self):
    return self.first_node.data

  def size(self):
    return self.size