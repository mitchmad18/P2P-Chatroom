import tkinter as tk
import socket
import sys

HOST = '127.0.0.1'
PORT = '4201'
CONNECTION = False

class App(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, height=360, width=565)

        self.label_ipaddress = tk.Label(self, text="IP Address: ")
        self.label_ipaddress.place(x=0,y=0)

        self.ip_address = tk.Entry(self, width = 30)
        self.ip_address.place(x=80,y=0)

        self.label_nickname = tk.Label(self, text="Nickname: ")
        self.label_nickname.place(x=275, y=0)

        self.nickname = tk.Entry(self, width = 30)
        self.nickname.place(x=350,y=0)

        self.textbox = tk.Text(self, height = 18, width = 70, state="disabled")
        self.textbox.place(x=0,y=30)

        self.message_edit = tk.Entry(self, width = 65)
        self.message_edit.place(x=5, y=335)

        self.btn_send = tk.Button(self, text="Send!", width = 10,command=lambda : self.send_text(self.nickname.get(), self.message_edit.get()))
        self.btn_send.place(x=450, y=330)
        master.bind('<Return>',lambda event: self.send_text(self.nickname.get(), self.message_edit.get()))

    #Insert text into chatbox
    def send_text(self, user, message):
        if user != '' and message != '':
            self.textbox.config(state='normal')
            self.textbox.insert(tk.END, user + ": " + message + "\n")
            self.message_edit.delete(0, 'end')
            self.textbox.config(state='disabled')
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
    CONNECTION = False

    sock = socket.socket()
    sock.bind((HOST,PORT))

    def try_to_connect(connection_status):
        sock.connect((HOST,PORT))
        sock.close

        CONNECTION = True
        print(CONNECTION)

        if CONNECTION == True:
            print("We are connected together!")

        popup = tk.Tk()
        popup.wm_title("Connected!")
        label = tk.Label(popup, text="You are successfully connected!")
        label.pack()
        btn_popup = tk.Button(popup,text="Okay", command=popup.destroy)
        btn_popup.pack()
        popup.mainloop()

    #Add a menu bar
    menubar = tk.Menu(root)
    menubar.add_command(label="Connect",command=lambda : try_to_connect(CONNECTION))
    menubar.add_command(label="Quit", command=root.quit)
    root.config(menu=menubar) 

    root.mainloop()

if __name__ == "__main__":
    main()