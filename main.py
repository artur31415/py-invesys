# !/usr/bin/python3
import invesys as invesys
import sys, os
import json

try:
    # for Python2
    import Tkinter as tk   ## notice capitalized T in Tkinter 
    print("python2")
except ImportError:
    # for Python3
    import tkinter as tk   ## notice lowercase 't' in tkinter here
    from tkinter import messagebox
    print("python3")


#------------------------------ GLOBAL VARS

counter = 0

Elements = []


#------------------------------ METHODS

def say_hi():
    print("yo ho!")

def setLabelText(label, text):
    global counter
    label['text'] = text + " " + str(counter)
    print("new text: " + label['text'])
    counter = counter + 1

def getEntryText(label, entry):
    eData = entry.get()
    label['text'] = eData
    #entry.delete(0, END)

def setDataOnTheList(listbox, entry):
    print("data is " + entry.get())
    listbox.insert(tk.END, entry.get())

def elementsToUI(listElements):
    global Elements

    
    
    listElements.delete(0, tk.END)

    for element in Elements:
        listElements.insert(tk.END, element.ToString())

def getElementFromUI(entryName, entryValue, listElements):
    global Elements

    entryNameVal = ""
    entryValueVal = 0

    try:
        entryNameVal = entryName.get()
        entryValueVal = float(entryValue.get())
    except:
        messagebox.showinfo("Error", "Error while retrievign data from the UI")
        print("val not defined!")
        return
    else:
        print("nothing went wrong")
    finally:
        print("The 'try except' is finished")

    element = invesys.Element(entryNameVal, entryValueVal)
    Elements.append(element)

    listElements.insert(tk.END, element.ToString())
    entryName.delete(0, tk.END)
    entryValue.delete(0, tk.END)

    #DEBUG
    print("All elements thus far!")
    for element in Elements:
        print(element.ToString())

    try:
        saveToTXT()
    except:
        print("Error while saving!")

def removeElement(listElements):
    global Elements

    selectedRow = listElements.get(listElements.curselection())
    selectedRowIndex = listElements.curselection()[0]
    print("selectedRow: " + selectedRow + "; " + str(selectedRowIndex))
    listElements.delete(selectedRowIndex)
    Elements.pop(selectedRowIndex)

def loadElements(listElements):
    global Elements
    Elements.clear()

    elementsOnFileStrJson = readFromTXT()

    for elementJsonStr in elementsOnFileStrJson:
        elementJson = json.loads(elementJsonStr)
        Elements.append(invesys.Element(elementJson["name"], elementJson["value"]))

    elementsToUI(listElements)

def updateElements():
    global Elements

    print("All elements thus far!")
    for element in Elements:
        print(element.ToString())

    try:
        saveToTXT()
    except:
        print("Error while saving!")

#----------------------------------------------------------------------------------------

def saveToTXT(fileName = "1"):
    global Elements

    filePath = os.path.dirname(sys.argv[0]) + "\\data" + fileName + ".txt"
    file = open(filePath, "w+")

    for element in Elements:
        file.write(element.ToJson() + "\n")

    file.close()

def readFromTXT(path=os.path.dirname(sys.argv[0]), fileName = "1"):
    global Elements

    filePath = os.path.dirname(sys.argv[0]) + "\\data" + fileName + ".txt"

    file = open(filePath, "r")

    fileData = []
    #print(file.read())

    for line in file:
        print(line)
        fileData.append(line)

    file.close()

    return fileData


#------------------------------------------------
#------------------------------ IMPLEMENTATION
#------------------------------------------------
root = tk.Tk()

root.geometry("700x600+100+100")

root.master = root

#shows the button
root.hi_there = tk.Button(root)
root.hi_there["text"] = "Yo mama!"
root.hi_there["command"] = say_hi
root.hi_there.pack()#pack(side="top")
root.hi_there.place(height=50, width=100, x=3, y=3)


#quit button
root.quit = tk.Button(root, text="QUIT", fg="red", command=root.master.destroy)
root.quit.pack()#pack(side="bottom")
root.quit.place(height=50, width=100, x=103, y=3)

root.l_debug = tk.Label(root, text="yo!", font=("Helvetica", 16))
root.l_debug.pack()
root.l_debug['text'] = "haha"
root.l_debug.place(x=203, y=3)

#another button
root.b_another = tk.Button(root, text="All right now!", command = lambda: setLabelText(root.l_debug, "mew!"))
root.b_another.pack()
root.b_another.place(height=50, width=100, x=3, y=103)


#endtry textfield
root.e_debug = tk.Entry(root, width=30)
root.e_debug.focus()
#FIXME: FIX THIS SHIT!
root.e_debug.bind("<Return>", lambda: getEntryText(root.l_debug, root.e_debug))
root.e_debug.pack()
root.e_debug.place(x=303, y=3)

root.b_another2 = tk.Button(root, text="Get Text", command = lambda: getEntryText(root.l_debug, root.e_debug))
root.b_another2.pack()
root.b_another2.place(height=50, width=100, x=303, y=33)


#set the list
root.lb_some_data = tk.Listbox(root)
root.lb_some_data.pack()
root.lb_some_data.place(x=303, y=103)


root.b_set_list_data = tk.Button(root, text="Add to the list", command = lambda: setDataOnTheList(root.lb_some_data, root.e_debug))
root.b_set_list_data.pack()
root.b_set_list_data.place(height=50, width=100, x=503, y=33)

################################################################
################################################################

#name entry label
root.l_element_name = tk.Label(root, text="name", font=("Helvetica", 12))
root.l_element_name.pack()
root.l_element_name.place(x=3, y=200)

#name entry
root.e_element_name = tk.Entry(root, width=30)
root.e_element_name.pack()
root.e_element_name.place(x=3, y=230)

#value entry label
root.l_element_value = tk.Label(root, text="value", font=("Helvetica", 12))
root.l_element_value.pack()
root.l_element_value.place(x=203, y=200)

#value entry
root.e_element_value = tk.Entry(root, width=8)
root.e_element_value.pack()
root.e_element_value.place(x=203, y=230)

#button save
root.b_get_element = tk.Button(root, text="Save", command = lambda: getElementFromUI(root.e_element_name, root.e_element_value, root.lb_some_data))
root.b_get_element.pack()
root.b_get_element.place(height=25, width=75, x=3, y=260)

#button delete
root.b_remove_element = tk.Button(root, text="remove", command = lambda: removeElement(root.lb_some_data))
root.b_remove_element.pack()
root.b_remove_element.place(height=25, width=75, x=80, y=260)

#button load
root.b_load_element = tk.Button(root, text="load", command = lambda: loadElements(root.lb_some_data))
root.b_load_element.pack()
root.b_load_element.place(height=25, width=75, x=157, y=260)

#button update
root.b_update_element = tk.Button(root, text="update", command = lambda: updateElements())
root.b_update_element.pack()
root.b_update_element.place(height=25, width=75, x=3, y=288)

print('sys.argv[0] =', sys.argv[0])             
pathname = os.path.dirname(sys.argv[0])        
print('path =', pathname)
print('full path =', os.path.abspath(pathname)) 




root.mainloop()



element = invesys.Element(name="pen", value=1.5)

print("mainloop: END")