import tkinter
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfile
import string

top = Tk()  # create object from library

top.title('Word Identifier')  # giving the window a tittle
top.minsize(1000, 650)

canvas = Canvas(top, width=900, height=450)  # creating a canvas to hold the picture
canvas.pack()  # displaying canvas
logo = Image.open('unnamed.jpg')  # opening image
img = ImageTk.PhotoImage(logo)  # converting image to tkinter image
canvas.create_image(130, 20, anchor=NW, image=img)  # displaying image on canvas by a 120 ,20 offset from top

label1 = Label(text='Enter text below')  # creating label
label1.pack()  # displaying label

entry1 = Entry(width=50, bd=7, justify='center')  # creating Entry for input
entry1.pack()  # displaying Entry


def gui_input():
    func(False)
    return None


def browse_file():
    func(True)
    but_text.set('Load a text file')
    return None


def func(file_open_request):
    if not file_open_request:
        text = entry1.get()  # getting elements from entry
    else:
        but_text.set('loading ...')
        file = askopenfile(mode='r', filetypes=[('Text files', '*.txt')])  # getting elements from text file
        if file is not None:
            text = file.read()

    lines = len(text.splitlines())  # getting number of lines
    original = (text.replace('\n', ' '))  # removing \n from text

    # Removing all punctuations
    container = original.split(' ')  # getting words and identifiers in a list
    numbers = []
    identifiers = []
    words = []
    characters = []
    punctuations = ''',!()-[]{};:'"<>./|\?@#$%^&*_~'''

    if len(container) == 1:
        for char in text:
            if char not in punctuations:
                characters.append(char)

    else:
        for item in range(0, len(container) - 1):
            for char in container[item]:
                if char not in punctuations:
                    characters.append(char)

    for element in range(0, len(container) - 1):
        for character in string.punctuation:
            container[element] = container[element].replace(character, '')

    # identifications of words, identifiers , numbers
    for txt in container:
        if txt.isnumeric():  # checking if the whole txt is a number
            numbers.append(txt)

        else:
            is_indent = False
            for char in txt:
                if char.isnumeric():  # checking if a character  is a number making it an identifier
                    identifiers.append(txt)
                    is_indent = True
                    break
            if not is_indent:
                if txt.isalnum():
                    words.append(txt)

    # checking repeated words / identifiers / numbers

    # words
    words_map = {}
    for txt in words:
        if txt != '' and txt != ' ':  # avoid listing '' and ' 'as a word
            if txt in words_map:
                words_map[txt] += 1
            else:
                words_map[txt] = 1
    # sorting mechanism that allows us to sort our dictionary by value.
    # This is an example of a Lambda function, which is a function without a name.
    words_sorted_list = sorted(words_map.items(), key=lambda x: x[1], reverse=True)

    # words_map = {k: v for k, v in words_map}

    # identifiers
    identifiers_map = {}
    for txt in identifiers:
        if txt in identifiers_map:
            identifiers_map[txt] += 1
        else:
            identifiers_map[txt] = 1
    identifier_sorted_list = sorted(identifiers_map.items(), key=lambda x: x[1], reverse=True)

    # numbers
    numbers_map = {}
    for txt in numbers:
        if txt in numbers_map:
            numbers_map[txt] += 1
        else:
            numbers_map[txt] = 1
    numbers_sorted_list = sorted(numbers_map.items(), key=lambda x: x[1], reverse=True)

    # characters
    characters_map = {}
    for char in characters:
        if char in characters_map:
            characters_map[char] += 1
        else:
            characters_map[char] = 1
    characters_sorted_list = sorted(characters_map.items(), key=lambda x: x[1], reverse=True)

    # tree view frame
    root = Tk()
    root.title('results')  # giving the window a tittle
    root.minsize(950, 500)

    lines_label = ttk.Label(root, text='Number of Lines :' + str(lines), padding=(0, 50, 0, 0), justify=tkinter.CENTER)
    lines_label.pack()

    words_label = ttk.Label(root, text='Number of words :' + str(len(words)), padding=(0, 20, 0, 0),
                            justify=tkinter.CENTER)
    words_label.pack()

    characters_label = ttk.Label(root, text='Number of characters :' + str(len(characters)), padding=(0, 20, 0, 0),
                                 justify=tkinter.CENTER)
    characters_label.pack()
    tree_frame = ttk.Frame(root)

    # column configuration
    root.columnconfigure(0, weight=10)
    root.columnconfigure(1, weight=1)

    # create Tree view
    tree = ttk.Treeview(tree_frame)

    # define our columns
    tree['columns'] = ('First Column', 'Second Column')

    # Defines headers
    tree.heading("First Column", text="Most Used Words", anchor=W)
    tree.heading("Second Column", text="Frequency", anchor=W)

    # Only shows headings and hides first empty column
    tree['show'] = 'headings'

    # Defines attributes of columns
    tree.column("First Column", width=140, minwidth=140, anchor=W)
    tree.column("Second Column", width=70, minwidth=70, anchor=W)

    # shows data in tree
    iteration = 0
    for tuple_i in words_sorted_list:  # values are themselves dictionaries
        if iteration < 5:
            tree.insert("", "end", values=(tuple_i[0], tuple_i[1]))
            iteration += 1
        else:
            break

    s = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=tree.yview)
    tree['yscrollcommand'] = s.set

    # Grids the tree and scrollbar
    tree.grid(row=0, column=0)
    s.grid(row=0, column=1, sticky=(N, S, E, W))

    # Packs the frame
    tree_frame.pack(expand=1, side=LEFT)

    # tree view frame
    tree_frame2 = ttk.Frame(root)

    # column configuration
    root.columnconfigure(0, weight=10)
    root.columnconfigure(1, weight=1)

    # create Tree view
    tree = ttk.Treeview(tree_frame2)

    # define our columns
    tree['columns'] = ('First Column', 'Second Column')

    # Defines headers
    tree.heading("First Column", text="Most Used Identifiers", anchor=W)
    tree.heading("Second Column", text="Frequency", anchor=W)

    # Only shows headings and hides first empty column
    tree['show'] = 'headings'

    # Defines attributes of columns
    tree.column("First Column", width=140, minwidth=140, anchor=W)
    tree.column("Second Column", width=70, minwidth=70, anchor=W)

    # shows data in tree
    iteration = 0
    for tuple_i in identifier_sorted_list:  # values are themselves dictionaries
        if iteration < 5:
            tree.insert("", "end", values=(tuple_i[0], tuple_i[1]))
            iteration += 1
        else:
            break

    s = ttk.Scrollbar(tree_frame2, orient=VERTICAL, command=tree.yview)
    tree['yscrollcommand'] = s.set

    # Grids the tree and scrollbar
    tree.grid(row=0, column=0)
    s.grid(row=0, column=1, sticky=(N, S, E, W))

    # Packs the frame
    tree_frame2.pack(expand=1, side=LEFT)

    # tree view frame
    tree_frame3 = ttk.Frame(root)

    # column configuration
    root.columnconfigure(0, weight=10)
    root.columnconfigure(1, weight=1)

    # create Tree view
    tree = ttk.Treeview(tree_frame3)

    # define our columns
    tree['columns'] = ('First Column', 'Second Column')

    # Defines headers
    tree.heading("First Column", text="Most Used Numbers", anchor=W)
    tree.heading("Second Column", text="Frequency", anchor=W)

    # Only shows headings and hides first empty column
    tree['show'] = 'headings'

    # Defines attributes of columns
    tree.column("First Column", width=140, minwidth=140, anchor=W)
    tree.column("Second Column", width=70, minwidth=70, anchor=W)

    # shows data in tree
    iteration = 0
    for tuple_i in numbers_sorted_list:  # values are themselves dictionaries
        if iteration < 5:
            tree.insert("", "end", values=(tuple_i[0], tuple_i[1]))
            iteration += 1
        else:
            break

    s = ttk.Scrollbar(tree_frame3, orient=VERTICAL, command=tree.yview)
    tree['yscrollcommand'] = s.set

    # Grids the tree and scrollbar
    tree.grid(row=0, column=0)
    s.grid(row=0, column=1, sticky=(N, S, E, W))

    # Packs the frame
    tree_frame3.pack(expand=1, side=LEFT)

    # tree view frame
    tree_frame4 = ttk.Frame(root)

    # column configuration
    root.columnconfigure(0, weight=10)
    root.columnconfigure(1, weight=1)

    # create Tree view
    tree = ttk.Treeview(tree_frame4)

    # define our columns
    tree['columns'] = ('First Column', 'Second Column')

    # Defines headers
    tree.heading("First Column", text="Most Used Characters", anchor=W)
    tree.heading("Second Column", text="Frequency", anchor=W)

    # Only shows headings and hides first empty column
    tree['show'] = 'headings'

    # Defines attributes of columns
    tree.column("First Column", width=140, minwidth=140, anchor=W)
    tree.column("Second Column", width=70, minwidth=70, anchor=W)

    # shows data in tree
    iteration = 0
    for tuple_i in characters_sorted_list:  # values are themselves dictionaries
        if iteration < 5:
            tree.insert("", "end", values=(tuple_i[0], tuple_i[1]))
            iteration += 1
        else:
            break

    s = ttk.Scrollbar(tree_frame4, orient=VERTICAL, command=tree.yview)
    tree['yscrollcommand'] = s.set

    # Grids the tree and scrollbar
    tree.grid(row=0, column=0)
    s.grid(row=0, column=1, sticky=(N, S, E, W))

    # Packs the frame
    tree_frame4.pack(expand=1, side=LEFT)

    return None


button1 = Button(text='start identification', command=gui_input, bg="#B06C05", fg="white", height=2, width=15)
button1.pack()

label2 = Label(text='or', bd=10)
label2.pack()

but_text = StringVar()
but_text.set('Load a text file')

button2 = Button(textvariable=but_text, command=browse_file, bg="#B06C05", fg="white", height=2, width=15)
button2.pack()

top.mainloop()
