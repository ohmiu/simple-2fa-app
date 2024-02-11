import pyotp, time, os
from jxdb import JsonDB
from threading import Thread
from tkinter import messagebox
import customtkinter as ctk

if not os.path.exists('data.jxdb'):
    def create_db():
        db = JsonDB()
        db.save('data.jxdb', 'password')
    create_db()

class MainWindow():

    def main():

        def update():
            while True:
                time.sleep(3)
                for i in inframe.winfo_children():
                    i.destroy()
                db = JsonDB()
                db.open('data.jxdb', 'password')
                tuples=db.items()
                for i in tuples:
                    appname = i[0]
                    token = i[1]
                    obj=pyotp.parse_uri(token)
                    now=obj.now()
                    ctk.CTkLabel(inframe, text=f'\n{appname}\n{now}\n', font=('', 16)).pack()

        def getnew():
            try:
                token=entry.get()
                pyotp.parse_uri(token)
                appname_parts = token.split('&')
                for name in appname_parts:
                    if 'issuer=' in name:
                        appname=name.replace('issuer=', '').replace('%20', ' ')
                db = JsonDB()
                db.open('data.jxdb', 'password')
                db.set(appname, token)
                db.save('data.jxdb', 'password')
                messagebox.showinfo(title='SUCCESS', message=f'Successfully added {appname}')
            except:
                messagebox.showerror(title='INVALID TOKEN', message='Incorrect token')

        def start_getnew():
            Thread(target=getnew).start()

        app = ctk.CTk()
        app.geometry("350x480")
        app.title("S2FA")

        ctk.CTkLabel(app, text='\n2FA TOTP', font=('', 24)).pack()

        entry = ctk.CTkEntry(app, placeholder_text="Enter otpauth:// token")
        entry.pack()
        btn = ctk.CTkButton(app, text="Add", command=start_getnew)
        btn.pack()

        Thread(target=update).start()

        inframe = ctk.CTkScrollableFrame(master=app, width=300, height=350)
        inframe.pack()       

        app.mainloop()


if __name__ == '__main__':
    MainWindow.main()
