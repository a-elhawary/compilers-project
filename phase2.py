from engine import engine

class Node:
    def __init__(self, label):
        self.label = label
        self.token = None
        self.nxt = []
    
    def addChildren(self, children):
        self.nxt += children

parseTable = {
    ("Exp", '(') : "Term ExpD",
    ("Exp", 'Number') : "Term ExpD",
    ("Exp", 'ID') : "Term ExpD",
    ("ExpD", ')') : "",
    ("ExpD", '+') : "+ Term ExpD",
    ("ExpD", '-') : "- Term ExpD",
    ("ExpD", '$') : "",
    ("Term", '(') : "Factor TermD",
    ("Term", "Number") : "Factor TermD",
    ("Term", "ID") : "Factor TermD",
    ("TermD", ")") : "",
    ("TermD", "-") : "",
    ("TermD", "+") : "",
    ("TermD", "*") : "* Factor TermD",
    ("TermD", "/") : "/ Factor TermD",
    ("TermD", "$") : "",
    ("Factor", "(") : "( Exp )",
    ("Factor", "Number") : "Number",
    ("Factor", "ID") : "ID",
}

def parser(expression):
    expression.append(["$", "EndToken"])
    stack = []
    stack.append(Node("$"))
    tree = Node("Exp")
    stack.append(tree)
    while len(stack) > 0 and len(expression) > 0:
        currentStackNode = stack.pop(-1) 
        currentStackHead = currentStackNode.label
        if currentStackHead == expression[0][0] or currentStackHead == expression[0][1]:
            print("matched " + str(currentStackHead))
            currentStackNode.token = expression[0][0]
            expression.pop(0)
        elif (currentStackHead, expression[0][0]) in parseTable:
            nxt = parseTable[(currentStackHead, expression[0][0])]
            if nxt != "":
                nxt = nxt.split(" ")
                nodeNxt = []
                for txt in nxt:
                    nodeNxt.append(Node(txt))
                currentStackNode.addChildren(nodeNxt)
                for i in reversed(range(len(nodeNxt))):
                    stack.append(nodeNxt[i])
            print("action taken: " + currentStackHead + "->" + str(nxt))
        elif (currentStackHead, expression[0][1]) in parseTable:
            nxt = parseTable[(currentStackHead, expression[0][1])]
            if nxt != "":
                nxt = nxt.split(" ")
                nodeNxt = []
                for txt in nxt:
                    nodeNxt.append(Node(txt))
                currentStackNode.addChildren(nodeNxt)
                for i in reversed(range(len(nodeNxt))):
                    stack.append(nodeNxt[i])
            print("action taken: " + currentStackHead + "->" + str(nxt))
        else:
            break
    return tree

def main():
    expression = input("Please enter an expression: ")
    isValid, tokens = engine(expression)
    if isValid:
        parser(tokens)

if __name__ == "__main__":
    main()