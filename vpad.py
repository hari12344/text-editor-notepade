import tkinter as tk
from tkinter import ttk
from tkinter import font,colorchooser
import os
from tkinter import filedialog,messagebox

win = tk.Tk()
win.geometry("1200x800")
win.title("Notepade")
# ==================================main menu====================================
main_menu = tk.Menu()
# image
win.wm_iconbitmap("icon.ico")
new_icon = tk.PhotoImage(file="icons2/new.png")
open_icon = tk.PhotoImage(file="icons2/open.png")
save_icon = tk.PhotoImage(file="icons2/save.png")
save_as_icon = tk.PhotoImage(file="icons2/save_as.png")
exit_icon = tk.PhotoImage(file="icons2/exit.png")
file =tk.Menu(main_menu,tearoff=0)


# new functionality
url = ''
def new_file(event=None):
        url=''
        text_editor.delete(1.0, tk.END)
        
file.add_command(label="New", image=new_icon, compound=tk.LEFT ,accelerator="ctrl+N", command=new_file)
# open file functionality
def open_file(event=None):
        global url
        url = filedialog.askopenfilename(initialdir=os.getcwd, title="Select File", filetypes=(('text file','*.txt'),('all file','*.*')))
        try:
                with open(url,'r') as fr:
                        text_editor.delete(1.0, tk.END)
                        text_editor.insert(1.0, fr.read())
        except FileNotFoundError:
                return
        except:
                return
        win.title(os.path.basename(url))

file.add_command(label="Open", image=open_icon, compound=tk.LEFT ,accelerator="ctrl+O",command=open_file)
file.add_separator()
# save file functionality
def save_file(event=None):
        global url
        try:
                if url:
                        content = str(text_editor.get(1.0, tk.END))
                        with open(url, 'w', encoding='utf-8') as fw:
                                fw.write(content)
                else:
                        url = filedialog.asksaveasfile(mode='w',defaultextension=".txt",filetypes=(('Text file','*.txt'),('All File','*.*')))
                        content2 = text_editor.get(1.0, tk.END)
                        url.write(content2)
                        url.close()
        except:
                return
file.add_command(label="Save", image=save_icon, compound=tk.LEFT ,accelerator="ctrl+S",command=save_file)
# save as file functionlity
def saveAs_file(event=None):
        try:
                url = filedialog.asksaveasfile(mode="w",defaultextension=".txt",filetypes=(('Text file',"*.txt"),("All File",'*.*')))
                content = text_editor.get(1.0,tk.END)
                url.write(content)
                url.close()
        except:
                return
file.add_command(label="Save As", image=save_as_icon, compound=tk.LEFT ,accelerator="ctrl+alt+s",command=saveAs_file)
file.add_separator()
# exit function 
def exit_func(event=None):
        global url,text_changed
        try:
                
                if text_changed:
                        
                        mbox = messagebox.askyesnocancel("Warning","Do you want to save this file")
                        if mbox is True:
                                if url:
                                        content = str(text_editor.get(1.0,tk.END))
                                        with open(url,'w',encoding='utf-8') as fw:
                                                fw.write(content)
                                                fw.close()
                                        win.destroy()
                                else:
                                        url = filedialog.asksaveasfile(mode="w",defaultextension=".txt",filetypes=(('Text file',"*.txt"),("All File",'*.*')))
                                        content2 = str(text_editor.get(1.0,tk.END))
                                        url.write(content2)
                                        url.close()
                                        win.destroy()
                        elif mbox is False:
                                win.destroy()
                else:
                        win.destroy()
                        
        except:
                return
file.add_command(label="Exit", image=exit_icon, compound=tk.LEFT ,accelerator="ctrl+Q",command=exit_func)

