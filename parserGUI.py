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
    nodeCount = 0
    while len(currentNodes) > 0:
        currentNode = None
        i = 0
        choosenI = 0
        currentDepth = currentNodes[0][1]
        for (node, depth) in currentNodes:
            if currentDepth == depth and isOperator(node.token) and (currentChildrenCount == 1 or syntaxTreeRoot is None):
                currentNode = node
                choosenI = i
            elif currentDepth == depth and not isOperator(node.token) and currentChildrenCount == 0:
                currentNode = node
                choosenI = i
            i += 1
        if currentNode is None:
            currentNode, currentDepth = currentNodes.pop(0)
            if currentNode.label != "Number" and currentNode.label != "ID" and not isOperator(currentNode.token):
                continue
        else:
            currentNodes.pop(choosenI)
        if len(currentNode.nxt) == 0 and currentNode.token is not None and currentNode.token != "(" and currentNode.token != ")":
            g.add_node(str(nodeCount) + ". " + currentNode.token)
            if syntaxTreeRoot == None:
                syntaxTreeRoot = str(nodeCount) + ". " + currentNode.token
                currentTreeNode = syntaxTreeRoot
            else:
                g.add_edge(currentTreeNode, str(nodeCount) + ". " + currentNode.token)
                currentChildrenCount+=1
                if isOperator(currentNode.token):
                    currentTreeNode = str(nodeCount) + ". " + currentNode.token
                    currentChildrenCount = 0
            nodeCount += 1

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