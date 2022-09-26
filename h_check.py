import tkinter
from tkinter import filedialog as fd
from skimage.measure import profile_line
from skimage.io import imread
from matplotlib import pyplot as plt
from sklearn import preprocessing
import numpy as np

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import numpy as np


root = tkinter.Tk()
root.wm_title("Uniformity check tool")
filename = ''

def browsefunc():
    filename = fd.askopenfilename(filetypes=(("bmp files","*.bmp"),("All files","*.*")))
    ent1.insert(tkinter.END, filename) # add this
    print(filename)
    show_plot(filename)

def on_key_press(event):
    print("you pressed {}".format(event.key))
    key_press_handler(event, canvas, toolbar)
    canvas.mpl_connect("key_press_event", on_key_press)


def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

print(filename)

# image line profiling
def show_plot(filename):
    image = imread(filename)  # Read the images

    start = (0, 0)  # Start of the profile line
    end = (1200, 1920)  # End of the profile line
    profile = profile_line(image, start, end)

    fig, ax = plt.subplots(1, 2)
    ax[0].set_title('Image')
    ax[0].imshow(image)  # Show the film
    ax[0].plot([start[1], end[1]], [start[0], end[0]], 'r-', lw=2)

    # make int array
    for i in range(0, len(profile)):
        profile[i] = int(profile[i])
    arr = np.array(profile)
    # reshaping
    newarr = arr.reshape(-1, 1)
    # normalization
    profile_norm = preprocessing.normalize(newarr, norm='max', axis=0)
    # define function to calculate cv
    cv = lambda x: np.std(x, ddof=1) / np.mean(x) * 100
    # calculate CV
    profile_cv = cv(profile)
    print(' CV: ', profile_cv)
    # define uniformity function
    uni = lambda x: np.min(x) / np.max(x) * 100
    # calculate uniformity
    profile_uni = uni(profile)
    print(' Uniformity: ', profile_uni)
    # define roll-off
    rolloff = lambda x: (np.max(x) - np.min(x)) / np.max(x) * 100
    # calculate roll-off
    profile_rolloff = rolloff(profile)
    print(' Roll-off along red line: ', profile_rolloff)

    # drawing ax-1 plot
    ax[1].plot(profile_norm)
    # these are matplotlib.patch.Patch properties
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    textstr = '\n'.join((
        r'$\mathrm{cv: }=%.2f$' % (profile_cv,),
        r'$\mathrm{uniformity: }=%.2f$' % (profile_uni,),
        r'$\mathrm{rolloff: }=%.2f$' % (profile_rolloff,)))
    # textstr = '\n'.join((' CV: ' % (str(profile_cv) ), ' Uniformity: ' %(str(profile_uni) ) , ' Roll-off along red line: ' %(str(profile_rolloff ))))
    # place a text box in upper left in axes coords
    ax[1].text(0.05, 0.3, textstr, fontsize=14,
               verticalalignment='top', bbox=props)

    ax[1].set_ylabel('Intensity')
    ax[1].set_xlabel('Pixels')
    ax[1].grid()
    title_name = 'no distribution'
    counter = 0
    treshold = 0.1
    ax[1].axhline(treshold)
    title_name = 'Check status:' + title_name + ' BPN:' + str(counter) + ' CV: '
    ax[1].set_title(title_name)

    # to start drawing in tkinter
    canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)


button = tkinter.Button(master=root, text="Quit", command=_quit)
button.pack(side=tkinter.BOTTOM)

ent1=tkinter.Entry(root,font=40)
ent1.pack(side=tkinter.BOTTOM)

button1 = tkinter.Button(root,text="Open file",font=40,command=browsefunc)
button1.pack(side=tkinter.BOTTOM)
# button1.grid(row=2,column=4)


tkinter.mainloop()
# If you put root.destroy() here, it will cause an error if the window is
# closed with the window manager.