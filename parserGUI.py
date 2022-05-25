import matplotlib.pyplot as plt
import networkx as nx
import pydot
from networkx.drawing.nx_pydot import graphviz_layout
from engine import engine
from phase2 import parser
from engine import isOperator

# pip install networkx
# pip install matplotlib
# install graphviz on windows somehow?
# pip install pydot

def drawParseTree(tree, G):
    currentNodes = [(0, None, tree)]
    i = 0
    while len(currentNodes) > 0:
        parentIndex, parent, currentNode = currentNodes.pop(0)
        G.add_node(str(i) + ". " + currentNode.label)
        if parent is not None:
            G.add_edge(str(parentIndex) + ". " + parent.label, str(i) + ". " + currentNode.label)
        for node in currentNode.nxt:
            currentNodes.append((i, currentNode, node))
        i+=1

def drawSyntaxTree(tree, g):
    tempNodes = [(tree, 0)]
    currentNodes = [(tree, 0)]
    while len(tempNodes) > 0:
       tempNode, tempDepth = tempNodes.pop(0)
       for node in tempNode.nxt:
           currentNodes.append((node, tempDepth+1))
           tempNodes.append((node, tempDepth+1))
    currentIndex = 0
    syntaxTreeRoot = None
    currentTreeNode = syntaxTreeRoot
    currentChildrenCount = 0
    while len(currentNodes) > 0:
        currentNode = None
        i = 0
        choosenI = 0
        currentDepth = currentNodes[0][1]
        for (node, depth) in currentNodes:
            print("checking " + str(node.label) + " " + str(node.token) + " " + str(depth) + " " + str(currentDepth))
            if currentDepth == depth and isOperator(node.token) and currentChildrenCount == 1:
                currentNode = node
                choosenI = i
            if currentDepth == depth and not isOperator(node.token) and currentChildrenCount == 0:
                currentNode = node
                choosenI = i
            i += 1
        if currentNode is None:
            currentNode, currentDepth = currentNodes.pop(0)
            if currentNode.label != "Number" and currentNode.label != "ID" and not isOperator(currentNode.token):
                continue
        else:
            currentNodes.pop(choosenI)
        print("choosing " + str(currentNode.label) + " " + str(currentNode.token))
        print()
        if len(currentNode.nxt) == 0 and currentNode.token is not None and currentNode.token != "(" and currentNode.token != ")":
            g.add_node(currentNode.token)
            if syntaxTreeRoot == None:
                syntaxTreeRoot = currentNode.token
                currentTreeNode = syntaxTreeRoot
            else:
                g.add_edge(currentTreeNode, currentNode.token)
                currentChildrenCount+=1
                if isOperator(currentNode.token):
                    currentTreeNode = currentNode.token
                    currentChildrenCount = 0

def main():
    expression = input("Please enter an expression: ")
    isValid, tokens  = engine(expression)
    tree = parser(tokens)
    i = 0
    G = nx.DiGraph()
    drawParseTree(tree, G)
    drawSyntaxTree(tree, G)
    pos = graphviz_layout(G, prog="dot")
    nx.draw_networkx_nodes(G, pos, node_size=1500)
    nx.draw_networkx_edges(G, pos, G.edges(), edge_color="black")
    nx.draw_networkx_labels(G, pos)
    plt.show()


if __name__ == "__main__":
    main()