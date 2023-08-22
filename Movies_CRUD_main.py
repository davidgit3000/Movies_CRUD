#--------------------------------------------------------------------------------------------------------------------#
#----------------------------------<<<<         Name: David Lam            >>>>--------------------------------------#
#----------------------------------<<<<         Course: CISP 71            >>>>--------------------------------------#
#----------------------------------<<<<      Professor Sohair Zaki         >>>>--------------------------------------#
#----------------------------------<<<<     Project: Movies_CRUD Program   >>>>--------------------------------------#
#--------------------------------------------------------------------------------------------------------------------#

from tkinter import *
from tkinter import font
from tkinter import messagebox
import tkinter.ttk as ttk
from tkinter.ttk import Combobox, Style
from PIL import ImageTk, Image
from tkinter.colorchooser import askcolor
import os
import sqlite3

# Customized module, not built-in or installed one
from MyTools import Change_Widget_Background, CreateToolTip, DeselectAll, Date_Bubble_Sort
from MovieCustomException import *
from MyCustomToplevel import MyCustomToplevel


#path=r'G:\CISP 71(L)\Project CRUD CISP 71\Movies_CRUD_py'   # The path to my project
#============== Create the root object to display a window =======================
root = Tk()
root.geometry('1350x730+100+30')
root.config(bg='#C7E3E1') # Glass color (RGB: (199, 227, 225))
root.resizable(0, 0)
root.title('Movies on Netflix')
root.iconbitmap("Netflix.ico")
#===============================================================================================================

#==============<<<< Create a status bar to display the status of events one at a time >>>>======================

status_bar = Label(root, text='', font=('Helvetica', 10, 'bold'), anchor=CENTER, bg='red', fg='black')
status_bar.pack(fill=X, side=BOTTOM, ipady=5)

#==============================================================================================================

#=====================<<<< Create connection to the Movies database using SQLite3 >>>>=========================
conn = sqlite3.connect('Movies.db')
try:
    c = conn.cursor()           # Send command to SQLite to run a query

    c.execute('''CREATE TABLE Movies (
                ID INTEGER NOT NULL UNIQUE,
	            Movies TEXT,
	            Genres TEXT,
	            Director TEXT,
	            ReleaseDate TEXT,
	            Rating REAL
            );''')
    status_bar.config(text='Table created successfully')
except:
    status_bar.config(text='Table already existed')
    conn.rollback()
finally:
    conn.close()
#================================================================================================================

#############################################################################################################################
#######################################<<<<     Create funtions for my program     >>>>######################################
#############################################################################################################################

#==============================<<<< Create a function to clear the Entry after a user enter info >>>>======================================

def clearFields():
    movie_En.delete(0, END)
    director_En.delete(0, END)
    mid_En.delete(0, END)
    rating_En.delete(0, END)
    months_Com.set('')
    days_Com.set('')
    years_Com.set('')
    DeselectAll(*varList) # Unpack the list of var for Checkbutton defined below and deselect all checked boxes

#==========================================================================================================================================

#=============================<<<< Create a function to clear all the row of the Treeview widget >>>>======================================

def clearTreeview():
    ''' Clear all rows in the table '''
    
    for row in movies_tv.get_children():
        movies_tv.delete(row)
           
#===============================================================================================================================================
# Check user entry to ensure that all entry are in correct data type or complete
def checkEntry():
    # Check if any empty entry exists
    if len(mid_En.get()) == 0:
        mid_En.focus()
        raise IncompleteEntryError('Please enter Movie ID!')
    if len(movie_En.get()) == 0:
        movie_En.focus()
        raise IncompleteEntryError('Please enter Movie Name')
    if len(get_date()) < 10:
        raise IncompleteEntryError('Incomplete or empty date')
    if len(director_En.get()) == 0:
        director_En.focus()
        raise IncompleteEntryError('Please enter the director!')
    if len(rating_En.get()) == 0:
        rating_En.focus()
        raise IncompleteEntryError('Please enter rating!')
    # Check if any movie ID or rating is entered properly (ID: int and Rating: float)
    if mid_En.get().isalpha() or (not mid_En.get().isdigit()):
        mid_En.focus()
        raise ValueError('Invalid Movie ID entry')
    if rating_En.get().isalnum() and (not rating_En.get().isdigit()):
        rating_En.focus()
        raise ValueError('Invalid Rating entry')
#================================================================================================================================================

#==============================<<<< Create a function that allow users to add movies or TV shows to database >>>>================================ 

