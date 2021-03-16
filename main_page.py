import os
import sqlite3
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from create_event import create_event
from tkinter import messagebox as msg
from global_functions import centeralize_screen


class top_bar(tk.Frame): # red bar at the top
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg="red")
        self.parent = parent
        l_title = tk.Label(self, text="Socialevent", anchor="w", bg="red", fg="white", font=(None, 20))
        l_title.grid(column=0, row=0, sticky="NSEW")


class side_menu(tk.Frame): #side navigation menu
    def __init__(self, parent, friend, system_user):
        tk.Frame.__init__(self, parent, bd=1)
        self.parent = parent
        self.friend = friend

        b_events = ttk.Button(self, text="Event podium", command=lambda : friend.open_eventpodium(0))
        b_events.pack(side=tk.TOP, fill=tk.X, pady=5)

        b_profile = ttk.Button(self, text="Profile page", command=lambda : friend.open_profile(system_user))
        b_profile.pack(side=tk.TOP, fill=tk.X, pady=5)

        b_custom = ttk.Button(self, text="Create new event", command=lambda: create_event(system_user))
        b_custom.pack(side=tk.TOP, fill=tk.X, pady=5)

        b_check = ttk.Button(self, text="My events",command=lambda : friend.open_eventpodium(1))
        b_check.pack(side=tk.TOP, fill=tk.X, pady=5)

        self.s_search = tk.StringVar()
        tb_search = tk.Entry(self, width=20, textvariable=self.s_search)
        tb_search.pack(side=tk.TOP, fill=tk.X)

        b_search = ttk.Button(self, text="Search",command=lambda: self.search())
        b_search.pack(side=tk.TOP, fill=tk.X)

    def search(self): # function to search user by username
        connection = sqlite3.connect("database.db")
        c = connection.cursor()
        pattern = self.s_search.get()
        c.execute("""SELECT username FROM users WHERE username LIKE ? """,(f"{pattern}%",))
        info = c.fetchall()
        connection.close()
        self.name_list = []
        i = 0
        for inf in info: # listing results
            if(len(self.name_list) < 30):
                self.name_list.append(tk.Label(self, text=inf[0]))
                self.name_list[i].pack(side=tk.TOP)
                self.name_list[i].bind("<Button-1>", lambda e: self.goto_profile(inf[0]))
            i += 1

    def goto_profile(self,p_user): # when user go to profile page of another user unbind username and delete search result
        for labels in self.name_list:
            labels.unbind("<Button 1>")
            labels.destroy()
        del self.name_list
        self.friend.open_profile(p_user)


