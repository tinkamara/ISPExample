import tkinter as tk
from abc import ABC, abstractmethod
from tkinter import ttk
from tkinter import messagebox
from pygame import mixer

class ScalableDevice(ABC):
    @abstractmethod
    def scale_device(self, value):
        pass

class BinaryDevice(ABC):
    @abstractmethod
    def toggle(self):
        pass

class BinaryLightBulb(BinaryDevice):
    def __init__(self, device_id, parent):
        self.id = device_id
        self.parent = parent
        self.state = False  # starts in off state, therefore False
        self.frame = ttk.Frame(self.parent)
        self.frame.pack(side=tk.LEFT, padx=10)
        self.canvas = tk.Canvas(self.frame, width=100, height=100)
        self.canvas.pack()
        self.bulb = self.canvas.create_oval(10, 10, 90, 90, fill='black')  # circle as improvised light bulb
        self.button = ttk.Button(self.frame, text="Ein/Aus", command=self.toggle)
        self.button.pack(pady=10)

    def toggle(self):
        self.state = not self.state
        if self.state:
            self.canvas.itemconfig(self.bulb, fill='yellow')  # turn on light bulb
        else:
            self.canvas.itemconfig(self.bulb, fill='black')  # turn off light bulb

class ScalableLightBulb(ScalableDevice):
    def __init__(self, device_id, parent):
        self.id = device_id
        self.parent = parent
        self.brightness = tk.DoubleVar()
        self.frame = ttk.Frame(self.parent)
        self.frame.pack(side=tk.LEFT, padx=10)
        self.canvas = tk.Canvas(self.frame, width=100, height=100)
        self.canvas.pack()
        self.bulb = self.canvas.create_oval(10, 10, 90, 90, fill='black')  # circle as improvised light bulb
        self.scale = ttk.Scale(self.frame, from_=0, to=1, orient=tk.HORIZONTAL, variable=self.brightness,
                               command=self.scale_device)
        self.scale.pack(pady=10)

    def scale_device(self, value):
        try:
            brightness_value = int(float(value) * 255)
            if brightness_value < 0:
                brightness_value = 0
            elif brightness_value > 255:
                brightness_value = 255
            color = '#{:02x}{:02x}00'.format(brightness_value, brightness_value)  # adjust color values to "adjust brightness"
            self.canvas.itemconfig(self.bulb, fill=color)
        except ValueError:
            pass

class Speaker(ScalableDevice, BinaryDevice):
    def __init__(self, device_id, parent):
        self.id = device_id
        self.parent = parent
        self.state = False
        self.volume = tk.DoubleVar()
        self.frame = ttk.Frame(self.parent)
        self.frame.pack(side=tk.LEFT, padx=10)
        self.scale = ttk.Scale(self.frame, from_=0, to=100, orient=tk.HORIZONTAL, variable=self.volume,
                               command=self.scale_device)
        self.scale.pack(pady=10)
        try:
            mixer.init()
        except Exception as e:
            messagebox.showerror("Error occured: ", str(e))
        self.scale.set(100)  # set scale value to the right because music will start playing on first button press
        self.play_music = ttk.Button(self.frame, text="Musik abspielen", command=self.toggle)
        self.play_music.pack()

    #def scale_volume(self, value):     #example for erroneous start because scale_device is not defined
    def scale_device(self, value):
        mixer.music.set_volume(float(value) / 100)  # adjust volume according to scaled value

    def toggle(self):
        if  self.state == False:
            mixer.init()
            mixer.music.load("background_music.mp3")
            mixer.music.play(-1)  # -1 means infinite loop
            self.play_music.configure(text="Musik stoppen")
            self.play_music.configure(command=self.toggle)
            self.state = True
        else:
            mixer.music.stop()
            self.play_music.configure(text="Musik abspielen")
            self.play_music.configure(command=self.toggle)
            self.state = False


class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Interface Example")

        self.new_device_id = 1
        self.devices = []

    def add_device(self, device):
        self.devices.append(device(self.new_device_id, self.root))
        self.new_device_id += 1
    
    def remove_device(self, device):
        self.devices.remove(device)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    gui = GUI()
    gui.add_device(Speaker)
    gui.add_device(BinaryLightBulb)
    gui.add_device(ScalableLightBulb)
    #gui.add_device(BinaryLightBulb)    #proof that different objects do not affect each other
    #gui.add_device(ScalableLightBulb)  #proof that different objects do not affect each other
    gui.run()