def add_Movie():
    ''' Add records to the Movies database '''

    conn = sqlite3.connect('Movies.db')
    try:
        checkEntry() # Check any existing empty entry
        
        # Check whether the ID that the user entered exists in the database. The ID of each movie should be unique
        c=conn.cursor()
        c.execute('SELECT oid FROM Movies WHERE ID=?', (mid_En.get(),))
        rows = c.fetchall()
        if len(rows) > 0:
            raise MatchedValueError('The record with entered ID already existed in the database')
        else:
            c.execute('INSERT INTO Movies VALUES (?,?,?,?,?,?)',
                (int(mid_En.get()), movie_En.get(), get_genres(), director_En.get(), get_date(), float(rating_En.get())))

        # Raise RatingError if the user is attempting to update the rating that has a value of over 10.0
        if float(rating_En.get()) > 10.0:
            #c.execute('DELETE FROM Movies WHERE Movies=?;', (movie_En.get(),))
            raise RatingError('Oh oh! The rating should be no more than 10. Please try again!')
        conn.commit()

    except RatingError as re:
        # Status bar for add_Movie() when rating error is more than 10.0
        status_bar.config(text='Rating Error')                                      
        messagebox.showerror('Error', re)
        conn.rollback()
    except MatchedValueError as mve:
        status_bar.config(text='Unable to add the records due to matched ID in the Moives database')
        messagebox.showerror('Error', mve)
        conn.rollback()
    except ValueError as v:
        # Status bar for add_Movie() when adding improper or incomplete values
        status_bar.config(text=v)   
        messagebox.showerror('Error', v)
        conn.rollback()
    except GenresLimitError as gle:
        status_bar.config(text='Genres limit exceeded')
        messagebox.showwarning('Warning', gle)
        conn.rollback()
    except IncompleteEntryError as iee:
        status_bar.config(text=iee)
        messagebox.showerror('ERROR', iee)
    
    else:
        display()
        # Status bar for add_Movie() when success
        status_bar.config(text='The record << {} >> was added to the Movies database'.format(movie_En.get()))    
        messagebox.showinfo('Info', 'The movie "{}" was added successfully'.format(movie_En.get()))
        clearFields()
    finally:
        conn.close()
        
#=========================================================================================================================================

#=====================<<<< Create a function to display available records in the Movies database >>>>=====================================

def display():
    ''' Display all records that exist in the Movies database '''

    clearTreeview()

    conn=sqlite3.connect('Movies.db')
    c=conn.cursor()
    c.execute('SELECT *, oid FROM Movies')
    records = c.fetchall()
    if len(records) == 0:           # If no records exist in the Movies databse, a warning message pops up
        status_bar.config(text='No records added in the Movies database')
        messagebox.showwarning('Warning', 'No records added in the Movies database')
    else:
        for rec in records:
            movies_tv.insert('', END, text=id, values=rec)
        status_bar.config(text='Movies displayed successfully')      # Status bar for display()
    conn.close()

#=========================================================================================================================================

#====================<<<< Create a funtion that allow updating records in the Movies database >>>>==========================================#

def update():
    ''' Update a record in the Movies database '''
                                                                                                                                                                                                                                                                       #
    conn=sqlite3.connect('Movies.db')
    try:
        
        selected = movies_tv.focus()                    # Retrieve the ID of the selected record in the Treeview widge
        #print(selected)
        record = movies_tv.item(selected, 'values')     # Return a tuple of values in the selected row
        #print(record)

        # Check if the users selected a row yet. If the user failed to select a row, raise NoSelectedItemError.
        if len(record) == 0:
            raise NoSelectedItemError('No record selected. Please try again!')

        checkEntry()
        c=conn.cursor()
        c.execute('''UPDATE Movies
                SET Movies=?, Genres=?, Director=?, ReleaseDate=?, Rating=?
                WHERE id=?''',
                (movie_En.get(), get_genres(), director_En.get(), get_date(), float(rating_En.get()), int(mid_En.get())))

        # Create a list of user entry
        entry_tuple = [mid_En.get(), movie_En.get(), get_genres(), director_En.get(), get_date(), rating_En.get()]

        # Check if any entry was updated. In other words, raise a MatchedValueError exception if they remain all unchanged
        isMatched = False     #Create a flag variable to check if all values are matched

        for entry in entry_tuple:   # Loop through the tuple and find any unmatched values. If matched, raise MatchedValueError.
            if entry in record:
                isMatched = True
            else:
                isMatched = False
                break     
        if isMatched == True:
            raise MatchedValueError('No entry updated at all')

        # Check if the user is attempting to change the Movie ID. If so, raise IDChangeError
        if not mid_En.get() == record[0]:
            raise IDChangeError('Oh oh! You are not allowed to change the Movie ID')

        # Raise RatingError if the user is attempting to update the rating that has a value of over 10.0
        if float(rating_En.get()) > 10.0:
            raise RatingError('Oh oh! The rating should be no more than 10. Please try again!')

        conn.commit()

    except ValueError as v:
        # Status bar for update() when updating improper or incomplete values
        status_bar.config(text=v)   
        messagebox.showerror('Error', v)
        conn.rollback()
    except RatingError as re:
        # Status bar for add_Movie() when rating error is more than 10.0
        status_bar.config(text='Rating Error')                                      
        messagebox.showerror('Error', re)
        conn.rollback()
    except MatchedValueError as mve:
        status_bar.config(text='No entry updated at all')
        messagebox.showerror('Error', mve)
        conn.rollback()
    except GenresLimitError as gle:
        status_bar.config(text='Genres limit exceeded')
        messagebox.showwarning('Warning', gle)
        conn.rollback()
    except IDChangeError as ide:
        status_bar.config(text='Error due to an attempt to change the Movie ID')
        messagebox.showerror('Error', ide)
        conn.rollback()
    except IncompleteEntryError as iee:
        status_bar.config(text=iee)
        messagebox.showerror('ERROR', iee)
    except NoSelectedItemError as nsie:
        # Status bar for update() when error occurs while updating
        status_bar.config(text='No record selected')                               
        messagebox.showerror('Error', nsie)  
        conn.rollback()

    else:
        # Display the updated record
        movies_tv.item(selected, values=entry_tuple)

        # Status bar for update() and an messagebox showing info pops up when success 
        status_bar.config(text='The record << {} >> was updated successfully'.format(movie_En.get()))      
        messagebox.showinfo('Update', 'The record "{}" was updated successfully'.format(movie_En.get()))
        clearFields()
    finally:
        conn.close()
        