class event_podium(tk.Canvas):
    def __init__(self, parent, mode, system_user):
        tk.Canvas.__init__(self, parent)
        self.parent = parent

        container = tk.Frame(self)
        self.frame_id = self.create_window((0, 0), window=container, anchor=tk.NW)
        # self.container.config(width=1500)
        # self.container.grid_propagate(False)

        self.bind("<Configure>", lambda e: self.configure_frame_width(self, self.frame_id))

        button_list = []
        delete_button_list = []
        self.label_frames = []
        self.event_titles = []

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        if mode == 0:
            c.execute("SELECT eventname, date, type, max_participant, participant_num, event_pic FROM event ORDER BY date(DATE) ASC")
        else:
            c.execute("SELECT eventname, date, type, max_participant, participant_num FROM event WHERE owner = ? ORDER BY date(DATE) ASC",(system_user,))
        result = c.fetchall()
        i = 0
        for r in result:  # list events  by displaying widgets by loop
            self.event_titles.append(r[0])
            if mode == 0:
                self.label_frames.append(tk.LabelFrame(container, width=700, height=550))
            else:
                self.label_frames.append(tk.LabelFrame(container, width=700, height=150))
            self.label_frames[i].grid_propagate(False)
            self.label_frames[i].pack(padx=10, pady=10, side=tk.TOP, expand=True)
            self.label_frames[i].columnconfigure(0, weight=3)
            self.label_frames[i].columnconfigure(1, weight=7)

            if mode == 0:  # mode 0 is event podium 1 is my events windowe.
                canvas_for_image = tk.Canvas(self.label_frames[i], bg='green', height=420, width=720, borderwidth=0,
                                             highlightthickness=0)
                canvas_for_image.grid(row=0, column=0, sticky='nesw', columnspan=2)

                with open("temporary.png", 'wb') as file:
                    file.write(r[5])
                image = Image.open('temporary.png')
                canvas_for_image.image = ImageTk.PhotoImage(image.resize((720, 420), Image.ANTIALIAS))
                canvas_for_image.create_image(0, 0, image=canvas_for_image.image, anchor='nw')
                os.remove("temporary.png")


            l_eventname = tk.Label(self.label_frames[i], text="", font=("Calibri", 15))
            l_eventname.grid(column=0, row=1, sticky=tk.W, columnspan=2)
            l_date = tk.Label(self.label_frames[i], text="", font=("Calibri", 15))
            l_date.grid(column=0, row=2, sticky=tk.W)
            l_participation = tk.Label(self.label_frames[i], text="", font=("Calibri", 15))
            l_participation.grid(column=0, row=3, sticky=tk.W)
            l_type = tk.Label(self.label_frames[i], text="", font=("Calibri", 15))
            l_type.grid(column=0, row=4, sticky=tk.W)

            l_eventname["text"] = r[0]
            l_date["text"] = r[1]
            l_type["text"] = "Event type: " + r[2]
            l_participation["text"] = str(r[4]) + "/" + str(r[3])

            progress_bar = ttk.Progressbar(self.label_frames[i], orient="horizontal", length=400, mode="determinate")
            progress_bar.grid(column=1, row=3, sticky=tk.E)
            progress_bar["maximum"] = r[3]
            progress_bar["value"] = r[4]

            button_list.append(
                tk.Button(self.label_frames[i], text="Check Event", command=lambda event_name=r[0]: self.show_details(system_user, event_name)))
            button_list[i].grid(column=1, row=4, sticky=tk.E)
            if mode == 1:
                delete_button_list.append(
                    tk.Button(self.label_frames[i], text="Delete Event",
                              command=lambda event_name=r[0]: self.delete(event_name)))
                delete_button_list[i].grid(column=1, row=5, sticky=tk.E)
            i += 1
        conn.close()

    def configure_frame_width(self, c_id, f_id):  # to centralize canvas on a frame
        c_id.itemconfig(f_id, width=self.parent.winfo_width())

    def show_details(self, p_username, p_eventname):
        self.parent.show_details(p_username, p_eventname)

    def delete(self, p_eventname): #  delete event from database
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("Delete FROM event WHERE eventname = ?", (p_eventname,))
        c.execute("Delete FROM participants WHERE event_name = ?", (p_eventname,))
        conn.commit()
        msg.showinfo("info!","Event deleted from event podium succesfully")
        conn.close()
        self.parent.open_eventpodium(1)


