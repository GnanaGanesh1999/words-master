# --------------------------------- Imports ----------------------------------- #
from tkinter import *
import pandas as pd
from random import choice
# --------------------------------- Constants --------------------------------- #
FONT_NAME = "Ariel"
LG_FONT, MD_FONT, SM_FONT = 60, 40, 18
BACKGROUND_COLOR = "#b1ddc6"
timer, arg = None, 1
# --------------------------------- Timer ------------------------------------- #


def flip_card(value):
    if value == 1:
        show_answer()
    else:
        select_a_random_word()


def restart_timer():
    global timer, arg
    root.after_cancel(timer)
    timer = root.after(3000, flip_card, arg)


def finished():
    global timer, current_word
    root.after_cancel(timer)
    canvas.itemconfig(card, image=img_front)
    canvas.itemconfig(language_text, text="Congratulations",font=(FONT_NAME, LG_FONT, "bold"),  fill="black")
    canvas.itemconfig(main_word, text="You have mastered all words !", font=(FONT_NAME, SM_FONT, "bold"), fill="black")
    canvas.itemconfig(transliterate_word, text="", fill="black")
    current_word = {}


# --------------------------------- Data -------------------------------------- #
data, current_word = {}, ""


def load_data():
    global data
    try:
        data_from_file = pd.read_csv("data/words_to_learn.csv")
        data = data_from_file.to_dict('records')
    except FileNotFoundError:
        data_from_file = pd.read_csv("data/hindi_to_english.csv")
        data = data_from_file.to_dict('records')
    except:
        finished()


    # for a_data in data_from_file.iterrows():
    #     data[a_data[1].WORD] = {
    #         "transliterate": a_data[1]["TRANSLITERATION"],
    #         "meaning": a_data[1].ENGLISH
    #     }
    #     words_list.append(a_data[1].WORD)
    # # print(data)


def select_a_random_word():
    global current_word, arg
    try:
        new_word = choice(data)
        canvas.itemconfig(card, image=img_front)
        canvas.itemconfig(language_text, text="Hindi", fill="black")
        canvas.itemconfig(main_word, text=new_word["WORD"], font=(FONT_NAME, LG_FONT, "bold"), fill="black")
        canvas.itemconfig(transliterate_word, text=new_word["TRANSLITERATION"], fill="black")
        current_word = new_word
        arg = 1
    except IndexError:
        finished()

    restart_timer()


def show_answer():
    try:
        global arg
        canvas.itemconfig(card, image=img_back)
        canvas.itemconfig(language_text, text="English", fill="white")
        canvas.itemconfig(main_word, text=current_word["ENGLISH"], font=(FONT_NAME, SM_FONT), fill="white")
        canvas.itemconfig(transliterate_word, text="")
        arg = -1
        restart_timer()
    except (TypeError, ValueError, KeyError):
        finished()


def remove_known_word():
    try:
        global data
        select_a_random_word()
        data.remove(current_word)
        new_data = pd.DataFrame(data)
        new_data.to_csv("data/words_to_learn.csv", index=False)
        load_data()
    except (AttributeError, ValueError):
        finished()


# --------------------------------- UI Setup ---------------------------------- #
# Window
root = Tk()
root.resizable(False, False)
root.title("Word Master")
root.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
timer = root.after(3000, flip_card, arg)

# Canvas
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
img_front = PhotoImage(file="images/card_front.png")
img_back = PhotoImage(file="images/card_back.png")
card = canvas.create_image(400, 265, image=img_front)
language_text = canvas.create_text(400, 140, text="Hindi", font=(FONT_NAME, MD_FONT, "bold"))
main_word = canvas.create_text(400, 280, text="लिए", font=(FONT_NAME, LG_FONT, "bold"))
transliterate_word = canvas.create_text(400, 370, text="lie", font=(FONT_NAME, SM_FONT))
canvas.grid(row=0, column=0, columnspan=3)

# Buttons
img_right = PhotoImage(file="images/right.png")
right_button = Button(command=remove_known_word, image=img_right, bg=BACKGROUND_COLOR, highlightthickness=0)
right_button.grid(row=1, column=2)

img_wrong = PhotoImage(file="images/wrong.png")
wrong_button = Button(command=show_answer, image=img_wrong, bg=BACKGROUND_COLOR, highlightthickness=0)
wrong_button.grid(row=1, column=0)

load_data()
select_a_random_word()
restart_timer()
root.eval('tk::PlaceWindow . center')
root.mainloop()
