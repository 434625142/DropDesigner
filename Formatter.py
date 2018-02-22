#用于wx的bitmap格式和pil的image格式的相互转换
from PIL import Image
import wx
def PIL2wx (image):
    width, height = image.size
    return wx.BitmapFromBuffer(width, height, image.tobytes())

def wx2PIL (bitmap):
    size = tuple(bitmap.GetSize())
    try:
        buf = size[0]*size[1]*3*"\x00"
        bitmap.CopyToBuffer(buf)
    except:
        del buf
        buf = bitmap.ConvertToImage().GetData()
    return Image.frombuffer("RGB", size, buf, "raw", "RGB", 0, 1)
if __name__ == '__main__':
    pilImage = Image.open('lena1.png')
    bmp=PIL2wx(pilImage)