class event_details(tk.Canvas):
    def __init__(self, parent, system_user, event_title):
        tk.Canvas.__init__(self, parent)
        self.parent = parent
        self.system_user = system_user
        self.event_title = event_title

        self.eventdetails_frame = tk.Frame(self)
        self.eventdetails_frame_int = self.create_window((0, 0), window=self.eventdetails_frame, anchor=tk.NW)

        self.bind("<Configure>", lambda e: self.configure_frame_width(self, self.eventdetails_frame_int))

        eventdetails_frame_c = tk.Frame(self.eventdetails_frame)
        eventdetails_frame_c.pack(expand=True)
        eventdetails_frame_c.columnconfigure(0, weight=7, minsize=700)

        top_frame = tk.Frame(eventdetails_frame_c, bg="red", height=20)
        top_frame.grid(column=0, row=0)

        event_name = tk.Label(top_frame, text=event_title, bg="red", fg="white", font=(None, 20), width=70)
        event_name.grid(column=0, row=0)

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("UPDATE event SET view = view + 1 WHERE  eventname=?", (event_title,)) # increase view counter
        c.execute("SELECT * FROM event Where eventname=?", (event_title,))
        event_data = c.fetchone()
        conn.commit()
        conn.close()

        canvas_for_image = tk.Canvas(eventdetails_frame_c, height=550, width=700, borderwidth=0,
                                     highlightthickness=0)
        canvas_for_image.grid(column=0, row=1, sticky='nesw', padx=0, pady=0) #canvas to place image

        with open("temporary.png", 'wb') as file:
            file.write(event_data[11], )
        image = Image.open('temporary.png')
        canvas_for_image.image = ImageTk.PhotoImage(image.resize((919, 550), Image.ANTIALIAS))
        canvas_for_image.create_image(0, 0, image=canvas_for_image.image, anchor='nw')
        os.remove("temporary.png")

        text_label = ttk.Label(eventdetails_frame_c, text="", wraplength=920)
        text_label.grid(column=0, row=2, pady=10, columnspan=2)
        text_label[
            "text"] = f"Event Description:\n{event_data[9]}\nWhat is Needed:\n{event_data[10]}\nDate/Time: {event_data[2]}\nDuration: {event_data[3]}\nLocation{event_data[4]}\n" \
                      f"Payment {event_data[5]}"

        counter_frame = tk.Frame(eventdetails_frame_c, bd=0, relief=tk.SOLID)
        counter_frame.grid(column=0, row=3)
        counter_frame.rowconfigure(0, weight=1)

        counter_frame_left = tk.Frame(counter_frame)
        counter_frame_left.grid(column=0, row=0, padx=10, pady=5)
        l_view = tk.Label(counter_frame_left, text="This event viewed", font=(None, 15, "bold"))
        l_view.pack()
        l_nview = tk.Label(counter_frame_left, text=event_data[12], font=(None, 40, "bold"))
        l_nview.pack()
        l_times = tk.Label(counter_frame_left, text="Times", font=(None, 15, "bold"))
        l_times.pack()

        counter_frame_right = tk.Frame(counter_frame)
        counter_frame_right.grid(column=1, row=0, padx=5)
        l_tr = tk.Label(counter_frame_right, text="There are:", font=(None, 15, "bold"))
        l_tr.pack()
        l_participantnum = tk.Label(counter_frame_right, text=f"{event_data[8]}/{event_data[7]}", font=(None, 40,"bold"))
        l_participantnum.pack()
        l_pn = tk.Label(counter_frame_right, text="Participants in this event", font=(None, 15, "bold"))
        l_pn.pack()

        button_frame = tk.Frame(eventdetails_frame_c, bg="red", height=15)
        button_frame.grid(column=0, row=4, columnspan=2, pady=10)
        join_b = tk.Button(button_frame, text="Go Back", command=lambda: self.cancel(),font=(None, 15))
        join_b.pack(side=tk.RIGHT, pady=10)
        join_b = tk.Button(button_frame, text="Join Event",font=(None, 15), command=lambda: self.join_event(event_title, ))
        join_b.pack(side=tk.RIGHT, pady=10)
        if event_data[8] >= event_data[7]:
            join_b.config(text="opss! full event", state="disabled")

    def configure_frame_width(self, c_id, f_id):
        c_id.itemconfig(f_id, width=self.parent.winfo_width())

    def join_event(self, event_name):  # add user to selected event as participant
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT event_name, user_name FROM participants WHERE event_name = ? AND user_name = ?", (self.event_title, self.system_user,))
        result = c.fetchone()
        if not result:
            c.execute(
                "insert into participants (event_name, user_name)"
                " VALUES (?, ?)",
                (event_name, self.system_user,))
            c.execute(
                "UPDATE users SET socialpoint = socialpoint + 100 WHERE  username=?", (self.system_user,))
            c.execute(
                "UPDATE event SET participant_num = participant_num + 1 WHERE  eventname=?", (event_name,))
        else:
            msg.showwarning("Warning!","You already joined this event")
        conn.commit()
        conn.close()
        self.cancel()

    def cancel(self):
        # self.scroll.pack_forget()
        self.parent.open_eventpodium(0)


