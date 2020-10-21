# -*-coding:utf-8-*-
import socket
import tensorflow as tf
import os
import numpy as np
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
tf.compat.v1.disable_v2_behavior()

HOST = "127.0.0.1"
PORT = 5050
# 监听5050端口
def init_socket():
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((HOST,PORT))
    server.listen(1)
    return server

Server = init_socket()
# 接受数据



# 读取训练好的模型并创建一个图
with tf.compat.v1.gfile.FastGFile("inception_model/output_graph.pb","rb") as f:
    graph_def = tf.compat.v1.GraphDef()
    graph_def.ParseFromString(f.read())
    tf.compat.v1.import_graph_def(graph_def,name="")


with tf.compat.v1.Session() as sess:
    # 通过图获得tensor对象
    softmax = sess.graph.get_tensor_by_name("final_result:0")
    while True:
        connection, address = Server.accept()
        rec = connection.recv(1024)
        filepath = str(rec, "utf-8")
        print("connection", connection)
        print("address", address)
        print("filepath", filepath)
        # 获得操作句柄
        # 出错点,出错原因,GFile后面要填绝对路径,也就是完整路径
        image_data = tf.compat.v1.gfile.GFile(filepath, "rb").read()
        # 查看看图,获得输入输出首位张量名称,首张量名:DecodeJpeg/contents,尾张量名:final_result
        tf.compat.v1.summary.FileWriter("temp/summary", sess.graph)
        prediction = sess.run(softmax,{"DecodeJpeg/contents:0":image_data})
        print(prediction)
        prediction = np.squeeze(prediction).tolist()
        print(prediction)
        with open("inception_model/output_labels.txt",encoding="utf-8") as f:
            feature = f.readlines()
        result = ""
        for i in range(5):
            element = "".join([feature[i].strip(),"(",str(prediction[i]),")"])
            result = "".join([result,element])
        print(result)
        connection.send(bytes(result,"utf-8"))


