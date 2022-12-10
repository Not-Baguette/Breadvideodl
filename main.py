from pytube import YouTube, exceptions
import os
import customtkinter
from PIL import Image
import urllib.request
import urllib.error
from tkinter import filedialog


# UI Build
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Breadvideodl")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)  # NOQA
        self.grid_rowconfigure((0, 1, 2), weight=1)  # NOQA

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="BREADVIDEODL",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_change_dl_path_button = customtkinter.CTkButton(self.sidebar_frame, command=self.dl_path_change,
                                                                     text="Change Download Path")
        self.sidebar_change_dl_path_button.grid(row=1, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                                       values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                               values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Enter link here")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2,
                                                     text_color=("gray10", "#DCE4EE"), text="Download",
                                                     command=self.download_video)
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=1, columnspan=2, rowspan=3, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("General Information")
        self.tabview.add("More")
        self.tabview.tab("General Information").grid_columnconfigure(0, weight=1)
        self.tabview.tab("More").grid_columnconfigure(0, weight=1)
        self.thumbnailimg = customtkinter.CTkImage(light_image=Image.open("defaultthumb.jpg"),
                                                   dark_image=Image.open("defaultthumb.jpg"),
                                                   size=thumbnail_default)
        self.thumbnailbutton = customtkinter.CTkButton(self.tabview.tab("General Information"), image=self.thumbnailimg,
                                                       state="disabled", text="", fg_color="gray10", border_width=2)
        self.thumbnailbutton.grid(row=0, column=0, padx=(0, 20), pady=(0, 20), sticky="nsew")
        self.titlelabel = customtkinter.CTkLabel(self.tabview.tab("General Information"), text="Title: None")
        self.titlelabel.grid(row=1, column=0, sticky="nsew")
        self.authorLabel = customtkinter.CTkLabel(self.tabview.tab("General Information"), text="Author: None")
        self.authorLabel.grid(row=2, column=0)
        self.lengthLabel = customtkinter.CTkLabel(self.tabview.tab("General Information"), text="Length: None")
        self.lengthLabel.grid(row=3, column=0)
        self.recheck_button = customtkinter.CTkButton(self.tabview.tab("General Information"), text="Recheck",
                                                      command=self.general_inf_generate)
        self.recheck_button.grid(row=4, column=0, padx=20, pady=20)
        self.tabview.tab("General Information").grid_rowconfigure(0, weight=1)

        self.descriptionTextbox = customtkinter.CTkTextbox(self.tabview.tab("More"), width=700, padx=20, pady=20,
                                                           height=600)
        self.descriptionTextbox.insert("end", "Description: None")
        self.descriptionTextbox.configure(state="disabled")
        self.descriptionTextbox.grid(row=0, column=0, columnspan=4)

        self.tabview.tab("More").grid_rowconfigure(0, weight=1)
        self.tabview.tab("More").grid_columnconfigure(0, weight=1)

        self.PublishDateLabel = customtkinter.CTkLabel(self.tabview.tab("More"), text="Publish Date: None")
        self.PublishDateLabel.grid(row=2, column=0)

        self.viewsLabel = customtkinter.CTkLabel(self.tabview.tab("More"), text="Views: None")
        self.viewsLabel.grid(row=4, column=0)

        # create switch frame
        self.slider_frame = customtkinter.CTkFrame(self)
        self.slider_frame.grid(row=0, column=3, rowspan=3, padx=(20, 20), pady=(20, 0), sticky="nsew")

        # Just copt this code and paste it to make a new switch if you want to make a new feature
        self.switch_1 = customtkinter.CTkSwitch(master=self.slider_frame, text="Bypass Age Restriction",
                                                command=self.bypass_age_restriction_event)
        self.switch_1.grid(row=3, column=0, pady=10, padx=20, sticky="nw")

        # set default values
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")

    def change_appearance_mode_event(self, new_appearance_mode: str):  # NOQA
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        global thumbnail_default, old_thumbnail_default
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
        if new_scaling_float == 0.8:
            thumbnail_default = (720, 405)
        elif new_scaling_float == 0.9:
            thumbnail_default = (640, 360)
        elif new_scaling_float == 1:
            thumbnail_default = old_thumbnail_default
        elif new_scaling_float == 1.1:
            thumbnail_default = (350, 210)
        elif new_scaling_float == 1.2:
            thumbnail_default = (300, 170)

        self.thumbnailimg.configure(size=thumbnail_default)
        self.update()

    def bypass_age_restriction_event(self):
        global bypass_age_restriction
        if self.switch_1.get() == 1:
            bypass_age_restriction = True
        else:
            bypass_age_restriction = False

    def dl_path_change(self):
        global path_dl_folder
        path_dl_folder = filedialog.askdirectory(initialdir="./",
                                                 title="Open a text file")

    def general_inf_generate(self):
        link = self.entry.get()

        # Thumbnail
        try:
            url = YouTube(link, on_progress_callback=self.progress_func, on_complete_callback=self.complete_download)
            # get the id of the video
            video_id = url.video_id

            urllib.request.urlretrieve(f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg", "maxresdefault.jpg")
            self.thumbnailimg.configure(dark_image=Image.open("maxresdefault.jpg"),
                                        light_image=Image.open("maxresdefault.jpg"),
                                        size=thumbnail_default)
        except exceptions.RegexMatchError:
            self.thumbnailimg.configure(dark_image=Image.open("defaultthumb.jpg"),
                                        light_image=Image.open("defaultthumb.jpg"),
                                        size=thumbnail_default)
        except urllib.error.HTTPError:
            self.thumbnailimg.configure(dark_image=Image.open("defaultthumb.jpg"),
                                        light_image=Image.open("defaultthumb.jpg"),
                                        size=thumbnail_default)
            print("The creator didn't put a thumbnail manually")

        # Title
        try:
            self.titlelabel.configure(text=f"Title: {url.title}")  # NOQA
        except exceptions.RegexMatchError:
            self.titlelabel.configure(text="Title: None")

        # Author
        try:
            self.authorLabel.configure(text="Author: " + url.author)
        except exceptions.RegexMatchError:
            self.authorLabel.configure(text="Author: None")

        # length
        try:
            runtime_seconds = url.length
            # convert seconds to minutes and seconds
            rt_min = str(runtime_seconds // 60)
            rt_sec = str(runtime_seconds % 60)

            if int(rt_sec) < 10:
                rt_sec = "0" + rt_sec
            elif rt_sec == "0":
                rt_sec = "00"

            self.lengthLabel.configure(text=f"Length: {rt_min}:{rt_sec}")
        except exceptions.RegexMatchError:
            self.lengthLabel.configure(text="Length: None")

        # Description
        try:
            self.descriptionTextbox.configure(state="normal")
            self.descriptionTextbox.delete("1.0", "end")
            self.descriptionTextbox.insert("end", text=f"Description: {url.description}")
        except exceptions.RegexMatchError:
            self.descriptionTextbox.insert("end", text="Description: None")

        # Publish Date
        try:
            self.PublishDateLabel.configure(text=f"Publish Date: {str(url.publish_date)[:10]}")
        except exceptions.RegexMatchError:
            self.PublishDateLabel.configure(text="Publish Date: None")

        # Views
        try:
            # make the viewcount more readable
            self.viewsLabel.configure(text=f"Views: {url.views}")
        except exceptions.RegexMatchError:
            self.viewsLabel.configure(text="Views: None")

        self.descriptionTextbox.configure(state="disabled")
        self.update()

    def progress_func(self, self2, chunk, bytes_remaining):  # NOQA
        print(self2)  # Just show it cuz it makes it slightly cooler ig
        global start, total_bytes
        if start is True:
            total_bytes = bytes_remaining
            print(f"Download started, total bytes: {round(total_bytes / 1024 / 1024, 2)}mb")
            start = False

        print(total_bytes)
        try:
            os.system("cls")
            percent = (100 * (total_bytes - bytes_remaining)) / total_bytes
            print(f"Download Progress: {percent:.2f}%")
            # round it the nearest 5th
            rounded_percent = round(percent / 5) * 5
            print(f"|{'█' * int(rounded_percent / 5)}{' ' * (20 - int(rounded_percent / 5))}|\n")
            os.system("\n" * 50)
        except ZeroDivisionError:
            print("ZeroDivisionError")
        except NameError:
            print("NameError")

    def complete_download(self, info, saved_path):  # NOQA
        print("Saved to:", saved_path)
        print("Download Completed")

    def download_video(self):
        link = self.entry.get()
        url = YouTube(link, on_progress_callback=self.progress_func, on_complete_callback=self.complete_download)

        if bypass_age_restriction:
            url.bypass_age_gate()

        video = url.streams.get_highest_resolution()
        video.download(path_dl_folder)


if __name__ == "__main__":
    start = True
    bypass_age_restriction = False
    total_bytes = 0
    path_dl_folder = f"C:\\Users\\{os.getlogin()}\\Downloads"  # Default download folder
    thumbnail_default = old_thumbnail_default = (480, 270)
    os.system("cls")
    print("Starting GUI...")
    print("Do not close this window if you want to see the progress")
    print("Breadvideodl, Made by Baguette with love")

    root = App()
    root.mainloop()