#=========================================================================================================================================

#==========================<<<< Create a funtion that allows removing a record from the DB >>>>=======================================

def delete():
    ''' Delete a selected record from the Movies database '''

    conn=sqlite3.connect('Movies.db')
    try:
        if len(mid_En.get()) == 0:
            raise NoSelectedItemError('Delete faliure due to no record selected')

        # Ask the user to select one of two responses (Yes or No):
        resp = messagebox.askquestion('Delete', 'Are you sure you want to delete it?')
        if resp == 'yes':
            c=conn.cursor()
            c.execute('DELETE FROM Movies WHERE ID=?;', (mid_En.get(),))
            conn.commit()
            display()
            status_bar.config(text='The record << {} >> was removed from the Movies databse'.format(movie_En.get()))
            messagebox.showinfo('Delete', 'The record "{}" was deleted successfully'.format(movie_En.get()))   
        else:
            display()
            status_bar.config(text='Deleting the record canceled')
            messagebox.showinfo('Delete', 'Deleting the record canceled')

    except NoSelectedItemError as nsie:
        display()
        status_bar.config(text=nsie)
        messagebox.showerror('Delete Error', nsie)
        conn.rollback()

    finally:
        conn.close()
        clearFields()

#==========================================================================================================================================

#===============<<<< Create a funtion that display the records from Treeview object in the Entry widget >>>>===============================

def show_selected_record(event):
    ''' Show the data entry when a record is selected '''

    clearFields()
    selected = movies_tv.focus()                    # Retrieve the ID of the selected record in the Treeview widget
    record = movies_tv.item(selected, 'values')     # Return a tuple of all values in the selected row from the Treeview 
    #print(record)    
    global id
    if len(record) == 0:
        pass
    else:
        #Display Movie ID
        mid_En.insert(0, record[0])

        # Display the movie name
        movie_En.insert(0, record[1])

        # Display the genres
        genre = record[2]
        if genre == 'NULL':
            genre = ''
        genre_li = genre.split(', ')

        # Find the index of the selected genres and use select() funtion to toggle CheckButton on
        for i in genre_li:
            if i == '':                         # Check if genres are't selected yet. If not, exit out of loop and proceed to the next statement
                break                           # after the for loop
            else:
                g_index = genreList.index(i)    # Find index of selected genres
                varList[g_index].set(1)         # Toggle the CheckButton ON for Checkbutton objects in the list genre_Cb_liselected genre whose index
                                                # matches the index found above
        # Display the director
        director_En.insert(0, record[3])

        # Display the date
        date = record[4]
        date_li = date.split('/')
        months_Com.set(date_li[0])
        days_Com.set(date_li[1])
        years_Com.set(date_li[2])

        # Display the rating
        rating_En.insert(0, record[5])

    return id

#=============================================================================================================================================

#========================================<<<< Supplementary functions >>>>====================================================================
# Create a function that gets date elements (month, day, and year) from the Combobox widget and returns a formated date (MM/DD/YYYY)  

def get_date():
    ''' Get date elements (month, day, and year) that the user selected and return a formated date (MM/DD/YYYY) '''
    month, day, year = months_Com.get(), days_Com.get(), years_Com.get()
    date = [month, day, year]
    return '/'.join(date)

#===========================================================================================================================
# Create a function that get genres of the movies after selecting one or more in genreList using CheckButton created in
# section "Create GUI elements for my program" below (starting line number: 827)

