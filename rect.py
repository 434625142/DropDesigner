#封装各类矩形的类
import wx
from PIL import Image,ImageFont,ImageDraw
from PIL import Image,ImageFont,ImageDraw
class rect():
    """docstring for ClassName"""
    def __init__(self, parent,pos1,pos2):
        self.parent = parent
        #这个矩形是否画周围八点和矩形框
        self.showpoint8mode=True
        self.reinitby2point(pos1,pos2)
    def get_mode(self):return 'None'
    def draw(self,dc):dc.DrawRectangle(self.pos1[0],self.pos1[1],self.pos2[0]-self.pos1[0],self.pos2[1]-self.pos1[1])
    def draw8(self,dc):
        if self.showpoint8mode==True:
            dc.SetBrush(wx.Brush("blue", wx.TRANSPARENT))
            dc.SetPen(wx.Pen('black', 1))
            self.draw(dc)
            dc.SetBrush(wx.Brush("blue"))
            dc.SetPen(wx.Pen('blue', 2))
            for i in self.pointlist:
                dc.DrawCircle(i[0],i[1],4)
    def IsInpoint(self,p1,p2):
    #p1是否在p2点内
        r=4
        if p2[0]-r<p1[0] and p2[0]+r>p1[0] and p2[1]-r<p1[1] and p2[1]+r>p1[1] : return True
        else : return False 
    def IsInpoint8(self,p):
    #是否在矩形的八个点周围
        if self.showpoint8mode==True:
            index=0
            for i in self.pointlist:
                if self.IsInpoint(self.win2pic(p),i) : return index
                index+=1
        return -1   
    #从window窗口的坐标转换为图片上的坐标
    def win2pic(self,pos):return (pos[0]-self.parent.BackImg.pos_x,pos[1]-self.parent.BackImg.pos_y)
    def pic2win(self,pos):return (pos[0]+self.parent.BackImg.pos_x,pos[1]+self.parent.BackImg.pos_y)
    #用保存的比例和传入的放缩倍数进行调整
    def reinitbyscale(self,size):
        self.pos1=self.scale_point1[0]*size[0],self.scale_point1[1]*size[1]        
        self.pos2=self.scale_point2[0]*size[0],self.scale_point2[1]*size[1]
        x1,y1=self.pos1
        x2,y2=self.pos2
        self.pointlist=[(x1,y1),(x2,y1),(x2,y2),(x1,y2),
        (x1+(x2-x1)/2,y1),(x2,y1+(y2-y1)/2),(x1+(x2-x1)/2,y2),(x1,y1+(y2-y1)/2)]
    #用矩形的两点对矩形进行调整
    def reinitby2point(self,pos1,pos2):
        x,y=self.parent.BackImg.get_times_size()
        x1,y1=pos1[0]-self.parent.BackImg.pos_x,pos1[1]-self.parent.BackImg.pos_y
        x2,y2=pos2[0]-self.parent.BackImg.pos_x,pos2[1]-self.parent.BackImg.pos_y
        self.pos1=(x1,y1)
        self.pos2=(x2,y2)
        #矩形的两点除以图片的尺寸的比例
        self.scale_point1=(self.pos1[0]/x,self.pos1[1]/y)
        self.scale_point2=(self.pos2[0]/x,self.pos2[1]/y)
        self.pointlist=[(x1,y1),(x2,y1),(x2,y2),(x1,y2),
        (x1+(x2-x1)/2,y1),(x2,y1+(y2-y1)/2),(x1+(x2-x1)/2,y2),(x1,y1+(y2-y1)/2)]
    def is_in_rect(self,pos):
        x,y=pos[0]-self.parent.BackImg.pos_x,pos[1]-self.parent.BackImg.pos_y
        x1,y1=self.pointlist[0]
        x2,y2=self.pointlist[2]
        if x>x1 and x<x2 and y>y1 and y<y2 and self.IsInpoint8(pos)<0:
            self.p_past1=(x1,y1)
            return True
        else: return False      
    def adjust(self,p_curry,mode):
        x,y=p_curry[0],p_curry[1]
        x1,y1=self.pointlist[0][0]+self.parent.BackImg.pos_x,self.pointlist[0][1]+self.parent.BackImg.pos_y
        x2,y2=self.pointlist[2][0]+self.parent.BackImg.pos_x,self.pointlist[2][1]+self.parent.BackImg.pos_y
        pos1,pos2=(x1,y1),(x2,y2)
        if mode==0:
            pos1=p_curry
        elif mode==1:
            pos1=(x1,y)
            pos2=(x,y2)
        elif mode==2:
            pos2=p_curry
        elif mode==3:
            pos1=(x,y1)
            pos2=(x2,y)
        elif mode==4:
            pos1=(x1,y)
        elif mode==5:
            pos2=(x,y2)
        elif mode==6:
            pos2=(x2,y)
        elif mode==7:
            pos1=(x,y1)
        self.reinitby2point(pos1,pos2)
    def move(self,p_curry,poslist):
        #拖动的x，y点的距离
        x_dist,y_dist=p_curry[0]-poslist[0][0],p_curry[1]-poslist[0][1]
        pos1=(poslist[1][0]+x_dist+self.parent.BackImg.pos_x,poslist[1][1]+y_dist+self.parent.BackImg.pos_y)
        pos2=(poslist[2][0]+x_dist+self.parent.BackImg.pos_x,poslist[2][1]+y_dist+self.parent.BackImg.pos_y)
        self.reinitby2point(pos1,pos2)
    def drawbymode(self,img):pass
