import os
from tkinter import *
from tkinter import Tk, Button, Label, PhotoImage, ttk, messagebox, filedialog
import tkinter
import shutil
import time
import sys
import json
import plistlib
from xml.etree import ElementTree
import webbrowser
import pkg_resources
import subprocess
required = {'pillow'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed
missingset=[*missing,]
if missing:
    res=messagebox.askquestion("Module Error","Some modules are not installed, do you want to download and install them?")
    if res=="yes":
        for x in range(len(missingset)):
            y=missingset[x]
            os.system('python -m pip install '+y)
        sys.exit()
    elif res=="no":
        print("Error: Required modules not available! \nWithout the modules you can't use this program. Please install them first!")
        sys.exit()
else:
    from PIL import Image 
def resource_path0(relative_path):
    base_path = getattr(
        sys,
        '_MEIPASS',
        os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
def openfile():
    global file, Common1, path1
    file=tkinter.filedialog.askopenfilename(filetypes =[('PNG', '*.png'),('All Files', '*.*')])
    if(len(file)>=1):
        LocationError.config(text=file, fg="#6D76CD", font=("Aharoni",15))
        saveImg['text']='Open Again'
        saveImg['bg']='#D0CECE'
        Common1=(os.path.basename(file).split('.')[0])
        path1=os.path.dirname(file)
    else:
        LocationError.config(text="PLEASE CHOOSE THE SPRITE IMAGE",fg="#6D76CD", font=("Aharoni",15))
        saveImg['text']='Open'
        saveImg['bg']="#82CC6C"
def openfile2():
    global file2, Common2, path2, extension
    file2=tkinter.filedialog.askopenfilename(filetypes =[('PLIST', '*.plist'),('XML', '*.xml'),('JSON', '*.json'),('COCOS', '*.cocos'),('All Files', '*.*')])
    if(len(file2)>=1):
        LocationError2.config(text=file2, fg="#6D76CD", font=("Aharoni",15))
        savePlist['text']='Open Again'
        savePlist['bg']='#D0CECE'
        Common2=(os.path.basename(file2).split('.')[0])
        extension=os.path.splitext(file2)[1]
        path2=os.path.dirname(file2)
    else:
        LocationError2.config(text="PLEASE CHOOSE THE DATA FILE",fg="#6D76CD", font=("Aharoni",15))
        savePlist['text']='Open'
        savePlist['bg']="#82CC6C"
def plist(Argument):
    my_progress['value']=20
    root.update_idletasks()
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
            data_filename = filename + '.plist'
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
            data_filename = filename + '.json'
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
            data_filename = filename + '.xml'
            data = ElementTree.parse(data_filename).getroot()
            print(data.get("imagePath"))
            data2 = data.findall('SubTexture')
            frames = {}
            for f in data:
                print(f.get('name'))
                x = int(f.get('x'))
                y = int(f.get('y'))
           
                if 'rotated' not in f.attrib:
                    rotated = False
                else:
                    rotated = True

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
                frames[f.get('name')] = d
            return frames.items()
        elif format == 'cocos':
            data_filename = filename + ".plist"
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
        else:
            messagebox.showerror("OOPS","Wrong data format on parsing:")
    def gen_png_from_data(filename, format):
        big_image = Image.open(filename + ".png")
        frames = frames_from_data(filename, format)
        for k, v in frames:
            frame = v
            print (v);
            box = frame['box']
            rect_on_big = big_image.crop(box)
            real_sizelist = frame['real_sizelist']
            result_image = Image.new('RGBA', real_sizelist, (0, 0, 0, 0))
            result_box = frame['result_box']
            result_image.paste(rect_on_big, result_box, mask=0)
            if frame['rotated']:
                result_image = result_image.rotate(90)
            outfile = (filename + '/' + k).replace('gift_', '') + '.png'
            dirname = os.path.dirname(outfile)
            if not os.path.isdir(dirname):
                os.makedirs(dirname)
            log=(outfile, "generated")
            print(outfile, "generated")
            loglabel.config(width=90,text=log, fg="#6D76CD", font=("Aharoni",10))
            print (result_image.format, result_image.size, result_image.mode)
            result_image.save(outfile)
            my_progress['value']+=0.1
            root.update_idletasks()
    if __name__ == '__main__':
        filename=Argument
        format = 'plist'
        if extension == '.plist':
            pass
        elif extension == '.json':
            format='json'
        elif extension == '.xml':
            format='xml'
        elif extension == '.cocos':
            format='cocos'
        else:
            messagebox.showerror("OOPS","Wrong data format passed!")
            my_progress['value']=100
            root.update_idletasks()
            my_progress.stop()
            my_progress.place_forget()
            loglabel.place_forget()
            Wait.place_forget()
            os.remove(copy1)
            os.remove(copy2)
        data_filename = filename + extension
        png_filename = filename + '.png'
        if os.path.exists(data_filename) and os.path.exists(png_filename):
            gen_png_from_data(filename, format)
        else:
            messagebox.showerror("OOPS", "Failed to extract! Maybe due to wrong formats.")
            my_progress['value']=100
            root.update_idletasks()
            my_progress.stop()
            my_progress.place_forget()
            loglabel.place_forget()
            Wait.place_forget()
            os.remove(copy1)
            os.remove(copy2)            
def Extract():
        def Convert():
            global copy1, copy2
            source1=file2
            source2=file
            Argument=Common2
            my_progress.place(relx=0.5,rely=0.8,anchor='center')
            my_progress['value']=5
            copy1=shutil.copy(source1,destination1)
            copy2=shutil.copy(source2,destination1)
            Wait.place(relx=0.5,rely=0.85,anchor='center')
            Wait.config(text="EXTRACTING...", fg="#6D76CD",bg='#FFFFFF', font=("Aharoni",15))
            root.update_idletasks()
            loglabel.place(relx=0.5,rely=0.9,anchor='center')
            plist(Argument)
            Wait.config(text="MOVING FILES...", fg="#6D76CD",bg='#FFFFFF', font=("Aharoni",15))
            my_progress['value']=80
            root.update_idletasks()
            if os.path.isdir(destexist):
                shutil.rmtree(destexist)
            else:
                pass
            shutil.move(extfolder,dest)
            os.remove(copy1)
            os.remove(copy2)
            my_progress['value']=100
            root.update_idletasks()
            time.sleep(1)
            Wait.config(text="DONE! 100%", fg="#6D76CD",bg='#FFFFFF', font=("Aharoni",15))
            messagebox.showinfo("DONE!", "Images Extracted Successfuly! \nPlease check the folder.")
            my_progress.stop()
            my_progress.place_forget()
            loglabel.place_forget()
            Wait.place_forget()
        try:
            if (len(file)>=1) and (len(file2)>=1):
                if Common2!=Common1:
                    messagebox.showwarning("OOPS", "The base name of both the file must be same!")
                elif path1!=path2:
                    messagebox.showwarning("OOPS", "Both the image file and data file \nmust be in the same location!")
                else:
                    btn['state']=DISABLED
                    btn['cursor']='watch'
                    destination1=os.getcwd()
                    try:
                        extfolder=destination1+"/"+Common1
                        dest=path1+"/"
                        destexist=path1+"/"+Common1
                        if os.path.isdir(destexist):
                            res=messagebox.askquestion("Warning!","Do you want to replace the folder with the new one? \n(Process not reversible)")
                            if res=='yes':
                                Convert()
                            elif res=='no':
                                Wait.place(relx=0.5,rely=0.85,anchor='center')
                                Wait.config(text="OPERATION NOT PERFORMED!", fg="#6D76CD",bg='#FFFFFF', font=("Aharoni",15))
                                messagebox.showinfo("DONE", "No Files Extracted!")
                                Wait.place_forget()
                        else:
                            Convert()
                    except:
                        messagebox.showerror("Something Went Wrong!", "Please check the files and retry!")     
                    btn['state']=NORMAL
                    btn['cursor']=''
            else:
                messagebox.showwarning("OOPS", "Please choose the files first!")
        except:
            messagebox.showwarning("OOPS", "Please choose the files and retry!")
def callback(url):
    webbrowser.open_new_tab("https://github.com/Akascape/Sprite-Extracter-On-The-Go")
def info():
    messagebox.showinfo("Help",
    "This program can unpack sprite sheet images to separate image files \nNOTE:"
    "\n➤You have to first input the sprite image file and the main data file(example-'.plist' files) in their respective sections."
    "\n➤Then just click on the 'Extract' Button and it will extract the images in the same location in a folder where the main files are."
    "\n➤Make sure the base name of both the files are same and they must be in the same directory(any)."
    "\n➤Please do not paste any files in the program's folder or else it might get deleted (Only use this folder to open the program)."
    "\n➤If you extract the same files in the same location again, then the new extracted folder will replace the old folder."
    "\n\nDeveloper: Akash Bora (a.k.a. Akascape)\nIf you have any issue then contact me on Github.")
root=Tk()
root.title("Sprite Extracter On-The-Go")
root.resizable(width=False, height=False)
root.geometry("800x500")
root.configure(bg='#FFFFFF')
path=resource_path0("programicon.ico")
root.wm_iconbitmap(path)
root.columnconfigure(0,weight=1)
path0=resource_path0("HeadLabel.png")
HeadLabelIMG=PhotoImage(file=path0)
headlabel=Label(image=HeadLabelIMG,borderwidth=0, highlightthickness=0, padx=0,pady=0)
headlabel.grid()
LocationError=Label(root,text="PLEASE CHOOSE THE SPRITE IMAGE",fg="#6D76CD",bg='#FFFFFF', font=("Aharoni",15))
LocationError.grid()
saveImg=Button(root, width=90,bg="#82CC6C",fg="white",highlightthickness=1,borderwidth=0.2,text="Open",relief="groove", command=openfile)
saveImg.grid()
LocationError2=Label(root,text="PLEASE CHOOSE THE DATA FILE",fg="#6D76CD",bg='#FFFFFF', font=("Aharoni",15))
LocationError2.grid()
savePlist=Button(root, width=90,bg="#82CC6C",highlightthickness=1,borderwidth=0.2,fg="white", text="Open",relief="groove", command=openfile2)
savePlist.grid()
path2=resource_path0("Extractbtn.png")
Icon=PhotoImage(file=path2)
btn=Button(image=Icon,width=204,borderwidth=0,bg='#FFFFFF',highlightthickness=2,padx=0,pady=0,command=Extract)
btn.place(relx=0.5,rely=0.65,anchor='center')
infobtn= Button(root, width=2,bg="#FFFFFF",fg="black", text="ⓘ",font=(10),relief="sunken",cursor='hand2', highlightthickness=0,borderwidth=0,padx=0,pady=0,command=info)
infobtn.place(x=765,y=9)
my_progress=ttk.Progressbar(root, orient=HORIZONTAL, length=300, mode='determinate')
Wait=Label(root,text="EXTRACTING...",fg="#6D76CD",bg='#FFFFFF', font=("Aharoni",15))
loglabel=Label(root, text='',fg="#6D76CD",bg='#FFFFFF',font=("Aharoni",15))
dev=Label(root, text='Developed by Akascape | For more info, visit:',bg='#FFFFFF',fg="#6D76CD", font=("Impact",10))
dev.place(x=5,y=480)
link=Label(root, text="https://github.com/Akascape/Sprite-Extracter-On-The-Go",font=('Impact',10),bg='#FFFFFF',fg="#6D76CD", cursor="hand2")
link.place(x=245,y=480)
link.bind("<Button-1>", lambda e:
callback("https://github.com/Akascape/Sprite-Extracter-On-The-Go"))
root.mainloop()
#DEVELOPER: AKASH BORA (a.k.a Akascape)
#Version=1.0
