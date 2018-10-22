## 安卓基本组件

* Activity

Activity为Android应用提供了可视化用户界面(是应用中负责于用户交互的组件)

* Service

Service组件通常位于后台运行，它一般不需要与用户交互，因此Service组件没有图形用户界面。
当一个Service组件被运行起来之后，它将拥有自己独立的生命周期，Service组件通常用于为其它组件提供后台服务或监控其它组件的运行状态。

* BroadcastReceiver

BroadcastReceiver代表广播消息接收器，从代码实现角度来看，其非常类似于事件编程中的监听器，其监听的事件源是Android应用中的其它组件

* ContentProvider

由于Android应用各自运行在自已的Dalvik虚拟机实例中，如果应用之间需要实现实时的数据交换，就要遵循Android系统为这种跨应用的数据交换制定的标准：ContentProvider。
通常与ContentProvider结合使用的是ContentResolver，一个应用程序使用ContentProvider暴露自己的数据，而另 一个应用程序则通过ContentResolver来访问数据。

* View

* Intent

Intent是Android应用内不同组件之间通信的载体，其可用于启动应用中另一个Activity、启动一个Service组件、发送一条广播消息来触发系统中的BroadcastReceiver

## 安卓逆向基础

#### Linux 下开发测试环境部署方法
1. install Java SDK
2. download the SDK Tools（最好使用 android-sdk_r24.0.2-linux.tgz ，24版本支持命令行进行所有操作，也支持界面操作）
3. sdkmanager --list
4. install other tools
5. PATH

```bash
# ./tools/bin/sdkmanager --list
Warning: File /root/.android/repositories.cfg could not be loaded.             
Installed packages:=====================] 100% Computing updates...             
  Path                                                  | Version | Description                                | Location                                             
  -------                                               | ------- | -------                                    | -------                                               
  add-ons;addon-google_apis-google-24                   | 1       | Google APIs                                | add-ons/addon-google_apis-google-24/                 
  build-tools;28.0.2                                    | 28.0.2  | Android SDK Build-Tools 28.0.2             | build-tools/28.0.2/                                   
  emulator                                              | 27.3.9  | Android Emulator                           | emulator/                                             
  patcher;v4                                            | 1       | SDK Patch Applier v4                       | patcher/v4/                                           
  platform-tools                                        | 28.0.0  | Android SDK Platform-Tools                 | platform-tools/                                       
  platforms;android-28                                  | 6       | Android SDK Platform 28                    | platforms/android-28/                                 
  sources;android-28                                    | 1       | Sources for Android 28                     | sources/android-28/                                   
  system-images;android-28;default;x86_64               | 4       | Intel x86 Atom_64 System Image             | system-images/android-28/default/x86_64/             
  system-images;android-28;google_apis;x86_64           | 5       | Google APIs Intel x86 Atom_64 System Image | system-images/android-28/google_apis/x86_64/         
  system-images;android-28;google_apis_playstore;x86_64 | 5       | Google Play Intel x86 Atom_64 System Image | system-images/android-28/google_apis_playstore/x86_64/
  tools                                                 | 26.1.1  | Android SDK Tools 26.1.1                   | tools/                                               

Available Packages:
  Path                                                                                     | Version      | Description                                                         
  -------                                                                                  | -------      | -------                                                             
```

#### 获得 ROOT 权限

##### 方法一：
第一步：Unlock bootloader

第二步：安装 recovery 软件

第三步：安装 Super Su 应用，此时已经获得了 ROOT 权限

第四步：将 ROM 刷入手机

##### 方法二：
直接使用第三方刷机工具包（第三方刷机包也就是将方法一使用到的软件打包在一起使用）

##### 关于 Unlock bootloader

1、检查设备是否支持 Unlock bootloader

2、从官方获取解锁码

3、解锁 bootloader
```bash
$ adb reboot bootloader # 手机进入 fastboot 模式
$ fastboot devices -l

# fastboot oem 相关命令
$ fastboot oem unlock
$ fastboot oem help
```

##### 关于 recovery

1、什么是 recovery

当用户获得设备的更新文件并进行更新时，安卓的recovery系统将会保证正确替换当前镜像，同时不会影响用户数据。

2、官方 recovery 和第三方 recovery

3、常见的第三方 recovery 有 TWRP、CWM、CF等

4、安装 recovery 的方法

方法一：直接使用命令行安装
```bash
下载 twrp-3.1.1-0-eva.img
adb reboot bootloader # 手机进入 fastboot 模式
fastboot flash recovery twrp-3.1.1-0-eva.img
fastboot reboot
```

方法二：使用第三方工具安装
* 使用 Odin（Odin 是用于三星设备 recovery 最流行的工具之一）
* 使用 Heimdall
* 使用 hisuite（用于华为设备）

##### 关于Super Su 应用

1、下载 Super Su 应用

2、adb push UPDATE-SuperSU-v1.94.zip /sdcard

3、adb reboot recovery

4、手机界面安装


##### 关于ROM

1、官方ROM（也叫 OEM ）和第三方ROM（也叫 AOSP ）

2、常见第三方ROM有 CyanogenMod、Stock Android、LineageOS、Kali Linux on Android

3、刷入ROM
* 下载 ROM
* adb push lineage-14.1-20180823-nightly-flo-signed.zip /sdcard
* adb reboot recovery
* 手机界面安装


##### 在安卓设备上安装 Linux 操作系统

1、Kali Linux on Android using Linux Deploy
note：
* Linux Deploy 是一个普通的APK应用
* https://www.kali.org/tutorials/kali-linux-android-linux-deploy/

