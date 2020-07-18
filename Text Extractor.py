import tkinter as tk
import cv2
import numpy as np
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def open_img():
        root.filename =  tk.filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("png files","*.png")))
        textBox2 = tk.Text(height =3, width =80,relief="sunken",bd=5,font=("Helvetica", 15))
        textBox2.insert('end',root.filename)
        textBox2.configure(state='disabled')
        textBox2.place(x=340,y=115)
class OCR(object):
    def __init__(self, master, **kwargs):
        self.master=master
        pad=10
        self._geom='600x600+0+0'
        master.geometry("{0}x{1}+0+0".format(master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>',self.toggle_geom)
        root.resizable(width = True, height = True) 
        root.configure(bg="#fbff12")
        textBox1= tk.Text(height =5, width =80,relief="sunken",bd=5,font=("Helvetica", 15))
        textBox1.configure(state='disabled')
        textBox1.place(x=340,y=300)
        global var
        var=tk.IntVar()
        l1=tk.Label(text="Image Background",font=("Helvetica", 15,"bold"),activeforeground="white",fg="white",bg="violet",padx=10,bd=5,relief="raised").place(x=840,y=500)
        r1=tk.Radiobutton(root,text="Light",activebackground="#fbff12",background="#fbff12",bd=5,font=("Helvetica", 15),variable=var,value=1).place(x=1050,y=500)
        r2=tk.Radiobutton(root,text="Dark",activebackground="#fbff12",background="#fbff12",bd=5,font=("Helvetica",15),variable=var,value=2).place(x=1150,y=500)

        menubutton = tk.Menubutton(text="Select language",indicatoron=True, fg="white",bg="#ed91af",
                                   activeforeground="#ffffff",activebackground="violet",width=15,
                                   height=1,font=("verdana",12,'bold'),bd=5, relief="raised")
        menu = tk.Menu(menubutton, tearoff=False)
        menubutton.configure(menu=menu)
        menubutton.place(x=135,y=500)
        self.choices = {}
        for choice in ("English","Sanskrit","Hindi","Telugu","Bengali","French","German","Japanese","Kannada","Malayalam","Tamil","Urdu","Arabic"):
            self.choices[choice] = tk.IntVar(value=0)
            menu.add_checkbutton(label=choice, variable=self.choices[choice], 
                                 onvalue=1, offvalue=0)
        btn1 = tk.Button(root, text="Select Image", bd=5,activeforeground="#ffffff",activebackground="violet",
                         fg="white",bg="#ed91af",width=12, height=1,font=("verdana",12,'bold'), command=open_img).place(x=140,y=128)
        btn2 = tk.Button(root, text="Get Text", bd=5,activeforeground="#ffffff",activebackground="violet",
                         fg="white",bg="#ed91af",width=12, height=1,font=("verdana",12,'bold'), command=lambda:self.get_Text(textBox1)).place(x=140,y=328)
    
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom
    def get_Text(self,textbox1):
        textbox1.configure(state='normal')
        textbox1.delete("1.0","end")
        choice=var.get()
        if choice==0:
            choice=1
        k=list(self.choices.keys())
        c=list(self.choices.values())
        l=[]
        s=""
        for i in range(len(k)):
            if c[i].get()==1:
                k2=k[i]
                if k2=="English":
                    l.append("eng") 
                elif k2=="Sanskrit":
                    l.append("san")  
                elif k2=="Hindi":
                    l.append("hin")
                elif k2=="Telugu":
                    l.append("tel")
                elif k2=="Bengali":
                    l.append("ben")
                elif k2=="French":
                    l.append("fra")
                elif k2=="German":
                    l.append("deu")
                elif k2=="Japanese":
                    l.append("jpn")
                elif k2=="Kannada":
                    l.append("kan")
                elif k2=="Malayalam":
                    l.append("mal")
                elif k2=="Tamil":
                    l.append("tam")
                elif k2=="Urdu":
                    l.append("urd")
                elif k2=="Arabic":
                    l.append("ara")
        if l!=[]:
            s="+".join(l)
            s="-l "+s
        im = cv2.imread(root.filename)
        gray= cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        if choice==1:
             thresh = cv2.threshold(gray, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
             coords = np.column_stack(np.where(thresh > 0))
             angle = cv2.minAreaRect(coords)[-1]
             if angle < -45:
                 angle = -(90 + angle)
             else:
                 angle = -angle
                 (h, w) = gray.shape[:2]
                 center = (w // 2, h // 2)
                 M = cv2.getRotationMatrix2D(center, angle, 1.0)
                 gray = cv2.warpAffine(gray, M, (w, h),flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)    
                 (thresh, im) = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        else: 
             thresh = cv2.threshold(gray, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
             coords = np.column_stack(np.where(thresh > 0))
             angle = cv2.minAreaRect(coords)[-1]
             if angle < -45:
                 angle = -(90 + angle)
             else:
                angle = -angle
             (h, w) = gray.shape[:2]
             center = (w // 2, h // 2)
             M = cv2.getRotationMatrix2D(center, angle, 1.0)
             gray = cv2.warpAffine(gray, M, (w, h),flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
             (thresh, im) = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
        config = (s+" --oem 1 --psm 3")
        text = pytesseract.image_to_string(im, config=config)
        text = text.split('\n')
        if "" in text:
             text.remove("")
        s="\n".join(text)
        textbox1.insert("end",s)
        textbox1.configure(state='disabled')
root=tk.Tk()
root.title("Text Extractor") 
app=OCR(root)
root.mainloop()