class profile_page(tk.Canvas):
    def __init__(self, parent, system_user):
        tk.Canvas.__init__(self, parent)
        self.parent = parent

        self.profile_f = tk.Frame(self)
        self.profile_f_int = self.create_window((0, 0), window=self.profile_f, anchor=tk.NW)

        self.bind("<Configure>", lambda e: self.configure_frame_width(self, self.profile_f_int))

        profile_f_c = tk.Frame(self.profile_f)
        profile_f_c.pack(expand=True)
        profile_f_c.columnconfigure(0, weight=2)
        profile_f_c.columnconfigure(1, weight=12, minsize=450)
        profile_f_c.columnconfigure(2, weight=2, minsize=140)



        profile_pic = tk.Frame(profile_f_c, bd=0)
        profile_pic.grid(column=0, row=0)


        canvas_for_image = tk.Canvas(profile_pic, bg='green', height=180, width=180, borderwidth=0, highlightthickness=0)
        canvas_for_image.grid(row=0, column=0, sticky='nesw', padx=0, pady=0)

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute(
            "SELECT fullname, city, country, date_of_birth, gender, about_me, socialpoint, biography, picture FROM users "
            "Where username=?", (system_user,))
        stats = c.fetchone()

        with open("temporary.png", 'wb') as file:
            file.write(stats[8],)
        image = Image.open('temporary.png')
        canvas_for_image.image = ImageTk.PhotoImage(image.resize((180, 180), Image.ANTIALIAS))
        canvas_for_image.create_image(0, 0, image=canvas_for_image.image, anchor='nw')
        os.remove("temporary.png")

        l_username = tk.Label(profile_pic, text=system_user, font=(None, 20, "bold"))# rearange to use in other frames
        l_username.grid(column=0, row=1)

        # ---------------------------------------- name bar
        name_f = tk.LabelFrame(profile_f_c, width=300, height=20, bd=0)
        name_f.grid(column=1, row=0, sticky=tk.NSEW)
        name_f.grid_propagate(False)

        center_f = tk.Frame(name_f, bd=0)
        center_f.pack(expand=True)
        l_fullname = tk.Label(center_f, text=stats[0], font=(None, 15))
        l_fullname.pack()
        l_biography = tk.Label(center_f, text=stats[7], font=(None, 15))
        l_biography.pack()
        l_adress = tk.Label(center_f, text=f"{stats[1]}/{stats[2]}", font=(None, 15))
        l_adress.pack()

        # ---------------------------------------- socila level box
        level_l = tk.LabelFrame(profile_f_c, width=10, height=10, bd=0)
        level_l.grid(column=2, row=0, sticky=tk.NSEW)
        c_l = tk.Frame(level_l, bd=0)
        c_l.pack(expand=True)
        socialpoint = stats[6]
        l_socialp = tk.Label(c_l, text=f"Social Point: {socialpoint}")
        l_socialp.pack()
        l_sociall = tk.Label(c_l, text="")
        if (socialpoint > 500):
            l_sociall["text"] = "Legend"
        elif (socialpoint > 400):
            l_sociall["text"] = "SuperNova"
        elif (socialpoint > 300):
            l_sociall["text"] = "SuperStar"
        elif (socialpoint > 200):
            l_sociall["text"] = "NewStar"
        elif (socialpoint > 100):
            l_sociall["text"] = "Sparkle"
        else:
            l_sociall["text"] = "Someone"
        l_sociall.pack()

        # -------------------------------------------------about user
        text_label = ttk.Label(profile_f_c, text="", wraplength=760)
        text_label.grid(column=0, row=1, columnspan=3)
        text_label["text"] = f"About me:\n{stats[5]}"
        participations_f = tk.Frame(profile_f_c)
        participations_f.grid(column=0, row=2, columnspan=3, sticky=tk.NSEW)
        c.execute("SELECT event_name FROM participants WHERE user_name = ?", (system_user,))
        events = c.fetchall()
        event_list = []
        button_list = []
        l = tk.Label(participations_f, text="events im participating:", anchor=tk.W, font=(None, 15, "bold"))
        l.grid(column=0, row=0)
        i = 0
        if events: # list events that user is planning to participate
            for e in events:
                event_list.append(tk.LabelFrame(participations_f, width=750, height=30))
                event_list[i].grid_propagate(False)
                event_list[i].grid(column=0, row=i+1)
                l_pname = tk.Label(event_list[i], text=f"{e[0]}")
                l_pname.grid(column=0, row=0)
                button_list.append(
                    tk.Button(event_list[i], text="Check Event", command=lambda x=e[0]: parent.show_details(system_user, x)))
                button_list[i].grid(column=1, row=0, sticky=tk.E)
                i += 1
        else:
            notp_label = tk.Label(participations_f, text="Not participating any event")
            notp_label.grid(column=0, row=1)
        c.close()

    def configure_frame_width(self, c_id, f_id):
        c_id.itemconfig(f_id, width=self.parent.winfo_width())


