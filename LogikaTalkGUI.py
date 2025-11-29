from customtkinter import *
import threading 
import socket 
from PIL import Image
SERVER_NAME ='localhost'
PORT = 8080
class ChatClient(CTk):
    def __init__(self):
        super().__init__()
        self.nickname = "Unknown"
        self.title("Chat box^^)")
        self.geometry("500x500")
        img = CTkImage(light_image=Image.open("C:\\logika Python\\LogikaTalk\\57e7f9977bc8c882328ea81e5eaacacf.jpg"),size=(500,500))
        self.image_lb =CTkLabel(self,text="",image=img)
        self.image_lb.pack()

        self.sock=None
        self.running=None
        self.recv_thread=None
        self.nicknameframe = CTkFrame(self)
        self.nicknameframe.configure(fg_color="grey")
        self.nicknameframe.place(x=100,y=100)
        self.nickname_lb = CTkLabel(
            self.nicknameframe,
            text="Введіть нік нейм",
            text_color="red",
            # fg_ color="grey,
            # bg_ color="black",
            # corner_radius=40,
            #border_width=2
        )
        self.configure(fg_color="grey")
        self.configure(bg_color="grey")
        self.nickname_lb.pack(pady=10, padx=10)
        self.nickname_entry = CTkEntry(
            self.nicknameframe,
            width=100,
            height=50,
            placeholder_text="Введіть нік тут",
            # border_color="white",
        )
        self.nickname_entry.configure(fg_color="light blue",placeholder_text_color="black")

        self.nickname_entry.pack(pady=10, padx=10)

        self.chat_frame = CTkFrame(self,width=500,height=500)
        self.chat_frame.configure(fg_color="grey")
        self.chat_box = CTkTextbox(
            self.chat_frame, width=450, height=300, state="disable"
        )
        self.chat_box.configure(fg_color="light grey") 
        self.chat_box.place(y=20, x=20)
        self.chat_entry = CTkEntry(
            self.chat_frame,
            width=350,
            height=40,
            placeholder_text="Введіть повідомлення",
            border_color="grey",
        )
        self.chat_entry.place(x=20, y=330)
        self.connect_btn = CTkButton(
            self.nicknameframe, text="Увійти у чат", width=140, height=50, command=self.start_chat,
        )
        self.connect_btn.pack(pady=10, padx=10)
        self.chat_frame.pack_forget()
        self.knopka_btn = CTkButton(
            self.chat_frame, text="Відправити", width=140, height=50, command=self.sent_message,
        )
        self.knopka_btn.place(x=350,y=330)
    def start_chat(self):
        self.nickname = self.nickname_entry.get().strip()
        self.nickname = self.nickname if self.nickname else "Unknown"
        self.nicknameframe.pack_forget()
        self.chat_frame.place(x=0, y=0)
        self.append_local("(SYSTEM) Спроба підключення")
        threading.Thread(target=self.connect_to_server).start()
    def connect_to_server(self):
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((SERVER_NAME,PORT))
            self.client =client
            self.running =True
            self.append_local(f"[SYSTEM] Підключення до {SERVER_NAME}:{PORT}")
            text =f"{self.nickname}"
            self.client.send(text.encode())
            self.recv_thread=threading.Thread(target=self.recv_loop)
            self.recv_thread.   start()
        except Exception as e:
            self.append_local(f"[SYSTEM] [ERROR] Не вдалося підключитися{e}")
    def append_local(self,text):
        self.chat_box.configure(state='normal')
        self.chat_box.insert(END,text+"\n")
        self.chat_box.see(END)
        self.chat_box.configure(state='disable')
    def sent_message(self):
        text = self.chat_entry.get().strip()
        if not text:
            return
        #self.append_local(text)
        self.client.send(text.encode())
        self.chat_entry.delete(0,END)
    def recv_loop(self):
        buffer =''
        try:
            while self.running:
                text =self.client.recv(4096).decode()
                if not text:
                    break
                buffer+=text
                while "\n" in buffer:
                    line,buffer =buffer.split("\n",1)
                    self.hadle_line(line.strip())
        except Exception as e:
            self.append_local(f"[SYSTEM [ERROR] {e}")
        finally:
            try:
                self.client.close()
            except:
                pass
            self.append_local(f"[SYSTEM] Відєднано від серверу ")
    def hadle_line(self,line):
        if not line:
            return
        parts = line.split("@",2)
        if len(parts)>=3 and parts[0] =="TEXT":
            a = parts[1]
            msg=parts[2]
            self.after(0,self.append_local(f'{a}: {msg}'))
        else:
            self.after(0,self.append_local(f'{line}'))

window = ChatClient()

window.mainloop()
