## FFmpeg 基础

#### 概述
FFmpeg

一个完整的跨平台解决方案，用于录制，转换和流式传输音频和视频。

* ffmpeg: ffmpeg tool

ffmpeg是一个非常快速的视频和音频转换器，也可以从现场音频/视频源获取。 它还可以在任意采样率之间进行转换，并使用高质量的多相滤波器动态调整视频大小。

* ffplay: ffplay tool

ffplay是一个使用FFmpeg库和SDL库的非常简单的便携式媒体播放器。 它主要用作各种FFmpeg API的测试平台。

* ffprobe: ffprobe tool

ffprobe从多媒体流中收集信息，并以人类和机器可读的方式打印。

* ffserver: ffserver tool

ffserver是音频和视频的流媒体服务器。 它支持多个实时馈送，文件流和实时馈送时移。 如果指定了足够大的Feed存储空间，您可以在每个实时Feed中查找过去的位置。


#### FFmpeg 基础测试
```bash
# 安装 ffmpeg、ffplay、ffprobe、ffserver
$ sudo apt-get install ffmpeg

# 测试视屏文件
$ ll 2924fc6c35ef34424e462f8da07931d2.*
-rw-r--r-- 1 lanzhiwang lanzhiwang 489943 10月 22 15:42 2924fc6c35ef34424e462f8da07931d2.mp4

# 安装 Python 模块
(test_ffmpeg) $ pip freeze
ffmpeg-python==0.1.16
future==0.16.0

# 获取视频分辨率、转码、调整分辨率
(test_ffmpeg) $ python3
Python 3.6.6 (default, Sep 12 2018, 18:26:19) 
[GCC 8.0.1 20180414 (experimental) [trunk revision 259383]] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import ffmpeg
>>> import pprint
>>> pp = pprint.PrettyPrinter()
>>> stream = ffmpeg.probe('./2924fc6c35ef34424e462f8da07931d2.mp4')
>>> type(stream)
<class 'dict'>
# 视频相关信息
>>> pp.pprint(stream)
{'format': {'bit_rate': '568296',
            'duration': '6.897000',
            'filename': './2924fc6c35ef34424e462f8da07931d2.mp4',
            'format_long_name': 'QuickTime / MOV',
            'format_name': 'mov,mp4,m4a,3gp,3g2,mj2',
            'nb_programs': 0,
            'nb_streams': 2,
            'probe_score': 100,
            'size': '489943',
            'start_time': '0.000000',
            'tags': {'compatible_brands': 'isomiso2avc1mp41',
                     'encoder': 'Lavf57.41.100',
                     'major_brand': 'isom',
                     'minor_version': '512'}},
 'streams': [{'avg_frame_rate': '24/1',
              'bit_rate': '498257',
              'bits_per_raw_sample': '8',
              'chroma_location': 'left',
              'codec_long_name': 'H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10',
              'codec_name': 'h264',
              'codec_tag': '0x31637661',
              'codec_tag_string': 'avc1',
              'codec_time_base': '1/48',
              'codec_type': 'video',
              'coded_height': 368,
              'coded_width': 640,
              'display_aspect_ratio': '16:9',
              'disposition': {'attached_pic': 0,
                              'clean_effects': 0,
                              'comment': 0,
                              'default': 1,
                              'dub': 0,
                              'forced': 0,
                              'hearing_impaired': 0,
                              'karaoke': 0,
                              'lyrics': 0,
                              'original': 0,
                              'timed_thumbnails': 0,
                              'visual_impaired': 0},
              'duration': '6.875000',
              'duration_ts': 84480,
              'has_b_frames': 2,
              'height': 368,
              'index': 0,
              'is_avc': 'true',
              'level': 30,
              'nal_length_size': '4',
              'nb_frames': '165',
              'pix_fmt': 'yuv420p',
              'profile': 'High',
              'r_frame_rate': '24/1',
              'refs': 1,
              'sample_aspect_ratio': '46:45',
              'start_pts': 0,
              'start_time': '0.000000',
              'tags': {'handler_name': 'VideoHandler', 'language': 'und'},
              'time_base': '1/12288',
              'width': 640},
             {'avg_frame_rate': '0/0',
              'bit_rate': '63955',
              'bits_per_sample': 0,
              'channel_layout': 'stereo',
              'channels': 2,
              'codec_long_name': 'AAC (Advanced Audio Coding)',
              'codec_name': 'aac',
              'codec_tag': '0x6134706d',
              'codec_tag_string': 'mp4a',
              'codec_time_base': '1/44100',
              'codec_type': 'audio',
              'disposition': {'attached_pic': 0,
                              'clean_effects': 0,
                              'comment': 0,
                              'default': 1,
                              'dub': 0,
                              'forced': 0,
                              'hearing_impaired': 0,
                              'karaoke': 0,
                              'lyrics': 0,
                              'original': 0,
                              'timed_thumbnails': 0,
                              'visual_impaired': 0},
              'duration': '6.872993',
              'duration_ts': 303099,
              'index': 1,
              'max_bit_rate': '64000',
              'nb_frames': '297',
              'profile': 'LC',
              'r_frame_rate': '0/0',
              'sample_fmt': 'fltp',
              'sample_rate': '44100',
              'start_pts': 0,
              'start_time': '0.000000',
              'tags': {'handler_name': 'SoundHandler', 'language': 'und'},
              'time_base': '1/44100'}]}
>>>

# 将 mp4 格式转为 flv 格式，调整分辨率为 640x368
>>> ffmpeg.input('./2924fc6c35ef34424e462f8da07931d2.mp4').output('./2924fc6c35ef34424e462f8da07931d2.flv', format='flv', video_size='640x368', vcodec="copy").run()
# 将 mp4 文件备份为普通文件
>>> ffmpeg.input('./2924fc6c35ef34424e462f8da07931d2.mp4').output('./2924fc6c35ef34424e462f8da07931d2.mp4.bak', format='mp4', video_size='640x368', vcodec="copy").run()
>>> exit()
$ ll 2924fc6c35ef34424e462f8da07931d2.*
-rw-rw-r-- 1 lanzhiwang lanzhiwang 546974 10月 22 16:22 2924fc6c35ef34424e462f8da07931d2.flv
-rw-r--r-- 1 lanzhiwang lanzhiwang 489943 10月 22 15:42 2924fc6c35ef34424e462f8da07931d2.mp4
-rw-rw-r-- 1 lanzhiwang lanzhiwang 545453 10月 22 16:27 2924fc6c35ef34424e462f8da07931d2.mp4.bak

```

