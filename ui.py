import tkinter as tk
import emoji
from backend import *

possible_emojis = []


def get_user_input():
    global possible_emojis
    possible_emojis.clear()
    output_label.config(text="")
    text = entry.get("1.0", tk.END).strip()
    print(text)
    for Emoji in get_emoji(text):
        possible_emojis.append(Emoji)

    listbox.delete(0, tk.END)

    for Emoji in possible_emojis:
        listbox.insert(tk.END, emoji.emojize(Emoji))


root = tk.Tk()

root.title("GetEmoji")

root.geometry("800x850")

root.configure(bg='white')

heading_label = tk.Label(root, text="AUTOMATIC EMOJI FINDER", font=("Helvetica", 16), bg='white')
heading_label.place(x=260, y=30)

input_label = tk.Label(root, text="Enter Text", font=("Helvetica", 16), bg='white')
input_label.place(x=350, y=80)
entry = tk.Text(root, width=50, height=2, bd=2, relief=tk.SOLID, font=("Helvetica", 12), padx=10, pady=5, bg='white')
entry.place(x=180, y=130)

button = tk.Button(root, text="Get Emoji", bg='white', command=get_user_input)
button.place(x=250, y=200)


def get_selected_emoji():
    if len(possible_emojis) != 0:
        selected_indices = listbox.curselection()
        if (len(selected_indices) != 0 and type(selected_indices[0]) == int):
            selected_emoji = possible_emojis[selected_indices[0]]
            user_input = entry.get("1.0", tk.END)
            user_input = user_input.replace("\n", "")
            output_label.config(text=f'{user_input} {selected_emoji}')


button2 = tk.Button(root, text="Select Emoji", bg='white', command=get_selected_emoji)
button2.place(x=450, y=200)

listbox = tk.Listbox(root, font=("Segoe UI Emoji", 30))
listbox.place(x=180, y=240)

output_label = tk.Label(root, font=("Helvetica", 15), bg='white', text="")
output_label.place(x=80, y=720)

root.mainloop()
