import presenter_message_pb2 as pb2
import presenter_types
import socket
import struct

class ChannelManager(object):
    def __init__(self):
        self.msg_head_len = 5
    '''
    Open channel,and return send data
    '''
    def OpenChannel(self, channel_name='video', content_type=1):
        message = pb2.OpenChannelRequest()
        message.channel_name = channel_name
        message.content_type = content_type
        msg_data = message.SerializeToString()
        msg_data_len = len(msg_data)
        msg_name = pb2._OPENCHANNELREQUEST.full_name
        # print('msg_name:', msg_name)
        msg_name_len = len(msg_name)
        # print('msg_name_len:', msg_name_len)
        msg_total_len = msg_name_len + msg_data_len + self.msg_head_len
        # print('msg_total_len:', msg_total_len)
        data = b''
        msg_total_len = socket.htonl(msg_total_len)
        # print('socket.htonl(msg_total_len)=', msg_total_len)
        pack_data = struct.pack('IB', msg_total_len, msg_name_len)
        # print('pack_data length=', len(pack_data))
        data += pack_data
        data += msg_name.encode()
        data += msg_data
        return data

    def PackRequestData(self, image_frame):
        request = pb2.PresentImageRequest()
        request.format = image_frame.format
        request.width = image_frame.width
        request.height = image_frame.height
        request.data = image_frame.data
        for resultList in image_frame.detection_results:
            myadd = request.rectangle_list.add()
            myadd.left_top.x = resultList.lt.x
            myadd.left_top.y = resultList.lt.y
            myadd.right_bottom.x = resultList.rb.x
            myadd.right_bottom.y = resultList.rb.y
            myadd.label_text = resultList.result_text
        

        buf = request.SerializeToString()
        msg_body_len = len(buf)
        msg_name = pb2._PRESENTIMAGEREQUEST.full_name
        # print('msg_name:', msg_name)
        msg_name_len = len(msg_name)

        msg_total_len = msg_name_len + msg_body_len + self.msg_head_len
        # print('msg_total_len:', msg_total_len)
        data = b''
        msg_total_len = socket.htonl(msg_total_len)
        # print('socket.htonl(msg_total_len)=', msg_total_len)
        pack_data = struct.pack('IB', msg_total_len, msg_name_len)
        # print('pack_data length=', len(pack_data))
        data += pack_data
        data += msg_name.encode()
        data += buf
        return data





