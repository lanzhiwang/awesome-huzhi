## FFmpeg 基础应用

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

#### FFmpeg 常见用法

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