class rectpic(rect):
    """docstring for ClassName"""
    def __init__(self,parent,pos1,pos2):
        rect.__init__(self,parent,pos1,pos2)
        self.parent=parent
        #初始化照片的路径
        self.picpath=''
        self.arg = {

            'mode':'UPCA',
        #
            'module_width': 0.2,
        #线高
            'module_height': 15.0,
        #左右空白区
            'quiet_zone': 6.5,
        #字体大小
            'font_size': 10,
        #文字离条形码的距离
            'text_distance': 5.0,
        #背景颜色
            'background': 'white',
        #前景颜色
            'foreground': 'black',
        #是否写文本
            'write_text': True,
        #文本
            'text':'123456789',
        #是否居中
            'center':True,
        }
    def get_mode(self):
        return 'picture'        
    def SetPicPath(self,object):
        filesFilter = "PNG files (*.png)|*.png|GIF files (*.gif)|*.gif|BMP files (*.bmp)|*.bmp"
        fileDialog =wx.FileDialog(object, wildcard = filesFilter, style = wx.FD_OPEN)
        if fileDialog.ShowModal() == wx.ID_OK:
            self.picpath=fileDialog.GetPath()
        fileDialog.Destroy()
        if self.picpath!='':
            self.GetOnRectsize()
    def GetPicPath(self):
        return self.picpath
    def GetPic(self):
        return self.img
    def GetOnRectsize(self):
        #以当前矩形的大小返回图片
        if self.picpath!='':
            self.img=Image.open(self.picpath).resize((int(self.pos2[0]-self.pos1[0]),int(self.pos2[1]-self.pos1[1])))
            return self.img
    def adjust(self,p_curry,mode):
        rect.adjust(self,p_curry,mode);
        self.GetOnRectsize()
    def move(self,p_curry,p_past):
        rect.move(self,p_curry,p_past)
        self.GetOnRectsize()
    def drawbymode(self,img):
        if self.picpath!='': img.paste(self.img,(int(self.pointlist[0][0]),int(self.pointlist[0][1])))
        else:self.showpoint8mode=True
class rectbar(rectpic):
    def __init__(self,parent,pos1,pos2):
        rectpic.__init__(self,parent,pos1,pos2)
    def get_mode(self):
        return 'Barcode' 
    def SetPicPath(self,path):
        self.picpath=path
        if self.picpath!='':
            self.GetOnRectsize()    
    def GetPicPath(self):
        return self.picpath
    def GetPic(self):
        return self.img  
    def reinitbyscale(self,size):pass      
class rectfont(rect):
    """docstring for rectfont"""
    def __init__(self,parent,pos1,pos2):
        rect.__init__(self,parent,pos1,pos2)
        self.parent=parent
        #创建参数字典
        self.arg= {'text':'','font':'simkai.ttf','align':'center','fill':'black','size':int(self.pos2[1]-self.pos1[1])}
    def get_mode(self):return 'Font'       
    def GetPicPath(self):return ''
    def drawbymode(self,img):
        img_rect=img.crop((self.pos1[0], self.pos1[1], self.pos2[0],self.pos2[1]))
        draw = ImageDraw.Draw(img_rect)
        #获取图片的大小
        W, H =  self.pos2[0]- self.pos1[0], self.pos2[1]- self.pos1[1]
        truetype=ImageFont.truetype(self.arg['font'],self.arg['size'])
        #获取画的区域的大小
        w, h = draw.multiline_textsize(text=self.arg['text'],font=truetype)
        if self.arg['align']=='left':
            print('left')
            draw.multiline_text((0,0),text=self.arg['text'],font=truetype,fill=self.arg['fill'])
        elif self.arg['align']=='center':
            print('middle')
            draw.multiline_text(((W-w)/2,0),text=self.arg['text'],font=truetype,fill=self.arg['fill'])
        elif self.arg['align']=='right':
            print('right')
            draw.multiline_text((W-w,0),text=self.arg['text'],font=truetype,fill=self.arg['fill'])                       
        img.paste(img_rect,(int(self.pointlist[0][0]),int(self.pointlist[0][1])))
        if self.arg['text']=='':
            self.showpoint8mode=True
        
    def GetOnRectsize(self):
        self.arg['size']=int(self.pos2[1]-self.pos1[1])
    #矩形的形状根据字体大小改变
    def GetOnFontsize(self):
        x1,y1=self.pos1
        x2,y2=self.pos2
        y2=y1+self.arg['size']
        self.reinitby2point(self.pic2win((x1,y1)),self.pic2win((x2,y2)))

    def adjust(self,p_curry,mode):
        rect.adjust(self,p_curry,mode);
        self.GetOnRectsize()
    def reinitbyscale(self,size):pass   
        