def get_genres():
    ''' Get the genres of the selected movie and return a string of genres'''
    selected_genres = []
    isChecked = False           # Create a flag variable to check if a Checkbox is checked or not. Set defaut to unchecked
    for i in varList:           # Loop through the varList to check any selected Checkbox           
        if i.get() == 1:        # If a check mark is done, set isChecked to True and break out of the loop.
            isChecked = True    # Otherwise, set it back to default (False)
            break
        else:
            isChecked = False
            
    if isChecked == False:      # Is not any of the Checkbox is marked, return "NULL". Otherwise, append each marked Checkbox
        return 'NULL'           # to the selected_genres list 
    else:
        for i in range(len(varList)):
            if varList[i].get() == 1:
                selected_genres.append(genreList[i])
    # Check if the user is attempting to select over five genres
    if len(selected_genres) > 5:                     
        raise GenresLimitError('Genres limit should be 5')
    else:
        return ', '.join(selected_genres)

#=========================================================================================================================
# Create a function that allows users to sort a column in ascending/descending order in the Treeview object

def treeview_sort_column(col, reverse=False):
    ''' Sort the selected column in the Treeview object '''

    # Retrieve the list of tuples that include a value (first element) and its ID (second element)
    li = [(movies_tv.set(k, col), k) for k in movies_tv.get_children()]     # k returns an ID of a record and col is the column number
                                                                            # defined in the treeview headings. set() return the value of the
                                                                            # specific value of each row in the column "col"
    
    for i in li:
        if '/' in i[0]:         # Check if the user selected the date column or not
            Date_Bubble_Sort(li, reverse=reverse)
        elif i[0].isnumeric():  # Check if the user selected the ID. If so, sort the column by number instead of string sorting
            li.sort(reverse=reverse, key=lambda x: int(x[0]))
        else:
            li.sort(reverse=reverse)
    # Rearrange items in sorted positions using move() funtion of Treeview widget
    for index, (name, k) in enumerate(li):   # name: value of a cell in the selected column, k: id of the record    
        movies_tv.move(k, '', index)
        
    # Reverse the sort the next time when clicking the column again
    movies_tv.heading(col, command=lambda: treeview_sort_column(col, not reverse))

# Source: https://stackoverflow.com/questions/1966929/tk-treeview-column-sort

#======================================================================================================================
# Date column sorting using SQL statement with ORDER BY clause and substr() function - Demo
# Date sorting in ascending order
""" def sort_date_asc(col):
    ''' Sort the date column in ascending order from the Treeview object '''
    clearTreeview()
    
    conn = sqlite3.connect(path + r'\Movies.db')
    c=conn.cursor()
    c.execute('''SELECT * FROM Movies
            ORDER BY substr(ReleaseDate, 7, 4)||"-"||substr(ReleaseDate, 1, 2)||"-"||substr(ReleaseDate, 4, 2)''')
    rows = c.fetchall()
    for row in rows:
        movies_tv.insert('', END, text=id, values=row)
    conn.close()
    
    movies_tv.heading(col, command=lambda: sort_date_desc(col)) """

# Date sorting in descending order
""" def sort_date_desc(col):
    ''' Sort the date column in descending order from the Treeview object '''
    clearTreeview()
    
    conn = sqlite3.connect(path + r'\Movies.db')
    c=conn.cursor()
    c.execute('''SELECT * FROM Movies
            ORDER BY substr(ReleaseDate, 7, 4)||"-"||substr(ReleaseDate, 1, 2)||"-"||substr(ReleaseDate, 4, 2) DESC''')
    rows = c.fetchall()
    for row in rows:
        movies_tv.insert('', END, text=id, values=row)
    conn.close()

    movies_tv.heading(col, command=lambda: sort_date_asc(col)) """
#========================================================================================================================
# Create a function for the "Sort-by" Combobox:
def sort_by(e, reverse=False):
    if sort_Com.get() == 'ID':
        treeview_sort_column('#1', reverse=reverse)
    elif sort_Com.get() == 'Movie Name':
        treeview_sort_column('#2', reverse=reverse)
    elif sort_Com.get() == 'Director':
        treeview_sort_column('#4', reverse=reverse)
    elif sort_Com.get() == 'Release Date':
        treeview_sort_column('#5', reverse=reverse)
    else:
        treeview_sort_column('#6', reverse=reverse)
        
is_reversed = False     # Create a flag variable and set it to False as the default value to toggle 
                        # between ascending and descending order for sorting operation
def orderClicked():
    global is_reversed  # Set the flag variable as global so that it can be changed whenver the user clicks the Order icon
    if is_reversed == False:
        is_reversed = True
        sort_by(None, reverse=is_reversed)
    else:
        is_reversed = False
        sort_by(None, reverse=is_reversed)

#========================================================================================================================
# Create a function that directly open the dabase from SQLite
def openDB():
    ''' Open the database using SQLite '''
    os.popen('Movies.db')

#=============================================================================================================================================

#================================================================================================================

##############################################################################################################################
##################################<<<<     Create GUI elements for my program     >>>>########################################
##############################################################################################################################

