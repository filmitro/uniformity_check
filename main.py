from matplotlib import pyplot as plt
from skimage.measure import profile_line
from skimage.io import imread
from sklearn import preprocessing
from tkinter import *
from tkinter import filedialog
import matplotlib as mp
import numpy as np

mp.use("TkAgg")
image = imread('with2.bmp') #Read the images

start = (0, 0) #Start of the profile line
end = (1200, 1920) #End of the profile line

profile = profile_line(image, start, end)

fig, ax = plt.subplots(1, 2)
ax[0].set_title('Image')
ax[0].imshow(image) #Show the film
ax[0].plot([start[1], end[1]], [start[0], end[0]], 'r-', lw=2) #Plot a red line across the film



title_name = 'no distribution'
counter = 0
treshold = 0.1
ax[1].axhline(treshold)

#make int array
for i in range(0, len(profile)):
    profile[i] = int(profile[i])
arr = np.array(profile)
#reshaping
newarr = arr.reshape(-1,1)
#normalization
profile_norm = preprocessing.normalize(newarr,norm='max', axis = 0)
#define function to calculate cv
cv = lambda x: np.std(x, ddof=1) / np.mean(x) * 100
#calculate CV
profile_cv = cv(profile)
print(' CV: ', profile_cv)
#define uniformity function
uni = lambda x: np.min(x) / np.max(x) * 100
#calculate uniformity
profile_uni =  uni(profile)
print(' Uniformity: ', profile_uni)
#define roll-off
rolloff = lambda x: (np.max(x) - np.min(x)) / np.max(x) * 100
#calculate roll-off
profile_rolloff = rolloff(profile)
print(' Roll-off along red line: ', profile_rolloff)


ax[1].plot(profile_norm)
# these are matplotlib.patch.Patch properties
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
textstr = '\n'.join((
    r'$\mathrm{cv: }=%.2f$' % (profile_cv, ),
    r'$\mathrm{uniformity: }=%.2f$' % (profile_uni, ),
    r'$\mathrm{rolloff: }=%.2f$' % (profile_rolloff, )))
#textstr = '\n'.join((' CV: ' % (str(profile_cv) ), ' Uniformity: ' %(str(profile_uni) ) , ' Roll-off along red line: ' %(str(profile_rolloff ))))
# place a text box in upper left in axes coords
ax[1].text(0.05, 0.3, textstr,  fontsize=14,
        verticalalignment='top', bbox=props)

ax[1].set_ylabel('Intensity')
ax[1].set_xlabel('Pixels')
ax[1].grid()

title_name = 'Check status:' + title_name + ' BPN:' + str(counter) + ' CV: '
ax[1].set_title(title_name)

plt.show()

def openFile():
    filepath = filedialog.askopenfilename(initialdir="C:\\Users\\Cakow\\PycharmProjects\\Main",
                                          title="Open file okay?",
                                          filetypes= (("text files","*.txt"),
                                          ("all files","*.*")))
    file = open(filepath,'r')
    print(file.read())
    file.close()

window = Tk()
button = Button(text="Open",command=openFile)
button.pack()
window.mainloop()




#check range
# for i in range(0, len(profile)-1):
#     if (profile[i, 1] <= treshold).any():
#         counter += 1
# if counter > 1:
#     title_name = ('REJECT')
# else:
#     title_name = ('PASS')

#make str
# profile_str = []
# for i in range(0, len(profile)-1):
#     profile_str.append(profile[i, 1])

# profile = profile_line(image, start, end, linewidth=1, mode='constant') #Take the profile line
# fig, ax = plt.subplots(2, 1, figsize=(10, 10)) #Create the figures
# ax[0].imshow(image) #Show the film at the top
# ax[0].plot(start, end, 'r-', lw=2) #Plot a red line across the film
# ax[1].plot(profile)
# ax[1].grid()