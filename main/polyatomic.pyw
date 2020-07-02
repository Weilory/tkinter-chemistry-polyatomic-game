from tkinter import *
from random import choice

one = "\N{SUBSCRIPT ONE}"
two = "\N{SUBSCRIPT TWO}"
three = "\N{SUBSCRIPT THREE}"
four = "\N{SUBSCRIPT FOUR}"
seven = "\N{SUBSCRIPT SEVEN}"


chemicals = ["CO"+three, "SO"+four, "NO"+three, "ClO"+three, "PO"+four, "IO"+three, "BrO"+three, "ClO"+two, "PO"+three, "SO"+three, "NO"+two, "MnO"+four, "BrO"+four, "ClO"+four, "IO"+four, "BrO", "ClO", "IO", "CH"+three+"COO", "OH", "HCO"+three, "Hg"+two, "NH"+four, "HSO"+four, "CN", "HPO"+four, "H"+two+"PO"+four, "SCN", "C"+two+"H"+three+"O"+two, "Cr"+two+"O"+seven, "CrO"+four, "O"+two, "C"+two+"O"+four]
terms = ['carbonate', 'sulfonate', 'nitrate', 'chlorate', 'phosphate', 'iodate', 'bromate', 'chlorite', 'phosphite', 'sulphite', 'nitrite', 'permanganate', 'perbromate', 'perchlorate', 'periodate', 'hypobromite', 'hypochlorite', 'hypoiodite', 'acetic acid', 'hydroxide', 'bicarbonate', "mercury(I)", "ammonium", "bisulfate", "cyanide", "biphosphate", "dihydrogen phosphate", "thiocyanate", "acetate", "dichromate", "chromate", "peroxide", "oxalate"]
valences = ["-2", "-2", "-1", "-1", "-3", "-1", "-1", "-1", "-3", "-2", "-1", "-2", "-1", "-1", "-1", "-1", "-1", "-1", "-1", "-1", "-1", "+2", "+1", "-1", "-1", "-2", "-1", "-1", "-1", "-2", "-2", "-2", "-2"]


# tkinter
root = Tk()
root.title("Polyatomic")
root.geometry("1000x500+200+20")


indices = 0
boolean = [True]
co = [x for x in range(len(chemicals))]
seq = list()
quiz = StringVar()
gen_chemicals = []
finish_sign = False


# shuffle a random index from 0 to len(chemicals)
def generate():
    global co, seq
    try:
        rand = choice(co)
        co.remove(rand)
        seq.append(rand)
        gen_chemicals.append(chemicals[rand])
        return rand
    except IndexError:
        global finish_sign
        finish_sign = True
        return False


# First Line: ask questions
# parameter True: mistake answer, ask the same question again
# parameter False: correct answer, ask the next question
def first_line_quiz(this=False):
    global quiz, last_answer
    if this:
        # mistake answer, ask the same question again
        graph = "#000000"
        rand = seq[-1]
    else:
        # last answer correct, ask the next question
        graph = "#0000FF"
        rand = generate()
        if rand is False:
            finish()
            return
    if boolean[-1]:
        # if boolean is True, it means the next one is chemical question
        quiz.set("What is the scientific term for %s ? " % chemicals[rand])
    else:
        # if boolean is False, it means the next one is valence question
        quiz.set("What is the valence for %s ? " % chemicals[rand])
    quiz_label = Label(root, textvariable=quiz, font=("Helvetica", 40), fg=graph)
    quiz_label.grid(row=0, columnspan=2)


# second line entry
sv = StringVar()
sv.set("Enter your answer here")

entryDia = Entry(root, font=("Helvetica", 50), textvariable=sv)
entryDia.grid(row=1, rowspan=2, columnspan=2)


# return Entry as string
def get_entry():
    return entryDia.get().strip()


# set Entry as None
def clear_entry():
    global sv
    sv.set("")


# info
total = -1
right = 0
mistake = 0


def average():
    try:
        return "%.2f%%" % float(((total - mistake) / total) * 100)
    except ZeroDivisionError:
        return "0.00%%"


third_line_sv = StringVar()
third_line_info = Label(root, textvariable=third_line_sv, font=("Helvetica", 40), fg="#000000")
third_line_info.grid(row=5, columnspan=2)


def third_line_change():
    global third_line_sv
    third_line_sv.set("")


# third line display: if none, give up. else, show error
def give_up_or_show_error(ind=None):
    global third_line_sv, third_line_info
    if ind is not None:
        # show error
        third_line_sv.set("Oops, it's incorrect")
        third_line_info = Label(root, textvariable=third_line_sv, font=("Helvetica", 40), fg="#fc4f30")
    else:
        # give up
        if boolean[-1]:
            third_line_sv.set(terms[seq[-1]])
        else:
            third_line_sv.set(valences[seq[-1]])


def finish():
    third_line_sv.set("Average: " + average())
    third_line_info1 = Label(root, textvariable=third_line_sv, font=("Helvetica", 40), fg="#0000FF")
    third_line_info1.grid(row=5, columnspan=2)


last_answer = [False]


def entry_press():
    global total, last_answer, finish_sign, mistake
    if finish_sign:
        finish()
        return
    # at start, jump cross one
    if total == -1:
        first_line_quiz()
        total += 1
        clear_entry()
        return
    # when the user play the game
    total += 1
    global boolean, right
    user_input = get_entry()
    if boolean[-1]:
        if user_input == terms[seq[-1]]:
            # term correct
            boolean.append(False)
            last_answer.append(True)
            right += 1
            first_line_quiz(last_answer[-1])
            clear_entry()
            third_line_change()
        else:
            # term wrong
            mistake += 1
            boolean.append(True)
            last_answer.append(True)
            give_up_or_show_error(ind=seq[-1])
    else:
        if user_input == valences[seq[-1]]:
            # valence correct
            boolean.append(True)
            last_answer.append(False)
            right += 1
            first_line_quiz(last_answer[-1])
            clear_entry()
            third_line_change()
        else:
            # valence wrong
            mistake += 1
            boolean.append(False)
            last_answer.append(True)
            give_up_or_show_error(ind=seq[-1])
    first_line_quiz(last_answer[-1])


def gu_press():
    global right
    if total == -1:
        return
    right -= 1
    give_up_or_show_error()


# button
guBTN = Button(root, text="give up", fg="#6d904f", font=("Helvetica", 40), command=lambda: gu_press())
guBTN.grid(row=3, rowspan=2, column=0)


entryBTN = Button(root, text="Entry", fg="#00bfd5", font=("Helvetica", 40), command=lambda: entry_press())
entryBTN.grid(row=3, rowspan=2, column=1)


# shortcut
def handle(event):
    if event.keysym == "comma":
        gu_press()
    elif event.keysym == "period":
        entry_press()


root.bind_all("<KeyPress>", handle)

# spacing
col_count, row_count = root.grid_size()

for col in range(col_count):
    root.grid_columnconfigure(col, minsize=60)

for row in range(row_count):
    root.grid_rowconfigure(row, minsize=60)

root.mainloop()