#### 基本逆向操作
```bash
# 工作目录中存在待运行的 apk 文件
# 3a7f459a4f8d6716d68e5df63f611b8b.apk 是待运行的apk文件
# vpn.apk 用于抓包
# 所有的apk文件都要有执行权限
lanzhiwang@lanzhiwang-dev:~/work/adb_work$ ll
total 44788
drwxrwxr-x 2 lanzhiwang lanzhiwang     4096 7月  24 14:11 ./
drwxr-xr-x 7 lanzhiwang lanzhiwang     4096 7月  24 14:09 ../
-rw-rw-r-- 1 lanzhiwang lanzhiwang 42848622 7月  12 16:53 3a7f459a4f8d6716d68e5df63f611b8b.apk
-rwxrwxr-x 1 lanzhiwang lanzhiwang  2994825 7月  20 10:41 vpn.apk*
lanzhiwang@lanzhiwang-dev:~/work/adb_work$

# 获取apk文件的包名和主应用名
lanzhiwang@lanzhiwang-dev:~/work/adb_work$ aapt dump badging 3a7f459a4f8d6716d68e5df63f611b8b.apk
package: name='com.subject.ysh' versionCode='20170401' versionName='2.3' platformBuildVersionName='5.1.1-1819727'

application-label-th:'原始会'
application-label-tl:'原始会'
application-label-tr:'原始会'
application-label-uk:'原始会'
application-label-ur-PK:'原始会'
application-label-uz-UZ:'原始会'
application-label-vi:'原始会'
application-label-zh-CN:'原始会'
application-label-zh-HK:'原始会'
application-label-zh-TW:'原始会'
application-label-zu:'原始会'
application-icon-160:'res/drawable-hdpi-v4/ic_launcher.png'
application-icon-240:'res/drawable-hdpi-v4/ic_launcher.png'
application-icon-320:'res/drawable-xhdpi-v4/ic_launcher.png'
application-icon-480:'res/drawable-xxhdpi-v4/ic_launcher.png'
application-icon-640:'res/drawable-xxhdpi-v4/ic_launcher.png'
application: label='原始会' icon='res/drawable-hdpi-v4/ic_launcher.png'
launchable-activity: name='com.subject.ysh.activity.SplashActivity'  label='' icon=''
feature-group: label=''
  uses-feature: name='android.hardware.bluetooth'
  uses-implied-feature: name='android.hardware.bluetooth' reason='requested android.permission.BLUETOOTH permission, requested android.permission.BLUETOOTH_ADMIN permission, and targetSdkVersion > 4'
  uses-feature: name='android.hardware.camera'
  uses-implied-feature: name='android.hardware.camera' reason='requested android.permission.CAMERA permission'
  uses-feature: name='android.hardware.location'
  uses-implied-feature: name='android.hardware.location' reason='requested android.permission.ACCESS_COARSE_LOCATION permission, requested android.permission.ACCESS_FINE_LOCATION permission, and requested android.permission.ACCESS_LOCATION_EXTRA_COMMANDS permission'
  uses-feature: name='android.hardware.location.gps'
  uses-implied-feature: name='android.hardware.location.gps' reason='requested android.permission.ACCESS_FINE_LOCATION permission'
  uses-feature: name='android.hardware.location.network'
  uses-implied-feature: name='android.hardware.location.network' reason='requested android.permission.ACCESS_COARSE_LOCATION permission'
  uses-feature: name='android.hardware.microphone'
  uses-implied-feature: name='android.hardware.microphone' reason='requested android.permission.RECORD_AUDIO permission'
  uses-feature: name='android.hardware.screen.landscape'
  uses-implied-feature: name='android.hardware.screen.landscape' reason='one or more activities have specified a landscape orientation'
  uses-feature: name='android.hardware.screen.portrait'
  uses-implied-feature: name='android.hardware.screen.portrait' reason='one or more activities have specified a portrait orientation'
  uses-feature: name='android.hardware.telephony'
  uses-implied-feature: name='android.hardware.telephony' reason='requested a telephony permission'
  uses-feature: name='android.hardware.touchscreen'
  uses-implied-feature: name='android.hardware.touchscreen' reason='default feature for all apps'
  uses-feature: name='android.hardware.wifi'
  uses-implied-feature: name='android.hardware.wifi' reason='requested android.permission.ACCESS_WIFI_STATE permission, and requested android.permission.CHANGE_WIFI_STATE permission'
main
other-activities
other-receivers
other-services
supports-screens: 'small' 'normal' 'large' 'xlarge'
supports-any-density: 'true'
locales: 'af' 'am' 'ar' 'bg' 'bn-BD' 'ca' 'cs' 'da' 'de' 'el' 'en-GB' 'en-IN' 'es' 'es-US' 'et-EE' 'eu-ES' 'fa' 'fi' 'fr' 'fr-CA' 'gl-ES' 'hi' 'hr' 'hu' 'hy-AM' 'in' 'is-IS' 'it' 'iw' 'ja' 'ka-GE' 'kk-KZ' 'km-KH' 'kn-IN' 'ko' 'ky-KG' 'lo-LA' 'lt' 'lv' 'mk-MK' 'ml-IN' 'mn-MN' 'mr-IN' 'ms-MY' 'my-MM' 'nb' 'ne-NP' 'nl' 'pl' 'pt' 'pt-PT' 'ro' 'ru' 'ru-RU' 'si-LK' 'sk' 'sl' 'sr' 'sv' 'sw' 'ta-IN' 'te-IN' 'th' 'tl' 'tr' 'uk' 'ur-PK' 'uz-UZ' 'vi' 'zh-CN' 'zh-HK' 'zh-TW' 'zu'
densities: '160' '240' '320' '480' '640'
native-code: 'arm64-v8a' 'armeabi' 'armeabi-v7a' 'mips' 'x86'
lanzhiwang@lanzhiwang-dev:~/work/adb_work$
############################################################################
lanzhiwang@lanzhiwang-dev:~/work/adb_work$ aapt dump badging vpn.apk
package: name='com.jude.interceptor' versionCode='1' versionName='1.0' platformBuildVersionName='6.0-2166767'
...
launchable-activity: name='com.jude.interceptor.ui.MainActivity'  label='影墙' icon=''
lanzhiwang@lanzhiwang-dev:~/work/adb_work$

# 获取连接的手机设备或者模拟器
lanzhiwang@lanzhiwang-dev:~/work/adb_work$ adb devices
List of devices attached
48db50a5b827    device

lanzhiwang@lanzhiwang-dev:~/work/adb_work$

# 查看手机上已经安装的软件包
lanzhiwang@lanzhiwang-dev:~/work/adb_work$ adb shell pm list packages -f | grep package:/data/
package:/data/dataapp/SohuNewsClient.apk=com.sohu.newsclient
package:/data/dataapp/UCBrowser.apk=com.UCMobile
package:/data/dataapp/CTAccount.apk=cn.com.chinatelecom.account
package:/data/dataapp/pre_enavi.apk=com.pdager
package:/data/dataapp/Qunar.apk=com.Qunar
package:/data/dataapp/ctclient.apk=com.ct.client
package:/data/dataapp/esurfing_WiFi.apk=com.akazam.android.wlandialer
package:/data/dataapp/SurfingClientKefu.apk=com.surfing.kefu
package:/data/dataapp/BestPay.apk=com.chinatelecom.bestpayclient
package:/data/dataapp/ReadingJoy.apk=com.iyd.reader.ReadingJoy
package:/data/dataapp/TYYD.apk=com.lectek.android.sfreader
package:/data/dataapp/icity.apk=cn.ffcs.wisdom.city
package:/data/dataapp/QYVideoClient.apk=com.qiyi.video
package:/data/dataapp/CTWallet.apk=chinatelecom.mwallet
package:/data/dataapp/cloud189.apk=com.cn21.ecloud
package:/data/dataapp/Huawei_eStore.apk=com.eshore.ezone
package:/data/dataapp/Huawei_Besttone.apk=com.besttone.hall
package:/data/dataapp/mail189.apk=com.corp21cn.mail189
package:/data/dataapp/pim.apk=com.chinatelecom.pim
package:/data/dataapp/libao.apk=com.corp21cn.flowpay
package:/data/dataapp/QQBrowser.apk=com.tencent.mtt
package:/data/dataapp/GaoDeMAP.apk=com.autonavi.minimap
package:/data/dataapp/iCartoon.apk=com.erdo.android.FJDXCartoon
package:/data/dataapp/egame.apk=cn.egame.terminal.client4g
package:/data/dataapp/TencentVideo.apk=com.tencent.qqlive
package:/data/dataapp/Com_TYSX_IKAN.apk=com.telecom.video.ikan4g
package:/data/dataapp/yixin.apk=im.yixin
package:/data/dataapp/yingyongbao.apk=com.tencent.android.qqplaza
package:/data/dataapp/PhotoShare.apk=com.huawei.gallery.photoshare
package:/data/dataapp/ITING.apk=com.imusic.iting
package:/data/dataapp/taobao.apk=com.taobao.taobao
lanzhiwang@lanzhiwang-dev:~/work/adb_work$

# 安装apk文件
lanzhiwang@lanzhiwang-dev:~/work/adb_work$ adb -s 48db50a5b827 install ./vpn.apk
256 KB/s (2994825 bytes in 11.388s)
    pkg: /data/local/tmp/vpn.apk
Success
lanzhiwang@lanzhiwang-dev:~/work/adb_work$

# 查看是否安装成功
lanzhiwang@lanzhiwang-dev:~/work/adb_work$ adb shell pm list packages -f | grep com.jude.interceptor
package:/data/app/com.jude.interceptor-1.apk=com.jude.interceptor
lanzhiwang@lanzhiwang-dev:~/work/adb_work$

lanzhiwang@lanzhiwang-dev:~/work/adb_work$ adb -s 48db50a5b827 install ./3a7f459a4f8d6716d68e5df63f611b8b.apk
279 KB/s (42848622 bytes in 149.798s)
    pkg: /data/local/tmp/3a7f459a4f8d6716d68e5df63f611b8b.apk
Success
lanzhiwang@lanzhiwang-dev:~/work/adb_work$

lanzhiwang@lanzhiwang-dev:~/work/adb_work$ adb shell pm list packages -f | grep com.subject.ysh
package:/data/app/com.subject.ysh-1.apk=com.subject.ysh
lanzhiwang@lanzhiwang-dev:~/work/adb_work$

lanzhiwang@lanzhiwang-dev:~/work/adb_work$ adb -s 48db50a5b827 shell pm list packages -3
package:com.subject.ysh
package:com.jude.interceptor
lanzhiwang@lanzhiwang-dev:~/work/adb_work$


# 启动抓包服务
lanzhiwang@lanzhiwang-dev:~/work/adb_work$ adb -s 48db50a5b827 shell am startservice -n com.jude.interceptor/.ui.MyService --ei cmd 1
Starting service: Intent { cmp=com.jude.interceptor/.ui.MyService (has extras) }

# 停止抓包服务
lanzhiwang@lanzhiwang-dev:~/work/adb_work$ adb -s 48db50a5b827 shell am startservice -n com.jude.interceptor/.ui.MyService --ei cmd 2
Starting service: Intent { cmp=com.jude.interceptor/.ui.MyService (has extras) }

lanzhiwang@lanzhiwang-dev:~/work/adb_work$ adb -s 48db50a5b827 shell am startservice -n com.jude.interceptor/.ui.MyService --ei cmd 1
Starting service: Intent { cmp=com.jude.interceptor/.ui.MyService (has extras) }
lanzhiwang@lanzhiwang-dev:~/work/adb_work$

# 查看抓包服务是否运行成功
lanzhiwang@lanzhiwang-dev:~/work/adb_work$ adb -s 48db50a5b827 shell ps | grep "com.jude.interceptor"
u0_a128   10839 269   952880 56472 ffffffff 00000000 S com.jude.interceptor
lanzhiwang@lanzhiwang-dev:~/work/adb_work$

# 启动待运行的apk应用
lanzhiwang@lanzhiwang-dev:~/work/adb_work$ adb -s 48db50a5b827 shell am start -n com.subject.ysh/com.subject.ysh.activity.SplashActivity
Starting: Intent { cmp=com.subject.ysh/.activity.SplashActivity }
lanzhiwang@lanzhiwang-dev:~/work/adb_work$

# 查看应用运行是否成功
lanzhiwang@lanzhiwang-dev:~/work/adb_work$ adb -s 48db50a5b827 shell ps | grep "com.subject.ysh"
u0_a129   11172 269   980728 71152 ffffffff 00000000 S com.subject.ysh
u0_a129   11225 269   896892 39920 ffffffff 00000000 S com.subject.ysh:bdservice_v1
lanzhiwang@lanzhiwang-dev:~/work/adb_work$


# 模拟点击应用n次
lanzhiwang@lanzhiwang-dev:~/work/adb_work$ adb -s 48db50a5b827 shell monkey -p com.jude.interceptor --pct-touch 100 100
Events injected: 100
## Network stats: elapsed time=350ms (0ms mobile, 0ms wifi, 350ms not connected)

lanzhiwang@lanzhiwang-dev:~/work/adb_work$ adb -s 48db50a5b827 shell monkey -p com.jude.interceptor --pct-touch 100 100
Events injected: 100
## Network stats: elapsed time=192ms (0ms mobile, 0ms wifi, 192ms not connected)

lanzhiwang@lanzhiwang-dev:~/work/adb_work$ adb -s 48db50a5b827 shell monkey -p com.jude.interceptor --pct-touch 100 100
Events injected: 100
## Network stats: elapsed time=435ms (0ms mobile, 0ms wifi, 435ms not connected)

lanzhiwang@lanzhiwang-dev:~/work/adb_work$ adb -s 48db50a5b827 shell monkey -p com.jude.interceptor --pct-touch 100 100
Events injected: 100
## Network stats: elapsed time=452ms (0ms mobile, 0ms wifi, 452ms not connected)

lanzhiwang@lanzhiwang-dev:~/work/adb_work$ adb -s 48db50a5b827  shell input tap 623 1076
lanzhiwang@lanzhiwang-dev:~/work/adb_work$ adb -s 48db50a5b827  shell input tap 623 1076


# 对应用进行截屏操作
lanzhiwang@lanzhiwang-dev:~$ adb -s 48db50a5b827 shell screencap -p /sdcard/3a7f459a4f8d6716d68e5df63f611b8b.png
lanzhiwang@lanzhiwang-dev:~$ adb -s 48db50a5b827 shell screencap -p /sdcard/3a7f459a4f8d6716d68e5df63f611b8b_01.png
lanzhiwang@lanzhiwang-dev:~$ adb -s 48db50a5b827 shell screencap -p /sdcard/3a7f459a4f8d6716d68e5df63f611b8b_02.png
lanzhiwang@lanzhiwang-dev:~$

# 查看相关截屏后的文件
lanzhiwang@lanzhiwang-dev:~$ adb -s 48db50a5b827 shell ls /sdcard/3a7f459a4f8d6716d68e5df63f611b8b.png
/sdcard/3a7f459a4f8d6716d68e5df63f611b8b.png
lanzhiwang@lanzhiwang-dev:~$
lanzhiwang@lanzhiwang-dev:~$ adb -s 48db50a5b827 shell ls /sdcard/3a7f459a4f8d6716d68e5df63f611b8b_01.png
/sdcard/3a7f459a4f8d6716d68e5df63f611b8b_01.png
lanzhiwang@lanzhiwang-dev:~$


# 将截屏文件上传到本地
lanzhiwang@lanzhiwang-dev:~$ adb -s 48db50a5b827 pull /sdcard/3a7f459a4f8d6716d68e5df63f611b8b.png
./3a7f459a4f8d6716d68e5df63f611b8b.png
309 KB/s (109604 bytes in 0.345s)
lanzhiwang@lanzhiwang-dev:~$


# 查看产生的pcap包 
lanzhiwang@lanzhiwang-dev:~$ adb -s 48db50a5b827 shell ls /sdcard/PacketCap
20180724_032636.pcap
# 将pcap包上传到本地
lanzhiwang@lanzhiwang-dev:~$ adb -s 48db50a5b827 pull  /sdcard/PacketCap/20180724_032636.pcap ./20180724_032636.pcap
62 KB/s (6236 bytes in 0.097s)
lanzhiwang@lanzhiwang-dev:~$ 

# 删除产生的截屏文件和pcap文件
lanzhiwang@lanzhiwang-dev:~$ adb -s 48db50a5b827 shell rm -f /sdcard/PacketCap/20180724_032636.pcap
lanzhiwang@lanzhiwang-dev:~$ adb -s 48db50a5b827 shell rm -f /sdcard/3a7f459a4f8d6716d68e5df63f611b8b.png  
lanzhiwang@lanzhiwang-dev:~$ adb -s 48db50a5b827 shell rm -f /sdcard/3a7f459a4f8d6716d68e5df63f611b8b_01.png
lanzhiwang@lanzhiwang-dev:~$ adb -s 48db50a5b827 shell rm -f /sdcard/3a7f459a4f8d6716d68e5df63f611b8b_02.png
lanzhiwang@lanzhiwang-dev:~$
 


# 查看网络请求的端口号
lanzhiwang@lanzhiwang-dev:~$ adb -s 48db50a5b827 shell cat /proc/self/net/tcp
  sl  local_address rem_address   st tx_queue rx_queue tr tm->when retrnsmt   uid  timeout inode                                                     
lanzhiwang@lanzhiwang-dev:~$  
lanzhiwang@lanzhiwang-dev:~$ adb -s 48db50a5b827 shell cat /proc/self/net/tcp6
  sl  local_address                         remote_address                        st tx_queue rx_queue tr tm->when retrnsmt   uid  timeout inode
   0: 0000000000000000FFFF000003231BAC:9EB7 0000000000000000FFFF0000762B110E:0050 01 00000000:00000000 00:00000000 00000000  1000        0 82839 1 00000000 23 4 24 10 -1
   1: 0000000000000000FFFF000003231BAC:EBEF 0000000000000000FFFF00003D3E4E75:01BB 01 00000000:00000000 00:00000000 00000000  1000        0 94422 1 00000000 21 4 0 10 -1
   2: 0000000000000000FFFF000003231BAC:DE7E 0000000000000000FFFF000081450D1F:0050 01 00000000:00000000 00:00000000 00000000  1000        0 96658 1 00000000 21 0 0 10 -1
   3: 0000000000000000FFFF000003231BAC:9EB5 0000000000000000FFFF0000762B110E:0050 01 00000000:00000000 00:00000000 00000000  1000        0 91476 1 00000000 27 4 24 10 -1
   4: 0000000000000000FFFF000003231BAC:89B1 0000000000000000FFFF000030120431:01BB 01 00000000:00000000 00:00000000 00000000 10070        0 91275 1 00000000 21 4 0 10 -1
   5: 0000000000000000FFFF000003231BAC:9EB8 0000000000000000FFFF0000762B110E:0050 01 00000000:00000000 00:00000000 00000000  1000        0 89376 1 00000000 21 4 24 19 16
   6: 0000000000000000FFFF000003231BAC:8974 0000000000000000FFFF000030120431:01BB 01 00000000:00000000 00:00000000 00000000 10070        0 72260 1 00000000 24 4 0 10 -1
   7: 0000000000000000FFFF000003231BAC:BA41 0000000000000000FFFF00003D37C276:01BB 01 00000000:00000000 00:00000000 00000000  1000        0 86823 1 00000000 21 4 8 10 -1
   8: 0000000000000000FFFF000003231BAC:9EBB 0000000000000000FFFF0000762B110E:0050 01 00000000:00000000 00:00000000 00000000  1000        0 90404 1 00000000 21 4 24 19 16
   9: 0000000000000000FFFF000003231BAC:CDC0 0000000000000000FFFF00006839C276:1467 01 00000000:00000000 00:00000000 00000000  1000        0 102080 1 00000000 378 4 14 4 -1
lanzhiwang@lanzhiwang-dev:~$

# 停止apk应用
lanzhiwang@lanzhiwang-dev:~$ adb -s 48db50a5b827 shell am force-stop com.subject.ysh
lanzhiwang@lanzhiwang-dev:~$
# 卸载apk应用  
lanzhiwang@lanzhiwang-dev:~$ adb -s 48db50a5b827 uninstall com.subject.ysh
Success
lanzhiwang@lanzhiwang-dev:~$  
lanzhiwang@lanzhiwang-dev:~$ adb -s 48db50a5b827 shell pm list packages -f | grep com.subject.ysh
lanzhiwang@lanzhiwang-dev:~$


lanzhiwang@lanzhiwang-dev:~/work/adb_work$ ll
total 45240
drwxrwxr-x 2 lanzhiwang lanzhiwang     4096 7月  24 16:05 ./
drwxr-xr-x 7 lanzhiwang lanzhiwang     4096 7月  24 14:09 ../
-rw-r--r-- 1 lanzhiwang lanzhiwang     6236 7月  24 15:32 20180724_032636.pcap
-rw-r--r-- 1 lanzhiwang lanzhiwang   172032 7月  24 15:10 3a7f459a4f8d6716d68e5df63f611b8b_01.png
-rw-r--r-- 1 lanzhiwang lanzhiwang   109604 7月  24 15:29 3a7f459a4f8d6716d68e5df63f611b8b_02.png
-rwxrwxr-x 1 lanzhiwang lanzhiwang 42848622 7月  12 16:53 3a7f459a4f8d6716d68e5df63f611b8b.apk*
-rw-r--r-- 1 lanzhiwang lanzhiwang   172032 7月  24 15:10 3a7f459a4f8d6716d68e5df63f611b8b.png
-rwxrwxr-x 1 lanzhiwang lanzhiwang  2994825 7月  20 10:41 vpn.apk*
lanzhiwang@lanzhiwang-dev:~/work/adb_work$
```

