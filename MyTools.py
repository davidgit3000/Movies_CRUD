from tkinter import *
from datetime import datetime

def DeselectAll(*var):
    ''' Deselect all checked item '''
    for i in var:
        if i.get() == 1:
            i.set(0)

class CreateToolTip(object):
    """
    Create a tooltip for a given widget
    """
    def __init__(self, widget, text='widget info'):
        self.waittime = 100     #miliseconds
        self.wraplength = 200   #pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(self.tw, text=self.text, justify='left',
                       background="#ffffe0", relief='solid', borderwidth=1,
                       wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()

    # Source: https://stackoverflow.com/questions/3221956/how-do-i-display-tooltips-in-tkinter - Coded by crxguy52
#====================================================================================================================

#====================================================================================================================
class Change_Widget_Background:
   '''
   Change the color of a button when the mouse is hovering over that button
   '''
   
   def __init__(self, widget, b_defaultColor=None, f_defaultColor=None, b_color=None, f_color=None):
      self.widget = widget
      self.b_defaultColor = b_defaultColor
      self.b_color = b_color
      self.f_defaultColor = f_defaultColor
      self.f_color = f_color
      self.widget.bind('<Enter>', self.change_color)
      self.widget.bind('<Leave>', self.no_color)


   def change_color(self, event=None):
      self.widget.config(background=self.b_color, foreground=self.f_color)

   def no_color(self, event=None):
      self.widget.config(background=self.b_defaultColor, foreground=self.f_defaultColor)

# Source: https://www.tutorialspoint.com/change-the-color-upon-hovering-over-button-in-tkinter
#======================================================================================================================

#======================================================================================================================
# Create a funtion that sort the date
def Date_Bubble_Sort(li, reverse):
    ''' Sort the date in a list of tuple including a date string '''
    if reverse == True:
        for i in range(len(li)):
            for j in range(len(li)-i-1):
                ele1 = datetime.strptime(li[j][0], '%m/%d/%Y')
                ele2 = datetime.strptime(li[j+1][0], '%m/%d/%Y')
                if ele1 < ele2:
                    temp = li[j]
                    li[j] = li[j+1]
                    li[j+1] = temp
        return li
    else:
        for i in range(len(li)):
            for j in range(len(li)-i-1):
                ele1 = datetime.strptime(li[j][0], '%m/%d/%Y')
                ele2 = datetime.strptime(li[j+1][0], '%m/%d/%Y')
                if ele1 > ele2:
                    temp = li[j]
                    li[j] = li[j+1]
                    li[j+1] = temp
        return li

""" a = [('02/03/2012', 121),('06/21/2000', 231),('05/15/2020', 148), ('07/28/2000',221)]
date_bubble_sort(a, False)
#c = date_bubble_sort(a, False)
print(a)
#print(c) """
#=============================================================================================
# Copy of the treeview_sort_column() funtion from the project Movies_CRUD.py (line 369)
""" def treeview_sort_column(col, reverse):
    ''' Sort the selected column in the Treeview object '''
    l = [(movies_tv.set(k, col), k) for k in movies_tv.get_children()]
    #l1 = [movies_tv.set(k, col) for k in movies_tv.get_children()]
    #print('l before sort\n', l)
    #print('l1 before sort\n',l1)
    #print()
    for i in l:
        if '/' in i[0]:                     # Check if user selected the date column or not
            date_bubble_sort(l, reverse)
        else:
            l.sort(reverse=reverse)
    # rearrange items in sorted positions using move() funtion of Treeview widget
    for index, (name, k) in enumerate(l):   # name: value of a cell in the selected column, k: id of the record    
        movies_tv.move(k, '', index)
    # reverse sort next time when clicking the column again
    movies_tv.heading(col, command=lambda: treeview_sort_column(col, not reverse)) """

# Source: https://stackoverflow.com/questions/1966929/tk-treeview-column-sort
# Change the row color by odd and even line
""" for rec in records:
        if count % 2 == 0:
            movies_tv.insert('', END, text=id, values=rec, tags=('even',))
        else:
            movies_tv.insert('', END, text=id, values=rec, tags=('odd',))
        count += 1 """