# Create a list of genres
genreList = ['Action','Adventure','Animation','Comedy','Crime','Drama','Family',
            'Fantasy','Horror','Mystery','Romance','Sci-Fi','Thriller']

#=============================<<<< Create Label widgets >>>>==========================================================
mid_lb = Label(root, text='Movie ID:', bg='#C7E3E1', font=('Helvetica', 12, 'bold'))
mid_lb.place(x=150, y=150)

movie_lb = Label(root, text='Movie Name:', bg='#C7E3E1', font=('Helvetica', 12, 'bold'))
movie_lb.place(x=150, y=200)

genre_lb = Label(root, text='Genres:', bg='#C7E3E1', font=('Helvetica', 12, 'bold'))
genre_lb.place(x=150, y=250)

director_lb = Label(root, text='Director(s):', bg='#C7E3E1', font=('Helvetica', 12, 'bold'))
director_lb.place(x=605, y=200)

date_lb = Label(root, text='Release Date:', bg='#C7E3E1', font=('Helvetica', 12, 'bold'))
date_lb.place(x=605, y=150)

rating_lb = Label(root, text='Rating (Out of 10):', bg='#C7E3E1', font=('Helvetica', 12, 'bold'))
rating_lb.place(x=605, y=250)

sort_lb = Label(root, text='Sort by:', bg='#C7E3E1', font=('Helvetica', 12, 'bold'))
sort_lb.place(x=750, y=380)

#===========================================================================================================================

#============================<<<<  Create Entry widgets  >>>>===============================================================
mid_En = Entry(root, font=('Helvetica', 12, 'bold'), width=33, bd=5, fg='white', bg='black',
            insertbackground='red', selectbackground='red')
mid_En.place(x=280, y=150)
CreateToolTip(mid_En, text='Enter Movie ID')

movie_En = Entry(root, font=('Helvetica', 12, 'bold'), width=33, bd=5, fg='white', bg='black',
                insertbackground='red', selectbackground='red')
movie_En.place(x=280, y=200)
CreateToolTip(movie_En, text='Enter a movie or TV show')

director_En = Entry(root, font=('Helvetica', 12, 'bold'), width=30, bd=5, fg='white', bg='black',
                insertbackground='red', selectbackground='red')
director_En.place(x=750, y=200)
CreateToolTip(director_En, text='Enter the director')

rating_En = Entry(root, font=('Helvetica', 12, 'bold'), width=30, bd=5, fg='white', bg='black',
                insertbackground='red', selectbackground='red')
rating_En.place(x=750, y=250)
CreateToolTip(rating_En, text='Enter the average rating')
#=============================================================================================================================

#=======================<<<<  Create Button widgets  >>>>=====================================================================
# "Add records" Button
add_But = Button(root, text='Add Movies', bg='white', font=('Helvetica', 12, 'bold'),
                    bd=5, width=15, activebackground='green', relief=RAISED, command=add_Movie)
add_But.place(x=1100, y=250)
Change_Widget_Background(add_But, 'white', 'black', 'green', 'white')

# "Update Records" Button
update_But = Button(root, text='Update Info', bg='white', font=('Helvetica', 12, 'bold'),
                    bd=5, width=15, activebackground='green', relief=RAISED, command=update)
update_But.place(x=1100, y=300)
Change_Widget_Background(update_But, 'white', 'black', 'green', 'white')

# "Display records" Button
display_But = Button(root, text='Display All Movies', bg='white', font=('Helvetica', 12, 'bold'),
                    bd=5, width=15, activebackground='green', relief=RAISED, command=display)
display_But.place(x=1100, y=150)
Change_Widget_Background(display_But, 'white', 'black', 'green', 'white')

# "Open Database" Button
open_DB_But = Button(root, text='Open Database', bg='white', font=('Helvetica', 12, 'bold'),
                    bd=5, width=15, activebackground='green', command=openDB)
open_DB_But.place(x=1100, y=200)
Change_Widget_Background(open_DB_But, 'white', 'black', 'green', 'white')

# "Delete" Button
delete_But = Button(root, text='Delete', bg='darkred', fg='white', font=('Helvetica', 12, 'bold'),
                    bd=5, width=15, activebackground='darkred', command=delete)
delete_But.place(x=1100, y=350)
Change_Widget_Background(delete_But, 'darkred', 'white', 'red', 'black')

# "Clear Entry" Button
clear_But = Button(root, text='Clear Entry', bg='darkred', fg='white', font=('Helvetica', 12, 'bold'),
                    bd=5, width=10, activebackground='red', command=clearFields)
clear_But.place(x=750, y=310)
Change_Widget_Background(clear_But, 'darkred', 'white', 'red', 'black')

# "Clear Table" Button
clear_table_But = Button(root, text='Clear Table', bg='darkred', fg='white', font=('Helvetica', 12, 'bold'),
                    bd=5, width=10, activebackground='red', command=clearTreeview)
clear_table_But.place(x=900, y=310)
Change_Widget_Background(clear_table_But, 'darkred', 'white', 'red', 'black')

