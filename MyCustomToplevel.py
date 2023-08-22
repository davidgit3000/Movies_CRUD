from tkinter import *
from MyTools import Change_Widget_Background
from tkinter import messagebox
from MovieCustomException import *
import sqlite3

#path=r'G:\CISP 71(L)\Project CRUD CISP 71\Movies_CRUD_py'
genreList = ['Action','Adventure','Animation','Comedy','Crime','Drama','Family',
            'Fantasy','Horror','Mystery','Romance','Sci-Fi','Thriller']

class MyCustomToplevel:
    def __init__(self, master, treeview, stat):
        self.master = master
        self.treeview = treeview
        self.stat = stat
        # Crreate a custom Toplevel widget
        global option_win
        option_win = Toplevel(self.master)
        option_win.title('Search Filters') 
        option_win.geometry('450x520+500+155')
        option_win.config(bg='#C7E3E1')
        option_win.iconbitmap('Netflix.ico')
        option_win.resizable(0, 0)
        option_win.grab_set() # grab_set() prevents users from interacting with the main window

        #Create label for the Toplevel widget
        l1 = Label(option_win, image="::tk::icons::question", bg='#C7E3E1')
        l1.place(x=35, y=10)
        l2 = Label(option_win, text='What do you want to search for?\nPlease choose one of the following options:',
                    font=('Helvetica', 12, 'bold'), bg='#C7E3E1', anchor=CENTER)
        l2.place(x=75, y=20)

        # Create Radiobutton for the Toplevel widget (Movie name, Director, Genres)
        global var, mov_R, dir_R, genres_R
        
        var = StringVar()
        var.set(None)
        mov_R = Radiobutton(option_win, text='Movie name',  font=('Helvetica', 12, 'bold'),
                        variable=var, value='movie', bg='#C7E3E1', activebackground='green', command=self.opt) 
        mov_R.place(x=10, y=70)
        Change_Widget_Background(mov_R, '#C7E3E1', 'black', 'green', 'black')

        dir_R = Radiobutton(option_win, text='Director', font=('Helvetica', 12, 'bold'),
                        variable=var, value='director', bg='#C7E3E1', activebackground='green', command=self.opt)
        dir_R.place(x=10, y=130)
        Change_Widget_Background(dir_R, '#C7E3E1', 'black', 'green', 'black')

        genres_R = Radiobutton(option_win, text='Genres',  font=('Helvetica', 12, 'bold'),
                        variable=var, value='genres', bg='#C7E3E1', activebackground='green', command=self.opt)
        genres_R.place(x=10, y=190)
        Change_Widget_Background(genres_R, '#C7E3E1', 'black', 'green', 'black')
        #var.set(None)

        # Sub-Radiobutton for ratings (Positive, Moderate, and Critical)
        global rating_R, pos_rate, medium_rate, crit_rate, rateVar
        rating_R = Radiobutton(option_win, text='Ratings', font=('Helvetica', 12, 'bold'),
                        variable=var, value='ratings', bg='#C7E3E1', activebackground='green', command=self.opt)
        rating_R.place(x=200, y=193)
        Change_Widget_Background(rating_R, '#C7E3E1', 'black', 'green', 'black')

        rateVar = StringVar()
        pos_rate = Radiobutton(option_win, text='Positive (8-10)', font=('Helvetica', 11, 'bold'),
                        variable=rateVar, value='p', bg='#C7E3E1', activebackground='green', command=self.opt)
        pos_rate.place(x=230, y=223)
        pos_rate.config(state=DISABLED)

        medium_rate = Radiobutton(option_win, text='Moderate (6-8)', font=('Helvetica', 11, 'bold'),
                        variable=rateVar, value='m', bg='#C7E3E1', activebackground='green', command=self.opt)
        medium_rate.place(x=230, y=253)
        medium_rate.config(state=DISABLED)

        crit_rate = Radiobutton(option_win, text='Critical (< 6)', font=('Helvetica', 11, 'bold'),
                        variable=rateVar, value='c', bg='#C7E3E1', activebackground='green', command=self.opt)
        crit_rate.place(x=230, y=283)
        crit_rate.config(state=DISABLED)
        rateVar.set(None)   # Set to None to avoid auto-click state

        # Sub-Radiobutton for date (Most recent and oldest)
        global date_R, dateVar, recent_R, oldest_R
        date_R = Radiobutton(option_win, text='Release Date', font=('Helvetica', 12, 'bold'),
                        variable=var, value='date', bg='#C7E3E1', activebackground='green', command=self.opt)
        date_R.place(x=200, y=310)
        Change_Widget_Background(date_R, '#C7E3E1', 'black', 'green', 'black')

        dateVar = StringVar()
        recent_R = Radiobutton(option_win, text='Most Recent', font=('Helvetica', 11, 'bold'),
                        variable=dateVar, value='r', bg='#C7E3E1', activebackground='green', command=self.opt)
        recent_R.place(x=230, y=340)
        recent_R.config(state=DISABLED)

        oldest_R = Radiobutton(option_win, text='Oldest', font=('Helvetica', 11, 'bold'),
                        variable=dateVar, value='o', bg='#C7E3E1', activebackground='green', command=self.opt)
        oldest_R.place(x=230, y=370)
        oldest_R.config(state=DISABLED)
        dateVar.set(None)

        # Create entry for each option in the Toplevel widget
        global mov_s_En, dir_s_En
        mov_s_En = Entry(option_win, font=('Helvetica', 10, 'bold'), width=40, bg='black', bd=5, fg='white',
                    insertbackground='red', highlightbackground='green')
        mov_s_En.insert(0, 'Click "Movie name" to enable entry')    # Set default text to the movie search Entry     
        mov_s_En.place(x=10, y=100)
        mov_s_En.config(state=DISABLED)

        dir_s_En = Entry(option_win, font=('Helvetica', 10, 'bold'), width=40, bg='black', bd=5, fg='white',
                    insertbackground='red', highlightbackground='green')
        dir_s_En.place(x=10, y=160)
        dir_s_En.insert(0, 'Click "Director" to enable entry')      # Set default text to the director search Entry           
        dir_s_En.config(state=DISABLED)

        # Create a Listbox including all genres that the user want to search
        global genres_Lib
        genres_Lib = Listbox(option_win, height=13, font=('Helvetica', 10, 'bold'), selectmode=MULTIPLE,
                        selectbackground='green', bd=5, relief=GROOVE, justify=CENTER, activestyle='none')
        for i in genreList:
            genres_Lib.insert(END, i)
        genres_Lib.place(x=10, y=220)
        genres_Lib.config(state=DISABLED)

        # Create three buttons in the Toplevel widget: Search, Redo, and Cancel
        global s_But, redo_But
        s_But = Button(option_win, text='Search', font=('Helvetica', 10, 'bold'), width=10,
                        bd=5, bg='#DCDCDC', activebackground='green', command=self.opt_bind_func)
        s_But.place(x=180, y=465)
        Change_Widget_Background(s_But, '#DCDCDC', 'black', 'green', 'white')

        redo_But = Button(option_win, text='Redo', font=('Helvetica', 10, 'bold'), width=10,
                        bd=5, bg='#DC143C', activebackground='green', command=self.redo)
        redo_But.place(x=60, y=465)
        redo_But.config(state=DISABLED)
        
        cancel_But = Button(option_win, text='Cancel', font=('Helvetica', 10, 'bold'), width=10,
                        bd=5, bg='#DC143C', activebackground='green', command=option_win.destroy)
        cancel_But.place(x=300, y=465)
        Change_Widget_Background(cancel_But, '#DC143C', 'black', 'red', 'white')
        
    def clearTreeview(self):
        ''' Clear all rows in the table '''
        for row in self.treeview.get_children():
            self.treeview.delete(row)

