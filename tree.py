class TreeNode:
    def __init__(self, question, left=None, symbolL=None, right=None , symbolR = None, state = None):
        self.question = question
        self.symbolL = symbolL
        self.left = left
        self.symbolR = symbolR
        self.right = right
        self.state = state
