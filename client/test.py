import presenter_message_pb2 as pb2

# message = presenter_message_pb2.OpenChannelRequest()
# message.channel_name = '123'
# message.content_type = 3
# data = message.SerializeToString()
# print('value:', data)

request = pb2.PresentImageRequest()
request.format = 1
request.width = 300
request.height = 200
request.data = b''
myadd = request.rectangle_list.add()
myadd.left_top.x = 1
myadd.left_top.x = 2
myadd.right_bottom.x = 3
myadd.right_bottom.y = 4
myadd.label_text = 'hello'



