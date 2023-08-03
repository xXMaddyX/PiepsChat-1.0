import tkinter as tk
import tkinter.simpledialog as sd
from PIL import Image, ImageTk
import ttkbootstrap as ttk
import threading
import socket

delay = 0.05

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 1600))

nickname = "Maddy"

# tkinter Main Window 
main = ttk.Window(themename="solar")
main.title("Piep´s Chat 1.0")
main.geometry("800x550")


image = Image.open("PiepsmitTasse.png").resize((100, 100))
photo = ImageTk.PhotoImage(image)


# Char Text Animation
def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == "NICK":
                client.send(nickname.encode('ascii'))
            else:
                output_widget.insert(tk.END, f"{message}")
                output_widget.insert(tk.END, f"\n")
                output_widget.configure(fg="yellow")
                output_widget.see(tk.END)
                output_widget.update()  

        except:
            print("An error occured")
            client.close()
            break   

def sendToServer():
    input_text = (f'{nickname}: {input_widget.get()}')
    if input_text: 
        client.send(input_text.encode('ascii'))  
        input_widget.delete(0, tk.END)


# Drop down menu 
def show_menu(event):
    menu.post(event.x_root, event.y_root)


# Stop Programm
def exit_programm():
    main.destroy()


menu = ttk.Menu(main, tearoff=0)
menu.add_command(label="Nickname")
menu.add_command(label="Beenden", command=exit_programm)

# Button placement
MenueButton = ttk.Button(main, text="Menue")
MenueButton.place(x=10, y=0)
MenueButton.bind("<Button-1>", show_menu)
MenueButton.bind("<Button-2>", exit_programm)

#photo placement
photo_label = ttk.Label(main, image=photo, text="by Freelance Archery", compound="left")
photo_label.config()
photo_label.place(x=30, y=465)


# Send Button
send_button = ttk.Button(main, text="Senden", command=sendToServer)
send_button.place(x=390, y=500)


# Textein- und -ausgabe-Widgets erstellen
output_widget = ttk.Text(main, font=("Helvetica", 14), height=18, width=70, wrap=tk.WORD)
output_widget.place(x=10, y=30)
output_widget.see(tk.END)
input_widget = ttk.Entry(main, font=("Helvetica", 16), width=64)
input_widget.place(x=10, y=450)
input_widget.focus_set()

receive_thread = threading.Thread(target=receive)
receive_thread.start()

main.mainloop()