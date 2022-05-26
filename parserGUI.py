import matplotlib.pyplot as plt
import networkx as nx
import pydot
from networkx.drawing.nx_pydot import graphviz_layout
from engine import engine
from phase2 import parser
from phase2 import parseTable
from engine import isOperator

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QWidget
import sys

# pip install networkx
# pip install matplotlib
# install graphviz on windows and add it to environment vars

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
    currentNodes = []
    while len(tempNodes) > 0:
        tempNode, tempDepth = tempNodes[0]
        choosenI = 0
        i = 0
        for (node, depth) in tempNodes:
            if tempDepth < depth:
                tempDepth = depth
                tempNode = node
                choosenI = i
            i += 1
        tempNodes.pop(choosenI)
        for node in tempNode.nxt:
            if node.token is not None and node.token != "(" and node.token != ")":
                currentNodes.append((node.token, tempDepth+1))
            tempNodes.append((node, tempDepth+1))
    # current nodes now contain non-epsilon leaves
    # from left to right with ther depth
    visited = []
    while len(currentNodes) != 1:
        deepestNode = None
        maxDepth = 0
        i = 0
        deepestI = 0
        for (node, depth) in currentNodes:
            if depth > maxDepth and isOperator(node) and (node, depth) not in visited:
                deepestNode = node
                maxDepth = depth
                deepestI = i
            i += 1
        # found deepest operator
        print(currentNodes)
        print(deepestNode)
        childOne = currentNodes[deepestI - 1]
        childTwo = currentNodes[deepestI + 1]
        g.add_node(deepestNode)
        g.add_node(childOne[0])
        g.add_node(childTwo[0])
        g.add_edge(deepestNode, childOne[0])
        g.add_edge(deepestNode, childTwo[0])
        visited.append((deepestNode, maxDepth))
        currentNodes.remove(childOne)
        currentNodes.remove(childTwo)
        print()

class TopBar(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setContentsMargins(0,0,0,0)
        self.expressionInput = QLineEdit()
        self.expressionInput.setStyleSheet("""
                padding:20px;
                border-radius:8px;
        """)
        showTreesButton = QPushButton("Show Trees")
        showTreesButton.setStyleSheet("""
                background-color:#212121; 
                color:#fff;
                padding:20px;
                border-radius:8px;
        """)
        showTreesButton.clicked.connect(parent.showTrees)
        hLayout = QHBoxLayout()
        hLayout.addWidget(self.expressionInput)
        hLayout.addWidget(showTreesButton)
        self.setLayout(hLayout)

class myApplication(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.messageBox = QMessageBox()
        self.messageBox.setText("Invalid Syntax")
        self.setGeometry(100,100,1080,720)
        self.setContentsMargins(0,0,0,0)
        self.setStyleSheet("""
            background-color:#fff; 
            color:#000;
            margin:0;
            padding:0
        """)
        self.topBar = TopBar(self)
        vLayout = QVBoxLayout()
        vLayout.addWidget(self.topBar)
        hContainer = QWidget()
        hLayout = QHBoxLayout()
        self.actions = QLabel()
        hLayout.addWidget(self.actions)
        text = "<html>"
        for entry in parseTable:
            text += entry[0]
            text += " , "
            text += entry[1]
            text += " -> "
            text += parseTable[entry]
            text += "<br/>"
        text += "<html>"
        hLayout.addWidget(QLabel(text))
        hContainer.setLayout(hLayout)
        vLayout.addWidget(hContainer)
        vLayout.addStretch()
        self.setLayout(vLayout)
    
    def showTrees(self):
        expression = self.topBar.expressionInput.text() 
        print(self.topBar.expressionInput.text())
        isValid, tokens = engine(expression)
        if not isValid:
            self.messageBox.show()
            return 
        tree, actions = parser(tokens)
        if actions[len(actions) -1] != "matched $":
            self.messageBox.show()
            return
        text = "<html>"
        for action in actions:
            text += action
            text += "<br/>"
        text += "</html>"
        self.actions.setText(text)
        self.update()
        G = nx.DiGraph()
        drawParseTree(tree, G)
        drawSyntaxTree(tree, G)
        pos = graphviz_layout(G, prog="dot")
        nx.draw_networkx_nodes(G, pos, node_size=0)
        nx.draw_networkx_edges(G, pos, G.edges(), edge_color="black")
        nx.draw_networkx_labels(G, pos)
        plt.show()

def main():
    app = QApplication(sys.argv)
    window = myApplication()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()