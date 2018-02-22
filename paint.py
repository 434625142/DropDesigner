#-*- coding:utf8 -*-
#用于绘图的部分
import wx
from Formatter import *
import sys
from cursor import *
from popupmenu import *
USE_BUFFERED_DC = True
class BufferedWindow(wx.Window):
    def __init__(self, *args, **kwargs):
        # make sure the NO_FULL_REPAINT_ON_RESIZE style flag is set.
        kwargs['style'] = kwargs.setdefault('style', wx.NO_FULL_REPAINT_ON_RESIZE) | wx.NO_FULL_REPAINT_ON_RESIZE
        wx.Window.__init__(self, *args, **kwargs)
        wx.EVT_PAINT(self, self.OnPaint)
        wx.EVT_SIZE(self, self.OnSize)
        self.OnSize(None)
    def Draw(self, dc):
        pass
    def OnPaint(self, event):
        # All that is needed here is to draw the buffer to screen
        if USE_BUFFERED_DC:
            dc = wx.BufferedPaintDC(self, self._Buffer)
        else:
            dc = wx.PaintDC(self)
            dc.DrawBitmap(self._Buffer, 0, 0)

    def OnSize(self,event):
        Size  = self.ClientSize
        self._Buffer = wx.Bitmap(*Size)
 #       wx.Create
        self.UpdateDrawing()

    def SaveToFile(self, FileName, FileType=wx.BITMAP_TYPE_PNG):
        self.img_save.SaveFile(FileName, FileType)

    def UpdateDrawing(self,savemode=False):
        dc = wx.MemoryDC()
        dc.SelectObject(self._Buffer)
        self.Draw(dc,savemode)
        del dc # need to get rid of the MemoryDC before Update() is called.
        self.Refresh()
        self.Update()
        
class DrawWindow(BufferedWindow):
    def __init__(self, *args, **kwargs):
        super(BufferedWindow, self).__init__() 
        BufferedWindow.__init__(self, *args, **kwargs)
        self.DrawRectMode = 'Normal'
        #实例化鼠标事件
        self.cursor=cursor(self)
        PopupMenu(self)

        self.rectlist=[]
        self.DrawData={}
    def AddTempRect(self,pos1,pos2):
        l=[]
        DrawData={}
        x1,y1=pos1
        x2,y2=pos2
        l.append( (x1,y1,x2-x1,y2-y1))
        DrawData["Temp"] = l
        return l
    def Draw(self, dc,savemode=False):
        dc.SetBackground( wx.Brush("gray"))
        dc.Clear() # make sure you clear the bitmap!
        try:
            #从背景图片中复制一份
            img_temp=self.BackImg.img.copy()
        except Exception as e : return 0
        #每次重绘前重新计算背景图片的位置，防止窗体缩放导致图片位置不在中心
        self.BackImg.size_reinit(self.ClientSize)
        img_temp=img_temp.resize(self.BackImg.get_times_size())
        for i in self.rectlist: i.drawbymode(img_temp)
        img_temp=PIL2wx(img_temp)
        if savemode==False:
            temp_dc = wx.MemoryDC()
            temp_dc.SelectObject(img_temp)
            for i in self.rectlist:
                i.draw8(temp_dc)
            del temp_dc
        else: 
            self.img_save=img_temp

        # 这个用来画暂时的图片
        dc.DrawBitmap(img_temp,self.BackImg.pos_x, self.BackImg.pos_y)
        for key, data in self.DrawData.items():
            if key == "Temp":
                dc.SetBrush(wx.Brush("blue", wx.TRANSPARENT))
                dc.SetPen(wx.Pen('black', 1))
                for r in data:
                    dc.DrawRectangle(*r)
                self.DrawData["Temp"] =[]


if __name__ == "__main__":
    a={}
    l=[]
    l.append((1,1))
    a['point']=l
    a['temp']=(2,3)
    