#### ffmpeg-python 常见用法

```python
#!/usr/bin/env python
# -*- coding:utf-8 -*-

import ffmpeg

# 获取视频文件分辨率信息
stream = ffmpeg.probe('http://static.grandcloud.cn/www/media/v3/new2/images/video.mp4#http://www.grandcloud.cn/')
coded_width = stream["streams"][0]["coded_width"]
coded_height = stream["streams"][0]["coded_height"]
rst = str(coded_height) + "x" + str(coded_width)  # 字母 x
print(rst)

# 调整分辨率
stream = ffmpeg.zoompan(stream=ffmpeg.input('./video.mp4'), s="640x480")
stream = ffmpeg.output(stream, 'output.mp4')
ffmpeg.run(stream)

# 调整分辨率简单写法
(ffmpeg.input('./video.mp4').output('output.mp4', format='mp4', video_size="640x480").run())


# 指定下载视频文件的大小
ffmpeg.input("rtmp://alsource.rtc.inke.cn/live/1530699745511095").output('output.flv', video_size="640x480", fs="6M" ).run()

# 指定下载视频文件的时长
ffmpeg.input("rtmp://wssource.pull.inke.cn/live/1530749086662633", t=20).output('。/output.flv', video_size="640x480").run()

# 转码 flv 为 mp4
ffmpeg.input("./input.flv").output('./vcode.mp4', format='mp4', video_size="640x480", vcodec="copy").run(overwrite_output=True)

```

#### 从视频中截图
```bash
$ ffmpeg -i 2924fc6c35ef34424e462f8da07931d2.mp4 -r 1 %03d.png
```

#### 总结

```
ffmpeg -i video.mp4 -r 1 -ss 00:00:26 -t 00:00:07 %03d.png

说明：输入一个叫 video.mp4 的文件，让它以每秒一帧的速度，从第 26 秒开始一直截取 7 秒长的时间，截取到的每一幅图像，都用 3 位数字自动生成从小到大的文件名

参数说明:

-i 设定输入流
-r 设定帧速率，也就是提取图像的频率，默认为25
-ss 开始时间
-t 持续时间
```

