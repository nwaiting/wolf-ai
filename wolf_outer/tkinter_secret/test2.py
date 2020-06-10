from tkinter import *

# Callbacks------------
def onClickOpen(selected):
#	f = open(selected, 'r+')
	print('open')

def onClickSaveAs(text):

	print('onClickSaveAs')

	saveAsWindow = Toplevel()
	saveAsWindow.title('Save As')

	fileNameEntry = Entry(saveAsWindow)
	fileNameEntry.pack(padx=10)

	saveAsButton = Button(saveAsWindow, text='Save As', command=lambda: saveAs(fileNameEntry.get(), text, saveAsWindow))
	saveAsButton.pack()

def saveAs(name, text, window):

	window.destroy()
	save(name, text)

def save(name, text):

	print('Save')
	f = open(name, 'a')
	f.write(text)
	f.close()

# Widgets--------------
root = Tk()

textBox = Text(root)
textBox.pack()

menuBar = Menu(root) # Create menu bar


fileMenu = Menu(menuBar, tearoff=0) # File button

#------------- Definition of file menu
fileMenu.add_command(label="Open", command=lambda: onClickOpen('x'))
#fileMenu.add_command(label='Save', command=lambda: save())
fileMenu.add_command(label="Save As", command=lambda: onClickSaveAs(textBox.get(0.0, END)))
fileMenu.add_separator()
fileMenu.add_command(label='Exit', command=root.quit)

menuBar.add_cascade(label='File', menu=fileMenu) # Adding file button to menuBar
#--------------

root.config(menu=menuBar)
#----------------------
mainloop()



