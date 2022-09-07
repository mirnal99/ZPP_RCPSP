from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from graph import get_imgs

root = Tk()
root.title('Resource Constrained Scheduling Problem')
#root.geometry(str(root.winfo_screenwidth()) + 'x' + str(root.winfo_screenheight()))
root.state('zoomed')


# Frames and canvases are made to enable fullscreen scrollbar

# Create a main frame
main_frame = Frame()
main_frame.pack(fill=BOTH, expand=1)

# Create a canvas
canvas = Canvas(main_frame)
canvas.pack(side=TOP, fill=BOTH , expand=1)

# Add a scrollbar to canvas
scrollbar = ttk.Scrollbar(main_frame, orient=HORIZONTAL, command=canvas.xview)
scrollbar.pack(side=TOP, fill=X)

# Configure canvas
canvas.configure(xscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Another frame inside canvas
second_frame = Frame(canvas)

# Add new frame to a window in canvas
canvas.create_window((0,0), window=second_frame, anchor='nw')


# Defining labels and images

# Frame to put images separately of menus
img_frame = Frame(second_frame)
img_frame.grid(row=1, column=0, rowspan=1000, columnspan=1000)

# Define labels so you can destroy them
img_label3 = Label(img_frame)
img_label2 = Label(img_frame)
img_label1 = Label(img_frame)
img_label0 = Label(img_frame)
legend_label0 = Label(img_frame)
legend_label1 = Label(img_frame)
legend_label2 = Label(img_frame)
legend_label3 = Label(img_frame)

# Define dropdown options
sgs_options = ['Parallel', 'Serial']
pr_options = ['SPT', 'MIS', 'LST', 'LFT', 'MSL', 'MTS', 'GRPW', 'GRPW2']
num_options = ['30', '60', '90', '120']
data_options = [str(i) for i in range(1,49)]


def updateScrollRegion():
	canvas.update_idletasks()
	canvas.config(scrollregion=img_frame.bbox())


def clear_screen():

    img_label3.destroy()
    img_label2.destroy()
    img_label1.destroy()
    img_label0.destroy()
    legend_label0.destroy()
    legend_label1.destroy()
    legend_label2.destroy()
    legend_label3.destroy()

    return


def generate():

    file = 'j' + num_clicked.get() + data_clicked.get() + '_5.txt'
    print(file, sgs_clicked.get(), pr_clicked.get())
    maxF, _ = get_imgs(num_clicked.get(), file, sgs_clicked.get(), pr_clicked.get())
    
    global img_label3
    global img_label2
    global img_label1
    global img_label0
    global legend_label0
    global legend_label1
    global legend_label3
    global legend_label2

    clear_screen()

    """
    Putting image on a screen:
    1. Open it
    2. Resize it
    3. Make it Tkinter friendly
    4. Put it in a label
    5. Tell label it's an image
    6. Position it on a screen
    Repeat process for as many images you need
    """

    img3 = Image.open("imgs\img3.png")
    resized = img3.resize((maxF*25, 230), Image.ANTIALIAS)
    photo3 = ImageTk.PhotoImage(resized)
    img_label3 = Label(img_frame, image=photo3)
    img_label3.image = photo3
    img_label3.grid(row=0, column=0, columnspan=6)

    img2 = Image.open("imgs\img2.png")
    resized = img2.resize((maxF*25, 230), Image.ANTIALIAS)
    photo2 = ImageTk.PhotoImage(resized)
    img_label2 = Label(img_frame, image=photo2)
    img_label2.image = photo2
    img_label2.grid(row=1, column=0, columnspan=6)

    img1 = Image.open("imgs\img1.png")
    resized = img1.resize((maxF*25, 230), Image.ANTIALIAS)
    photo1 = ImageTk.PhotoImage(resized)
    img_label1 = Label(img_frame, image=photo1)
    img_label1.image = photo1
    img_label1.grid(row=2, column=0, columnspan=6)

    img0 = Image.open("imgs\img0.png")
    resized = img0.resize((maxF*25, 230), Image.ANTIALIAS)
    photo0 = ImageTk.PhotoImage(resized)
    img_label0 = Label(img_frame, image=photo0)
    img_label0.image = photo0
    img_label0.grid(row=3, column=0, columnspan=6)


    while(True):
        
        # keep track of how many legends are needed
        num_of_legends = int(int(num_clicked.get())/30)

        legend0 = ImageTk.PhotoImage(Image.open("imgs\legend0.png"))
        legend_label0 = Label(img_frame, image=legend0)
        legend_label0.image = legend0
        legend_label0.grid(row=0, column=7, rowspan=4)
        if num_of_legends==1:
            break

        legend1 = ImageTk.PhotoImage(Image.open("imgs\legend1.png"))
        legend_label1 = Label(img_frame, image=legend1)
        legend_label1.image = legend1
        legend_label1.grid(row=0, column=8, rowspan=4)
        if num_of_legends==2:
            break

        legend2 = ImageTk.PhotoImage(Image.open("imgs\legend2.png"))
        legend_label2 = Label(img_frame, image=legend2)
        legend_label2.image = legend2
        legend_label2.grid(row=0, column=9, rowspan=4)
        if num_of_legends==3:
            break

        legend3 = ImageTk.PhotoImage(Image.open("imgs\legend3.png"))
        legend_label3 = Label(img_frame, image=legend3)
        legend_label3.image = legend3
        legend_label3.grid(row=0, column=10, rowspan=4)
        if num_of_legends==4:
            break

        if num_of_legends > 4:
            raise Exception('num_of_legends is greater than 4!')


    updateScrollRegion()
    


# set default option
sgs_clicked = StringVar()
pr_clicked = StringVar()
num_clicked = StringVar()
data_clicked = StringVar()
sgs_clicked.set(sgs_options[0])
pr_clicked.set(pr_options[0])
num_clicked.set(num_options[0])
data_clicked.set(data_options[0])

# create labels
sgs_label = Label(second_frame, text='Schedule Generation Scheme: ')
pr_label = Label(second_frame, text='Priority Rule: ')
data_label = Label(second_frame, text='Data: ')
sgs_label.grid(row=0, column=0)
pr_label.grid(row=0, column=2)
data_label.grid(row=0, column=4)

# create dropdown menus
sgs_drop = OptionMenu(second_frame, sgs_clicked, *sgs_options)
pr_drop = OptionMenu(second_frame, pr_clicked, *pr_options)
num_drop = OptionMenu(second_frame, num_clicked, *num_options)
data_drop = OptionMenu(second_frame, data_clicked, *data_options)
sgs_drop.grid(row=0, column=1)
pr_drop.grid(row=0, column=3)
num_drop.grid(row=0, column=5)
data_drop.grid(row=0, column=6)

# create button
button = Button(second_frame, text='Generate Schedule', command=generate)
button.grid(row=0, column=7)


root.mainloop()