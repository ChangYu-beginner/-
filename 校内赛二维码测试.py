import cv2 as cv
import pyzbar.pyzbar as pyzbar
import requests
import webbrowser


def decodeDisplay(image):  # 解析二维码
    barcodes = pyzbar.decode(image)
    global count
    count = 0
    for barcode in barcodes:
        (x, y, w, h) = barcode.rect  # 获取二维码位置
        cv.rectangle(image, (x, y), (x + w, y + h), (225, 225, 225), 2)
        global barcodeData, barcodeType
        barcodeData = None
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        # 绘出图像上条形码的数据和条形码类型
        text = "{} ({})".format(barcodeData, barcodeType)
        cv.putText(image, text, (x, y - 10), cv.FONT_HERSHEY_SIMPLEX,
                    .5, (225, 225, 225), 2)
        # 向终端打印条形码数据和条形码类型
        print("Found {} barcode: {}".format(barcodeType, barcodeData))
        count += 1
    return image


def detect():
    camera = cv.VideoCapture(0, cv.CAP_DSHOW)
    while True:
        # 读取当前帧
        success, frame = camera.read()
        # 转为灰度图像
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        im = decodeDisplay(gray)
        k = cv.waitKey(1)
        cv.imshow("camera", im)
        # 按esc或者检测到二维码跳出循环
        if count != 0:
            cv.destroyAllWindows()
            break
        elif k == 27:
            cv.destroyAllWindows()
            break
    camera.release()
    cv.destroyAllWindows()


def Get():  # 获取网页内容
    try:
        _url = barcodeData
        url = str(_url)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0 Win64x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
        }
        r = requests.get(url, headers=headers)
        info = r.text.split('\n')
        code_info = info[0].split(":")
        word_info = info[1].split(":")
        if code_info[1] == "0":  #
            print("响应的code为0，正确。")
            html = open("D:\\Right.html", "w")         # 通过输出的颜色不同进行区分
            string = '<!DOCtype HTML><head><title>返回值为0</title></head><body><font color="#FF0000">%s</font><br/></body>' % r.text
            html.write(string)
            html.close()
            webbrowser.open("D:\\Right.html")
            print(r.url)
        elif code_info[1] == "1":
            print("响应的code为1，出现错误。")
            html = open("D:\\Error.html", "w")
            string = '<!DOCtype HTML><head><title>返回值为1</title></head><body><font color="#0080FF">%s</font><br/></body>' % r.text
            html.write(string)
            html.close()
            webbrowser.open("D:\\Error.html")
            print(r.url)
        else:
            print("为什么会出现别的结果，我也不知道。。。。。。")
    except:
        print("获取内容出错")


if __name__ == '__main__':
    detect()
    Get()
