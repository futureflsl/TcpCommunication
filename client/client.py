# encoding: utf-8
import threading
import socket
import time
import struct
import presenter_message_pb2 as pb2
import time
from presenter_types import *
import ChannelManager


class PresenterSocketClient(object):
    def __init__(self, server_address, reconnectiontime=5,recvCallback=None):
        self._server_address = server_address
        self._reconnectiontime = reconnectiontime
        self.__recvCallback = recvCallback
        self._sock_client = None
        self._bstart = True
        self.SEND_BUF_SIZE=204800
        self.RECV_BUF_SIZE = 204800
        # threading.Thread(target=self.start_connect()).start()

    def start_connect(self):
        print("create socket object...")
        self._sock_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock_client.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, self.SEND_BUF_SIZE)
        self._sock_client.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.RECV_BUF_SIZE)

        # bufsize = self._sock_client.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
        # print("发送数据缓存区大小：%d" % bufsize)
        # bufsize = self._sock_client.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
        # print("接收数据缓存区大小：%d" % bufsize)
        try:
            print("connect server...")
            self._sock_client.connect(self._server_address)
        except Exception as e:
            print(e)
            print("reconnect server...")
            time.sleep(self._reconnectiontime)
            self.start_connect()
            return
        self._bstart = True
        print("wait data comming...")
        threading.Thread(target=self.__start_listenning()).start()

    def __start_listenning(self):
        while self._bstart:
            try:
                self._read_sock_and_process_msg()
                # print("等待数据到达...")
                # data = self._sock_client.recv(self.RECV_BUF_SIZE)
                #if data:
                #    if self.__recvCallback:
                #        self.__recvCallback(data)
                    #print(data)
                    # self.send_data("hello".encode())
                # else:
                #     print("close")
                #     self._sock_client.close()
                #     self.start_connect()
                #     break
            except Exception as e:
                print(e)
                self._sock_client.close()
                self.start_connect()
                break
    def _read_socket(self, read_len):
        has_read_len = 0
        read_buf = b''
        total_buf = b''
        
        while has_read_len != read_len:
            try:
                read_buf = self._sock_client.recv(read_len - has_read_len)
            except socket.error:
                print("socket error")
                return False, None
            if read_buf == b'':
                return False, None
            total_buf += read_buf
            has_read_len = len(total_buf)

        return True, total_buf

    def _read_msg_head(self,read_len):
        ret, msg_head = self._read_socket(read_len)
        print("msg head data is :", msg_head)
        if not ret:
            print("socket receive msg head null")
            return None, None

        # in Struct(), 'I' is unsigned int, 'B' is unsigned char
        msg_head_data = struct.Struct('IB')
        (msg_total_len, msg_name_len) = msg_head_data.unpack(msg_head)
        msg_total_len = socket.ntohl(msg_total_len)
        print("msg total length is :",msg_total_len)
        print("msg name is :", msg_name_len)
        return msg_total_len, msg_name_len

    def _read_msg_name(self, msg_name_len):
        ret, msg_name = self._read_socket(msg_name_len)
        print("direct msg name is :", msg_name)
        if not ret:
            print("socket receive msg name null")
            return False, None
        try:
            msg_name = msg_name.decode("utf-8")
            print("decode msg name is :", msg_name)
        except Exception as e:
            print("msg name decode to utf-8 error")
            return False, None

        return True, msg_name

    def _read_msg_body(self,  msg_body_len):
        print("msg body length is :", msg_body_len)
        ret, msg_body = self._read_socket(msg_body_len)
        if not ret:
            print("socket receive msg body null")
            return False,None
        return True,  msg_body

    def _read_sock_and_process_msg(self):
        # Step1: read msg head
        msg_total_len, msg_name_len = self._read_msg_head(5)
        if msg_total_len is None:
            print("msg_total_len is None.")
            return False

        # Step2: read msg name
        ret, msg_name = self._read_msg_name(msg_name_len)
        if not ret:
            return ret

        # Step3:  read msg body
        msg_body_len = msg_total_len - 5 - msg_name_len
        if msg_body_len < 0:
            print("msg_total_len is 0")
            return False
        ret, msg_body = self._read_msg_body(msg_body_len)
        if not ret:
            return ret

        # Step4: process msg
        ret = self._process_msg(msg_name, msg_body)
        return ret
    def _process_msg(self, msg_name,msg_data):
        if msg_name == pb2._PRESENTIMAGEREQUEST.full_name:
            request = pb2.PresentImageRequest()
            try:
                print("ParseFromString start")
                print("msg_data type is :", type(msg_data))
                request.ParseFromString(msg_data)
            except Exception as e:
                print("ParseFromString exception: Error parsing message")
                return
            with open('result.jpg','wb') as f:
                f.write(request.data)
            

    def send_data(self, data):
	# print(data)
        self._sock_client.sendall(data)

    def close(self):
        self._bstart = False
        self._sock_client.shutdown()
        self._sock_client.close()


if __name__ == "__main__":
    print('start client...')

    def recvdata(data):
        print(data)

    psc = PresenterSocketClient(("127.0.0.1", 7006), 5, None)
    threading.Thread(target=psc.start_connect).start()
    channel_manager = ChannelManager.ChannelManager()
    data = channel_manager.OpenChannel()


    image_data = b''
    with open('test.jpg', mode='rb') as f:
        image_data = f.read()

    image_frame = ImageFrame()
    image_frame.format = 0
    image_frame.width = 300
    image_frame.height = 200
    image_frame.data = image_data
    image_frame.size = 0

    dr= DetectionResult()
    dr.lt.x = 10
    dr.lt.y = 10
    dr.rb.x = 100
    dr.rb.y = 100
    dr.result_text = 'fuck you!'
    image_frame.detection_results.append(dr)



    dr= DetectionResult()
    dr.lt.x = 20
    dr.lt.y = 20
    dr.rb.x = 200
    dr.rb.y = 200
    dr.result_text = 'shit!'
    image_frame.detection_results.append(dr)

    all_data = channel_manager.PackRequestData(image_frame)
    while True:
        raw_input('please input data you need to send:')
        psc.send_data(data)
        time.sleep(0.2)
        psc.send_data(all_data)
