
class node : 
  def __init__(self, question, reponses):
    self.question = question
    self.reponses = reponses
    self.next_nodes = []

class treeQ : 
  def __init__(self,first_question):
    self.first_node = node(first_question,[])
    self.current_node = self.first_node

  def append_question(self,question,reponses,previous_question):
    current_node = self.first_node
    while(current_node):
          return
    pass

  def delete_question(self,question):
    pass

  def get_question(self):
    return self.current_node.question

  def send_answer(self, reponse):
    pass