#============================<<<< Create a Toplevel widget for searching >>>>=============================================
# Create a funtion that let users search a movie, a director, or genres

    # Select one of three options to search a movie, director(s), or genre(s) 
    def opt(self):
        global rb_list
        rb_list = [mov_R, dir_R, genres_R, rating_R, date_R]
        
        if var.get() == 'movie':                      # If the user select the Movie search (value = 1)
            for i in rb_list:
                if i == mov_R:
                    Change_Widget_Background(mov_R, '#C7E3E1', 'black', 'green', 'black')
                    continue
                else:
                    i.config(state=DISABLED)    # Disable Radiobutton (director, genres, ratings, and date)
                    Change_Widget_Background(i)               
            redo_But.config(state=NORMAL)
            Change_Widget_Background(redo_But, '#DC143C', 'black', 'red', 'white')
            mov_s_En.config(state=NORMAL)       # Enable the movie search Entry 
            mov_s_En.delete(0, END)             # Delete the default text in the movie search Entry
            mov_s_En.focus()                    # Grab focus to movie search Entry so that the cursor blinks
            mov_s_En.bind('<Return>', self.search_movie)
        elif var.get() == 'director':                    # If the user select the Director search (value = 2)
            for i in rb_list:
                if i == dir_R:
                    Change_Widget_Background(dir_R, '#C7E3E1', 'black', 'green', 'black')
                    continue
                else:
                    i.config(state=DISABLED)
                    Change_Widget_Background(i)
            redo_But.config(state=NORMAL)
            Change_Widget_Background(redo_But, '#DC143C', 'black', 'red', 'white')
            dir_s_En.config(state=NORMAL)
            dir_s_En.delete(0, END)
            dir_s_En.focus()
            dir_s_En.bind('<Return>', self.search_director)
        elif var.get() == 'genres':                    # If the user select the Genres search (value = 3)
            for i in rb_list:
                if i == genres_R:
                    Change_Widget_Background(genres_R, '#C7E3E1', 'black', 'green', 'black')
                    continue
                else:
                    i.config(state=DISABLED)
                    Change_Widget_Background(i)
            redo_But.config(state=NORMAL)
            Change_Widget_Background(redo_But, '#DC143C', 'black', 'red', 'white')
            genres_Lib.config(state=NORMAL) 
        elif var.get() == 'ratings':                    # If the user select the Ratings search (value = 4)
            for i in rb_list:
                if i == rating_R:
                    Change_Widget_Background(rating_R, '#C7E3E1', 'black', 'green', 'black')
                    continue
                else:
                    i.config(state=DISABLED)
                    Change_Widget_Background(i)
            redo_But.config(state=NORMAL)
            Change_Widget_Background(redo_But, '#DC143C', 'black', 'red', 'white')
            pos_rate.config(state=NORMAL)
            Change_Widget_Background(pos_rate, '#C7E3E1', 'black', 'green', 'black')
            medium_rate.config(state=NORMAL)
            Change_Widget_Background(medium_rate, '#C7E3E1', 'black', 'green', 'black')
            crit_rate.config(state=NORMAL)
            Change_Widget_Background(crit_rate, '#C7E3E1', 'black', 'green', 'black')   
        elif var.get() == 'date':                    # If the user select the Date search (value = 5)
            for i in rb_list:
                if i == date_R:
                    Change_Widget_Background(date_R, '#C7E3E1', 'black', 'green', 'black')
                    continue
                else:
                    i.config(state=DISABLED)
                    Change_Widget_Background(i)
            redo_But.config(state=NORMAL)
            Change_Widget_Background(redo_But, '#DC143C', 'black', 'red', 'white')
            recent_R.config(state=NORMAL)
            Change_Widget_Background(recent_R, '#C7E3E1', 'black', 'green', 'black')
            oldest_R.config(state=NORMAL)
            Change_Widget_Background(oldest_R, '#C7E3E1', 'black', 'green', 'black')

    # Create a function that bind to another function when the user selects one of the options and clicks "Search"                      
    def opt_bind_func(self):
        try:
            if var.get() == 'movie':
                self.search_movie(None)
            elif var.get() == 'director':
                self.search_director(None) 
            elif var.get() == 'genres':
                self.search_genres()
            elif var.get() == 'ratings':
                self.search_ratings()
            elif var.get() == 'date':
                self.search_date()
            else:
                raise NoSelectedItemError('Please select one of the four main options before clicking "Search"')
        except NoSelectedItemError as nsie:
            self.stat.config(text='No options selected')
            messagebox.showerror('ERROR', nsie)

    # Redo the search
    def redo(self):
        for i in rb_list:
            i.config(state=NORMAL)
            Change_Widget_Background(i, '#C7E3E1', 'black', 'green', 'black')
            
        choice = [mov_s_En, dir_s_En, genres_Lib, pos_rate, medium_rate, crit_rate, recent_R, oldest_R]
        genres_Lib.selection_clear(0, END)
        for i in choice:
            if i == mov_s_En:
                i.insert(0, 'Click "Movie name" to enable entry')
            if i == dir_s_En:
                i.insert(0, 'Click "Director" to enable entry')
            i.config(state=DISABLED)
            Change_Widget_Background(i)

        for i in (var, rateVar, dateVar):
            i.set(None) 
        redo_But.config(state=DISABLED)
        Change_Widget_Background(redo_But)

        
    # Search a movie:
    def search_movie(self, event):
        conn = sqlite3.connect('Movies.db')
        try:
            if mov_s_En.get() == '':
                messagebox.showerror('Error', 'Please enter movie name')
            else:
                self.clearTreeview()
                c=conn.cursor()
                # Format the user entry to accomodate the proper syntax to run a SQL statement
                mov_s_En_copy = '%{}%'.format(mov_s_En.get())

                c.execute('SELECT *,oid FROM Movies WHERE Movies LIKE ?;', (mov_s_En_copy,))
                records = c.fetchall()
                #print(records)
                if len(records) == 0:
                    raise NotFoundError('The movie that you searched was not found. Please try again!')
                else:
                    for rec in records:
                        self.treeview.insert('', END, text=id, values=rec)
                    option_win.withdraw()       # Close the Option window after finishing searching
                    self.master.grab_set()      # Grab focus back to the main window
                    self.stat.config(text='The movie << {} >> was found'.format(records[0][1]))
                    messagebox.showinfo('Movie Search', 'The movie "{}" was found'.format(records[0][1]))
            conn.commit()

        except NotFoundError as m:
            self.stat.config(text='The record << {} >> was not found or matched'.format(mov_s_En.get()))
            messagebox.showerror('Movie Search', m)
            mov_s_En.focus()
            conn.rollback()

        conn.close() 
        
            

    # Search director(s):
    def search_director(self, event):
        conn = sqlite3.connect('Movies.db')
        try:
            if dir_s_En.get() == '':
                messagebox.showerror('Error', 'Please enter director name')
            else:
                self.clearTreeview()
                c=conn.cursor()
                dir_s_En_copy = '%{}%'.format(dir_s_En.get())
                c.execute('SELECT *,oid FROM Movies WHERE Director LIKE ?;', (dir_s_En_copy,))
                records = c.fetchall()
                #print(records)
                if len(records) == 0:
                    raise NotFoundError('The director that you searched was not found. Please try again!')
                else:
                    for rec in records:
                        self.treeview.insert('', END, text=id, values=rec)
                    option_win.withdraw()
                    self.master.grab_set()    
                    self.stat.config(text='The director << {} >> was found'.format(records[0][3]))
                    messagebox.showinfo('Director Search', 'The director "{}" was found'.format(records[0][3]))
            
            conn.commit()

        except NotFoundError as m:
            self.stat.config(text='The record << {} >> was not found or matched'.format(dir_s_En.get()))
            messagebox.showerror('Director Search', m)
            dir_s_En.focus()
            conn.rollback()

        conn.close()
            

    # Fetch all selected genre(s) from the Listbox widget
    def fetch_filtered_genres(self):
        global selected_g
        selected_g = []
        for i in genres_Lib.curselection():
            selected_g.append(genres_Lib.get(i))
        #print(selected_g)
        sel_g = selected_g[:]
        for i in range(len(sel_g)):
            sel_g[i] = '%{}%'.format(sel_g[i])
        #print(sel_g)
        return sel_g

    # Search genres that match the record in the Movie database
    def search_genres(self):
        self.clearTreeview()

        g_list = self.fetch_filtered_genres()
        query1 = '''SELECT * FROM Movies
                WHERE Genres LIKE ?'''
        query2 = '''SELECT * FROM Movies
                WHERE (Genres LIKE ?) AND (Genres LIKE ?)'''
        query3 = '''SELECT * FROM Movies
                WHERE (Genres LIKE ?) AND (Genres LIKE ?) AND (Genres LIKE ?)'''
        query4 = '''SELECT * FROM Movies
                WHERE (Genres LIKE ?) AND (Genres LIKE ?) AND (Genres LIKE ?) AND (Genres LIKE ?)'''
        query5 = '''SELECT * FROM Movies
                WHERE (Genres LIKE ?) AND (Genres LIKE ?) AND (Genres LIKE ?) AND (Genres LIKE ?) AND (Genres LIKE ?)'''
        conn = sqlite3.connect('Movies.db')
        c=conn.cursor()
        try:
            if len(g_list) == 0:
                raise NoSelectedItemError('No genres selected at all')
            elif len(g_list) == 1:
                c.execute(query1, (g_list[0],))
                records1 = c.fetchall() 
                if len(records1) == 0:
                        raise NotFoundError('The movies whose genre you searched for was not found. Please try again!')
                else:    
                    for rec in records1:
                        self.treeview.insert('', END, text=id, values=rec)
                        option_win.withdraw()
                        self.master.grab_set()       
                        self.stat.config(text='The genre << {} >> was found'.format(selected_g[0]))
                    messagebox.showinfo('Genres Search', 'Movies with entered genre(s) was retrieved')

            elif len(g_list) == 2:
                c.execute(query2, (g_list[0], g_list[1]))
                records2 = c.fetchall()
                if len(records2) == 0:
                        raise NotFoundError('The movies whose genres you searched for was not found. Please try again!')
                else:
                    for rec in records2:
                        self.treeview.insert('', END, text=id, values=rec)
                        option_win.withdraw()
                        self.master.grab_set()       
                        self.stat.config(text='The genres << {} and {} >> was found'.format(selected_g[0], selected_g[1]))
                    messagebox.showinfo('Genres Search', 'Movies with entered genre(s) was retrieved')

            elif len(g_list) == 3:
                c.execute(query3, (g_list[0], g_list[1], g_list[2]))
                records3 = c.fetchall()
                if len(records3) == 0:
                        raise NotFoundError('The movies whose genres you searched for was not found. Please try again!')
                else:
                    for rec in records3:
                        self.treeview.insert('', END, text=id, values=rec)
                        option_win.withdraw()
                        self.master.grab_set()       
                        self.stat.config(text='The genres << {}, {} and {} >> was found'.format(selected_g[0], selected_g[1], selected_g[2]))
                    messagebox.showinfo('Genres Search', 'Movies with entered genre(s) was retrieved')
            elif len(g_list) == 4:
                c.execute(query4, (g_list[0], g_list[1], g_list[2], g_list[3]))
                records4 = c.fetchall()
                if len(records4) == 0:
                        raise NotFoundError('The movies whose genres you searched for was not found. Please try again!')
                else:
                    for rec in records4:
                        self.treeview.insert('', END, text=id, values=rec)
                        option_win.withdraw()
                        self.master.grab_set()       
                        self.stat.config(text='The genres << {}, {}, {}, and {} >> was found'.format(selected_g[0], selected_g[1],
                                                                                                    selected_g[2], selected_g[3]))
                    messagebox.showinfo('Genres Search', 'Movies with entered genre(s) was retrieved')
            elif len(g_list) == 5:
                c.execute(query5, (g_list[0], g_list[1], g_list[2], g_list[3], g_list[4]))
                records5 = c.fetchall()
                if len(records5) == 0:
                        raise NotFoundError('The movies whose genres you searched for was not found. Please try again!')
                else:
                    for rec in records5:
                        self.treeview.insert('', END, text=id, values=rec)
                        option_win.withdraw()
                        self.master.grab_set()      
                        self.stat.config(text='The genres << {}, {}, {}, {}, and {} >> was found'.format(selected_g[0], selected_g[1],
                                                                                            selected_g[2], selected_g[3], selected_g[4]))
                    messagebox.showinfo('Genres Search', 'Movies with entered genre(s) was retrieved')
            else: 
                raise GenresLimitError('Genres limit should be 5')
            conn.commit()
        except NotFoundError as m:
            self.stat.config(text='The record whose genre(s) you searched for was not found')
            messagebox.showerror('Genres Search', m)
            conn.rollback()
        except GenresLimitError as gle:
            self.stat.config(text='Genres limit exceeded')
            messagebox.showwarning('Warning', gle)
            conn.rollback()
        except NoSelectedItemError as nsie:
            self.stat.config(text='No genres selected')
            messagebox.showerror('ERROR', nsie)
            conn.rollback()
        
        conn.close()

    # Search ratings based on two options: positive or critical
    def search_ratings(self):
        conn = sqlite3.connect('Movies.db')
        try:
            if rateVar.get() == 'p':
                self.clearTreeview()
                c=conn.cursor()
                c.execute('SELECT * FROM Movies WHERE Rating BETWEEN 8.0 AND 10.0;')
                records1 = c.fetchall()
                if len(records1) == 0:
                    raise NotFoundError('The ratings that you searched was not found. Please try again!')
                else:
                    for rec in records1:
                        self.treeview.insert('', END, text=id, values=rec)
                option_win.withdraw()       # Close the Option window after finishing searching
                self.master.grab_set()
                self.stat.config(text='Display positive ratings')
                messagebox.showinfo('Ratings Search', 'Here are movies with positive ratings')
            elif rateVar.get() == 'm':
                self.clearTreeview()
                c=conn.cursor()
                c.execute('SELECT * FROM Movies WHERE Rating BETWEEN 6.0 AND 8.0;')
                records2 = c.fetchall()
                if len(records2) == 0:
                    raise NotFoundError('The ratings that you searched was not found. Please try again!')
                else:
                    for rec in records2:
                        self.treeview.insert('', END, text=id, values=rec)
                option_win.withdraw()       # Close the Option window after finishing searching
                self.master.grab_set()
                self.stat.config(text='Display moderate ratings')
                messagebox.showinfo('Ratings Search', 'Here are movies with moderate ratings')
            elif rateVar.get() == 'c':
                self.clearTreeview()
                c=conn.cursor()
                c.execute('SELECT * FROM Movies WHERE Rating < 6.0;')
                records3 = c.fetchall()
                if len(records3) == 0:
                    raise NotFoundError('The ratings that you searched was not found. Please try again!')
                else:
                    for rec in records3:
                        self.treeview.insert('', END, text=id, values=rec)
                option_win.withdraw()
                self.master.grab_set()       
                self.stat.config(text='Display critical ratings')
                messagebox.showinfo('Ratings Search', 'Here are movies with critical ratings')
            else:
                raise NoSelectedItemError('No ratings type selected')
            conn.commit()
        except NotFoundError as m:
            self.stat.config(text='The rating type that you search was not found')
            messagebox.showerror('Movie Search', m)
            conn.rollback()
        except NoSelectedItemError as nsie:
            self.stat.config(text=nsie)
            messagebox.showerror('ERROR', nsie)
            conn.rollback()
       
        conn.close()
            

    # Search date with the most recent or the oldest movie (May add try-except block if no data exists in the database)
    def search_date(self):
        conn = sqlite3.connect('Movies.db')
        try:
            if dateVar.get() == 'r':
                self.clearTreeview()
                c=conn.cursor()
                c.execute('''SELECT * FROM Movies
                    ORDER BY substr(ReleaseDate, 7, 4)||"-"||substr(ReleaseDate, 1, 2)||"-"||substr(ReleaseDate, 4, 2) DESC LIMIT 1;''')
                records1 = c.fetchall()
                for rec in records1:
                    self.treeview.insert('', END, text=id, values=rec)
                option_win.withdraw()       # Close the Option window after finishing searching
                self.master.grab_set()
                self.stat.config(text='The most recent movie displayed successfully')
                messagebox.showinfo('Date Search', 'Here is the most recent movie in the Movies database')
            elif dateVar.get() == 'o':
                self.clearTreeview()
                c=conn.cursor()
                c.execute('''SELECT * FROM Movies
                    ORDER BY substr(ReleaseDate, 7, 4)||"-"||substr(ReleaseDate, 1, 2)||"-"||substr(ReleaseDate, 4, 2) LIMIT 1;''')
                records2 = c.fetchall()
                for rec in records2:
                    self.treeview.insert('', END, text=id, values=rec)
                option_win.withdraw()
                self.master.grab_set()       
                self.stat.config(text='The oldest movie displayed successfully')
                messagebox.showinfo('Date Search', 'Here is the oldest movie in the Movies database')
            else:
                raise NoSelectedItemError('No date options selected')
            conn.commit()
        except NoSelectedItemError as nsie:
            self.stat.config(text=nsie)
            messagebox.showerror('ERROR', nsie)
            conn.rollback()
        else:
            self.master.grab_set()
        finally:
            conn.close()