#### 反编译 APK 文件
```bash
$ ll
total 41860
drwxrwxr-x 3 lanzhiwang lanzhiwang     4096 7月  25 19:37 ./
drwxr-xr-x 8 lanzhiwang lanzhiwang     4096 7月  25 19:36 ../
-rwxrwxr-x 1 lanzhiwang lanzhiwang 42848622 7月  25 19:36 3a7f459a4f8d6716d68e5df63f611b8b.apk*
drwxrwxr-x 2 lanzhiwang lanzhiwang     4096 7月  25 19:37 out_dir/
$
$ apktool d -f ./3a7f459a4f8d6716d68e5df63f611b8b.apk -o ./out_dir/ -p ./out_dir/
I: Using Apktool 2.3.3 on 3a7f459a4f8d6716d68e5df63f611b8b.apk
I: Loading resource table...
I: Decoding AndroidManifest.xml with resources...
I: Loading resource table from file: ./out_dir/1.apk
I: Regular manifest package...
I: Decoding file-resources...
W: Cant find 9patch chunk in file: "drawable-hdpi-v4/show_head_toast_bg.9.PNG". Renaming it to *.png.
I: Decoding values */* XMLs...
I: Baksmaling classes.dex...
I: Baksmaling classes2.dex...
I: Copying assets and libs...
I: Copying unknown files...
I: Copying original files...
$ ll
total 41860
drwxrwxr-x 3 lanzhiwang lanzhiwang     4096 7月  25 19:38 ./
drwxr-xr-x 8 lanzhiwang lanzhiwang     4096 7月  25 19:36 ../
-rwxrwxr-x 1 lanzhiwang lanzhiwang 42848622 7月  25 19:36 3a7f459a4f8d6716d68e5df63f611b8b.apk*
drwxrwxr-x 9 lanzhiwang lanzhiwang     4096 7月  25 19:38 out_dir/
$ ll out_dir/
total 1720
drwxrwxr-x   9 lanzhiwang lanzhiwang    4096 7月  25 19:38 ./
drwxrwxr-x   3 lanzhiwang lanzhiwang    4096 7月  25 19:38 ../
-rw-rw-r--   1 lanzhiwang lanzhiwang 1684017 7月  25 19:38 1.apk
-rw-rw-r--   1 lanzhiwang lanzhiwang   23635 7月  25 19:38 AndroidManifest.xml
-rw-rw-r--   1 lanzhiwang lanzhiwang    9800 7月  25 19:38 apktool.yml
drwxrwxr-x   9 lanzhiwang lanzhiwang    4096 7月  25 19:38 assets/
drwxrwxr-x   7 lanzhiwang lanzhiwang    4096 7月  25 19:38 lib/
drwxrwxr-x   3 lanzhiwang lanzhiwang    4096 7月  25 19:38 original/
drwxrwxr-x 116 lanzhiwang lanzhiwang    4096 7月  25 19:38 res/
drwxrwxr-x  11 lanzhiwang lanzhiwang    4096 7月  25 19:38 smali/
drwxrwxr-x   4 lanzhiwang lanzhiwang    4096 7月  25 19:38 smali_classes2/
drwxrwxr-x   3 lanzhiwang lanzhiwang    4096 7月  25 19:38 unknown/
$
```


