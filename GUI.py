from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QWidget
from PyQt5.QtSvg import QSvgWidget
from engine import engine
import sys

WIDTH = 1080
HEIGHT = 720

app = QApplication(sys.argv)

#Window 
window = QWidget()
window.setStyleSheet("""
    QWidget{
        background-color:#fff;
        color:#000;
    }
""")
window.setWindowTitle('PyQt5 App')
window.setGeometry(500, 100, WIDTH , HEIGHT)

windowLayout = QVBoxLayout()
windowLayout.setContentsMargins(0,0,0,0)

#Top Bar Section
topBar = QWidget()
topBar.setStyleSheet("""QWidget{
    background-color:#448e96;
    padding:15px;
}
""")
topBarLayout = QHBoxLayout()
topBarLayout.setContentsMargins(0,0,0,0)
topBarLayout.addWidget(QLabel("Compilers Project"), 2)
expressionInput = QLineEdit()
expressionInput.setStyleSheet(""" 
    background-color:#fff;
    margin:20px;
    border-radius:8px;
""")
left = QWidget()
leftLayout = QVBoxLayout()
leftLayout.addStretch()
temp = QWidget()
def leftLayoutFunc(tokens, isValid):
    for i in reversed(range(leftLayout.count())):
        widget = leftLayout.itemAt(i).widget()
        if widget is not None:
            widget.setParent(None)
    leftLayout.setContentsMargins(0,0,0,0)
    if isValid:
        validLabel = QLabel("Valid Expression!")
        validLabel.setStyleSheet("""
            color:green;
        """)
    else:
        validLabel = QLabel("Invalid Expression!")
        validLabel.setStyleSheet("""
            color:red;
        """)
    leftLayout.insertWidget(0,validLabel)
    for i in reversed(range(len(tokens))):
        token = tokens[i]
        widget = QLabel("<" + token[0] + ", " + token[1] + ">" + " Transition: " + str(token[2]) + " -> " + str(token[3]))
        leftLayout.insertWidget(0,widget)
    left.update()

def onStart():
    isValid, tokens = engine(expressionInput.text())
    leftLayoutFunc(tokens, isValid)
    renderImage()
    tokens.clear()

main = QWidget()
image = QSvgWidget()
def renderImage():
    image.load("./dfa.svg")
    main.update()

sendExpressionButton = QPushButton("Start")
sendExpressionButton.clicked.connect(onStart)
sendExpressionButton.setStyleSheet("""
    background-color:#212121;
    color:#fff;
    margin-right:15px;
    border-radius:8px;
""")
topBarLayout.addWidget(expressionInput, 2)
topBarLayout.addWidget(sendExpressionButton)
topBar.setLayout(topBarLayout)
windowLayout.addWidget(topBar)

# Main Section
mainLayout = QHBoxLayout()
mainLayout.setContentsMargins(0,0,0,0)

#Left Section
left.setStyleSheet("""
    background-color:#dedede;
""")
left.setLayout(leftLayout)

mainLayout.addWidget(left, 1)
#Right Section
dfaContainer = QWidget()
dfaLayout = QVBoxLayout()
regexContainer = QWidget()
regexLayout = QHBoxLayout()
regexLayout.addStretch()
regexLayout.addWidget(QLabel("((ID | NUM) OP)* (ID | NUM)"))
regexContainer.setLayout(regexLayout)
dfaLayout.addWidget(regexContainer)
dfaLayout.addWidget(image, 1)
dfaContainer.setLayout(dfaLayout)
mainLayout.addWidget(dfaContainer, 3)
main.setLayout(mainLayout)

windowLayout.addWidget(main, 3)

window.setLayout(windowLayout)

#Header

window.show()
sys.exit(app.exec_())