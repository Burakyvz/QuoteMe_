from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import json
from random import randint
import smtplib
import datetime as dt
from twilio.rest import Client
import tkinter.messagebox

specific_author = ""
SENDER_MAIL_ADRESS = ""
SENDER_MAIL_PASSWORD = ""
RECEIVER_MAIL_ADRESS = ""
PHONE_NUMBER = ""


# ---------------------------- SAVE QUOTE ------------------------------- #
def save():
    now = dt.datetime.now()
    date = f"{now.year}-{now.month}-{now.day} {now.hour}:{now.minute}:{now.second}"

    quote = add_UI.quote_text.get("1.0", END).capitalize()
    author = add_UI.author_entry.get()
    from_ = add_UI.from_entry.get()
    new_data = {
        author: {
            "quote": quote,
            "from": from_,
            "date": date,
        }
    }

    if len(quote) == 0 or len(author) == 0:
        messagebox.showerror(title="Oops", message="Please don't leave any fields empty!")
    else:
        try:
            with open("quote.json", "r") as f:
                # Reading old data
                d = json.load(f)
        except FileNotFoundError:
            with open("quote.json", "w") as f:
                json.dump(new_data, f, indent=4)
        else:
            # Updating old data with new data
            d.update(new_data)

            with open("quote.json", "w") as f:
                # Saving updated data
                json.dump(d, f, indent=4)
        finally:
            add_UI.quote_text.delete("1.0", END)
            add_UI.author_entry.delete(0, END)

    try:
        with open("author.txt", "a") as author_txt:
            author_txt.write(author + "\n")
    except FileNotFoundError:
        with open("author.txt", "w") as author_txt:
            author_txt.write(author + "\n")


# ------------------------- UI SETUP FOR CHOOSING ADD OR READ ----------------------------- #
def choose_UI():
    choose_UI.window = Tk()
    choose_UI.window.title("QuoteME")
    choose_UI.window.config(padx=50, pady=50)  # padding for window

    canvas = Canvas(height=250, width=280)
    logo_img = ImageTk.PhotoImage(Image.open("QuoteME.png"))  # PIL solution
    canvas.create_image(150, 140, image=logo_img)  # create_image(position, **options) I gave the half of images lengths
    # for a coordinate
    choose_UI.window.resizable(False, False)
    canvas.grid(row=0, column=1, padx=40, pady=30)  # padding for canvas

    # Label
    label = Label(text="What do you want?")
    label.grid(row=1, column=1, padx=5, pady=5)

    # Buttons
    add = Button(text="Adding new quotes", width=35, command=add_UI)
    add.grid(row=2, column=1, padx=5, pady=5)
    show = Button(text="Show me from existing quotes", width=35, command=show_UI)
    show.grid(row=3, column=1, padx=5, pady=5)
    mail = Button(text="Send me a mail", width=35, command=send_mail_button_func)
    mail.grid(row=4, column=1, padx=5, pady=5)
    sms = Button(text="Send me a sms", width=35, command=send_sms_button_func)
    sms.grid(row=5, column=1, padx=5, pady=5)
    generate_quote_by_author_name = Button(text="Generate quote for a specific author", width=35, command=author_specific_UI)
    generate_quote_by_author_name.grid(row=6, column=1, padx=5, pady=5)

    choose_UI.window.mainloop()


# ----------------------------- UI SETUP FOR ADDING QUOTES ------------------------------- #
def add_UI():
    global which_UI
    which_UI = "add_UI"

    choose_UI.window.destroy()
    add_UI.window = Tk()
    add_UI.window.title("QuoteME")
    add_UI.window.config(padx=50, pady=50)  # padding for window

    canvas = Canvas(height=250, width=280)
    logo_img = img = ImageTk.PhotoImage(Image.open("QuoteME.png"))  # PIL solution
    canvas.create_image(125, 140, image=logo_img)  # create_image(position, **options) I gave the half of images lengths
    # for a coordinate
    add_UI.window.resizable(False, False)
    canvas.grid(row=0, column=1, padx=20, pady=20)  # padding for canvas

    # Labels
    quote_label = Label(text="Write Your Quote:")
    quote_label.grid(row=2, column=0)
    author_label = Label(text="Says Who:")
    author_label.grid(row=3, column=0)
    from_label = Label(text="From: ")
    from_label.grid(row=4, column=0)

    # Entries
    add_UI.author_entry = Entry(width=50)
    add_UI.author_entry.grid(row=3, column=1)
    add_UI.from_entry = Entry(width=50)
    add_UI.from_entry.grid(row=4, column=1)

    # Text (you can't alter the height of an entry but you can with a text)
    add_UI.quote_text = Text(width=70, height=5)
    add_UI.quote_text.grid(row=2, column=1)
    add_UI.quote_text.focus()  # starts the cursor in that text

    # Buttons
    save_button = Button(text="SAVE", width=35, command=save)
    save_button.grid(row=5, column=1)
    return_img = PhotoImage(file="return_button1.png")
    return_button = Button(image=return_img, command=return_)
    return_button.place(x=-30, y=-30)

    add_UI.window.mainloop()