#### 命令行编译安卓应用

```bash
查看当前拥有的API的id号
root@1cdcb6828dd7:~# /usr/local/android-sdk/tools/android list target
Available Android targets:
----------
id: 1 or "android-19"
     Name: Android 4.4.2
     Type: Platform
     API level: 19
     Revision: 4
     Skins: WVGA800 (default), WXGA800-7in, WSVGA, WXGA800, WVGA854, WXGA720, WQVGA400, WQVGA432, HVGA, QVGA
 Tag/ABIs : default/armeabi-v7a, default/x86
----------
id: 2 or "android-21"
     Name: Android 5.0.1
     Type: Platform
     API level: 21
     Revision: 2
     Skins: WVGA800 (default), WXGA800-7in, WSVGA, WXGA800, WVGA854, WXGA720, WQVGA400, WQVGA432, HVGA, QVGA
 Tag/ABIs : default/armeabi-v7a, default/x86
----------
id: 3 or "android-22"
     Name: Android 5.1.1
     Type: Platform
     API level: 22
     Revision: 2
     Skins: WVGA800 (default), WXGA800-7in, WSVGA, WXGA800, WVGA854, WXGA720, WQVGA400, WQVGA432, HVGA, QVGA
 Tag/ABIs : default/armeabi-v7a, default/x86
root@1cdcb6828dd7:~#

创建简单的android项目
root@1cdcb6828dd7:~/AndroidStutio# /usr/local/android-sdk/tools/android create project --target android-22 --name demo --path ./demo --activity MainActivity --package com.demo.www
Created project directory: ./demo
Created directory /root/AndroidStutio/demo/src/com/demo/www
Added file ./demo/src/com/demo/www/MainActivity.java
Created directory /root/AndroidStutio/demo/res
Created directory /root/AndroidStutio/demo/bin
Created directory /root/AndroidStutio/demo/libs
Created directory /root/AndroidStutio/demo/res/values
Added file ./demo/res/values/strings.xml
Created directory /root/AndroidStutio/demo/res/layout
Added file ./demo/res/layout/main.xml
Created directory /root/AndroidStutio/demo/res/drawable-xhdpi
Created directory /root/AndroidStutio/demo/res/drawable-hdpi
Created directory /root/AndroidStutio/demo/res/drawable-mdpi
Created directory /root/AndroidStutio/demo/res/drawable-ldpi
Added file ./demo/AndroidManifest.xml
Added file ./demo/build.xml
Added file ./demo/proguard-project.txt
root@1cdcb6828dd7:~/AndroidStutio#
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio$ tree -a demo/
demo/
├── AndroidManifest.xml
├── ant.properties
├── bin
├── build.xml
├── libs
├── local.properties
├── proguard-project.txt
├── project.properties
├── res
│   ├── drawable-hdpi
│   │   └── ic_launcher.png
│   ├── drawable-ldpi
│   │   └── ic_launcher.png
│   ├── drawable-mdpi
│   │   └── ic_launcher.png
│   ├── drawable-xhdpi
│   │   └── ic_launcher.png
│   ├── layout
│   │   └── main.xml
│   └── values
│       └── strings.xml
└── src
    └── com
        └── demo
            └── www
                └── MainActivity.java

13 directories, 13 files
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio$
编译资源生成R.java文件
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$ mkdir gen
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$ aapt package -f -M ./AndroidManifest.xml -S ./res/ -J ./gen/ -m -I /usr/local/android-sdk/platforms/android-22/android.jar
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$ git status
On branch master
Untracked files:
  (use "git add <file>..." to include in what will be committed)

    gen/

nothing added to commit but untracked files present (use "git add" to track)
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$ tree -a gen/
gen/
└── com
    └── demo
        └── www
            └── R.java

3 directories, 1 file
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$
将 .java 文件编译成 .class 文件
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$ javac -encoding UTF-8 -target 1.8 -bootclasspath /usr/local/android-sdk/platforms/android-22/android.jar -d bin ./src/com/demo/www/*.java ./gen/com/demo/www/R.java
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$ git status
On branch master
Untracked files:
  (use "git add <file>..." to include in what will be committed)

    bin/
    gen/

nothing added to commit but untracked files present (use "git add" to track)
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$ tree -a gen/
gen/
└── com
    └── demo
        └── www
            └── R.java

3 directories, 1 file
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$ tree -a bin/
bin/
└── com
    └── demo
        └── www
            ├── MainActivity.class
            ├── R$attr.class
            ├── R.class
            ├── R$drawable.class
            ├── R$layout.class
            └── R$string.class

3 directories, 6 files
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$ git add .
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$ git commit -m "aapt and javac"
[master 9850161] aapt and javac
 7 files changed, 22 insertions(+)
 create mode 100644 bin/com/demo/www/MainActivity.class
 create mode 100644 bin/com/demo/www/R$attr.class
 create mode 100644 bin/com/demo/www/R$drawable.class
 create mode 100644 bin/com/demo/www/R$layout.class
 create mode 100644 bin/com/demo/www/R$string.class
 create mode 100644 bin/com/demo/www/R.class
 create mode 100644 gen/com/demo/www/R.java
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$
将 .class 文件编译成 .dex 文件
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$ dx --dex --output=./bin/classes.dex ./bin/
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$ git status
On branch master
Untracked files:
  (use "git add <file>..." to include in what will be committed)

    bin/classes.dex

nothing added to commit but untracked files present (use "git add" to track)
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$
将资源文件初始化
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$ mkdir assets
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$ aapt package -f -M ./AndroidManifest.xml -S ./res/ -A ./assets/ -I /usr/local/android-sdk/platforms/android-22/android.jar -F ./bin/resources
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$ git status
On branch master
Untracked files:
  (use "git add <file>..." to include in what will be committed)

    bin/classes.dex
    bin/resources

nothing added to commit but untracked files present (use "git add" to track)
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$
打包生产APK包
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$ java -cp /usr/local/android-sdk-linux/tools/lib/sdklib.jar com.android.sdklib.build.ApkBuilderMain ./Demo.apk -v -u -z ./bin/resources -f ./bin/classes.dex -rf src

THIS TOOL IS DEPRECATED. See --help for more information.

Packaging Demo.apk
./bin/resources:
=> AndroidManifest.xml
=> res/drawable-hdpi-v4/ic_launcher.png
=> res/drawable-ldpi-v4/ic_launcher.png
=> res/drawable-mdpi-v4/ic_launcher.png
=> res/drawable-xhdpi-v4/ic_launcher.png
=> res/layout/main.xml
=> resources.arsc
./bin/classes.dex => classes.dex
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$ git status
On branch master
Untracked files:
  (use "git add <file>..." to include in what will be committed)

    Demo.apk
    bin/classes.dex
    bin/resources

nothing added to commit but untracked files present (use "git add" to track)
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$
生成私钥用于签名
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$ keytool -genkey -v -keystore my-release-key.jks -keyalg RSA -keysize 2048 -validity 10000 -alias my-alias
Enter keystore password: 
Re-enter new password:
What is your first and last name?
  [Unknown]:  lanzhiwang
What is the name of your organizational unit?
  [Unknown]:  Technical Support
What is the name of your organization?
  [Unknown]:  lanzhiwang
What is the name of your City or Locality?
  [Unknown]:  wuhan
What is the name of your State or Province?
  [Unknown]:  hubei
What is the two-letter country code for this unit?
  [Unknown]:  china
Is CN=lanzhiwang, OU=Technical Support, O=lanzhiwang, L=wuhan, ST=hubei, C=china correct?
  [no]:  yes

Generating 2,048 bit RSA key pair and self-signed certificate (SHA256withRSA) with a validity of 10,000 days
    for: CN=lanzhiwang, OU=Technical Support, O=lanzhiwang, L=wuhan, ST=hubei, C=china
Enter key password for <my-alias>
    (RETURN if same as keystore password): 
Re-enter new password:
[Storing my-release-key.jks]

Warning:
The JKS keystore uses a proprietary format. It is recommended to migrate to PKCS12 which is an industry standard format using "keytool -importkeystore -srckeystore my-release-key.jks -destkeystore my-release-key.jks -deststoretype pkcs12".
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$ git status
On branch master
Untracked files:
  (use "git add <file>..." to include in what will be committed)

    Demo.apk
    bin/classes.dex
    bin/resources
    my-release-key.jks

nothing added to commit but untracked files present (use "git add" to track)
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$
使用 zipalign 对齐未签署的 APK
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$ zipalign -v -p 4 Demo.apk Demo-aligned.apk
Verifying alignment of Demo-aligned.apk (4)...
      53 AndroidManifest.xml (OK - compressed)
     708 res/drawable-hdpi-v4/ic_launcher.png (OK)
    8652 res/drawable-ldpi-v4/ic_launcher.png (OK)
   11116 res/drawable-mdpi-v4/ic_launcher.png (OK)
   15692 res/drawable-xhdpi-v4/ic_launcher.png (OK)
   27886 res/layout/main.xml (OK - compressed)
   28260 resources.arsc (OK)
   29937 classes.dex (OK - compressed)
Verification succesful
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$ git status
On branch master
Untracked files:
  (use "git add <file>..." to include in what will be committed)

    Demo-aligned.apk
    Demo.apk
    bin/classes.dex
    bin/resources
    my-release-key.jks

nothing added to commit but untracked files present (use "git add" to track)
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$
通过 apksigner 使用私钥签署 APK
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$ apksigner sign --ks my-release-key.jks --out Demo-release.apk Demo-aligned.apk
Keystore password for signer #1:
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$ git status
On branch master
Untracked files:
  (use "git add <file>..." to include in what will be committed)

    Demo-aligned.apk
    Demo-release.apk
    Demo.apk
    bin/classes.dex
    bin/resources
    my-release-key.jks

nothing added to commit but untracked files present (use "git add" to track)
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$
验证 APK 是否已签署
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$ apksigner verify Demo-release.apk
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$ git status
On branch master
Untracked files:
  (use "git add <file>..." to include in what will be committed)

    Demo-aligned.apk
    Demo-release.apk
    Demo.apk
    bin/classes.dex
    bin/resources
    my-release-key.jks

nothing added to commit but untracked files present (use "git add" to track)
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$
解压APK文件验证
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$ mkdir unzip_apk
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$ cp Demo-release.apk ./unzip_apk/Demo-release.zip
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$ cd unzip_apk
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo/unzip_apk$ ll
total 52
drwxrwxr-x  2 lanzhiwang lanzhiwang  4096 8月  15 19:44 ./
drwxr-xr-x 10 lanzhiwang lanzhiwang  4096 8月  15 19:44 ../
-rw-rw-r--  1 lanzhiwang lanzhiwang 41761 8月  15 19:44 Demo-release.zip
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo/unzip_apk$ unzip Demo-release.zip
Archive:  Demo-release.zip
  inflating: AndroidManifest.xml     
 extracting: res/drawable-hdpi-v4/ic_launcher.png 
 extracting: res/drawable-ldpi-v4/ic_launcher.png 
 extracting: res/drawable-mdpi-v4/ic_launcher.png 
 extracting: res/drawable-xhdpi-v4/ic_launcher.png 
  inflating: res/layout/main.xml     
 extracting: resources.arsc         
  inflating: classes.dex             
  inflating: META-INF/MY-ALIAS.SF   
  inflating: META-INF/MY-ALIAS.RSA   
  inflating: META-INF/MANIFEST.MF   
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo/unzip_apk$ ll
total 72
drwxrwxr-x  4 lanzhiwang lanzhiwang  4096 8月  15 19:44 ./
drwxr-xr-x 10 lanzhiwang lanzhiwang  4096 8月  15 19:44 ../
-rw-rw-r--  1 lanzhiwang lanzhiwang  1472 8月  15 17:40 AndroidManifest.xml
-rw-rw-r--  1 lanzhiwang lanzhiwang  1832 8月  15 17:36 classes.dex
-rw-rw-r--  1 lanzhiwang lanzhiwang 41761 8月  15 19:44 Demo-release.zip
drwxrwxr-x  2 lanzhiwang lanzhiwang  4096 8月  15 19:44 META-INF/
drwxrwxr-x  7 lanzhiwang lanzhiwang  4096 8月  15 19:44 res/
-rw-rw-r--  1 lanzhiwang lanzhiwang  1636 1月   1  1980 resources.arsc
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo/unzip_apk$ cd ..
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$ git status
On branch master
Untracked files:
  (use "git add <file>..." to include in what will be committed)

    Demo-aligned.apk
    Demo-release.apk
    Demo.apk
    bin/classes.dex
    bin/resources
    my-release-key.jks
    unzip_apk/

nothing added to commit but untracked files present (use "git add" to track)
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$
解压 resources 文件验证
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$ mkdir unzip_resources
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$ cp bin/resources ./unzip_resources/
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$ cd ./unzip_resources/
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo/unzip_resources$
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo/unzip_resources$ ll
total 40
drwxrwxr-x  2 lanzhiwang lanzhiwang  4096 8月  15 20:04 ./
drwxr-xr-x 11 lanzhiwang lanzhiwang  4096 8月  15 20:03 ../
-rw-rw-r--  1 lanzhiwang lanzhiwang 30393 8月  15 20:04 resources
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo/unzip_resources$
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo/unzip_resources$ unzip resources
Archive:  resources
  inflating: AndroidManifest.xml     
 extracting: res/drawable-hdpi-v4/ic_launcher.png 
 extracting: res/drawable-ldpi-v4/ic_launcher.png 
 extracting: res/drawable-mdpi-v4/ic_launcher.png 
 extracting: res/drawable-xhdpi-v4/ic_launcher.png 
  inflating: res/layout/main.xml     
 extracting: resources.arsc         
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo/unzip_resources$ ll
total 52
drwxrwxr-x  3 lanzhiwang lanzhiwang  4096 8月  15 20:04 ./
drwxr-xr-x 11 lanzhiwang lanzhiwang  4096 8月  15 20:03 ../
-rw-rw-rw-  1 lanzhiwang lanzhiwang  1472 1月   1  1980 AndroidManifest.xml
drwxrwxr-x  7 lanzhiwang lanzhiwang  4096 8月  15 20:04 res/
-rw-rw-r--  1 lanzhiwang lanzhiwang 30393 8月  15 20:04 resources
-rw-rw-rw-  1 lanzhiwang lanzhiwang  1636 1月   1  1980 resources.arsc
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo/unzip_resources$
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo/unzip_resources$
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo/unzip_resources$ cd ..
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$ git status
On branch master
Untracked files:
  (use "git add <file>..." to include in what will be committed)

    Demo-aligned.apk
    Demo-release.apk
    Demo.apk
    bin/classes.dex
    bin/resources
    my-release-key.jks
    unzip_apk/
    unzip_resources/

nothing added to commit but untracked files present (use "git add" to track)
lanzhiwang@lanzhiwang-dev2:~/AndroidStutio/demo$
```