# edit icon
copy_icon = tk.PhotoImage(file="icons2/copy.png")
paste_icon = tk.PhotoImage(file="icons2/paste.png")
cut_icon = tk.PhotoImage(file="icons2/cut.png")
find_icon = tk.PhotoImage(file="icons2/find.png")
clear_all_icon = tk.PhotoImage(file="icons2/clear_all.png")
edit =tk.Menu(main_menu,tearoff=0)
edit.add_command(label="Copy", image=copy_icon, compound=tk.LEFT, accelerator="ctrl+C",command=lambda:text_editor.event_generate('<Control c>'))
edit.add_command(label="Paste", image=paste_icon, compound=tk.LEFT, accelerator="ctrl+V",command=lambda:text_editor.event_generate('<Control v>'))
edit.add_separator()
edit.add_command(label="Cut", image=cut_icon, compound=tk.LEFT, accelerator="ctrl+X",command=lambda:text_editor.event_generate('<Control x>'))
edit.add_command(label="Clear All", image=clear_all_icon, compound=tk.LEFT, accelerator="ctrl+alt+X",command=lambda:text_editor.delete(1.0,tk.END))
edit.add_separator()
# find function
def find_func(event=None):
        def find():
                word = find_ent.get()
                text_editor.tag_remove('match','1.0',tk.END)
                matches = 0
                if word:
                        start_pos='1.0'
                        while True:
                                start_pos = text_editor.search(word,start_pos,stopindex=tk.END)
                                if not start_pos:
                                        break
                                end_pos=f'{start_pos}+{len(word)}c'
                                text_editor.tag_add('match',start_pos,end_pos)
                                matches+=1
                                start_pos=end_pos
                                text_editor.tag_config('match',foreground="red",background="yellow")
                                        
        def replace():
                word = find_ent.get()
                replace_txt = replace_ent.get()
                content = str(text_editor.get(1.0, tk.END))
                new_content = content.replace(word,replace_txt)
                text_editor.delete(1.0,tk.END)
                text_editor.insert(1.0,new_content)
                
        try:
                frame_dialog = tk.Toplevel()
                frame_dialog.geometry('300x200+750+250')
                frame_dialog.maxsize(300,250)
                frame_dialog.title("Find/Replace")
                myfm=tk.LabelFrame(frame_dialog,text="Find/Replace")
                myfm.pack(fill=tk.BOTH,pady=10)
                myfm.propagate(0)
                
                # lbl
                find_lbl = ttk.Label(myfm,text="Find")
                replace_lbl = ttk.Label(myfm,text="Replace")
                find_lbl.grid(row=0,column=0,padx=4,pady=10)
                replace_lbl.grid(row=1,column=0,padx=4,pady=3)
                # entry box
                find_ent = ttk.Entry(myfm,width=20)
                replace_ent = ttk.Entry(myfm,width=20)
                find_ent.grid(row=0,column=1)
                replace_ent.grid(row=1,column=1)
                
                # button
                find_btn = ttk.Button(myfm, text="Find",command=find)
                replace_btn = ttk.Button(myfm, text="Replace",command=replace)
                find_btn.grid(row=2,column=1,padx=4,pady=5)
                replace_btn.grid(row=2,column=2,padx=4,pady=5)
                
                frame_dialog.mainloop()
        except:
                return
        
edit.add_command(label="Find", image=find_icon, compound=tk.LEFT, accelerator="ctrl+f",command=find_func)
# icon for view 

tool_bar_icon = tk.PhotoImage(file="icons2/tool_bar.png")
status_bar_icon = tk.PhotoImage(file="icons2/status_bar.png")
view =tk.Menu(main_menu,tearoff=0)
# shoe status and tool bar
show_tool_bar = tk.BooleanVar()
show_status_bar =tk.BooleanVar()
show_tool_bar = True
show_status_bar =True
def hide_tool():
        global show_tool_bar
        if show_tool_bar:
                tool_bar_lable.pack_forget()
                show_tool_bar=False
        else:
                text_editor.pack_forget()
                status_bar.pack_forget()
                tool_bar_lable.pack(side=tk.TOP,fill=tk.X)
                text_editor.pack(fill=tk.BOTH,expand=True)
                status_bar.pack(tk.BOTTOM, fill=tk.X)
                show_tool_bar=True
def hide_status():
        global show_status_bar
        if show_status_bar:
                status_bar.pack_forget()
                show_status_bar=False
        else:
                status_bar.pack(side=tk.BOTTOM,fill=tk.X)
                show_status_bar=True
                
        
view.add_checkbutton(label="Tool Bar",onvalue=True,offvalue=False,variable=show_tool_bar, image=tool_bar_icon, compound=tk.LEFT,command=hide_tool)
view.add_checkbutton(label="Status Bar",onvalue=True,offvalue=False,variable=show_status_bar, image=status_bar_icon, compound=tk.LEFT,command=hide_status)
view.add_separator()

