# SPRITE EXTRACTOR OTG
# DEVELOPER: AKASH BORA (Akascape)
# Version: 1.3

import os
from tkinter import *
from tkinter import Tk, Button, Label, PhotoImage, ttk, messagebox, filedialog
import tkinter
import time
import sys
import json
import plistlib
from xml.etree import ElementTree
import webbrowser
from PIL import Image
    
def resource_path(relative_path):
    base_path = getattr(
        sys,
        '_MEIPASS',
        os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def openfile():
    global file
    file = tkinter.filedialog.askopenfilename(filetypes =[('PNG', '*.png'),('All Files', '*.*')])
    if file:
        locationlabel.config(text=os.path.basename(file), fg="#6D76CD", font=("Aharoni",15))
        saveImg['text']='Open Again'
        saveImg['bg']='#D0CECE'
    else:
        locationlabel.config(text="IMPORT THE SPRITE IMAGE",fg="#6D76CD", font=("Aharoni",15))
        saveImg['text']='Open'
        saveImg['bg']="#82CC6C"
        
def openfile2():
    global file2, extension
    file2 = tkinter.filedialog.askopenfilename(filetypes =[('Data File', ['*.plist', '*.xml', '*.json', '*.cocos']),('All Files', '*.*')])
    if file2:
        locationlabel2.config(text=os.path.basename(file2), fg="#6D76CD", font=("Aharoni",15))
        savePlist['text']='Open Again'
        savePlist['bg']='#D0CECE'
        extension = os.path.splitext(file2)[-1]
    else:
        locationlabel2.config(text="IMPORT THE DATA FILE",fg="#6D76CD", font=("Aharoni",15))
        savePlist['text']='Open'
        savePlist['bg']="#82CC6C"
        
def ExtractSprite(imagefile, datafile):
    
    def tree_to_dict(tree):
        d = {}
        for index, item in enumerate(tree):
            if item.tag == 'key':
                if tree[index + 1].tag == 'string':
                    d[item.text] = tree[index + 1].text
                elif tree[index + 1].tag == 'true':
                    d[item.text] = True
                elif tree[index + 1].tag == 'false':
                    d[item.text] = False
                elif tree[index + 1].tag == 'dict':
                    d[item.text] = tree_to_dict(tree[index + 1])
        return d
    
    def frames_from_data(filename, format):
    
        if format == 'plist':
            root = ElementTree.fromstring(open(data_filename, 'r').read())
            plist_dict = tree_to_dict(root[0])
            to_list = lambda x: x.replace('{', '').replace('}', '').split(',')
            frames = plist_dict['frames'].items()
            for k, v in frames:
                frame = v
                rectlist = to_list(frame['frame'])
                width = int(rectlist[3] if frame['rotated'] else rectlist[2])
                height = int(rectlist[2] if frame['rotated'] else rectlist[3])
                frame['box'] = (
                    int(rectlist[0]),
                    int(rectlist[1]),
                    int(rectlist[0]) + width,
                    int(rectlist[1]) + height
                )
                real_rectlist = to_list(frame['sourceSize'])
                real_width = int(real_rectlist[1] if frame['rotated'] else real_rectlist[0])
                real_height = int(real_rectlist[0] if frame['rotated'] else real_rectlist[1])
                real_sizelist = [real_width, real_height]
                frame['real_sizelist'] = real_sizelist
                offsetlist = to_list(frame['offset'])
                offset_x = int(offsetlist[1] if frame['rotated'] else offsetlist[0])
                offset_y = int(offsetlist[0] if frame['rotated'] else offsetlist[1])
                frame['result_box'] = (
                    int((real_sizelist[0] - width) / 2 + offset_x),
                    int((real_sizelist[1] - height) / 2 + offset_y),
                    int((real_sizelist[0] + width) / 2 + offset_x),
                    int((real_sizelist[1] + height) / 2 + offset_y)
                )
            return frames
        
        elif format == 'json':
            json_data = open(data_filename)
            data = json.load(json_data)
            frames = {}
            for f in data['frames']:
                x = int(f["frame"]["x"])
                y = int(f["frame"]["y"])
                w = int(f["frame"]["h"] if f['rotated'] else f["frame"]["w"])
                h = int(f["frame"]["w"] if f['rotated'] else f["frame"]["h"])
                real_w = int(f["sourceSize"]["h"] if f['rotated'] else f["sourceSize"]["w"])
                real_h = int(f["sourceSize"]["w"] if f['rotated'] else f["sourceSize"]["h"])
                d = {
                    'box': (
                        x,
                        y,
                        x + w,
                        y + h
                    ),
                    'real_sizelist': [
                        real_w,
                        real_h
                    ],
                    'result_box': (
                        int((real_w - w) / 2),
                        int((real_h - h) / 2),
                        int((real_w + w) / 2),
                        int((real_h + h) / 2)
                    ),
                    'rotated': f['rotated']
                }
                frames[f["filename"]] = d
            json_data.close()
            return frames.items()
        
        elif format == 'xml':
            data = ElementTree.parse(data_filename).getroot()
            frames = {}
            for f in data:
                x = int(f.get('x'))
                y = int(f.get('y'))
           
                if 'rotated' not in f.attrib:
                    rotated = False
                else:
                    rotated = True
                try:
                    w = int(f.get('w'))
                    h = int(f.get('h'))
                except:
                    w = int(f.get('width'))
                    h = int(f.get('height'))

                if 'frameHeight' in f.attrib:
                    real_w = int(f.get('frameHeight') if rotated else f.get('frameWidth'))
                    real_h = int(f.get('frameWidth') if rotated else f.get('frameHeight'))
                else:
                    real_w = w;
                    real_h = h;
                d = {
                    'box': (
                        x,
                        y,
                        x + w,
                        y + h
                    ),
                    'real_sizelist': [
                        real_w,
                        real_h
                    ],
                    'result_box': (
                        int((real_w - w) / 2),
                        int((real_h - h) / 2),
                        int((real_w + w) / 2),
                        int((real_h + h) / 2)
                    ),
                    'rotated': rotated
                }
                try:
                    frames[f.get('n')] = d
                except:
                    frames[f.get('name')] = d
                    
            return frames.items()
        
        elif format == 'cocos':
            pl = plistlib.readPlist(data_filename)
            data = pl['frames'].items()
            frames = {}
            for k, f in data:
                x = int(f["x"])
                y = int(f["y"])
                w = int(f["width"])
                h = int(f["height"])
                real_w = int(f["originalWidth"])
                real_h = int(f["originalHeight"])
                d = {
                    'box': (
                        x,
                        y,
                        x + w,
                        y + h
                    ),
                    'real_sizelist': [
                        real_w,
                        real_h
                    ],
                    'result_box': (
                        int((real_w - w) / 2),
                        int((real_h - h) / 2),
                        int((real_w + w) / 2),
                        int((real_h + h) / 2)
                    ),
                    'rotated': False
                }
                frames[k] = d
            return frames.items()
            
    def gen_png_from_data(filename, format):
        big_image = Image.open(filename)
        frames = frames_from_data(filename, format)
        total_frames = len(frames)
        x = 1
        
        for k, v in frames:
            frame = v
            box = frame['box']
            rect_on_big = big_image.crop(box)
            real_sizelist = frame['real_sizelist']
            result_image = Image.new('RGBA', real_sizelist, (0, 0, 0, 0))
            result_box = frame['result_box']
            result_image.paste(rect_on_big, result_box, mask=0)
            if frame['rotated']:
                result_image = result_image.rotate(90)
            
            outfile = os.path.join(dest, k.replace(".png","")[:-4]+".png")
            if not os.path.isdir(dest):
                os.makedirs(dest)
                
            log = f"| {k} generated |"
            loglabel.config(width=90, text=log, fg="#6D76CD", font=("Aharoni",10))
            result_image.save(outfile)
            root.update_idletasks()
            my_progress['value']=int((x/total_frames)*100)
            x+=1
            
    filename = imagefile
    data_filename = datafile
    
    if extension == '.plist':
        format = 'plist'
    elif extension == '.json':
        format = 'json'
    elif extension == '.xml':
        format = 'xml'
    elif extension == '.cocos':
        format = 'cocos'
    else:
        None
        
    gen_png_from_data(filename, format)
            
def Extract():
    global dest
    def convert():     
        my_progress.place(relx=0.5,rely=0.8,anchor='center')
        my_progress["value"]=0
        Wait.place(relx=0.5,rely=0.85,anchor='center')
        Wait.config(text="EXTRACTING...", fg="#6D76CD",bg='#FFFFFF', font=("Aharoni",15))
        root.update_idletasks()
        loglabel.place(relx=0.5,rely=0.9,anchor='center')
        
        try:
            ExtractSprite(file, file2)
            loglabel.place_forget()
            time.sleep(1)
            Wait.config(text="DONE! 100%", fg="#6D76CD",bg='#FFFFFF', font=("Aharoni",15))
            messagebox.showinfo("DONE!", "Images Extracted Successfuly! \nPlease check the folder: "+dest)

        except Exception as errors:
            loglabel.place_forget()
            Wait.config(text="", fg="#6D76CD",bg='#FFFFFF', font=("Aharoni",15))
            messagebox.showerror("OOPS!", f"Something went wrong! \nLogs: {errors}")
        
        my_progress.stop()
        my_progress.place_forget()
        Wait.place_forget()
        
    if file and file2:
        askfolder = tkinter.filedialog.askdirectory()
        if askfolder:
            dest = os.path.join(askfolder, os.path.splitext(os.path.basename(file2))[0])
        else:
            return
        btn['state']=DISABLED
        btn['cursor']='watch'
        s=1
        while os.path.exists(dest):
            dest = os.path.join(askfolder, os.path.splitext(os.path.basename(file2))[0]+str(s))
            s+=1
        convert()     
        btn['state']=NORMAL
        btn['cursor']=''
    else:
        messagebox.showwarning("OOPS", "Please import the files!")
    
def callback(url):
    webbrowser.open_new_tab(url)
    
def info():
    messagebox.showinfo("Help",
    "This program can unpack sprite sheet to separate image files \n\nHow to use:"
    "\n➤ You have to first input the sprite image file and the main data file (like a '.plist' file) in their respective sections."
    "\n➤ Then click on the 'EXTRACT' button and the export location"
    "\n\nDeveloper: Akash Bora (Akascape)\nIf you have any issue then contact me on Github.")
    
root = Tk()
root.title("Sprite Extracter On-The-Go")
root.resizable(width=False, height=False)
root.geometry("800x500")
root.configure(bg='#FFFFFF')

path = resource_path("programicon.ico")
root.wm_iconbitmap(path)
root.columnconfigure(0,weight=1)

file = None
file2 = None

path0 = resource_path("HeadLabel.png")
HeadLabelIMG = PhotoImage(file=path0)
headlabel = Label(image=HeadLabelIMG,borderwidth=0, highlightthickness=0, padx=0,pady=0)
headlabel.grid(row=0)

infobtn = Button(root, width=2,bg="#FFFFFF",fg="black", text="ⓘ",relief="sunken",cursor='hand2',
                 highlightthickness=0,borderwidth=0,padx=0,pady=0,command=info)
infobtn.grid(row=0, sticky="ne", pady=10, padx=10)

locationlabel = Label(root,text="IMPORT THE SPRITE IMAGE",fg="#6D76CD",bg='#FFFFFF', font=("Aharoni",15))
locationlabel.grid()

saveImg = Button(root, width=90,bg="#82CC6C",fg="white",highlightthickness=1,borderwidth=0.2,text="Open",
                 relief="groove", font=("Aharoni",10), command=openfile)
saveImg.grid()

locationlabel2 = Label(root,text="IMPORT THE DATA FILE",fg="#6D76CD",bg='#FFFFFF', font=("Aharoni",15))
locationlabel2.grid()

savePlist  = Button(root, width=90,bg="#82CC6C",highlightthickness=1,borderwidth=0.2,fg="white",
                    text="Open", font=("Aharoni",10),relief="groove", command=openfile2)
savePlist.grid()

path2 = resource_path("Extractbtn.png")
Icon = PhotoImage(file=path2)

btn = Button(image=Icon,width=204,borderwidth=0, bg='#FFFFFF', highlightthickness=2,padx=0,pady=0, command=Extract)
btn.grid(pady=10)

my_progress = ttk.Progressbar(root, orient=HORIZONTAL, length=300, mode='determinate')

Wait = Label(root,text="EXTRACTING...",fg="#6D76CD",bg='#FFFFFF', font=("Aharoni",15))
loglabel = Label(root, text='',fg="#6D76CD",bg='#FFFFFF',font=("Aharoni",15))

dev = Label(root, text='Developed by Akascape | For more info, visit:',bg='#FFFFFF',fg="#6D76CD", font=("Impact",10))
dev.place(x=5,y=480)
link = Label(root, text="https://github.com/Akascape/Sprite-Extracter-On-The-Go",font=('Impact',10),bg='#FFFFFF',fg="#6D76CD", cursor="hand2")
link.place(x=245,y=480)
link.bind("<Button-1>", lambda e: callback("https://github.com/Akascape/Sprite-Extracter-On-The-Go"))

root.mainloop()