#### 通过 adb 获取安卓应用屏幕所有控件信息

```bash
$ adb -s 48db50a5b827 shell uiautomator dump /sdcard/ui.xml

$ adb -s 48db50a5b827 shell ls /sdcard/ui.xml

$ adb -s 48db50a5b827 pull /sdcard/ui.xml ./ui.xml

$ adb -s 48db50a5b827 shell rm -f  /sdcard/ui.xml
```

原理:
调用安卓设备系统文件中/system/bin/uiautomator.jar包执行dump指令.

```bash
$ find /usr/local/android-sdk/ -name uiautomator.jar
/usr/local/android-sdk/platforms/android-22/uiautomator.jar
/usr/local/android-sdk/platforms/android-28/uiautomator.jar
$
```


#### adb shell input 命令示例

```bash
$ adb -s 48db50a5b827 shell input
Usage: input [<source>] <command> [<arg>...]

The sources are:
      trackball
      joystick
      touchnavigation
      mouse
      keyboard
      gamepad
      touchpad
      dpad
      stylus
      touchscreen

The commands and default sources are:
      text <string> (Default: touchscreen)
      keyevent [--longpress] <key code number or name> ... (Default: keyboard)
      tap <x> <y> (Default: touchscreen)
      swipe <x1> <y1> <x2> <y2> [duration(ms)] (Default: touchscreen)
      press (Default: trackball)
      roll <dx> <dy> (Default: trackball)
$
```