# ----------------------------- UI SETUP FOR SHOWING QUOTES ------------------------------- #
def show_UI():
    global which_UI
    which_UI = "show_UI"

    global specific_author
    if specific_author == "":
        choose_UI.window.destroy()

    BACKGROUND_COLOR = "#B1DDC6"

    show_UI.window = Tk()
    show_UI.window.title("QuoteME")
    show_UI.window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
    show_UI.window.resizable(False, False)

    show_UI.canvas = Canvas(width=800, height=526)
    card_front_img = PhotoImage(file="card_front.png")
    show_UI.canvas.create_image(400, 263, image=card_front_img)
    show_UI.author_word = show_UI.canvas.create_text(400, 420, text=f"{quote_generator()[0]}",
                                                     font=("Ariel", 40, "italic"))
    show_UI.quote_word = show_UI.canvas.create_text(420, 150, text=f"{quote_generator()[1]}",
                                                    font=("Ariel", 50, "bold"))
    show_UI.canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
    show_UI.canvas.grid(row=0, column=0)

    # Button
    next_button = Button(text="Next", width=20, height=2, command=next_quote)
    next_button.grid(row=1, column=0, padx=20, pady=20)
    del_button = Button(text="Delete", width=20, height=2, command=delete_json_element)
    del_button.grid(row=2, column=0)
    return_img = PhotoImage(file="return_button1.png")
    return_button = Button(image=return_img, command=return_)
    return_button.place(x=-30, y=-30)

    show_UI.window.mainloop()


# ----------------------------- QUOTE GENERATOR ------------------------------- #

def quote_generator():
    with open('author.txt', 'r') as f:
        author_list = [line.strip() for line in f]

    author_list_without_duplicates = []

    for i in author_list:
        if i not in author_list_without_duplicates:
            author_list_without_duplicates.append(i)

    with open("quote.json", "r") as f:
        data = json.load(f)

    x = randint(0, (len(author_list_without_duplicates) - 1))
    author_name = author_list_without_duplicates[x]
    quote = data[author_name]["quote"]
    my_list = [author_name, quote]

    global specific_author
    if specific_author != "":
        my_list = [specific_author, data[specific_author]["quote"]]

    quote_generator.msg = f"{quote} -{author_name}"
    return my_list

x = ""
def next_quote():
    global x
    x = quote_generator()
    quote_letters = []
    a = 0
    for i in x[1]:
        if a % 25 != 0:
            quote_letters.append(i)
            a += 1
        elif a % 25 == 0:
            quote_letters.append("\n" + i)
            a += 1
    quote_with_spaces = "".join(quote_letters)

    show_UI.canvas.itemconfig(show_UI.quote_word, text=quote_with_spaces)
    show_UI.canvas.itemconfig(show_UI.author_word, text=x[0])


my_email = SENDER_MAIL_ADRESS
my_password = SENDER_MAIL_PASSWORD


def msg():
    x = quote_generator()
    return f"{x[1]} -{x[0]}"


msg = msg()


def send_email():
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=RECEIVER_MAIL_ADRESS,
            msg=msg.encode("utf-8")
        )
        connection.close()


def send_sms():
    account_sid = "AC46d58ed437f1b38146b42014e9840896"
    auth_token = "8a06521ab95cab9f8e88d361986a2899"
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=msg,
        from_='+17197455841',
        to=PHONE_NUMBER
    )


def pop_up(x):
    tkinter.messagebox.showinfo(title="Sended!", message=f"A random quote is sent {x}!")


def send_mail_button_func():
    send_email()
    pop_up("by mail")


def send_sms_button_func():
    send_sms()
    pop_up("to your phone")


def return_():
    if which_UI == "show_UI":
        show_UI.window.destroy()
    if which_UI == "add_UI":
        add_UI.window.destroy()
    choose_UI()

# ----------------------------- UI SETUP FOR SHOWING AUTHOR SPECIFIC QUOTES ------------------------------- #
def author_specific_UI():
    author_specific_UI.window = Tk()
    author_specific_UI.window.title("QuoteME")
    choose_UI.window.destroy()
    author_specific_UI.window.config(padx=50, pady=50)

    author_specific_UI.listbox = Listbox(author_specific_UI.window)
    author_specific_UI.listbox.grid(row=0, column=0)

    with open('author.txt', 'r') as f:
        author_list = [line.strip() for line in f]

    for i in range(0, len(author_list)):
        author_specific_UI.listbox.insert(END, author_list[i])

    def select():
        global specific_author
        specific_author = author_specific_UI.listbox.get(ANCHOR)
        print(specific_author)
        author_specific_UI.window.destroy()
        show_UI()

    button = Button(author_specific_UI.window, text="Select", command=select)
    button.grid(row=1, column=0)

    author_specific_UI.window.mainloop()

# ----------------------------- DELETING A JSON ELEMENT ------------------------------- #
def delete_json_element():
    try:
        with open("quote.json", "r") as f:
            # Reading old data
            d = json.load(f)
    except FileNotFoundError:
        pass

    global x

    for element in d:
        del element[x]
 
    with open('data.json', 'w') as data_file:
        d = json.dump(d, f)

choose_UI()