# theme icons
light_default_icon = tk.PhotoImage(file="icons2/light_default.png")
light_plus_icon = tk.PhotoImage(file="icons2/light_plus.png")
night_blue_icon = tk.PhotoImage(file="icons2/night_blue.png")
monokai_icon = tk.PhotoImage(file="icons2/monokai.png")
dark_icon = tk.PhotoImage(file="icons2/dark.png")
red_icon = tk.PhotoImage(file="icons2/red.png")
color_theme =tk.Menu(main_menu,tearoff=0)

# backgroung color

def bg_theme(bg):
        text_editor.configure(background=bg)
        

color_theme.add_radiobutton(image=light_default_icon, label="Light Default",compound=tk.LEFT,command=lambda:bg_theme('#C1CDCD'))
color_theme.add_radiobutton(image=light_plus_icon, label="night Plus", compound=tk.LEFT,command=lambda:bg_theme('#838B8B'))
color_theme.add_radiobutton(image=night_blue_icon, label="Night Blue", compound=tk.LEFT,command=lambda:bg_theme('#0000CD'))
color_theme.add_radiobutton(image=monokai_icon, label="Monokai", compound=tk.LEFT,command=lambda:bg_theme('#EED5B7'))
color_theme.add_radiobutton(image=dark_icon, label="Dark", compound=tk.LEFT,command=lambda:bg_theme('#1A1A1A'))
color_theme.add_radiobutton(image=red_icon, label="Red", compound=tk.LEFT,command=lambda:bg_theme('#EE0000'))

# cascade
main_menu.add_cascade(label="File", menu=file)
main_menu.add_cascade(label="Edit", menu=edit)
main_menu.add_cascade(label="view", menu=view)
main_menu.add_cascade(label="Color Theme", menu=color_theme)
# ----------------------------------End Menu-------------------------------------

# ===================================tool bar===================================

# font style
tool_bar_lable = ttk.Label(win)
tool_bar_lable.pack(side=tk.TOP, fill=tk.X)

font_tuple=tk.font.families()
font_type = tk.StringVar()
font_box=ttk.Combobox(tool_bar_lable,width=30, textvariable=font_type, state="readonly",)
font_box.grid(row=0,column=0,padx=4)
font_box['values']=font_tuple
font_box.current(font_tuple.index("Arial"))
                 
        # font size


font_size=tk.IntVar()        
font_size_box=ttk.Combobox(tool_bar_lable,width=12, state='readonly',textvariable=font_size)
font_size_box.grid(row=0,column=1,padx=4)
font_size_box['values']=tuple(range(8,80,2))
font_size_box.current(font_size_box.index(12))

bold_icon = tk.PhotoImage(file="icons2/bold.png")
italic_icon = tk.PhotoImage(file="icons2/italic.png")
underline_icon=tk.PhotoImage(file="icons2/underline.png")

bold_button=ttk.Button(tool_bar_lable,image=bold_icon)
bold_button.grid(row=0,column=2,padx=3)

italic_button=ttk.Button(tool_bar_lable,image=italic_icon)
italic_button.grid(row=0,column=3,padx=3)

underline_button = ttk.Button(tool_bar_lable,image=underline_icon)
underline_button.grid(row=0,column=4,padx=3)


left_align = tk.PhotoImage(file="icons2/align_left.png")
left_align_button = ttk.Button(tool_bar_lable,image=left_align) 
left_align_button.grid(row=0,column=5,padx=3)

right_align = tk.PhotoImage(file="icons2/align_right.png")
right_align_button = ttk.Button(tool_bar_lable,image=right_align)
right_align_button.grid(row=0,column=6,padx=3)

center_align = tk.PhotoImage(file="icons2/align_center.png")
center_align_button = ttk.Button(tool_bar_lable,image=center_align)
center_align_button.grid(row=0,column=7,padx=3)

color_choice_icon = tk.PhotoImage(file="icons2/font_color.png")
color_choice_button = ttk.Button(tool_bar_lable,image=color_choice_icon)
color_choice_button.grid(row=0,column=8,padx=3)

# -----------------------------------end tool bar-------------------------------
# ----------------------------------text Editor--------------------------------