class main_frame(tk.Frame): # all windows are at top of this frame
    def __init__(self, parent, system_user):
        tk.Frame.__init__(self, parent, bd=0)
        self.parent = parent
        self.system_user = system_user
        self.columnconfigure(0, weight=1)

        self.event_podium_c = event_podium(self, 0, self.system_user)
        self.event_podium_c.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scroll_bar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.event_podium_c.yview)
        self.scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
        self.event_podium_c.configure(yscrollcommand=self.scroll_bar.set)
        self.bind("<Configure>", lambda e: self.event_podium_c.configure(scrollregion=self.event_podium_c.bbox("all")))

    def show_details(self, sys_user, event_title):  # change current window with event details
        self.destroy_current_window()
        self.event_details_c = event_details(self, sys_user, event_title)
        self.event_details_c.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.set_scroll_bar(self.event_details_c)

    def open_eventpodium(self, mode):  # change current window with event podium
        self.destroy_current_window()
        self.event_podium_c = event_podium(self, mode, self.system_user)
        self.event_podium_c.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.set_scroll_bar(self.event_podium_c)



    def open_profile(self, p_username): # change current window by user proflile
        self.destroy_current_window()
        self.profile_c = profile_page(self, p_username)
        self.profile_c.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.set_scroll_bar(self.profile_c)


    def destroy_current_window(self):
        for child in self.winfo_children():
            if child != self.scroll_bar:
                child.destroy()

    def set_scroll_bar(self, p_frame): # set scroll bar to given frame
        self.scroll_bar.config(command=p_frame.yview)
        p_frame.configure(yscrollcommand=self.scroll_bar.set)
        self.bind("<Configure>", lambda e: p_frame.configure(scrollregion=p_frame.bbox("all")))
        self.update()
        self.scroll_bar.update()


class window(tk.Tk):
    def __init__(self, system_user):
        tk.Tk.__init__(self)
        self.title("SocialEvent")
        self.geometry(centeralize_screen(screen_width=self.winfo_screenwidth(),
                                                      screen_height=self.winfo_screenheight(),
                                                      window_width=1000,
                                                      window_height=1000))
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=9)
        self.rowconfigure(1, weight=1)

        top_frame = top_bar(self)
        top_frame.grid(column=0, row=0, columnspan=2, sticky=tk.NSEW)

        self.main_frame = main_frame(self, system_user)
        self.main_frame.grid(column=1, row=1, sticky=tk.NSEW)  # other windows

        side_frame = side_menu(self, self.main_frame, system_user)  # side navigation menu
        side_frame.grid(column=0, row=1, sticky=tk.NSEW)

        self.mainloop()