# "Search" Button
search_But = Button(root, text='Search Filters', bg='white', font=('Helvetica', 12, 'bold'),
                    bd=5, width=15, activebackground='green',
                    command=lambda: MyCustomToplevel(root, treeview=movies_tv, stat=status_bar))
search_But.place(x=600, y=640)
Change_Widget_Background(search_But, 'white', 'black', 'green', 'white')

# "Sort by" Button
order_img_f = Image.open('order.png').resize((20, 20))
order_img = ImageTk.PhotoImage(order_img_f)
order_But = Button(root, image=order_img, activebackground='green', bd=3, relief=GROOVE, command=orderClicked)
order_But.place(x=1000, y=380)
order_But.config(state=DISABLED, background='gray')
#=============================================================================================================================

#=======================<<<<  Create ComboBox widgets  >>>>===============================
style = Style()
style.theme_use('clam')
style.configure("TCombobox", background= "#E50914", fieldbackground= "white")
# Source: https://www.tutorialspoint.com/how-to-set-the-background-color-of-a-ttk-combobox-in-tkinter

months = [('{:02d}'.format(i)) for i in range(1, 13)]
months_Com = Combobox(root, values=months, width=5, foreground='black',
                    font=('Helvetica', 12, 'bold'), state='readonly')
months_Com.place(x=750, y=150)
CreateToolTip(months_Com, text='Month')

days = [('{:02d}'.format(i)) for i in range(1, 32)]
days_Com = Combobox(root, values=days, width=5, foreground='black',
                    font=('Helvetica', 12, 'bold'), state='readonly')
days_Com.place(x=815, y=150)
CreateToolTip(days_Com, text='Day')

years = [i for i in range(1990, 2022)]
years_Com = Combobox(root, values=years, width=8, foreground='black',
                    font=('Helvetica', 12, 'bold'), state='readonly')
years_Com.place(x=880, y=150)
CreateToolTip(years_Com, text='Year')

sort_li = ['ID', 'Movie Name', 'Director', 'Release Date', 'Ratings']
sort_Com = Combobox(root, values=sort_li, width=15, foreground='gray', font=('Helvetica', 12, 'bold'))
sort_Com.place(x=830, y=380)
sort_Com.set(sort_li[0])
sort_Com.config(state=DISABLED)
sort_Com.bind('<<ComboboxSelected>>', sort_by)
#=============================================================================================================================

#======================<<<<  Create CheckButton widget  >>>>==================================================================
var1 = IntVar()
genre_Cb1 = Checkbutton(root, text=genreList[0], font=('Helvetica', 12 ,'bold'),
                        variable=var1, bg='#C7E3E1', fg='black', activebackground='green')
genre_Cb1.place(x=230, y=250)
Change_Widget_Background(genre_Cb1, '#C7E3E1', 'black', 'green', 'black')

var2 = IntVar()
genre_Cb2 = Checkbutton(root, text=genreList[1], font=('Helvetica', 12 ,'bold'),
                        variable=var2, bg='#C7E3E1', fg='black', activebackground='green')
genre_Cb2.place(x=330, y=250)
Change_Widget_Background(genre_Cb2, '#C7E3E1', 'black', 'green', 'black')

var3 = IntVar()
genre_Cb3 = Checkbutton(root, text=genreList[2], font=('Helvetica', 12 ,'bold'),
                        variable=var3, bg='#C7E3E1', fg='black', activebackground='green')
genre_Cb3.place(x=460, y=250)
Change_Widget_Background(genre_Cb3, '#C7E3E1', 'black', 'green', 'black')

var4 = IntVar()
genre_Cb4 = Checkbutton(root, text=genreList[3], font=('Helvetica', 12 ,'bold'),
                        variable=var4, bg='#C7E3E1', fg='black', activebackground='green')
genre_Cb4.place(x=150, y=300)
Change_Widget_Background(genre_Cb4, '#C7E3E1', 'black', 'green', 'black')

var5 = IntVar()
genre_Cb5 = Checkbutton(root, text=genreList[4], font=('Helvetica', 12 ,'bold'),
                        variable=var5, bg='#C7E3E1', fg='black', activebackground='green')
genre_Cb5.place(x=255, y=300)
Change_Widget_Background(genre_Cb5, '#C7E3E1', 'black', 'green', 'black')

var6 = IntVar()
genre_Cb6 = Checkbutton(root, text=genreList[5], font=('Helvetica', 12 ,'bold'),
                        variable=var6, bg='#C7E3E1', fg='black', activebackground='green')
genre_Cb6.place(x=345, y=300)
Change_Widget_Background(genre_Cb6, '#C7E3E1', 'black', 'green', 'black')

var7 = IntVar()
genre_Cb7 = Checkbutton(root, text=genreList[6], font=('Helvetica', 12 ,'bold'),
                        variable=var7, bg='#C7E3E1', fg='black', activebackground='green')
