# Marketing Tool
This package is a tool help you do follow marketing job:

1. Transcribe the speech in video
2. Insert a video into antho video
3. Translate subtitle files
4. Insert text into video (todo)

### Install requirement
This program require python 3.9 installed
### How to use

Transcribe the speech in video
```
Marketingtool --action transcribe -f videofilepath
```

Insert Video into another video
```
 Marketingtool -a insertVideo -f ~/path/to/video -o ~/result/video.mp4 --insert-video ~/insert/video.mp4
```

Translate subtitle files
```
Marketingtool --action translate -f /path/to/subtitle/file --source-lang chinese --targetlang english
```

### How to develop
You can also install python package comfortably with pip:

```
python3 -m venv ./
source markenv/bin/activate
pip3 install -e .
```

#### Update depend python package for requirement.txt
```
pip3 install pipreqs
pipreqs ./ --force
```

#### How to test
test edit movie function
```
python3 -m unittest Tests.videoedit_tests.VideoeditTestCase.test_insert_text
```