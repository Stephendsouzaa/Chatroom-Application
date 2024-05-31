
import sys
from PyQt5.QtWidgets import QApplication, QTextEdit, QWidget, QVBoxLayout,QPushButton,QAction,QMainWindow,QLabel

import socket
import threading
import alias

class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.user = alias.dialogue()
        
        self.terminate=f"{self.user} has left the chat\n"
        self.users = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #initialized object and ip address type

        self.begin()
        self.initUI()
        self.show()

    def initUI(self):
        #User interface design
        self.setWindowTitle('Chat Window') #title 
        self.setGeometry(100, 100, 500, 500) #dimension 

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.layout = QVBoxLayout()
        self.centralWidget.setLayout(self.layout)

        self.txt = QLabel("Howdy!Welcome to the chatroom")
        self.layout.addWidget(self.txt)

        self.txt1 = QTextEdit() #Text view
        self.txt1.setReadOnly(True)
        self.layout.addWidget(self.txt1)
        
 
        #text box
        self.tplace = QTextEdit()
        self.tplace.setFixedHeight(70)
        self.layout.addWidget(self.tplace)
        #send button
        self.sendButton = QPushButton('Send')
        self.sendButton.clicked.connect(self.send)
        self.sendButton.setFixedSize(45,45)
        self.layout.addWidget(self.sendButton)
        #Menubar
        self.menuBar = self.menuBar()
        fileMenu = self.menuBar.addMenu('File')
        endChatAction = QAction('End Chat', self) #ends the conversation with user
        endChatAction.triggered.connect(self.end_chat)
        fileMenu.addAction(endChatAction)
        exitAction = QAction('Exit', self) #closes the desktop
        exitAction.triggered.connect(self.close)
        fileMenu.addAction(exitAction)

    def send(self):
        user_input = self.tplace.toPlainText().strip()
        if not user_input:#if clicked with void text box
            return
        letter = f"{self.user}: {user_input}\n"
        self.txt1.append(letter)
        self.users.send(letter.encode('utf-8'))#sends the message to other users in BIN format
        self.tplace.clear()

    def end_chat(self):
        
        self.users.send(self.terminate.encode('utf-8')) #sends "an individual has left the chat"
        self.txt1.setReadOnly(True)
        try:
          self.users.close() #termination of user connection 
        except Exception as e:
            self.txt1.append(self.terminate)

    def user_receive(self):
        while True:
            try:
                message = self.users.recv(1024).decode('utf-8')
                self.txt1.insertPlainText(message)
            except:
                self.txt1.insertPlainText(self.terminate)
                self.end_chat()
                break

    def begin(self):
        self.address = input("Enter the server address: ")
        self.users.connect((self.address, 59000)) #binds to the chatroom server at port 59000
        print(f"Connected to {self.address}")
        data = f'{self.user} has joined the chat\n'
        rec_thread = threading.Thread(target=self.user_receive) #multi-threading of the process
        rec_thread.start()
        self.users.send(data.encode('utf-8'))
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ChatWindow()
    window.show()
    sys.exit(app.exec_()) #terminates the process
#programmed by Oliver
