#!bin/bash
i=$(ps -ef | grep presenter | grep face_detection | grep -o '[0-9]\+' | head -n1)
if [ -z "$i" ] ;then
echo presenter sever not in process!
else
kill -9 $i
echo presenter sever stop success!
fi
python3 presenterserver/presenter_server.py --app face_detection &