#### APK静态分析

#### APK动态分析


#### ADB 模型
![](https://github.com/lanzhiwang/awesome-huzhi/blob/master/images/adb_model.png)

#### adb forward 原理
![](https://github.com/lanzhiwang/awesome-huzhi/blob/master/images/adb_forward_model.png)


PC端的应用与手机端应用通信建立的过程：
（1）执行adb forward tcp:11111 tcp:22222
（2）启动手机端应用，建立端口为22222的server，并处于监听状态（LISTENING）
（3）启动PC端应用，连接端口为11111的server（adb创建的）
之后，就可以传输数据了。

PC端的应用与手机端应用之间传输数据的过程：
（1）PC端应用将数据发送给端口为11111的server（adb创建的）
（2）adb将数据转发给手机端adbd进程（通过USB传输）
（3）adbd进程将数据发送给端口为22222的server（手机端应用创建的）
传递是双向的，第（1）和第（3）步是通过socket实现的，所以通过socket的读和写就完成了PC端应用和手机端应用的数据传递。


```bash
$ adb

 forward --list           list all forward socket connections
 forward [--no-rebind] LOCAL REMOTE
     forward socket connection using:
       tcp:<port> (<local> may be "tcp:0" to pick any open port)
       localabstract:<unix domain socket name>
       localreserved:<unix domain socket name>
       localfilesystem:<unix domain socket name>
       dev:<character device name>
       jdwp:<process pid> (remote only)
 forward --remove LOCAL   remove specific forward socket connection
 forward --remove-all     remove all forward socket connections

 reverse --list           list all reverse socket connections from device
 reverse [--no-rebind] REMOTE LOCAL
     reverse socket connection using:
       tcp:<port> (<remote> may be "tcp:0" to pick any open port)
       localabstract:<unix domain socket name>
       localreserved:<unix domain socket name>
       localfilesystem:<unix domain socket name>
 reverse --remove REMOTE  remove specific reverse socket connection
 reverse --remove-all     remove all reverse socket connections from device
```



#### AVD 构建和运行方法

step1：构建 AVD 基本文件
step2：运行 AVD 后产生完整的模拟器

step1：构建 AVD 基本文件的方法
1、使用 android-studio 自带的工具
2、使用命令行工具（不同版本的 SDK 工具不一样）
notes：
* 构建 AVD 的过程中需要配置 device 和 target 信息，所以需要确定有哪些可用的 device 和 target
* device 和 target 是随着 SDK 一起安装的
* device，target，API 等与版本密切相关，所以要使用统一的版本
* 在不同版本的 SDK 中具体的命令行工具不一样
* 命令行工具的选项也有差异
* 有些命令需要使用图形界面，所以需要使用桌面版的操作系统
* 具体的相关命令如下：

```bash
$ avdmanager -h create avd

$ android -h create avd
```

###### android create avd 命令示例如下：

```bash
$ android list device  # Lists existing devices.

$ android list target  # Lists existing targets.

$ android -h create avd  # 查看相关选项

$ android create avd -c 52M -n GPhone -s QVGA  -d 22  --target 1 --abi default/armeabi-v7a
Created AVD 'GPhone' based on Android 4.1.2, ARM (armeabi-v7a) processor,
with the following hardware config:
hw.accelerometer=yes
hw.audioInput=yes
hw.battery=yes
hw.dPad=no
hw.device.hash2=MD5:ce947414aa538ac299b8d4f2b7faac44
hw.device.manufacturer=Generic
hw.device.name=3.7in WVGA (Nexus One)
hw.gps=yes
hw.keyboard=no
hw.lcd.density=240
hw.mainKeys=yes
hw.ramSize=512
hw.sdCard=yes
hw.sensors.orientation=yes
hw.sensors.proximity=yes
hw.trackBall=yes
vm.heapSize=48

$ pwd  # AVD默认存储路径
/home/cuckoo/.android/avd/

AVD 基本文件如下
drwxrwxr-x 2 cuckoo cuckoo 4.0K  9月 21 15:19 GPhone.avd
-rw-rw-r-- 1 cuckoo cuckoo  107  9月 21 14:39 GPhone.ini

$ cat GPhone.ini
avd.ini.encoding=UTF-8
path=/home/cuckoo/.android/avd/GPhone.avd
path.rel=avd/GPhone.avd
target=android-16

$ ll GPhone.avd
total 56M
-rw-rw-r-- 1 cuckoo cuckoo  613  9月 21 14:39 config.ini
-rw-rw-r-- 1 cuckoo cuckoo  52M  9月 21 14:39 sdcard.img
-rw-rw-r-- 1 cuckoo cuckoo 4.0M  9月 21 14:39 userdata.img

$ cat config.ini
avd.ini.encoding=UTF-8
abi.type=armeabi-v7a
hw.accelerometer=yes
hw.audioInput=yes
hw.battery=yes
hw.cpu.arch=arm
hw.cpu.model=cortex-a8
hw.dPad=no
hw.device.hash2=MD5:ce947414aa538ac299b8d4f2b7faac44
hw.device.manufacturer=Generic
hw.device.name=3.7in WVGA (Nexus One)
hw.gps=yes
hw.keyboard=no
hw.lcd.density=240
hw.mainKeys=yes
hw.ramSize=512
hw.sdCard=yes
hw.sensors.orientation=yes
hw.sensors.proximity=yes
hw.trackBall=yes
image.sysdir.1=system-images/android-16/default/armeabi-v7a/
sdcard.size=52M
skin.name=qvga
skin.path=platforms/android-16/skins/QVGA
tag.display=Default
tag.id=default
vm.heapSize=48
$
```

######avdmanager create avd 命令示例如下：

```bash
$ avdmanager list avd
Available Android Virtual Devices:
$
$ avdmanager create avd -c 52M -n GPhone -d 15 -k "system-images;android-16;default;armeabi-v7a"
$ avdmanager list avd
Available Android Virtual Devices:
    Name: GPhone
  Device: Nexus One (Google)
    Path: /home/lanzhiwang/.android/avd/GPhone.avd
  Target:
          Based on: Android 4.1 (Jelly Bean) Tag/ABI: default/armeabi-v7a
  Sdcard: 52M
$
$ ll /home/lanzhiwang/.android/avd/GPhone.avd
total 57300
drwxrwxr-x 2 lanzhiwang lanzhiwang     4096 9月  21 16:56 ./
drwxrwxr-x 3 lanzhiwang lanzhiwang     4096 9月  21 16:56 ../
-rw-rw-r-- 1 lanzhiwang lanzhiwang      548 9月  21 16:56 config.ini
-rw-rw-r-- 1 lanzhiwang lanzhiwang 54525952 9月  21 16:56 sdcard.img
-rw-rw-r-- 1 lanzhiwang lanzhiwang  4135296 9月  21 16:56 userdata.img
$
$ ll /home/lanzhiwang/.android/avd/GPhone.ini
-rw-rw-r-- 1 lanzhiwang lanzhiwang 111 9月  21 16:56 /home/lanzhiwang/.android/avd/GPhone.ini
$ cat  /home/lanzhiwang/.android/avd/GPhone.ini
avd.ini.encoding=UTF-8
path=/home/lanzhiwang/.android/avd/GPhone.avd
path.rel=avd/GPhone.avd
target=android-16
$
$ cat /home/lanzhiwang/.android/avd/GPhone.avd/config.ini
PlayStore.enabled=false
abi.type=armeabi-v7a
avd.ini.encoding=UTF-8
hw.accelerometer=yes
hw.audioInput=yes
hw.battery=yes
hw.cpu.arch=arm
hw.cpu.model=cortex-a8
hw.dPad=no
hw.device.hash2=MD5:0250c2773d1dd25bb2b12d9502c789f7
hw.device.manufacturer=Google
hw.device.name=Nexus One
hw.gps=yes
hw.lcd.density=240
hw.lcd.height=800
hw.lcd.width=480
hw.mainKeys=yes
hw.sdCard=yes
hw.sensors.orientation=no
hw.sensors.proximity=yes
hw.trackBall=yes
image.sysdir.1=system-images/android-16/default/armeabi-v7a/
sdcard.size=52M
tag.display=
tag.id=default
```

notes ：
* 创建 AVD 的过程中要确定 device，target。
* 并且target下要有 Tag/ABIs 选项，并且 Tag/ABIs 有多个可用值，要使用 --abi 选择其中的一
* target 指定 android 版本，API版本，皮肤选项，Tag/ABIs等

```bash
$ android list target
Available Android targets:  # 有多个target 
----------
id: 1 or "android-16"
     Name: Android 4.1.2
     Type: Platform
     API level: 16
     Revision: 5
     Skins: HVGA, QVGA, WQVGA400, WQVGA432, WSVGA, WVGA800 (default), WVGA854, WXGA720, WXGA800, WXGA800-7in  # 可选的皮肤选项 
Tag/ABIs : default/armeabi-v7a, default/x86, google_apis/x86  # 该target下有多个 Tag/ABIs 选项
----------
id: 2 or "android-21"
     Name: Android 5.0.1
     Type: Platform
     API level: 21
     Revision: 2
     Skins: HVGA, QVGA, WQVGA400, WQVGA432, WSVGA, WVGA800 (default), WVGA854, WXGA720, WXGA800, WXGA800-7in
Tag/ABIs : no ABIs.  # 该target下没有 Tag/ABIs 选项
----------
id: 7 or "Google Inc.:Google APIs:16"
     Name: Google APIs
     Type: Add-On
     Vendor: Google Inc.
     Revision: 4
     Description: Android + Google APIs
     Based on Android 4.1.2 (API level 16)
     Libraries:
      * com.google.android.media.effects (effects.jar)
          Collection of video effects
      * com.android.future.usb.accessory (usb.jar)
          API for USB Accessories
      * com.google.android.maps (maps.jar)
          API for Google Maps
     Skins: HVGA, QVGA, WQVGA400, WQVGA432, WSVGA, WVGA800 (default), WVGA854, WXGA720, WXGA800, WXGA800-7in
Tag/ABIs : default/armeabi-v7a  # 该target下只要一个 Tag/ABIs 选项
```


step2：运行 AVD 后产生完整的模拟器
notes：
* 需要在图形界面运行
* 不同的AVD基础文件有可能需要使用不同的 emulator 命令选项
* 具体命令如下

```bash
$ emulator -avd GPhone

$ emulator -avd GPhone -qemu -nand -system,size=0x1f400000,file=/home/cuckoo/Tools/android-sdk-linux/system-images/android-16/default/armeabi-v7a/system.img &
```

###### emulator -avd GPhone 示例：

```bash
$ emulator -avd GPhone
出现图形界面

# 运行模拟器的过程中产生一些新的文件，构建出一个完整的模拟器
$ ll GPhone.avd/
total 62492
drwxrwxr-x 2 lanzhiwang lanzhiwang     4096 9月  21 17:13 ./
drwxrwxr-x 3 lanzhiwang lanzhiwang     4096 9月  21 16:56 ../
-rw-r--r-- 1 lanzhiwang lanzhiwang       67 9月  21 17:13 AVD.conf
-rw------- 1 lanzhiwang lanzhiwang     8412 9月  21 17:13 cache.img
-rw------- 1 lanzhiwang lanzhiwang        6 9月  21 17:13 cache.img.lock
-rw-rw-r-- 1 lanzhiwang lanzhiwang      548 9月  21 16:56 config.ini
-rw-r--r-- 1 lanzhiwang lanzhiwang     1978 9月  21 17:13 hardware-qemu.ini
-rw------- 1 lanzhiwang lanzhiwang        6 9月  21 17:13 hardware-qemu.ini.lock
-rw-rw-r-- 1 lanzhiwang lanzhiwang 54525952 9月  21 16:56 sdcard.img
-rw------- 1 lanzhiwang lanzhiwang        6 9月  21 17:13 sdcard.img.lock
-rw-rw-r-- 1 lanzhiwang lanzhiwang  4135296 9月  21 16:56 userdata.img
-rw------- 1 lanzhiwang lanzhiwang  5277852 9月  21 17:15 userdata-qemu.img
-rw------- 1 lanzhiwang lanzhiwang        6 9月  21 17:13 userdata-qemu.img.lock
$

# 模拟器关闭后也会产生新的文件
$ ll GPhone.avd/
total 72396
drwxrwxr-x 2 lanzhiwang lanzhiwang     4096 9月  21 17:17 ./
drwxrwxr-x 3 lanzhiwang lanzhiwang     4096 9月  21 16:56 ../
-rw-r--r-- 1 lanzhiwang lanzhiwang       67 9月  21 17:13 AVD.conf
-rw------- 1 lanzhiwang lanzhiwang     8412 9月  21 17:13 cache.img
-rw------- 1 lanzhiwang lanzhiwang        6 9月  21 17:13 cache.img.lock
-rw-rw-r-- 1 lanzhiwang lanzhiwang      548 9月  21 16:56 config.ini
-rw-r--r-- 1 lanzhiwang lanzhiwang       51 9月  21 17:17 emulator-user.ini
-rw-r--r-- 1 lanzhiwang lanzhiwang     1978 9月  21 17:13 hardware-qemu.ini
-rw------- 1 lanzhiwang lanzhiwang        6 9月  21 17:13 hardware-qemu.ini.lock
-rw-rw-r-- 1 lanzhiwang lanzhiwang 54525952 9月  21 17:16 sdcard.img
-rw------- 1 lanzhiwang lanzhiwang        6 9月  21 17:13 sdcard.img.lock
-rw------- 1 lanzhiwang lanzhiwang        6 9月  21 17:17 snapshot.lock.lock
-rw-rw-r-- 1 lanzhiwang lanzhiwang  4135296 9月  21 16:56 userdata.img
-rw------- 1 lanzhiwang lanzhiwang 15411228 9月  21 17:17 userdata-qemu.img
-rw------- 1 lanzhiwang lanzhiwang        6 9月  21 17:13 userdata-qemu.img.lock
lanzhiwang@lanzhiwang-dev2:~/.android/avd$
```

###### 模拟器界面如下：
![](https://github.com/lanzhiwang/awesome-huzhi/blob/master/images/emu.png)
