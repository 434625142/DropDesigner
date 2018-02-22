#-*- coding:utf8 -*-
import wx
from paint import *
from BackImg import *
import os
from setui import *
#USE_BUFFERED_DC = False
USE_BUFFERED_DC = True
class TestFrame(wx.Frame):
    def __init__(self, parent=None):
        wx.Frame.__init__(self, parent,
                          size = (800,800),
                          title="Double Buffered Test",
                          style=wx.DEFAULT_FRAME_STYLE)
        tb = wx.ToolBar( self, -1 ) 
        self.CreateStatusBar()
        self.ToolBar = tb 
        tb.AddLabelTool(99,'',self.get_bitmap("imgdata/open.png",(50,50)),longHelp='新建')
        tb.AddLabelTool(100,'',self.get_bitmap("imgdata/open1.png",(50,50)),longHelp='打开图片')
        tb.AddLabelTool(101,'',self.get_bitmap("imgdata/font.png",(50,50)),longHelp='文字区域')
        tb.AddLabelTool(102,'',self.get_bitmap("imgdata/picture.png",(50,50)),longHelp='图片区域')
        tb.AddLabelTool(103,'',self.get_bitmap("imgdata/barcode.png",(50,50)),longHelp='条形码区域')
        tb.AddLabelTool(104,'',self.get_bitmap("imgdata/add.png",(50,50)),longHelp='放大')
        tb.AddLabelTool(105,'',self.get_bitmap("imgdata/reduce3.png",(50,50)),longHelp='缩小')
        tb.AddLabelTool(106,'',self.get_bitmap("imgdata/save.png",(50,50)),longHelp='保存')  
        tb.AddLabelTool(107,'',self.get_bitmap("imgdata/printer.png",(50,50)),longHelp='打印')        
        tb.Bind(wx.EVT_TOOL, self.Onright)
#        self.toolbar = wx.ToolBar( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL )
        tb.Realize() 

        self.Bind(wx.EVT_CLOSE,self.OnQuit) 

        self.Window = DrawWindow(self)
        self.Show()
    def get_bitmap(self,path,size):
        x,y=size
        return wx.BitmapFromImage(wx.Image(path).Rescale(x,y))  
    def Onright(self, event): 
        temp=event.GetId()
        if temp==99:newsetui(self.Window,'新建')

        elif temp==100 :
            filesFilter = "PNG files (*.png)|*.png|GIF files (*.gif)|*.gif|BMP files (*.bmp)|*.bmp"
            fileDialog =wx.FileDialog(self, wildcard = filesFilter, style = wx.FD_OPEN)
            if fileDialog.ShowModal() == wx.ID_OK:
                path=fileDialog.GetPath()
            fileDialog.Destroy()
            #实例一个背景图片
            self.Window.BackImg = BackImg(path=path,size=self.Window.ClientSize)
            self.Window.UpdateDrawing()
        elif temp==101 : self.Window.DrawRectMode = 'Font'
        elif temp==102 : self.Window.DrawRectMode = 'Picture'
        elif temp==103 : self.Window.DrawRectMode = 'Barcode'
        elif temp==104 :
            if self.Window.BackImg.timesindex<8:
                self.Window.BackImg.timesindex+=1
                self.Window.BackImg.TimesChange()
            self.Window.BackImg.size_reinit(self.Window.ClientSize)
            for i in self.Window.rectlist:
                i.reinitbyscale(self.Window.BackImg.get_times_size())
                i.GetOnRectsize()
                # else:i.GetFontOnRectsize()
        elif temp==105:
            if self.Window.BackImg.timesindex>0:
                self.Window.BackImg.timesindex-=1
                self.Window.BackImg.TimesChange()
            self.Window.BackImg.size_reinit(self.Window.ClientSize)
            for i in self.Window.rectlist:
                i.reinitbyscale(self.Window.BackImg.get_times_size())
                i.GetOnRectsize()
                # else:i.GetFontOnRectsize()    
        elif temp==106:
            print('save')
            dlg = wx.FileDialog(self, "Choose a file name to save the image as a PNG to",
                               defaultDir = "",
                               defaultFile = "",
                               wildcard = "*.png",
                               style = wx.FD_SAVE)
            if dlg.ShowModal() == wx.ID_OK:
                self.Window.UpdateDrawing(True)
                self.Window.SaveToFile(dlg.GetPath(), wx.BITMAP_TYPE_PNG)
            dlg.Destroy()     
        #打印功能
        elif temp==107:pass
        self.Window.UpdateDrawing()            
    def OnQuit(self,event):
        for i in self.Window.rectlist:
            if i.GetPicPath()!='':os.remove(i.GetPicPath())
        self.Destroy()
    def MakeNewData(self):
        MaxX, MaxY =self.Window.ClientSize
        DrawData = {}
        l = []
        return l

class DemoApp(wx.App):
    def OnInit(self):
        frame = TestFrame()
        self.SetTopWindow(frame)
        return True

if __name__ == "__main__":
    app = DemoApp(0)
    app.MainLoop()

    
