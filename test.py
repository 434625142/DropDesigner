#用于读取字体文件的信息代码 
import win32api
def getFileProperties(fname):
    propNames=('Comments', 'InternalName', 'ProductName',
        'CompanyName', 'LegalCopyright', 'ProductVersion',
        'FileDescription', 'LegalTrademarks', 'PrivateBuild',
        'FileVersion', 'OriginalFilename', 'SpecialBuild')
    props = {'FixedFileInfo': None, 'StringFileInfo': None, 'FileVersion': None}
    try:
        fixedInfo = win32api.GetFileVersionInfo(fname, '\\')
#        print(fixedInfo)
        props['FixedFileInfo'] = fixedInfo
        props['FileVersion'] = "%d.%d.%d.%d" % (fixedInfo['FileVersionMS'] / 65536,
            fixedInfo['FileVersionMS'] % 65536, fixedInfo['FileVersionLS'] / 65536,
            fixedInfo['FileVersionLS'] % 65536)
        lang, codepage = win32api.GetFileVersionInfo(fname, '\\VarFileInfo\\Translation')[0]
        strInfo = {}
        for propName in propNames:
            strInfoPath = u'\\StringFileInfo\\%04X%04X\\%s' % (lang, codepage, propName)
            strInfo[propName] = win32api.GetFileVersionInfo(fname, strInfoPath)
        props['StringFileInfo'] = strInfo
    except Exception as e:
        print(e)
        pass
    return props
f=getFileProperties('python.exe')
print(f)