```
ffmpeg -i video.mp4 -vcodec copy -an video_video.mp4　　//分离视频流

ffmpeg -i video.mp4 -acodec copy -vn video_audio.mp4　　//分离音频流

说明：分离视频音频流

参数说明:

-i 设定输入流
-vcodec 设定视频编解码器，未设定时则使用与输入流相同的编解码器
-an 不处理音频
-acodec 设定声音编解码器，未设定时则使用与输入流相同的编解码器
-vn 不处理视频
```

```
ffmpeg –i test.mp4 -vcodec copy –an –f m4v test.264
ffmpeg –i test.avi -vcodec copy –an –f m4v test.264

说明：视频解复用 (将test.mp4和test.avi两个视频文件合并为一个)

参数说明:
-i 设定输入流
-vcodec 设定视频编解码器，未设定时则使用与输入流相同的编解码器
-an 不处理音频
-f 设定输出格式
```

```
ffmpeg –i test.mp4 -vcodec h264 –s 352*278 –an –f m4v test.264              //将mp4格式的视频文件装码为m4v格式
ffmpeg –i test.mp4 -vcodec h264 –s 352*278 –an –f m4v –bf 0 –g 25 test.264  //将mp4格式的视频文件装码为m4v格式
ffmpeg –i test.avi -vcodec mpeg4 -vtag xvid –qsame test_xvid.avi            //将原视频文件以相同格式封装成另一个文件

说明: 视频转码

参数说明:
-i 设定输入流
-vcodec 设定视频编解码器，未设定时则使用与输入流相同的编解码器
-s 设定画面的宽与高(分辨率)
-an 不处理音频
-f 设定输出格式
-bf B帧数目控制
-g 关键帧间隔控制
-vtag xvid
–qsame
```

```
ffmpeg –i video_file –i audio_file –vcodec copy –acodec copy output_file

说明: 视频封装 (将视频文件和音频文件封装成一个视频文件)

参数说明:

–i 设定输入流
–vcodec 设定视频编解码器，未设定时则使用与输入流相同的编解码器
–acodec 设定声音编解码器，未设定时则使用与输入流相同的编解码器
```

```
ffmpeg –i test.avi –r 1 –f image2 image-%3d.jpeg        //提取图片
ffmpeg -i input.avi -ss 0:1:30 -t 0:0:20 -vcodec copy -acodec copy output.avi    //剪切视频

说明：提取图片，剪切视频

参数说明:

-i 设定输入流
-r 设定帧速率，也就是提取图像的频率，默认为25
-f 设定输出格式
-ss 开始时间
-t 持续时间
–vcodec 设定视频编解码器，未设定时则使用与输入流相同的编解码器
–acodec 设定声音编解码器，未设定时则使用与输入流相同的编解码器
```

```
ffmpeg –i rtsp://192.168.3.205:5555/test –vcodec copy out.avi

说明：在线视频录制

参数说明:

-i 设定输入流
–vcodec 设定视频编解码器，未设定时则使用与输入流相同的编解码器
```

```
ffplay -f rawvideo -video_size 1920x1080 input.yuv

说明：YUV序列播放(使用自带的ffplay播放器播放视频)

参数说明:

-f 设定输出格式
-video_size 视频分辨率

```

```
ffmpeg –i input.yuv –s w*h –pix_fmt yuv420p –vcodec mpeg4 output.avi

说明：YUV序列转AVI

参数说明:

–i 设定输入流
–s 设定画面的宽与高，分辨率控制
–pix_fmt
–vcodec 设定视频编解码器，未设定时则使用与输入流相同的编解码器

```

```
ffmpeg -i input.avi -s 640x480 output.avi

ffmpeg -i input.avi -strict -2 -s vga output.avi


说明: 压缩视频文件
```

```
ffmpeg -re -i localFile.mp4 -c copy -f flv rtmp://server/live/streamName

说明: 将文件当做直播送至live

ffmpeg -i rtmp://server/live/streamName -c copy dump.flv

说明: 将直播媒体保存至本地文件

```













