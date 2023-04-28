import customtkinter
import time
import pygame
import tkinter
from tkinter import messagebox
from PIL import Image
from customtkinter import CTkFont
import pyglet


FG_COLOR = "#DADADA"


class MyTimer:

    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("blue")

    def __init__(self, app):

        self.app = app
        self.app.title("MyTimer")
        self.app.geometry("{}x{}+{}+{}".format(400, 240, 750, 250))
        self.app.resizable(False, False)
        self.app.grid_rowconfigure(0, weight=1)
        self.app.grid_columnconfigure(0, weight=1)
        self.app.iconbitmap("images/stopwatch.ico")
        pygame.init()
        pygame.mixer.init()
        self.sound = pygame.mixer.music.load("audio/buzzer.mp3")
        self.font = customtkinter.CTkFont(family="Dubai", size=23)

        self.running = False
        self.paused = False
        self.elapsed = False

        self.bg_image = customtkinter.CTkImage(
            light_image=Image.open("images/bg.png"), size=(400, 240)
        )
        self.start_icon = customtkinter.CTkImage(
            light_image=Image.open("images/start_icon.png"), size=(70, 70)
        )
        self.pause_icon = customtkinter.CTkImage(
            light_image=Image.open("images/pause_icon.png"), size=(70, 70)
        )
        self.reset_icon = customtkinter.CTkImage(
            light_image=Image.open("images/reset_icon.png"), size=(70, 70)
        )
        self.logo_image = customtkinter.CTkImage(
            light_image=Image.open("images/stopwatch.png"), size=(70, 70)
        )

        self.bg = customtkinter.CTkLabel(master=self.app, text="", image=self.bg_image)
        self.bg.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.frame = customtkinter.CTkFrame(master=self.app)
        self.frame.grid(row=0, column=0, padx=7, pady=7, columnspan=2, sticky="NSEW")

        self.hour_entry = customtkinter.CTkEntry(
            master=self.frame,
            placeholder_text="H",
            width=70,
            height=70,
            font=self.font,
            justify="center",
        )
        self.hour_entry.place(relx=1 / 6, rely=0.3, anchor=tkinter.CENTER)

        self.colon = customtkinter.CTkLabel(
            master=self.frame, text=":", font=("CTkDefaultFont", 20)
        )
        self.colon.place(relx=2 / 6, rely=0.3, anchor=tkinter.CENTER)

        self.min_entry = customtkinter.CTkEntry(
            master=self.frame,
            placeholder_text="M",
            width=70,
            height=70,
            font=self.font,
            justify="center",
        )
        self.min_entry.place(relx=3 / 6, rely=0.3, anchor=tkinter.CENTER)

        self.second_entry = customtkinter.CTkEntry(
            master=self.frame,
            placeholder_text="S",
            width=70,
            height=70,
            font=self.font,
            justify="center",
        )
        self.second_entry.place(relx=5 / 6, rely=0.3, anchor=tkinter.CENTER)

        self.colon1 = customtkinter.CTkLabel(
            master=self.frame, text=":", font=("CTkDefaultFont", 20)
        )
        self.colon1.place(relx=4 / 6, rely=0.3, anchor=tkinter.CENTER)

        self.start_butt = customtkinter.CTkButton(
            master=self.frame,
            text="",
            image=self.start_icon,
            command=self.start,
            fg_color="transparent",
            hover_color=FG_COLOR,
            width=1,
            height=1,
        )
        self.start_butt.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

        self.pause_butt = customtkinter.CTkButton(
            master=self.frame,
            text="",
            image=self.pause_icon,
            command=self.pause,
            fg_color="transparent",
            hover_color=FG_COLOR,
            width=1,
            height=1,
        )
        self.reset_butt = customtkinter.CTkButton(
            master=self.frame,
            text="",
            image=self.reset_icon,
            command=self.reset,
            fg_color="transparent",
            hover_color=FG_COLOR,
            width=1,
            height=1,
        )

        self.frame.grid_rowconfigure(1, weight=0)
        self.frame.grid_columnconfigure(2, weight=0)
        self.frame.grid_rowconfigure(2, weight=0)

    def start(self):
        """Operations after clicking "Play" button"""

        # Entry validation
        if (
            (self.hour_entry.get().isnumeric() == False and self.hour_entry.get() != "")
            or (
                self.min_entry.get().isnumeric() == False and self.min_entry.get() != ""
            )
            or (
                self.second_entry.get().isnumeric() == False
                and self.second_entry.get() != ""
            )
        ):
            return messagebox.showerror(
                "Wrong input", "You have to enter numeric value, pelase try again."
            )

        # First launch (with displayed entry boxed)
        if self.running == False:
            if self.hour_entry.get() == "":
                self.hour_label = customtkinter.CTkLabel(
                    master=self.frame, text="00", font=self.font
                )
            else:
                self.hour_label = customtkinter.CTkLabel(
                    master=self.frame,
                    text=self.hour_entry.get().zfill(2),
                    font=self.font,
                )
            if self.min_entry.get() == "":
                self.min_label = customtkinter.CTkLabel(
                    master=self.frame, text="00", font=self.font
                )
            else:
                self.min_label = customtkinter.CTkLabel(
                    master=self.frame,
                    text=self.min_entry.get().zfill(2),
                    font=self.font,
                )
            if self.second_entry.get() == "":
                self.second_label = customtkinter.CTkLabel(
                    master=self.frame, text="00", font=self.font
                )
            else:
                self.second_label = customtkinter.CTkLabel(
                    master=self.frame,
                    text=self.second_entry.get().zfill(2),
                    font=self.font,
                )
            self.reset_butt.place(relx=5 / 6, rely=0.7, anchor=tkinter.CENTER)

            self.hour_entry.place_forget()
            self.min_entry.place_forget()
            self.second_entry.place_forget()
            self.min_label.place(relx=3 / 6, rely=0.3, anchor=tkinter.CENTER)
            self.hour_label.place(relx=1 / 6, rely=0.3, anchor=tkinter.CENTER)
            self.second_label.place(relx=5 / 6, rely=0.3, anchor=tkinter.CENTER)
            self.running = True

        # If launched while paused
        else:
            self.paused = False

        # Actions performed always, regardless launched while paused or not
        self.start_butt.place_forget()
        self.pause_butt.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)
        self.app.after(1000, self.update_timer)

    def reset(self):
        """Operations after clickng 'Reset' button"""

        self.elapsed = False
        self.running = False
        self.paused = False
        self.hour_label.place_forget()
        self.min_label.place_forget()
        self.second_label.place_forget()
        self.hour_entry.place(relx=1 / 6, rely=0.3, anchor=tkinter.CENTER)
        self.min_entry.place(relx=3 / 6, rely=0.3, anchor=tkinter.CENTER)
        self.second_entry.place(relx=5 / 6, rely=0.3, anchor=tkinter.CENTER)
        self.pause_butt.place_forget()
        self.start_butt.place_forget()
        self.reset_butt.place_forget()
        self.start_butt.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

    def pause(self):
        """Operations after clickng 'Pause' button"""
        self.paused = True
        self.pause_butt.place_forget()
        self.start_butt.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

    def update_timer(self):
        """Timer mechanism"""

        if self.running == True and self.paused == False and self.elapsed == False:
            if (
                int(self.min_label.cget("text")) == 0
                and int(self.hour_label.cget("text")) == 0
                and int(self.second_label.cget("text")) == 0
            ):
                self.elapsed = True
                self.running = False
                pygame.mixer.music.play(-1)
                end_info = messagebox.showinfo("Time's up!", "Time have passed!")
                pygame.mixer.music.stop()
                self.start_butt.place_forget()
                self.pause_butt.place_forget()
            elif int(self.second_label.cget("text")) > 0:
                second_label_new = int(self.second_label.cget("text")) - 1
                self.second_label.configure(text=str(second_label_new).zfill(2))
            else:
                self.second_label.configure(text="59")
                if int(self.min_label.cget("text")) > 0:
                    min_label_new = int(self.min_label.cget("text")) - 1
                    self.min_label.configure(text=str(min_label_new).zfill(2))
                else:
                    if int(self.hour_label.cget("text")) > 0:
                        self.min_label.configure(text="59")
                        hour_label_new = int(self.hour_label.cget("text")) - 1
                        self.hour_label.configure(text=str(hour_label_new).zfill(2))

            self.app.after(1000, self.update_timer)


app = customtkinter.CTk()
running = MyTimer(app)
app.mainloop()
