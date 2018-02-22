#背景图片的类
from PIL import Image,ImageFont,ImageDraw
class BackImg():
    """存储背景图片的相关参数"""
    def __init__(self,size,img=None,path=''):
        self.timeslist=[0.25,0.5,0.75,1,1.5,2,3,5,10]
        self.timesindex=3
        x,y=size
        if path!='':
            self.img=Image.open(path)
        else:
            self.img=img
        x1,y1=self.img.size
        self.pos_x=(x-x1)/2
        self.pos_y=(y-y1)/2
        self.pos_x1=self.pos_x+x1
        self.pos_y1=self.pos_y+y1
        self.times=self.timeslist[self.timesindex]
    def get_times_size(self):
        #获取当前图片的缩放倍数倍数的大小
        return (int(self.img.size[0]*self.times),int(self.img.size[1]*self.times))

    def size_reinit(self,size):
        x,y=size
        x1,y1=self.get_times_size()
        self.pos_x=(x-x1)/2
        self.pos_y=(y-y1)/2
        self.pos_x1=self.pos_x+x1
        self.pos_y1=self.pos_y+y1
    def TimesChange(self):
        self.times=self.timeslist[self.timesindex]
