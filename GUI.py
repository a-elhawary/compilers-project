from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
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

#Top Bar
topBar = QWidget()
topBar.setStyleSheet("""QWidget{
    background-color:#448e96;
}
""")
topBarLayout = QHBoxLayout()
topBarLayout.addWidget(QLabel("Compilers Project"))
topBar.setLayout(topBarLayout)
windowLayout.addWidget(topBar)
windowLayout.addWidget(QLabel("Main"), 3)

window.setLayout(windowLayout)

#Header

window.show()
sys.exit(app.exec_())