genre_Cb7.place(x=440, y=300)
Change_Widget_Background(genre_Cb7, '#C7E3E1', 'black', 'green', 'black')

var8 = IntVar()
genre_Cb8 = Checkbutton(root, text=genreList[7], font=('Helvetica', 12 ,'bold'),
                        variable=var8, bg='#C7E3E1', fg='black', activebackground='green')
genre_Cb8.place(x=535, y=300)
Change_Widget_Background(genre_Cb8, '#C7E3E1', 'black', 'green', 'black')

var9 = IntVar()
genre_Cb9 = Checkbutton(root, text=genreList[8], font=('Helvetica', 12 ,'bold'),
                        variable=var9, bg='#C7E3E1', fg='black', activebackground='green')
genre_Cb9.place(x=150, y=350)
Change_Widget_Background(genre_Cb9, '#C7E3E1', 'black', 'green', 'black')

var10 = IntVar()
genre_Cb10 = Checkbutton(root, text=genreList[9], font=('Helvetica', 12 ,'bold'),
                        variable=var10, bg='#C7E3E1', fg='black', activebackground='green')
genre_Cb10.place(x=245, y=350)
Change_Widget_Background(genre_Cb10, '#C7E3E1', 'black', 'green', 'black')

var11 = IntVar()
genre_Cb11 = Checkbutton(root, text=genreList[10], font=('Helvetica', 12 ,'bold'),
                        variable=var11, bg='#C7E3E1', fg='black', activebackground='green')
genre_Cb11.place(x=345, y=350)
Change_Widget_Background(genre_Cb11, '#C7E3E1', 'black', 'green', 'black')

var12 = IntVar()
genre_Cb12 = Checkbutton(root, text=genreList[11], font=('Helvetica', 12 ,'bold'),
                        variable=var12, bg='#C7E3E1', fg='black', activebackground='green')
genre_Cb12.place(x=460, y=350)
Change_Widget_Background(genre_Cb12, '#C7E3E1', 'black', 'green', 'black')

var13 = IntVar()
genre_Cb13 = Checkbutton(root, text=genreList[12], font=('Helvetica', 12 ,'bold'),
                        variable=var13, bg='#C7E3E1', fg='black', activebackground='green')
genre_Cb13.place(x=545, y=350)
Change_Widget_Background(genre_Cb13, '#C7E3E1', 'black', 'green', 'black')


varList = [var1, var2, var3, var4, var5, var6, var7,
            var8, var9, var10, var11, var12, var13]
#===================================================================================================================

#=====================================<<<< Treeview widget >>>>=====================================================
# Create a Treeview widget called movies_tv
movies_tv = ttk.Treeview(root, show='headings', height=8, columns=('#1','#2','#3','#4','#5','#6'))
movies_tv.place(x=150, y=430)

# Specify the heading with particular column name created in database
movies_tv.heading('#1', text='ID', anchor=CENTER, command=lambda: treeview_sort_column('#1'))
movies_tv.column('#1', width=80, anchor=CENTER, stretch=True)

movies_tv.heading('#2', text='Movie Name', anchor=CENTER, command=lambda: treeview_sort_column("#2"))
movies_tv.column('#2', width=260, anchor=CENTER, stretch=True)

movies_tv.heading('#3', text='Genres', anchor=CENTER, command=lambda: treeview_sort_column('#3'))
movies_tv.column('#3', width=345, anchor=CENTER, stretch=True)

movies_tv.heading('#4', text='Director(s)', anchor=CENTER, command=lambda: treeview_sort_column('#4'))
movies_tv.column('#4', width=175, anchor=CENTER, stretch=True)

movies_tv.heading('#5', text='Release Date', anchor=CENTER, command=lambda: treeview_sort_column('#5'))
movies_tv.column('#5', width=140, anchor=CENTER, stretch=True)

movies_tv.heading('#6', text='Rating', anchor=CENTER, command=lambda: treeview_sort_column('#6'))
movies_tv.column('#6', width=140, anchor=CENTER, stretch=True)

# Bind the show_selected_record function to the event when the user selects a record
movies_tv.bind('<<TreeviewSelect>>', show_selected_record)

# Create a Scrollbar for the Treeview object
#style.configure("Vertical.TScrollbar", background="black", bordercolor="red", arrowcolor="red")
scroll = Scrollbar(root, orient='vertical', command=movies_tv.yview)
scroll.place(x=1293, y=430, height=193)
movies_tv.config(yscrollcommand=scroll.set)

# Style the treeview Widget
style.configure("Treeview", font=('Helvetica', 10, 'bold'))
style.configure('Treeview.Heading', font=('Helvetica', 12, 'bold'), background="black", foreground="red")
style.map('Treeview', background=[('selected', 'green')])

# Display all records from the Movies database in the Treeview object as soon as the the user opens the program
display()

