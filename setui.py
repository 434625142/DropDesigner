#设置的界面代码
from panelconfig import *
import barcode
from barcode.writer import ImageWriter
import os
from BackImg import *
#基础类，包含矩形的调整、移动以及坐标输入
class setui(ParaDialog):
    """docstring for setui"""
    def __init__( self, parent,rect, title):
        ParaDialog.__init__(self, parent, title)
        self.view=[
                 ('lab','=========  左上角点  ========='),
                (int, (0,2000), 0, 'x', 'x', 'pixel'),
                (int, (0,2000), 0, 'y', 'y', 'pixel'),
                 ('lab','=========  矩形宽高  ========='),
                (int, (0,2000), 0, '宽', 'width', 'pixel'),
                (int, (0,2000), 0, '高', 'hight', 'pixel'),
                ]
        self.rect=rect
        #备份一份数据，若点取消则用此数据
        self.cancel_buf=[rect.pos1,rect.pos2]
#        self.arg_buf={}
        #读取矩形的坐标信息      
        self.data = {'x':rect.pos1[0], 'y':rect.pos1[1], 'width':rect.pos2[0]-rect.pos1[0],'hight':rect.pos2[1]-rect.pos1[1] ,'preview':False}
#        self.btn_cancel.Bind( wx.EVT_BUTTON, lambda e:self.commit('cancel'))
    def handle_(self,para):
        self.rect.reinitby2point(self.rect.pic2win((para['x'],para['y'])),self.rect.pic2win((para['x']+para['width'],para['y']+para['hight'])))
        self.rect.parent.UpdateDrawing()
    def commit(self, state):
        if state=='ok':self.on_ok1()
        if state=='cancel':self.on_cancel1()
        self.Destroy()
    def on_ok1(self):
        self.handle_(self.para)
    def on_cancel1(self):
        self.rect.arg=self.arg_buf
        self.handle_(self.arg_buf)
        self.rect.reinitby2point(self.rect.pic2win(self.cancel_buf[0]),self.rect.pic2win(self.cancel_buf[1]))
        self.rect.parent.UpdateDrawing()
#图片设置页面
class PicSetUi(setui):
    def __init__( self, parent,rect, title):
        setui.__init__(self, parent,rect, title)
        self.view+=[(bool, 'Preview', 'preview') ]
        self.arg_buf=self.data.copy()
        self.init_view(self.view, self.data,modal=False)
        self.pack()
        self.ShowModal()
    def handle_(self,para):
        setui.handle_(self,para)
        self.rect.GetOnRectsize()
        self.rect.parent.UpdateDrawing()
class BarSetUi(setui):
    def __init__( self, parent,rect, title):
        setui.__init__(self, parent,rect, title)
        modelist=['Code39','PZN','EAN-13','EAN8','JAN',
                    'ISBN13','ISBN10','ISSN','UPCA',]
        self.view+=[  
                ('lab','=========  二维码设置  ========='),
                (list, modelist, str, '编码', 'mode', ''),
                (str,  '字符', 'text', ''),
                (float, (0,500), 1, '线宽', 'module_width', 'mm'),
                (float, (0,500), 1, '线高', 'module_height', 'mm'),
                (float, (0,500), 1, '空白区', 'quiet_zone', 'mm'),
                (int, (0,500), 0, '字体大小', 'font_size', 'pixel'),
                (float, (0,500), 1, '距离', 'text_distance', 'mm'),
                (bool, '居中', 'center'),
                (bool, 'Preview', 'preview')]

        # data = {'mode':'UPCA','text':'123456789','module_width':0.2,'module_height':15.0,
        #         'quiet_zone':6.5,'font_size':10,'text_distance':5.0,'center_text':True}
        data=self.rect.arg 
        self.data.update(data)
        self.arg_buf=self.data.copy()
        self.init_view(self.view, self.data,modal=False)
        self.pack()
        self.ShowModal()
    def handle_(self,para):
        setui.handle_(self,para)
#        self.rect.arg=self.data
        ean = barcode.get('UPCA', para['text'], writer=ImageWriter())
        self.rect.picpath=para['text']
        filename = ean.save(self.rect.picpath,self.data)
        self.rect.SetPicPath(para['text']+'.png')
class fontsetui(setui):
    """docstring for fontsetui"""
    def __init__( self, parent,rect, title):
        setui.__init__(self, parent,rect, title)
        fontlist=[]
        files = os.listdir('C:\WINDOWS\Fonts')
#        “left”, “center” or “right”.
        alignlist=['left','center','right']
        #去除后缀.ttf
        for i in files: fontlist.append(i)
        self.view+=[  
                ('lab','=========  文字设置  ========='),
                (str,  '文字', 'text', ''),
                (int, (0,500), 0, '字体大小', 'size', 'pixel'),
                (list, fontlist, str, '字体', 'font', ''),
                ('color','颜色', 'fill', ''),
                (list, alignlist, str, '排列', 'align', ''),
                (bool, 'Preview', 'preview'),
                ]
        data = {'text':self.rect.arg['text'],'font':self.rect.arg['font'],'align':self.rect.arg['align'],
        'fill':self.rect.arg['fill'],'size':self.rect.arg['size']}
        self.data.update(data)
        self.arg_buf=self.data.copy()
        self.init_view(self.view, self.data,modal=False)
        self.pack()
        self.ShowModal()
    #重写handle函数
    def handle_(self,para):
        setui.handle_(self,para)
        self.rect.arg=para
        self.rect.GetOnFontsize()
#        self.rect.GetOnFontsize()
        self.rect.parent.UpdateDrawing()          

#新建的工作区
class newsetui(ParaDialog):
    """docstring for setui"""
    def __init__( self, parent, title):
        ParaDialog.__init__(self, parent, title)
        self.parent=parent
        self.view=[
                (int, (1,2000), 0, '宽', 'width', 'pixel'),
                (int, (1,2000), 0, '高', 'hight', 'pixel'),
                (bool, 'Preview', 'preview'),
                ]
        #读取矩形的坐标信息      
        self.data = {'width':0,'hight':0,'preview':False}
        self.init_view(self.view, self.data,modal=False)
        self.pack()
        self.ShowModal()
#        self.btn_cancel.Bind( wx.EVT_BUTTON, lambda e:self.commit('cancel'))
    def handle_(self,para):
        self.parent.BackImg = BackImg(size=self.parent.ClientSize,img=Image.new('RGB', (para['width'],para['hight']), "white"))
        self.parent.UpdateDrawing()
        self.parent.UpdateDrawing()
    def commit(self, state):
        if state=='ok':self.on_ok1()
        if state=='cancel':self.on_cancel1()
        self.Destroy()
    def on_ok1(self):
        self.handle_(self.para)
        self.parent.UpdateDrawing()
    def on_cancel1(self):
        self.parent.BackImg=None
        self.parent.UpdateDrawing()
if __name__ == '__main__':
    app = wx.PySimpleApp()
    pd = newsetui(None, '设置')
