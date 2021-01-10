import tkinter as tk
from tkinter import ttk, scrolledtext
from global_functions import centeralize_screen, days, months, years
import sqlite3
from tkinter import messagebox as messagebox
from tkinter import filedialog
from main_page import window




class login_register_window: #class for login and register windows
    def __init__(self):
        self.login = tk.Tk()
        self.login.title("socialEvent")
        self.login.geometry(centeralize_screen(screen_width=self.login.winfo_screenwidth(),
                                                   screen_height=self.login.winfo_screenheight(),
                                                   window_width=800,
                                                   window_height=620))
        self.login.resizable(False, False)
        self.login.columnconfigure(1, weight=1)
        self.login.rowconfigure(0, weight=1)
        self.login.grid_propagate(False)

# ------------------------------------------------------------- side frame
        left_frame = tk.Frame(self.login, width=250, bg="red")
        left_frame.grid(column=0, row=0,sticky=tk.NSEW)
        left_frame.grid_propagate(False)
        left_frame.rowconfigure(0, weight=1)
        left_frame.rowconfigure(1, weight=1)

        left_frame_top = tk.Frame(left_frame, width=250, height=300, bg="red")
        left_frame_top.grid(column=0, row=0,sticky=tk.NSEW)
        left_frame_top.grid_propagate(False)
        centralize_frame_top = tk.Frame(left_frame_top)
        centralize_frame_top.pack(expand=True)
        appname = tk.Label(centralize_frame_top, text="Socialevent", bg="red", fg="white", font=(None, 40))
        appname.pack(fill=tk.BOTH,expand=True)

        left_frame_bottom = tk.Frame(left_frame, width=250, height=300, bg="red")
        left_frame_bottom.grid(column=0, row=1, sticky=tk.NSEW)
        left_frame_bottom.grid_propagate(False)
        c_frame_bottom = tk.Frame(left_frame_bottom)
        c_frame_bottom.pack(expand=True)
        quote = tk.Label(c_frame_bottom, text="“A friend may be waiting\n behind a stranger’s face.”\n ― Maya Angelou", bg="red", fg="white", font=(None, 15))
        quote.pack(fill=tk.BOTH, expand=True)

# -------------------------------------------------------------------- widgets of login form
        self.login_form = tk.Frame(self.login, bg="white")
        self.login_form.grid(column=1, row=0,sticky=tk.NSEW)
        # self.login_form.grid_propagate(False)
        login_form_c = tk.Frame(self.login_form, bg="white")
        login_form_c.pack(expand=True)
        self.l_warning1 = tk.Label(login_form_c, text="")
        self.l_warning1.grid(column=0, row=0, columnspan=2)
        self.s1 = tk.StringVar()
        name_box = ttk.Entry(login_form_c, width=35, textvariable=self.s1)
        name_box.insert(0, "Username")
        name_box.grid(column=0, row=1,columnspan=2,pady=8)
        self.s2 = tk.StringVar()
        password_box = ttk.Entry(login_form_c, width=35, textvariable=self.s2, show="*")
        password_box.insert(0, "Password")
        password_box.grid(column=0, row=2,columnspan=2)
        login_button = ttk.Button(login_form_c, text="Login", command=self.check_user_password)
        login_button.grid(column=0, row=3, pady=8)
        register_button = ttk.Button(login_form_c, text="Register", command=self.registration_frame)
        register_button.grid(column=1, row=3)


    def check_user_password(self):
        username = self.s1.get()
        password = self.s2.get()
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT username, password FROM users WHERE username = ? AND password = ?",(username, password))
        results = c.fetchall()
        if results:
            self.l_warning1.configure(text="Please Wait", fg="green")
            self.system_user = username
            self.login.destroy()
            window(self.system_user) # open main page by giving user as parameter
        else:
            self.l_warning1.configure(text="Username or Password is Incorrect", fg="red")

        conn.commit()
        conn.close()

