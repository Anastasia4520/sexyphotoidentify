# -*-coding:utf-8-*-
import sys
import operator
import asyncio
import os
import time
import socket
import numpy as np
import tornado.web
import tornado.ioloop

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
staticFilePath = "static"

class UploadfileHandler(tornado.web.RequestHandler):
    def get(self):
        # htmlSource = '<!DOCTYPE html> ' \
        #              + '<head> <meta charset="UTF-8"> </head> ' \
        #              + '<body> ' \
        #              + '<img src="static\\127.0.0.1\\2020-10-20-22-53-59-512.jpg"/>' \
        #              + '</body>' \
        #              + '</html>'
        # self.write(htmlSource)
        self.render("UploadFile.html")

    def post(self):
        file_metas = self.request.files['file']
        print(file_metas[0].keys())
        fileName = file_metas[0]["filename"]
        fileType = file_metas[0]["content_type"]
        fileContent = file_metas[0]["body"]
        print("fileName",fileName)
        print("fileType",fileType)
        # 判断格式是否为jpeg格式
        if operator.eq(fileType,"image/jpeg")==False:
            self.write("请输入正确的图片格式!")
        # 修改图片名称并存入static文件夹中
        graphPath = os.path.join(staticFilePath,self.request.remote_ip)
        print("graphPath",graphPath)
        if not os.path.exists(graphPath):
            os.makedirs(graphPath)
        filePath = "C:/Users/ling li/PycharmProjects/script/色情图片识别/"+os.path.join(graphPath,fileName)
        print(filePath)
        if not os.path.exists(filePath):
            with open(filePath,"wb") as f:
                f.write(fileContent)
        # 将图片传给Tensorflow
        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client.connect(("127.0.0.1",5050))
        client.send(bytes(filePath,"utf-8"))

        # 接收结果
        print("graphPath:",graphPath)
        result = client.recv(1024)
        result = str(result,"utf-8")
        n = filePath.find(staticFilePath)
        imagePath = filePath[n:]
        print("imagePath",imagePath)
        htmlSource = '<!DOCTYPE html> ' \
                     + '<head> <meta charset="UTF-8"> </head> ' \
                     + '<body> ' \
                     + '<p> ' + result + '</p>' \
                     + '<img src="' + imagePath + '"/>' \
                     + '</body>' \
                     + '</html>'
        self.write(htmlSource)





setting = dict(
    #template_path = os.path.join(os.path.dirname(__file__), "temploop"),
    static_path = os.path.join(os.path.dirname(__file__), staticFilePath)
)

app = tornado.web.Application([(r"/file",UploadfileHandler)],**setting)

if __name__=="__main__":
    app.listen(8080)
    tornado.ioloop.IOLoop.instance().start()