text_editor = tk.Text(win)
text_editor.config(wrap="word",relief=tk.FLAT)
text_editor.focus()

scroll_bar=tk.Scrollbar(win)
scroll_bar.pack(side=tk.RIGHT,fill=tk.Y)

text_editor.pack(fill=tk.BOTH,expand=True)

scroll_bar.config(command=text_editor.yview)
text_editor.config(yscrollcommand=scroll_bar.set)

# ----------------------------text editor configration----------------------

current_font_style ="Arial"
current_font_size = 12
def change_fontstyle(event=None):
        
        global current_font_style
        current_font_style = font_type.get()
        text_editor.configure(font=(current_font_style,current_font_size))
def change_fontsize(event=None):
        global current_font_size
        current_font_size = font_size.get()
        text_editor.configure(font=(current_font_style,current_font_size))
        
        
font_box.bind("<<ComboboxSelected>>",change_fontstyle)
font_size_box.bind("<<ComboboxSelected>>",change_fontsize)



                

text_editor.configure(font=("Arial",12))

def bold():
        text_property=tk.font.Font(font=text_editor['font'])

        if text_property.actual()['weight']=='normal':
                text_editor.configure(font=(current_font_style,current_font_size,'bold'))
        else:
                text_editor.configure(font=(current_font_style,current_font_size,'normal'))
        
# italic function
def italic():
        text_property=tk.font.Font(font=text_editor['font'])
        
        
        
        if text_property.actual()['slant']=='roman':
                
                text_editor.configure(font=(current_font_style,current_font_size,'italic'))
        if text_property.actual()['slant']=='italic':
        
                text_editor.configure(font=(current_font_style,current_font_size,'roman'))

def underline():
        text_property=tk.font.Font(font=text_editor['font'])

        if text_property.actual()['underline'] == 0:
                
                text_editor.configure(font=(current_font_style,current_font_size,"underline"))
        else:
                text_editor.configure(font=(current_font_style,current_font_size,"normal"))
                
def font_color():
        color_var = colorchooser.askcolor()
        text_editor.configure(fg=color_var[1])
        

color_choice_button.configure(command=font_color)
italic_button.configure(command=italic)
bold_button.configure(command=bold)
underline_button.configure(command=underline)


def align_left():
        text_content = text_editor.get(1.0,'end')
        text_editor.tag_config('left',justify=tk.LEFT)
        text_editor.delete(1.0,tk.END)
        text_editor.insert(tk.INSERT, text_content, tk.LEFT)
        
def align_center():
        text_content = text_editor.get(1.0,'end')
        text_editor.tag_config('center',justify=tk.CENTER)
        text_editor.delete(1.0,tk.END)
        text_editor.insert(tk.INSERT, text_content, tk.CENTER)
def align_right():
        text_content = text_editor.get(1.0,'end')
        text_editor.tag_config('right',justify=tk.RIGHT)
        text_editor.delete(1.0,tk.END)
        text_editor.insert(tk.INSERT, text_content, tk.RIGHT)
center_align_button.configure(command=align_center)        
left_align_button.configure(command=align_left)
right_align_button.configure(command=align_right)
# color choser





# =============================================================================
# bold buttton

        
# ==================================End text Editor============================

# ===================================Status Bar=================================
status_bar = ttk.Label(win)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)
status_lable=ttk.Label(status_bar,text="status bar")
# status_lable.grid(row=0,column=40,padx=400)
status_lable.pack()
text_changed=False
def change_status(event=None):
        global text_changed
        if text_editor.edit_modified():
                text_changed=True
                words=len(text_editor.get(1.0, 'end-1c').split())
                char = len(text_editor.get(1.0,'end-1c'))
                status_lable['text']=f"character : {char} words : {words}"
                text_editor.edit_modified(False)
text_editor.bind('<<Modified>>', change_status)

# -----------------------------------End Status Bar-----------------------------
win.config(menu=main_menu)

# shortcut keys binding
win.bind('<Control-n>',new_file)
win.bind('<Control-o>',open_file)
win.bind('<Control-s>',save_file)
win.bind('<Control-Alt-s>',saveAs_file)
win.bind('<Control-q>',exit_func)
win.bind('<Control-f>',find_func)


win.mainloop()