# ---------------------------------------------------------------------------- widgets for registration form
    def registration_frame(self):
        self.login_form.grid_forget()
        self.register_form = tk.Frame(self.login, bg="white")
        self.register_form.grid(column=1, row=0,sticky=tk.NSEW)
        # self.register_form.grid_propagate(False)

        register_form_c = tk.Frame(self.register_form, bg="white")
        register_form_c.pack(expand=True)

        self.l_warning2 = tk.Label(register_form_c, text="")
        self.l_warning2.grid(column=0, row=0, columnspan=4)

        l_fullname = tk.Label(register_form_c, text="fullname")
        l_fullname.grid(column=0, row=1, pady=5)
        self.s_fullname = tk.StringVar()
        tb_fullname = tk.Entry(register_form_c, width=30, textvariable=self.s_fullname)
        tb_fullname.grid(column=1, row=1, columnspan=3, sticky=tk.W)

        l_username = tk.Label(register_form_c, text="username")
        l_username.grid(column=0, row=2, pady=5)
        self.s_username = tk.StringVar()
        tb_username = tk.Entry(register_form_c, width=30, textvariable=self.s_username)
        tb_username.grid(column=1, row=2, pady=10, columnspan=3, sticky=tk.W)

        l_password = tk.Label(register_form_c, text="Password")
        l_password.grid(column=0, row=3, pady=5)
        self.s_password = tk.StringVar()
        tb_password = tk.Entry(register_form_c, width=30, textvariable=self.s_password, show="*")
        tb_password.grid(column=1, row=3, pady=5, columnspan=3, sticky=tk.W)

        l_country = tk.Label(register_form_c, text="Country")
        l_country.grid(column=0, row=4, pady=5)
        self.s_country = tk.StringVar()
        c_country = ttk.Combobox(register_form_c, text="Country", width=30, textvariable=self.s_country, state="readonly")
        c_country['values'] = ("Britain", "Italian", "Germany", "Turkey", "France", "Spain")
        c_country.grid(column=1, row=4, columnspan=3, sticky=tk.W)

        l_city = tk.Label(register_form_c, text="city")
        l_city.grid(column=0, row=5, pady=5)
        self.s_city = tk.StringVar()
        tb_city = tk.Entry(register_form_c, width=20, textvariable=self.s_city)
        tb_city.grid(column=1, row=5, columnspan=3, sticky=tk.W)

        l_gender = tk.Label(register_form_c, text="Gender")
        l_gender.grid(column=0, row=6, pady=5)
        self.s_gender = tk.StringVar()
        c_gender = ttk.Combobox(register_form_c, text="Country", width=30, textvariable=self.s_gender, state="readonly")
        c_gender['values'] = ("Male", "Female")
        c_gender.grid(column=1, row=6, columnspan=3, sticky=tk.W)

        l_birthdate = tk.Label(register_form_c, text="date of birth")
        l_birthdate.grid(column=0, row=7, pady=5)
        self.s_day = tk.StringVar()
        c_day = ttk.Combobox(register_form_c, width=3, textvariable=self.s_day, values=days(), state="readonly")
        c_day.grid(column=1, row=7, sticky=tk.W)
        self.s_month = tk.StringVar()
        c_month = ttk.Combobox(register_form_c, width=3, textvariable=self.s_month, values=months(), state="readonly")
        c_month.grid(column=2, row=7, sticky=tk.W)
        self.s_year = tk.StringVar()
        c_year = ttk.Combobox(register_form_c, width=5, textvariable=self.s_year, values=years(), state="readonly")
        c_year.grid(column=3, row=7, sticky=tk.W)

        l_about = tk.Label(register_form_c, text="Write about yourself:")
        l_about.grid(column=0, row=8, pady=5)
        self.about_text = scrolledtext.ScrolledText(register_form_c, width=60, height=15, wrap=tk.WORD)
        self.about_text.grid(column=0, row=9, columnspan=4, sticky=tk.W)

        biography_label = tk.Label(register_form_c, text="Biography")
        biography_label.grid(column=0, row=10, pady=5)
        self.biography_s = tk.StringVar()
        biography_tb = tk.Entry(register_form_c, width=20, textvariable=self.biography_s)
        biography_tb.grid(column=1, row=10, columnspan=3, sticky=tk.W)

        picture_button = tk.Button(register_form_c, text="Upload Profile Picture", command=lambda: self.get_picture_path())
        picture_button.grid(column=0, row=11, pady=5)
        self.path_picture = tk.StringVar()
        self.entry_path_picture = tk.Entry(register_form_c, width=30, textvariable=self.path_picture)
        self.entry_path_picture.grid(column=1, row=11, columnspan=3, sticky=tk.W)

        register_button = tk.Button(register_form_c, text="Register", command=lambda: self.register_command())
        register_button.grid(column=0, row=12, columnspan=2, pady=5)

        cancel_button = tk.Button(register_form_c, text="Cancel", command=lambda: self.cancel_command())
        cancel_button.grid(column=2, row=12, columnspan=2, pady=5)

        self.login.update()


    def register_command(self):# function that write new user data to database
        new_user_info = [self.s_username.get(),
        self.s_password.get(),
        self.s_fullname.get(),
        self.s_city.get(),
        self.s_country.get(),
        f"{self.s_year.get()}-{self.s_month.get()}-{self.s_day.get()}",
        self.s_gender.get(),
        self.about_text.get('1.0', tk.END),
        0,
        self.biography_s.get()]

        if "" in new_user_info:
            self.l_warning2.configure(text="Please fill all empty fields", fg="red")
        else:
            connection = sqlite3.connect("database.db")
            c = connection.cursor()
            c.execute("SELECT username FROM users WHERE username = ?", (new_user_info[0],))
            username = c.fetchone()

            if not username: # ceck username uniqness
                c.execute(
                    "insert into users (username, password, fullname, city, country, date_of_birth, gender, about_me, socialpoint, biography)"
                    " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (new_user_info))
                messagebox.showinfo("info!", "registration completed!")
                self.cancel_command()

                if self.path_picture.get():
                    with open("question_mark.png", 'rb') as file:
                        binaryData = file.read()
                    c.execute("UPDATE users SET picture = ? WHERE  username=?",(binaryData, new_user_info[0],))
                else: # if proflie picture is not provided write default profile picture
                    with open(self.path_picture.get(), 'rb') as file:
                        binaryData = file.read()
                    c.execute("UPDATE users SET picture = ? WHERE  username=?",(binaryData, new_user_info[0],))
                connection.commit()
                connection.close()

            else:
                self.l_warning2.configure(text="This Username name already used. Want to try with a different name?", fg="red")
                connection.close()

    def cancel_command(self):  # cancel registration and turn back to login window
        self.register_form.destroy()
        self.login_form.grid(column=1, row=0)
        self.login.update()


    def get_picture_path(self): # get path of profile picture selected by user
        file_path = filedialog.askopenfilename()
        self.entry_path_picture.insert(0, file_path)


if __name__ == "__main__":
    app = login_register_window()
    app.login.mainloop()




