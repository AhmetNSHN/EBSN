import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
import sqlite3
from global_functions import centeralize_screen, days, months, hour, minute, future_years

class create_event:
    def __init__(self, system_user):

        self.event_form = tk.Toplevel()
        self.event_form.title("Create New Event")
        self.event_form.geometry(centeralize_screen(screen_width=self.event_form.winfo_screenwidth(),
                                                        screen_height=self.event_form.winfo_screenheight(),
                                                        window_width=500,
                                                        window_height=700))
        self.event_form.resizable(False, False)

        self. system_user = system_user

        l_title = tk.Label(self.event_form, text=f"New Event by {system_user}", bg="red", fg="white", font=(None, 15))
        l_title.grid(column=0, row=0, ipady=10, sticky="EW", columnspan = 7)

        l_eventname = tk.Label(self.event_form, text="Event Name    ")
        l_eventname.grid(column=0, row=1, pady=10)
        self.s_eventname = tk.StringVar()
        tb_eventname = tk.Entry(self.event_form, width=38, textvariable=self.s_eventname)
        tb_eventname.grid(column=1, row=1, columnspan=6, sticky=tk.W)

        l_date_time = tk.Label(self.event_form, text="Date/Time")
        l_date_time.grid(column=0, row=2, pady=10)
        self.s_day = tk.StringVar()
        c_day = ttk.Combobox(self.event_form, width=3, textvariable=self.s_day, values=days(), state="readonly")
        c_day.grid(column=1, row=2, sticky=tk.W)
        self.s_month = tk.StringVar()
        c_month = ttk.Combobox(self.event_form, width=3, textvariable=self.s_month, values=months(), state="readonly")
        c_month.grid(column=1, row=2, sticky=tk.E)
        self.s_year = tk.StringVar()
        c_year = ttk.Combobox(self.event_form, width=5, textvariable=self.s_year, values=future_years(), state="readonly")
        c_year.grid(column=2, row=2, sticky=tk.W)
        self.s_hour = tk.StringVar()
        c_hour = ttk.Combobox(self.event_form, width=2, textvariable=self.s_hour, values=hour(), state="readonly")
        c_hour.grid(column=3, row=2, sticky=tk.W)
        self.s_minute = tk.StringVar()
        c_minute = ttk.Combobox(self.event_form, width=2, textvariable=self.s_minute, values=minute(), state="readonly")
        c_minute.grid(column=4, row=2, sticky=tk.W)

        l_duration = tk.Label(self.event_form, text="Duration ")
        l_duration.grid(column=0, row=3, pady=10)
        self.s_duration = tk.StringVar()
        tb_duration = tk.Entry(self.event_form, width=10, textvariable=self.s_duration)
        tb_duration.grid(column=1, row=3, columnspan=6, sticky=tk.W)

        l_payment = tk.Label(self.event_form, text="Any payment? ")
        l_payment.grid(column=2, row=3, pady=10)
        self.s_payment = tk.StringVar()
        c_payment = ttk.Combobox(self.event_form, width=3, textvariable=self.s_payment, values=("Yes", "No"), state="readonly")
        c_payment.grid(column=3, row=3, columnspan=1, sticky=tk.W)

        l_location = tk.Label(self.event_form, text="Location  ")
        l_location.grid(column=0, row=4, pady=10)
        self.s_location = tk.StringVar()
        tb_location = tk.Entry(self.event_form, width=38, textvariable=self.s_location)
        tb_location.grid(column=1, row=4, columnspan=6, sticky=tk.W)

        l_type = tk.Label(self.event_form, text="Event type  ")
        l_type.grid(column=0, row=5, pady=10)
        self.s_type = tk.StringVar()
        c_minute = ttk.Combobox(self.event_form, width=10, textvariable=self.s_type,
                                values=("Home", "Yard", "club", "Restaurant", "Others", "Bussines", "Online"), state="readonly")
        c_minute.grid(column=1, row=5, sticky=tk.W)

        l_max = tk.Label(self.event_form, text="  Maximum participant")
        l_max.grid(column=2, row=5, pady=10)
        self.s_max = tk.StringVar()
        tb_max = tk.Entry(self.event_form, width=8, textvariable=self.s_max)
        tb_max.grid(column=3, row=5, columnspan=2, sticky=tk.W)

        l_description = tk.Label(self.event_form, text="Describe your Event")
        l_description.grid(column=0, row=6, pady=10, sticky=tk.NW)
        self.s_description = scrolledtext.ScrolledText(self.event_form, width=48, height=10, relief="solid", wrap=tk.WORD)
        self.s_description.grid(column=1, row=6, columnspan=6, pady=10, sticky=tk.W)

        l_spec = tk.Label(self.event_form, text="Spesifications")
        l_spec.grid(column=0, row=7, pady=10, sticky=tk.NW)
        self.s_spec = scrolledtext.ScrolledText(self.event_form, width=48, height=10, relief="solid", wrap=tk.WORD)
        self.s_spec.grid(column=1, row=7, columnspan=6, pady=10, sticky=tk.NW)

        b_picture = tk.Button(self.event_form, text="Upload Event Picture", command=lambda: self.get_picture_path())
        b_picture.grid(column=0, row=8, pady=5)
        self.s_picture = tk.StringVar()
        self.tb_picture = tk.Entry(self.event_form, width=35, textvariable=self.s_picture)
        self.tb_picture.grid(column=1, row=8, columnspan=3)

        b_createevent = tk.Button(self.event_form, text="Create Event", command=lambda: self.database_event())
        b_createevent.grid(column=0, row=9, columnspan=5, pady=5)

        self.warning_l = tk.Label(self.event_form, text="", fg="red")
        self.warning_l.grid(column=0, row=10, columnspan=7)

        l_red = tk.Label(self.event_form, text="", bg="red")
        l_red.grid(column=0, row=11, columnspan=5, ipady=5, sticky=tk.EW)

    def get_picture_path(self):
        file_path = filedialog.askopenfilename()
        self.tb_picture.insert(0, file_path)

    def database_event(self): # add event to database
        entry_list =[
            self.s_eventname.get(),
            self.system_user,
            f"{self.s_year.get()}-{self.s_month.get()}-{self.s_day.get()} {self.s_hour.get()}:{self.s_minute.get()}",
            self.s_duration.get(),
            self.s_location.get(),
            self.s_payment.get(),
            self.s_type.get(),
            self.s_max.get(),
            0,
            self.s_description.get('1.0', tk.END),
            self.s_spec.get('1.0', tk.END),
            self.s_picture.get(),
            0]
        print(entry_list)

        if "" in entry_list:
            self.warning_l.configure(text="Please fill all empty fields", fg="red")
        else:
            with open(entry_list[11], 'rb') as file:
                d_picture = file.read()
                entry_list[11] = d_picture
            print(entry_list)
            conn = sqlite3.connect("database.db")
            c = conn.cursor()
            c.execute(
                "insert into event (eventname, owner, date, duration, location, payment, type, max_participant, participant_num, description, customspec, event_pic, view)"
                " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                entry_list)
            conn.commit()
            conn.close()
            self.event_form.destroy()





if __name__ == "__main__":
    app = create_event()
    app.event_form.mainloop()
