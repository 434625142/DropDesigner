#用于处理鼠标的点击事件，进行绘制矩形等相关操作
import wx
from rect import *
class cursor():
    """docstring for ClassName"""
    def __init__(self, parent):
        #鼠标的父类是绘制类
        self.parent = parent
        self.parent.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.parent.Bind(wx.EVT_MOTION, self.OnDrag)
        self.parent.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.cursormode='normal'
    def PosDeal(self,pos):
        #如果点超出了图片范围，将点拉回到图像边界
        if pos[0]<self.parent.BackImg.pos_x:pos[0]=self.parent.BackImg.pos_x
        if pos[1]<self.parent.BackImg.pos_y:pos[1]=self.parent+BackImg.pos_y
        if pos[0]>self.parent.BackImg.pos_x1:pos[0]=self.parent.BackImg.pos_x1
        if pos[1]>self.parent.BackImg.pos_y1:pos[1]=self.parent.BackImg.pos_y1
        return pos      

    def OnDrag(self,event):
        try:
            pos_temp=self.PosDeal(event.GetPosition())
        except Exception as e:
            return 0
        #将当前位置保存一份，以供后面弹出popupmenu
        self.currypos=pos_temp
        if event.LeftIsDown():
            if self.cursormode=='draw':self.parent.DrawData["Temp"]=self.parent.AddTempRect(self.Ld,pos_temp)
            elif self.cursormode=='adjust':self.parent.rectlist[self.RecrIndex].adjust(pos_temp,self.PointIndex)
            elif self.cursormode=='move':self.parent.rectlist[self.RecrIndex].move(pos_temp,self.MovePoint)
            self.parent.UpdateDrawing() 
        elif self.cursormode=='normal':
            j=0
            for i in self.parent.rectlist:
                self.PointIndex=i.IsInpoint8(pos_temp)
                if self.PointIndex>=0:
                    self.RecrIndex=j
                    self.parent.SetCursor( wx.StockCursor(wx.CURSOR_HAND))
                    self.cursormode='hand'
                    return 0
                j+=1
        elif self.cursormode=='hand':
            for i in self.parent.rectlist:
                self.PointIndex=i.IsInpoint8(pos_temp)
                if self.PointIndex>=0:
                    self.parent.SetCursor( wx.StockCursor(wx.CURSOR_HAND))
                    return 0
            self.cursormode='normal'
            self.parent.SetCursor( wx.StockCursor(wx.CURSOR_ARROW))
    def OnLeftDown(self,event):
        try:
            pos_temp=self.PosDeal(event.GetPosition())
        except Exception as e:
            return 0

        if self.parent.DrawRectMode!='normal': 
            self.cursormode='draw'
            self.Ld=pos_temp
        elif self.cursormode=='hand':
            self.cursormode='adjust'
        elif self.cursormode=='normal': 
            j=0
            for i in self.parent.rectlist:
                if i.is_in_rect(pos_temp)==True:
                    #记录当前点和此时矩形的左上角点,右下角点
                    self.MovePoint=[pos_temp,i.pointlist[0],i.pointlist[2]]
                    self.cursormode='move'
                    self.RecrIndex=j
                    print('ok')
                    i.showpoint8mode=True
                else:i.showpoint8mode=False
                    # return 0
                j+=1
            self.parent.UpdateDrawing()
    def OnLeftUp(self,event):
        try:
            pos_temp=self.PosDeal(event.GetPosition())
        except Exception as e:
            return 0
        if self.cursormode=='draw':
            if self.parent.DrawRectMode=='Picture': self.parent.rectlist.append(rectpic(self.parent,self.Ld,pos_temp))
            elif self.parent.DrawRectMode=='Barcode':  self.parent.rectlist.append(rectbar(self.parent,self.Ld,pos_temp))
            elif self.parent.DrawRectMode=='Font': self.parent.rectlist.append(rectfont(self.parent,self.Ld,pos_temp))
            self.parent.DrawRectMode='normal'
            self.cursormode='normal'
            self.parent.UpdateDrawing()
        elif self.cursormode=='adjust' : 
            self.cursormode='normal'
        elif self.cursormode=='move':
            self.cursormode='normal'
            self.MovePoint=[]

