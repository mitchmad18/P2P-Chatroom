import tkinter as tk
import socket
import sys

HOST = '127.0.0.1'
PORT = 4201
ConnectionEstablished = False

class App(tk.Frame):
    def __init__(self, master):

        tk.Frame.__init__(self, master, height=360, width=565)
        master.title("P2P Chatroom")

        self.label_nickname = tk.Label(self, text="Nickname: ")
        self.label_nickname.place(x=0, y=0)

        self.nickname = tk.Entry(self, width = 30)
        self.nickname.place(x=80,y=0)

        self.largeTextbox = tk.Text(self, height = 18, width = 70, state="disabled")
        self.largeTextbox.place(x=0,y=30)

        self.message_edit = tk.Entry(self, width = 65)
        self.message_edit.place(x=5, y=335)

        self.btn_send = tk.Button(self, text="Send!", width = 10,command=lambda : self.send_text(self.nickname.get(), self.message_edit.get()))
        self.btn_send.place(x=450, y=330)
        master.bind('<Return>',lambda event: self.send_text(self.nickname.get(), self.message_edit.get()))

    #Insert text into chatbox
    def send_text(self, user, message):
        if user != '' and message != '':
            self.largeTextbox.config(state='normal')
            self.largeTextbox.insert(tk.END, user + ": " + message + "\n")
            self.message_edit.delete(0, 'end')
            self.largeTextbox.config(state='disabled')
            #main().send_and_recieve(user,message)
        elif user == "Computer":
            self.largeTextbox.config(state='normal')
            self.largeTextbox.insert(tk.END, user + ": " + message + "\n")
            self.message_edit.delete(0, 'end')
            self.largeTextbox.config(state='disabled')
        else:
            self.errorPopup()

    #Error popup dialoge
    def errorPopup(self):
        popup = tk.Tk()
        popup.wm_title("Error!")
        self.label = tk.Label(popup, text="Please make sure you have a nickname and a message before hitting send!")
        self.label.pack()
        self.btn_popup = tk.Button(popup,text="Okay", command=popup.destroy)
        self.btn_popup.pack()
        popup.mainloop()

def main():
    root = tk.Tk()
    App(root).pack(expand=True, fill='both')

    HOST = '127.0.0.1'
    PORT = 4201

    global s
    global conn
    s = socket.socket()

    #Displays the welcome dialog box
    def welcome():
        popup = tk.Tk()
        popup.resizable(height = 1000)
        popup.wm_title("Welcome!")
        label = tk.Label(popup, text="Welcome to P2P chatroom!")
        label.pack()
        btn_server = tk.Button(popup,text="Create Server", command=lambda: [popup.destroy(),create_server_popup()])
        btn_connect = tk.Button(popup, text="Connect to Server", command=lambda: [popup.destroy(),connect_server_popup()])
        btn_exit = tk.Button(popup,text="Exit", command=root.quit)
        btn_server.pack()
        btn_connect.pack()
        btn_exit.pack()
        popup.mainloop()

    #Establishes a connection that listens for another person to join
    def establish_connection():
        global ConnectionEstablished
        global s
        global conn
        s.bind((HOST,PORT))
        print("Server established on Host: "+ HOST + ", on Port: " + str(PORT))

        s.listen()
        conn, address = s.accept()
        with conn:
            ConnectionEstablished = True
            print("Connected")
            conn.sendall("Welcome to the chatroom!".encode())

    def create_server_popup():
        popup = tk.Tk()
        popup.resizable()
        popup.wm_title("!")
        label = tk.Label(popup, text="Please enter your Host and Port numbers:")
        label.pack()
        hostNum = tk.Entry(popup, width = 30)
        hostNum.pack()
        portNum = tk.Entry(popup, width = 30)
        portNum.pack()
        btn_start = tk.Button(popup,text="Start", command=lambda: [popup.destroy(),establish_connection()])
        btn_start.pack()
        popup.mainloop()

    def connect_server_popup():
        popup = tk.Tk()
        popup.resizable()
        popup.wm_title("!")
        label = tk.Label(popup, text="Please enter your Host and Port numbers:")
        label.pack()
        hostNum = tk.Entry(popup, width = 30)
        hostNum.pack()
        portNum = tk.Entry(popup, width = 30)
        portNum.pack()
        btn_start = tk.Button(popup,text="Start", command=lambda: [popup.destroy(),connect_to_server()])
        btn_start.pack()
        popup.mainloop()

    #Attenpts to connect to another active user
    def connect_to_server():
        global ConnectionEstablished
        try:
            s.settimeout(5)
            s.connect((HOST,PORT))
        except:
            print("Failed to connect")
            root.quit
        ConnectionEstablished = True
        print("Connected")
        send_message_out("Computer", "Welcome to the chatroom!")

    #Tries to send a message to the other user
    def send_message_out(user, message):
        global s
        fullMessage = user + ": " + message + '\n'
        s.send(fullMessage.encode())

    #Listens for incomming messages
    def listen_for_message():
        while True:
            data = conn.recv(1024)
            print(data.decode())

    #Add a menu bar
    menubar = tk.Menu(root)
    menubar.add_command(label="Connect")
    menubar.add_command(label="Quit", command=root.quit)
    root.config(menu=menubar) 

    welcome()

    if ConnectionEstablished == True:
        print("Message sent")
        listen_for_message()
    else:
        print("nope....")

    root.mainloop()

if __name__ == "__main__":
    main()