#========================<<<< Create a right-click menu >>>>===============================================
# Create a function that pops up a context menu whenever the user right click on the window
def root_popup_menu(e):
    root_menu.tk_popup(e.x_root, e.y_root)

# Create a delete shortcut menu on the treeview object
def del_menu(e):
    del_rec_menu.tk_popup(e.x_root, e.y_root)

# Create a function that lets the user change prefered window background
def change_win_bg():
    color = askcolor(title='Choose window background')
    widget = [root, img_But, label2, label3, gif_label, button_border, img_But,
            genre_Cb1, genre_Cb2, genre_Cb3, genre_Cb3, genre_Cb4, genre_Cb5,
            genre_Cb6, genre_Cb7, genre_Cb8, genre_Cb9, genre_Cb10, genre_Cb10,
            genre_Cb11, genre_Cb12, genre_Cb13, mid_lb, movie_lb, director_lb,
            genre_lb, date_lb, rating_lb, sort_lb]
    for w in widget:
        w.config(bg=color[1])
        if w == img_But:
            Change_Widget_Background(w, color[1], 'white', '#F08080', 'red')
    for w in widget[7:22]:
        Change_Widget_Background(w, color[1], 'black', 'green', 'black')
    

MENU = {
    'Display records': display, 
    'Add': add_Movie, 
    'Update': update, 
    'Open Databse': openDB, 
    'Clear entry': clearFields, 
    'Clear table': clearTreeview,
    'Change window color background': change_win_bg
    }
root_menu = Menu(root, tearoff=0, background='black', foreground='white',
                font=('Helvetica', 10 ,'bold'), activebackground='green')
for menu_lb, menu_com in MENU.items():
    root_menu.add_command(label=menu_lb, command=menu_com)
root_menu.add_separator()
root_menu.add_command(label='Exit', command=root.quit)
root.bind('<Button-3>', root_popup_menu)        # Bind the function root_popup_menu to show a menu whenever the user right-clicks
                                                # <Button-3>: right-click on the mouse event
# Create a small right-click menu to delete a selected record 
del_rec_menu = Menu(movies_tv, tearoff=0, background='black', foreground='white',
                font=('Helvetica', 10 ,'bold'), activebackground='green')
del_rec_menu.add_command(label='Delete', command=delete)
movies_tv.bind('<Button-3>', del_menu)
#=============================================================================================================

#=========================<<<< Decorate the program with images >>>>==========================================
# Logo image
button_border = Frame(root, bd=0, width=80, height=140, bg='#C7E3E1')
button_border.place(x=0, y=0)
logo_img = Image.open(r'Images\NLogo1.png').resize((70, 130))
logo1 = ImageTk.PhotoImage(logo_img)
img_But = Button(button_border, image=logo1, background='#C7E3E1', activebackground='#C7E3E1',
                width=70, height=130, bd=0, command=root.quit)
img_But.place(x=0, y=0)
Change_Widget_Background(img_But, '#C7E3E1', 'white', '#F08080', 'red')

# Movie image
film_img = Image.open(r'Images\Film_logo.png').resize((140, 130))
logo2 = ImageTk.PhotoImage(film_img)
label2 = Label(image=logo2, background='#C7E3E1')
label2.place(x=150, y=10)

film_img_r = Image.open(r'Images\Film_logo_r.png').resize((140, 130))
logo3 = ImageTk.PhotoImage(film_img_r)
label3 = Label(image=logo3, background='#C7E3E1')
label3.place(x=1130, y=10)

# Gif image and its funtion (gif_frame_change) to change frame
gif_path ='netflix_animated.gif'
gif_file = Image.open(gif_path)
frameCount = gif_file.n_frames
#print(frameCount)
frames = [PhotoImage(file=gif_path, format ='gif -index {}'.format(i)) for i in range(frameCount)]

# Create a function to change frame of the gif image file
def gif_frame_change(f):
    frame = frames[f]       # Loop through the list "frames" to show each frame of the gif image
    f += 1
    if f == frameCount:     # If the the maximum number of frames is reached, set the frame back to 0 
        f = 0
    gif_label.configure(image=frame)
    root.after(50, gif_frame_change, f)     # The first argument (50) indicates how long the frame will be re-displayed (milliseconds)
                                            # Then, continue call gif_frame_change function and pass f (f = 0) as an arguemnt to go back the
                                            # first frame

gif_label = Label(root, background='#C7E3E1')
gif_label.pack(side=TOP, anchor=CENTER)
root.after(0, gif_frame_change, 0)          # The first arguemnt (0) passed to the after() function that indicate after how long
                                            # a gif image will be displayed (in milliseconds).
                                            # In this case, the value of 0 indicates that it will be shown immediately after opening this program 
                                            # The third argument (0) passed to the gif_frame_change() function is the starting frame of 
                                            # the gif image.

# Source: https://newbedev.com/play-animations-in-gif-with-tkinter
#=========================================================================================================

root.mainloop()