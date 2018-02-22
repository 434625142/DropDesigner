#用于右键弹出菜单的代码
import wx
from setui import *
class PopupMenu():
    """docstring for popupmenu"""
    def __init__(self, parent):
    #popupmenu的父类是window绘图窗口
        self.parent = parent
        self.popupmenu1 = wx.Menu()
        self.TextList=['Add Picture','Setting','Del']
        for text in self.TextList:
            item = self.popupmenu1.Append(-1, text)
            self.parent.Bind(wx.EVT_MENU, self.OnPopupItemSelected, item)

        self.popupmenu2 = wx.Menu()
        self.TextList1=['Setting','Del']
        for text in self.TextList1:
            item = self.popupmenu2.Append(-1, text)
            self.parent.Bind(wx.EVT_MENU, self.OnPopupItemSelected1, item)
        self.parent.Bind(wx.EVT_CONTEXT_MENU, self.OnShowPopup)
    def OnShowPopup(self,event):
        #判断当前鼠标的形式
        print(self.parent.cursor.cursormode)
        if self.parent.cursor.cursormode=='normal':
            j=0
            for i in self.parent.rectlist:
                #判断是否在矩形内 
                if i.is_in_rect(self.parent.cursor.currypos)==True:
                    #判断矩形的模式，对于不同的模式弹出不同的菜单
                    print(i.get_mode())
                    if i.get_mode()=='picture':
                    #判断出矩形的模式是图片模式
                        self.parent.RecrIndex=j
                        #这个是弹出菜单栏
                        self.parent.PopupMenu(self.popupmenu1,self.parent.cursor.currypos)
                    else :
                        self.parent.RecrIndex=j
                        self.parent.PopupMenu(self.popupmenu2,self.parent.cursor.currypos)
                j+=1 
    def OnPopupItemSelected(self,event):
        if self.parent.rectlist[self.parent.RecrIndex].get_mode()=='picture':
            item = self.popupmenu1.FindItemById(event.GetId())
            text = item.GetText()
            print(self.parent.RecrIndex)
            if text=='Add Picture':
                path=self.parent.rectlist[self.parent.RecrIndex].SetPicPath(self.parent)
                self.parent.UpdateDrawing()
            elif text=='Setting':
                pd = PicSetUi(None,self.parent.rectlist[self.parent.RecrIndex], '设置')
            elif text=='Del':
                del(self.parent.rectlist[self.parent.RecrIndex])
            self.parent.UpdateDrawing()
    def OnPopupItemSelected1(self,event):
        item = self.popupmenu2.FindItemById(event.GetId())
        text = item.GetText()
        print(self.parent.RecrIndex)
        if text=='Setting':
            if self.parent.rectlist[self.parent.RecrIndex].get_mode()=='Font':
                fontsetui(None,self.parent.rectlist[self.parent.RecrIndex], '设置')
            elif self.parent.rectlist[self.parent.RecrIndex].get_mode()=='Barcode':
                BarSetUi(None,self.parent.rectlist[self.parent.RecrIndex], '设置')
        elif text=='Del':
            del(self.parent.rectlist[self.parent.RecrIndex])
        self.parent.UpdateDrawing()
