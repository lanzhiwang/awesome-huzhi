```php
$ php MailContent.class.php 
string(11) "./email.eml" //邮件内容文件

// 读取内容，按 \n 分割为数组
Array
(
    [0] => Received: from pgg4ag.mail.toptal.com (unknown [54.174.63.102])
    [1] => 	by mx1 (Coremail) with SMTP id M8CowAC3UFCfPjdcE4u1Ag--.37719S15;
    [2] => 	Thu, 10 Jan 2019 20:46:55 +0800 (CST)
    [3] => Received: by 172.16.62.47 with SMTP id azlpzyulybvgvw37quuv1kafb1ikena6rwo52rn3r;
    [4] =>         Thu, 10 Jan 2019 12:46:50 GMT
    [5] => DKIM-Signature: v=1; s=hs1; d=mail.toptal.com;
    [6] =>         i=@mail.toptal.com;
    [7] =>         h=sender:from:reply-to:to:subject:mime-version:content-type:list-unsubscribe:x-report-abuse:form-sub;
    [8] =>         a=rsa-sha256; c=relaxed/relaxed;
    [9] =>         bh=Sr7c8dMnFS8BSAe1SfSfi7QRDDj8Qa9YrqQwHaHis0s=;
    [10] =>         b=bkRa1hIlLfpdlwrzk2OCvHWtHU0MC8/gJzm+0U1SUO4SJGSnOCPXDrZ/U5IUFR
    [11] =>          mcbVr3+P71feew58w6HuDe67hZoDQV5jLI1Qo3QwjaIAlQk2RA+I/RNW24DQxxq
    [12] =>          JTuI1wkHZ3tPSDZAXFhGEHcMPn3HHoNZdzQqiI5kXLyn0XAwJjL/eaRHh4o49G3
    [13] =>          zyKxDzCxIJJRrJMb0sNVoVbvJ6AxiF+DTssrWC1FOmliHXmUdaFb//cUokGeLG3
    [14] =>          3mT3Jf0Wxv2QmUhyq04X6Ukb59oAu46Em/luVOveo2JRmB5iHtmlTW6Uh0AInE4
    [15] =>          RnV4/RUlRVFDDs5r9+bA29bFaj3w==; q=dns/txt; t=1547124410;
    [16] => DKIM-Signature: v=1; s=hs1; d=toptal.com; i=@toptal.com;
    [17] =>         h=sender:from:reply-to:to:subject:mime-version:content-type:list-unsubscribe:x-report-abuse:form-sub;
    [18] =>         a=rsa-sha256; c=relaxed/relaxed;
    [19] =>         bh=Sr7c8dMnFS8BSAe1SfSfi7QRDDj8Qa9YrqQwHaHis0s=;
    [20] =>         b=K9jqmLCdxgii3sJAp3SHwmZpkybw10QQOm6794zbeJf9BL1WQjNN+8zSUbwV+G
    [21] =>          mEj+YzTbXXwXVtBrzm3/YiOOo2rfiG7MZK00J1dNiXhD/AZtbupfRPmEHSWLAB6
    [22] =>          kuhAJnxkUcHDkgQAtKauqwXYtHS1SBB6vGCxIvE+WP9TvYEDVesHukLUIGf6kNU
    [23] =>          Aq8JmMao8GRuOUfZWvaeqnL7/VUnBjxQh9LEZzDI90bjdsodEgAiRx2Z3Oxdjfz
    [24] =>          5hWsYErFfK/pN+IkxFfUgqnt6Hy7f6Zh1tvJtAU1oqyG/dyIb1PvQU8RI0Zuigz
    [25] =>          aA24wG3vTrlp+xPuwx4gf9viZF8w==; q=dns/txt; t=1547124410;
    [26] => Return-Path: <1axb06mzipx5up3rzlxc81eh16nhe81h8l7omi-hzhilamp=163.com@mail.toptal.com>
    [27] => X-HS-Cid: 1axe7t3rcjxusl6j2ajxiy9nriv74kj7tc6hc6
    [28] => List-Unsubscribe: <mailto:1axcxdq1nuanq1ngwg63bfoqiiso594ogfoq46-hzhilamp=163.com@mail.toptal.com?subject=unsubscribe>
    [29] => Date: Thu, 10 Jan 2019 07:46:50 -0500
    [30] => From: Toptal Design Blog <editor@toptal.com>
    [31] => Reply-To: editor@toptal.com
    [32] => To: hzhilamp@163.com
    [33] => Message-ID: <1547123744075.0d3893bc-90b5-4e61-b39a-581746f20905@mail.toptal.com>
    [34] => Subject: Influence with Design - a Guide to Color and Emotions
    [35] => MIME-Version: 1.0
    [36] => Content-Type: multipart/alternative;
    [37] => 	boundary="----=_Part_1968210_2144246150.1547124410177"
    [38] => X-Report-Abuse-To: abuse@hubspot.com (see
    [39] =>  https://www.hubspot.com/abuse-complaints)
    [40] => X-CM-TRANSID:M8CowAC3UFCfPjdcE4u1Ag--.37719S15
    [41] => Authentication-Results: mx1; spf=neutral smtp.mail=1axb06mzipx5up3rzlx
    [42] => 	c81eh16nhe81h8l7omi-hzhilamp=163.com@mail.toptal.com; dkim=pass header
    [43] => 	.i=@mail.toptal.com; dkim=pass header.i=@toptal.com
    [44] => X-Coremail-Antispam: 1Uf129KBjvdXoW7Wr43GF4rZr1xtrWrCw1kuFg_yoWDKrXE9r
    [45] => 	4ktr17Xw45X3WfJrWUta1j9rWjy3yUWr1kJrWfXF40q3sayws0ywnrCFykZw1fXayYgrZx
    [46] => 	Wr98Aa1fKa92vjkaLaAFLSUrUUUU2b8apTn2vfkv8UJUUUU8Yxn0WfASr-VFAUDa7-sFnT
    [47] => 	9fnUUvcSsGvfC2KfnxnUUI43ZEXa7IU5O183UUUUU==
    [48] => Sender: 1axb06mzipx5up3rzlxc81eh16nhe81h8l7omi-hzhilamp=163.com@mail.toptal.com
    [49] => 
    [50] => ------=_Part_1968210_2144246150.1547124410177
    [51] => Content-Type: text/plain; charset=utf-8
    [52] => Content-Transfer-Encoding: quoted-printable
    [53] => 
    [54] => The relationship between color and emotion is one of the most important asp=
    [55] => ects of good UX design.
    [56] => 
    [57] => Influence with Design - a Guide to Color and Emotions
    [58] => (https://hs-2799924.t.hubspotemail.net/e2t/sc2/MmZ-8yjQ-24W6KZMpC7wTwfKW8f8=
    [59] => c377nvVV6VtSqRl55LdHfdBzP8M04 )
    [60] => 
    [61] => The relationship between color and emotion is one of the most important asp=
    [62] => ects of good UX design.
    [63] => 
    [64] => Design blog editor Cameron Chapman explains why the right color palette enc=
    [65] => ourages people to behave in ways designers want them to behave, while the w=
    [66] => rong palette can drive visitors away.
    [67] => 
    [68] => Continue Reading (https://hs-2799924.t.hubspotemail.net/e2t/sc2/MmZ-8yjQ-24=
    [69] => W6KZMpC7wTwfKW8f8c377nvVV6VtSqRl55LdHfdBzP8N04 )
    [70] => 
    [71] => Other recommended articles:
    [72] => 
    [73] => -
    [74] => A Spectrum of Possibilities: The Go-To UI Color Guide  (https://hs-2799924.=
    [75] => t.hubspotemail.net/e2t/sc2/MmZ-8yjQ-24W6KZMpC7wTwfKW8f8c377nvVV6VtSqRl55LdH=
    [76] => fdBzP8P04 )
    [77] => 
    [78] => -
    [79] => Design Psychology and the Neuroscience of Awesome UX (https://hs-2799924.t.=
    [80] => hubspotemail.net/e2t/sc2/MmZ-8yjQ-24W6KZMpC7wTwfKW8f8c377nvVV6VtSqRl55LdHfd=
    [81] => BzP8Q04 )
    [82] => 
    [83] => -
    [84] => Cause and Effect =E2=80=93 Exploring Color Psychology (https://hs-2799924.t=
    [85] => .hubspotemail.net/e2t/sc2/MmZ-8yjQ-24W6KZMpC7wTwfKW8f8c377nvVV6VtSqRl55LdHf=
    [86] => dBzP8R04 )
    [87] => 
    [88] => -
    [89] => Design for Emotion to Increase User Engagement (https://hs-2799924.t.hubspo=
    [90] => temail.net/e2t/sc2/MmZ-8yjQ-24W6KZMpC7wTwfKW8f8c377nvVV6VtSqRl55LdHfdBzP8S0=
    [91] => 4 )
    [92] => 
    [93] => -
    [94] => The Role of Color in UX (https://hs-2799924.t.hubspotemail.net/e2t/sc2/MmZ-=
    [95] => 8yjQ-24W6KZMpC7wTwfKW8f8c377nvVV6VtSqRl55LdHfdBzP8T04 )
    [96] => 
    [97] => Cameron Chapman
    [98] => 
    [99] => Design Blog Editor
    [100] => 
    [101] => Cameron comes from a design background and is the author of two web design =
    [102] => books: Color for Web Design and The Smashing Idea Book.
    [103] => 
    [104] => Hiring UX Designers?
    [105] => 
    [106] => Looking for an elite UX designer to join your team? Get started with a Topt=
    [107] => al account.
    [108] => 
    [109] => Start Hiring (https://hs-2799924.t.hubspotemail.net/e2t/sc2/MmZ-8yjQ-24W6KZ=
    [110] => MpC7wTwfKW8f8c377nvVV6VtSqRl55LdHfdBzP8V04 )
    [111] => 
    [112] => =C2=A9 2010-2019 Toptal, LLC. All rights reserved. Toptal, LLC, 548 Market =
    [113] => Street, San Francisco, California 94104.
    [114] => 
    [115] => Update your subscription preferences (https://hs-2799924.s.hubspotemail.net=
    [116] => /hs/manage-preferences/unsubscribe?d=3DeyJlYSI6Imh6aGlsYW1wQDE2My5jb20iLCJl=
    [117] => YyI6Njg4ODc0MTksInN1YnNjcmlwdGlvbklkIjozNTQ0Mjk2LCJldCI6MTU0NzEyMzc0NDA3NSw=
    [118] => iZXUiOiIwZDM4OTNiYy05MGI1LTRlNjEtYjM5YS01ODE3NDZmMjA5MDUifQ%3D%3D&v=3D1&_hs=
    [119] => enc=3Dp2ANqtz-8jhVrWldbSl_t6hyr5qjx7m2yOvvaa0V8mbQlYYtSC3aBGCw4vZsG5Un-N5N-=
    [120] => KsSZ23u-J0dgMR0Cp1kHLDVaNf4aXmg&_hsmi=3D68887419 )
    [121] => ------=_Part_1968210_2144246150.1547124410177
    [122] => Content-Type: text/html; charset="utf-8"
    [123] => Content-Transfer-Encoding: quoted-printable
    [124] => 
    [125] => <!DOCTYPE html><!-- start coded_template: id:5876930156 path:Custom/email/E=
    [126] => ngineering_Blog_Emails/New_Article_v2.html --><html lang=3D"en"><head>
    [127] =>     <meta charset=3D"UTF-8">
    [128] =>     <meta name=3D"viewport" content=3D"width=3Ddevice-width, initial-scale=
    [129] => =3D1.0">
    [130] =>     <meta http-equiv=3D"X-UA-Compatible" content=3D"ie=3Dedge">
    [131] =>     <title></title>
    [132] =>     <style type=3D"text/css"></style>
    [133] => <meta name=3D"generator" content=3D"HubSpot"><meta property=3D"og:url" cont=
    [134] => ent=3D"http://toptal-2799924.hs-sites.com/-temporary-slug-83a57569-07a1-4bb=
    [135] => e-8952-98d64272021b"><meta name=3D"x-apple-disable-message-reformatting"><m=
    [136] => eta name=3D"robots" content=3D"noindex,follow"></head>
    [137] => <body style=3D"min-width: 640px; margin: 0; padding: 0;">
    [138] =>     <div id=3D"preview_text" style=3D"display: none; font-size: 1px; color:=
    [139] =>  #f2f2f2; line-height: 1px; max-height: 0px; max-width: 0px; opacity: 0; ov=
    [140] => erflow: hidden;">The relationship between color and emotion is one of the m=
    [141] => ost important aspects of good UX design.</div>
    [142] =>     <div style=3D"width: 640px; margin: 0 auto;">
    [143] =>         <div style=3D"letter-spacing: 636px; line-height: 0; mso-hide: all"=
    [144] => >&nbsp;</div>
    [145] =>         <table style=3D"width: 100%; border-spacing: 0; border-collapse: co=
    [146] => llapse;">
    [147] =>             <tbody>
    [148] =>                 <tr>
    [149] =>                     <td style=3D"padding: 0;">
    [150] =>                        =20
    [151] =>                        =20
    [152] =>                        =20
    [153] =>                        =20
    [154] =>                        =20
    [155] =>                        =20
    [156] =>                         <div style=3D"display: block; width: 100%; height: =
    [157] => 76px; background: #204ECF;">
    [158] =>                             <div style=3D"width: 588px; margin: 0 auto; pad=
    [159] => ding: 23px 10px 0;">
    [160] =>                                 <div style=3D"float: right;">
    [161] =>                                     <a href=3D"https://hs-2799924.t.hubspot=
    [162] => email.net/e2t/c/*W3Lv-Nv3x5_DBW8x51Kp94S_Jb0/*W69QJxk3JRjd0W2bVg0y5YXRP20/5=
    [163] => /f18dQhb0Sjv58XJ888N7rRy-jHyjJqW3LqXLs8q5JFzN3hHhbrVMsQMVnQ9Qq8Z_pJ9W2MyX6Q=
    [164] => 8YztwfW8ZY7p12K85XYW30TLQp8W56w8W8HbRxP8k1dMQVpSKsd3lCBR6W5k4Yfp2qgPMPN7q68=
    [165] => 357d2jqW1L4xyj6FKg-TW2XsCWx7tfTF5W7kcs3h1FpGp3VMCFPP7zN65hW1Ccbx-99TJLMW5Rl=
    [166] => SdT5xNCj8W8mGgzn313G3wW8k4nkj33xJV6W3ZNVwx5mWmT-W5G3dd43jMWjkVNbbJZ3VZNjyW8=
    [167] => tXxl633zJNNW8r1PN23RpN_pVHlk_P17qc0TW41TnwW8HSh-pN5ljjfDTD64SW8qxRgX3RYJ_DW=
    [168] => 8mFrrV15RNs5W11YP5x1BgLjvW6rKDzl73QsnmW1d5pgb52TGYwW1y7CdL8t_H7XW1Vp9PT1m13=
    [169] => GxW49FShz6ltRMnW9lMQJm8Frwq9W4ZfWVH5QJwTxVx-Qph3rcbQ8N4h0J_FVs7V_VVmc-z1SPD=
    [170] => 9r102" style=3D"margin-left: 20px;" data-hs-link-id=3D"0" target=3D"_blank"=
    [171] => ><img src=3D"https://uploads.toptal.io/blog/image/125668/toptal-blog-image-=
    [172] => 1521005292111-0582221c638699855c9370718a6dc648.png" alt=3D"" width=3D"32"><=
    [173] => /a><a href=3D"https://hs-2799924.t.hubspotemail.net/e2t/c/*W3Lv-Nv3x5_DBW8x=
    [174] => 51Kp94S_Jb0/*W1HLk8P591w2YW3Xhq4x1pZky_0/5/f18dQhb0SbTY8XJ9c2N7rRy-jHyjJqW3=
    [175] => LqXLs8q5JFzW3hHhd92P7_nXVcnTGj992gLmW4t8DZ37Zs-5QW4rJcyL6PZs53W973HLL7d0nlN=
    [176] => W95lb1c24Pv3cW5DHNhQ2yH5gzW61SSZm7mG7sDN50QvwtCdDVWW35_0Hr38cMfvW8n-Zvr6nSM=
    [177] => m8W2_1lbg5rcZX1W2-294g5J0bHmW1y7l0Q1Y147_W38kffx24ZF-xW1ZY5-P46PQjKW6G2lbz7=
    [178] => NMdQNV4cNXy75WRHJVpZgcl1XRGp_W5Tsxfn5r7PCBW1sD8JT5_fDvnW4_zWtX2FK0jmW7p46r6=
    [179] => 2Z40g3W17zzwl7h9przW94rzfp3QbQGlW7V52FL5nVH1KVjXZhY94P7THW6pHRB067_gXDW5K3t=
    [180] => zh1zMkb2W2QM0bK5gSHY5W6H5W1X3nTjygVVR6H24q1HYHV8hgJ41Syp30N47kQfDdNPzRW2nRy=
    [181] => lc5rgWcCW527FSR64Mpz4W1vNXZj7QXHPcW5ywNFS23ZxZkW3vRJ3d4Pxhj5W3DlwBb6ddfszf3=
    [182] => 5KTgn04" style=3D"margin-left: 20px;" data-hs-link-id=3D"0" target=3D"_blan=
    [183] => k"><img src=3D"https://uploads.toptal.io/blog/image/125667/toptal-blog-imag=
    [184] => e-1521005283540-4d933a4bb042a18e5843222a037d0201.png" alt=3D"" width=3D"32"=
    [185] => ></a><a href=3D"https://hs-2799924.t.hubspotemail.net/e2t/c/*W3Lv-Nv3x5_DBW=
    [186] => 8x51Kp94S_Jb0/*W7BjFJm45_LTsW884TBY1c3RQC0/5/f18dQhb0Sjvh8XJ9c2N7rRy-jHyjJq=
    [187] => W3LqXLs8q5JFzW3hHhbJ2P7_nXVcnTGj992gLmW4txBlX6b16HkW7Z5GVw6PZb6JVb8m6N1xc3b=
    [188] => NW8xGYBQ7dChrhW6PVKcr6N3nz4W6ZLb6n31rP00N1n8mtVdplspW8m8m3Z6d5y9_W5x5KNk7-X=
    [189] => B_5W67h1CP8r97s-W8m7Y9z5wM1SsVphC7_8sYvvlW5tGksb4FW991W7zLV652NnQ5KW4bQW_q6=
    [190] => c41L2W47yXsr6ck454W1-VYMN2JYsFKW2RxD626lXGj4VnCjBP6DxR4-W8YvN6y6bm0z_W4dw94=
    [191] => M1Xc5dwVl992g5dgyZLW20Ybjk4krBtqW2H8mp_54VcLxW4dfW4v6C1hrwN4bQJG-yXBZTVw-p5=
    [192] => 75tb4QNW3fBJpw53NYtcW4PLwTV7pDXPsN5ZYC4whCrxZW2sB_Hx5dbfxsW8mhg5w3hVGHxW9jr=
    [193] => DtM7ZM5S0VBnvjp2gh8YpW11-FQN6Tp_6JW8B_Zvs1MWhN-W1MKdb073jzQ-111" style=3D"m=
    [194] => argin-left: 20px;" data-hs-link-id=3D"0" target=3D"_blank"><img src=3D"http=
    [195] => s://uploads.toptal.io/blog/image/125666/toptal-blog-image-1521005268330-d7a=
    [196] => e3975c766ab789a8da965bd772e6a.png" alt=3D"" width=3D"32"></a><a href=3D"htt=
    [197] => ps://hs-2799924.t.hubspotemail.net/e2t/c/*W3Lv-Nv3x5_DBW8x51Kp94S_Jb0/*W8w2=
    [198] => jFF4x9YCFW94n6pb2__sJX0/5/f18dQhb0Sjv48YXM9FN7rRy-jHyjJqW3LqXLs8q5JFzN3hHh9=
    [199] => SVMsQMVnQ9Qq8-2DTPW5p9k8q31J0t5N4dPXSCqgSh5W8Fdh1C8k1dMQVpSBF38WhRz6MXTrLlZ=
    [200] => vX8WVQrzNb4X1VMbW6Qbzkw47YlYyW4bfcHb47Xx4zW3C8dd25-GNDdW3VKVtL6nGl8CW2PS9sY=
    [201] => 2HT8mrW6l4S5J1gvjSzW8hz0Ys806yj3W70ml3s3pBrS5W8XScvv89dBVfW75XRN62jD09KVML6=
    [202] => 668373lWW7TNzL18ksc0mW4-ZTqK2CkP11W12PdC35rYjVKN32zF7K1GH4mW1jbtZD8XvVDFW8c=
    [203] => VX3v1lnBGtW6dKX6m5y7v3pW6pDvqx75n04MW4b2m-55DhyW9W17Vwtg11rnNbV4VjkT6L4g-PW=
    [204] => 1S2k2j3slVGKW1THz9r4J35S4W2N6Sl_7Jq7BtW5G7v9r7sRvPRW7z5yFw8990XGW5sr1f14wr1=
    [205] => PqM4ZDML2LMBkTvBvh7-F_Fj103" style=3D"margin-left: 20px;" data-hs-link-id=
    [206] => =3D"0" target=3D"_blank"><img src=3D"https://uploads.toptal.io/blog/image/1=
    [207] => 26721/toptal-blog-image-1532963894726-d76db748a103cc747e6d37cb8363ab7a.png"=
    [208] =>  alt=3D"" width=3D"32"></a><a href=3D"https://hs-2799924.t.hubspotemail.net=
    [209] => /e2t/c/*W3Lv-Nv3x5_DBW8x51Kp94S_Jb0/*W4x8-PJ25YkN1W4BvMb63RGJ8N0/5/f18dQhb0=
    [210] => Sjv78XJ8w6N7rRy-jHyjJqW3LqXLs8q5JFzW3hHh8k2P7_nXVcnTGj992gLmW4thjXc51fy5BW4=
    [211] => tGhJG97zph7W1n3kH56b-B4_W4s2zfB90G7thN8S3yR5bXTd6W3_71qY7QQY33W35-9M426dRsL=
    [212] => W6gpfJv8sZ4WSW67b7w67hYCG4W3N1M0F2GRw4YW3HtrQn2K4XMjW8tzC3F8q-1tCW4kPzgK55T=
    [213] => 8N8W7w3wPS1NC3KcW1F6KTt8Pqhf5W8WNvPX1yhvGPW1wt9XX49xsQhN2LlNkmhTKGmW1X_RKl1=
    [214] => FJR48W8-KnRd1Qz-sXN2PmhS7yH1wVW90tZ3P1Gczr8W7mw39J1NgF9CW7Bw4bT1yN57nW1zg2t=
    [215] => Q1wPf7xW1RNDZT4d_g_NW7ZjRCN1BxxJmW7Ql6KJ73R1h2W224lJ_1bpp9kN1TJ8nkgkPS5N6YH=
    [216] => zwY215-pW1Jp47H2HlqhfW3TmGm01VW0ZXW257w0c4DlsZJW3cp_yn8Kzpc4MmRw0WdXyXbV1Fb=
    [217] => Ch4YZQCd103" style=3D"margin-left: 20px;" data-hs-link-id=3D"0" target=3D"_=
    [218] => blank"><img src=3D"https://uploads.toptal.io/blog/image/126722/toptal-blog-=
    [219] => image-1532963900770-fb212b2a7d25e09be33ad613555bbde7.png" alt=3D"" width=3D=
    [220] => "32"></a>
    [221] =>                                 </div>
    [222] =>                                 <div>
    [223] =>                                    =20
    [224] =>                                         <a href=3D"https://hs-2799924.t.hub=
    [225] => spotemail.net/e2t/c/*W3Lv-Nv3x5_DBW8x51Kp94S_Jb0/*W8SNqqt8ZRqQ0W3P0Bcf24y6l=
    [226] => B0/5/f18dQhb0Sjv98YHrCHN7rRy-jHyjJqW3LqXLs8q5JFzN3hHhdQVMsQMVnQ9Qq8--HBkW8Z=
    [227] => _2Kr2K85-MW5mZ50N32pJXXW7MbyQp549CJRW8V6qQD2MTPSyVKng6q4LxVF9N3xbNcCdbBjtW2=
    [228] => mjNwP58p-HfW47YlYy4bfcHbW47Xx4z3C811XW4-SZvb2KQ2YYW3_VZwP5ThdHgW3s1XjF51G0B=
    [229] => 5W4YFc4457-WqMW3H_Pty2DzCtRW1yBHg37W55GXW1zC13x78fxhCW3GPXM38l18GvN7qg85F1G=
    [230] => CpfW2NLPfH6qllLfW2Kz1Jk91zY72W8k21lC2YvqQ5W93kSNj3228ljW93dwX18Z8Y_qW93CNk8=
    [231] => 92G-QsVqV5Xj21TZw_W5hDykp7DhkvJW6Pc2NR7Pwr4kMVzQv-Vn7DDW6jPzhC6cQNM7W4JNVsx=
    [232] => 1W_FZrW3jzyPP5bN279W4jtyHN3vFgyrW85DKHs46BgYbW5pNn9g8f51-tW6glNTQ6ml62FN4Pv=
    [233] => 86f5XTRrf4NRkyh02" data-hs-link-id=3D"0" target=3D"_blank"><img src=3D"http=
    [234] => s://uploads.toptal.io/blog/image/126937/toptal-blog-image-1534853024441-458=
    [235] => a4fdcc29014af487fb468537abbfa.png" alt=3D"" height=3D"29" style=3D"float: l=
    [236] => eft;"></a>
    [237] =>                                    =20
    [238] =>                                 </div>
    [239] =>                             </div>
    [240] =>                         </div>
    [241] =>                     </td>
    [242] =>                 </tr>
    [243] =>                 <tr>
    [244] =>                     <td style=3D"padding: 0;">
    [245] =>                         <div style=3D"display: block; width: 100%; overflow=
    [246] => : hidden; background: #FFFFFF; background: linear-gradient(180deg, #11286C =
    [247] => 334px, #FFFFFF 334px);">
    [248] =>                             <div style=3D"display: block; width: 640px; mar=
    [249] => gin: 0 auto; padding: 0 0 8px; background: url(https://cdn2.hubspot.net/hub=
    [250] => fs/2799924/0107-ColorAndEmotions_Dan_Newsletter.png) 0% 0% / 640px 334px no=
    [251] => -repeat;  background-image: url(https://cdn2.hubspot.net/hubfs/2799924/0107=
    [252] => -ColorAndEmotions_Dan_Newsletter.png); background-size: 640px 334px; backgr=
    [253] => ound-repeat: no-repeat;">
    [254] =>                                 <a href=3D"https://hs-2799924.t.hubspotemai=
    [255] => l.net/e2t/c/*W3Lv-Nv3x5_DBW8x51Kp94S_Jb0/*VtbZKJ5-lw4gW96k1FY2QHK8P0/5/f18d=
    [256] => Qhb0SbTL8Y9XHdW5vB61F1m4DtzW7sSSsW7t5xj_W6Dk5R21Nvw7TVLDpF18CSvhfW8CRP2G5qj=
    [257] => cTMW1nPLDM66NxVpN65k5JRQfxpjW8v3mGX8l29DDW1qMMTn65jP-LW3J4LPS81gM8-N7d-tJnQ=
    [258] => J0n_W7Zby5m6cDM9PW4JZgrV2TlMg5W3VpkgJ96zRPSW6bT6L38RRjRDW5CktzD83KHrFW7J39q=
    [259] => H2m8DqKW2HT8mr6m41wNW2x-ccw7d094fW6G7Fbl4DFfS3W6Q8VBs8xy5CNW6Zp9Sx4TLPLBW4D=
    [260] => cBQ31wrQMDW6N8fX76nrJ2gN7fRq5MFPptcW5bGyZj25ztb6W1xMM-N656SL3V3klfs2zqqq2W8=
    [261] => wTrPk74GZfBW2HN9jY36lmXHW1Jb-jz3s75TXW4VCHKy8n4LYbW1VtdWZ2kL7-5N22TNxn9Mb5m=
    [262] => W471F-d3K39w2W9g-5_K3LlLY5V215-p1Jp47HW2Hlqhf3TmGm0W1VW0ZX257w0cW4DlsZJ3cp_=
    [263] => ynN8Kzpc4mRw0WDdXyXbWWz0ddFztl03" style=3D"display: block; width: 100%; hei=
    [264] => ght: 296px; text-decoration: none;" data-hs-link-id=3D"0" target=3D"_blank"=
    [265] => >&nbsp;</a>
    [266] =>                                 <div style=3D"display: block; width: 548px;=
    [267] =>  margin: 0 auto 0; padding: 30px; background: #FFFFFF;">
    [268] =>                                     <a href=3D"https://hs-2799924.t.hubspot=
    [269] => email.net/e2t/c/*W3Lv-Nv3x5_DBW8x51Kp94S_Jb0/*VPsPcN9lYCB2VNbYDW5KkNz20/5/f=
    [270] => 18dQhb0SbTL8Y9XHdW5vB61F1m4DtzW7sSSsW7t5xj_W6Dk5R21Nvw7TVLDpF18CSvhfW8CRP2G=
    [271] => 5qjcTMW1nPLDM66NxVpN65k5JRQfxpjW8v3mGX8l29DDW1qMMTn65jP-LW3J4LPS81gM8-N7d-t=
    [272] => JnQJ0n_W7Zby5m6cDM9PW4JZgrV2TlMg5W3VpkgJ96zRPSW6bT6L38RRjRDW5CktzD83KHrFW7J=
    [273] => 39qH2m8DqKW2HT8mr6m41wNW2x-ccw7d094fW6G7Fbl4DFfS3W6Q8VBs8xy5CNW6Zp9Sx4TLPLB=
    [274] => W4DcBQ31wrQMDW6N8fX76nrJ2gN7fRq5MFPptcW5bGyZj25ztb6W1xMM-N656SL3V3klfs2zqqq=
    [275] => 2W8wTrPk74GZfBW2HN9jY36lmXHW1Jb-jz3s75TXW4VCHKy8n4LYbW1VtdWZ2kL7-5N22TNxn9M=
    [276] => b5mW471F-d3K39w2W9g-5_K3LlLY5V215-p1Jp47HW2Hlqhf3TmGm0W1VW0ZX257w0cW4DlsZJ3=
    [277] => cp_ynN8Kzpc4mRw3gMdXyXb1x6ZPf29cx8803" style=3D"text-decoration: none;" dat=
    [278] => a-hs-link-id=3D"1" target=3D"_blank"><h1 style=3D"margin: 0; font-family: '=
    [279] => Helvetica Neue', Helvetica, 'Segoe UI', Arial, sans-serif; font-weight: 400=
    [280] => ; font-size: 30px; color: #204ECF;">Influence with Design - a Guide to Colo=
    [281] => r and Emotions</h1></a>
    [282] =>                                     <div style=3D"margin-top: 24px; font-fa=
    [283] => mily: 'Helvetica Neue', Helvetica, 'Segoe UI', Arial, sans-serif; font-size=
    [284] => : 16px; line-height: 23px;"><p style=3D"margin-bottom: 1em; "><span style=
    [285] => =3D"font-weight: 400;">The relationship between color and emotion is one of=
    [286] =>  the most important aspects of good UX design.</span></p>
    [287] => <p style=3D"margin-bottom: 1em; "><span style=3D"font-weight: 400;">Design =
    [288] => blog editor Cameron Chapman explains why the right color palette encourages=
    [289] =>  people to behave in ways designers want them to behave, while the wrong pa=
    [290] => lette can drive visitors away. </span></p></div>
    [291] =>                                     <a href=3D"https://hs-2799924.t.hubspot=
    [292] => email.net/e2t/c/*W3Lv-Nv3x5_DBW8x51Kp94S_Jb0/*W3dpm3-8_RtnYW7krm__5S29Dk0/5=
    [293] => /f18dQhb0SbTL8Y9XHdW5vB61F1m4DtzW7sSSsW7t5xj_W6Dk5R21Nvw7TVLDpF18CSvhfW8CRP=
    [294] => 2G5qjcTMW1nPLDM66NxVpN65k5JRQfxpjW8v3mGX8l29DDW1qMMTn65jP-LW3J4LPS81gM8-N7d=
    [295] => -tJnQJ0n_W7Zby5m6cDM9PW4JZgrV2TlMg5W3VpkgJ96zRPSW6bT6L38RRjRDW5CktzD83KHrFW=
    [296] => 7J39qH2m8DqKW2HT8mr6m41wNW2x-ccw7d094fW6G7Fbl4DFfS3W6Q8VBs8xy5CNW6Zp9Sx4TLP=
    [297] => LBW4DcBQ31wrQMDW6N8fX76nrJ2gN7fRq5MFPptcW5bGyZj25ztb6W1xMM-N656SL3V3klfs2zq=
    [298] => qq2W8wTrPk74GZfBW2HN9jY36lmXHW1Jb-jz3s75TXW4VCHKy8n4LYbW1VtdWZ2kL7-5N22TNxn=
    [299] => 9Mb5mW471F-d3K39w2W9g-5_K3LlLY5V215-p1Jp47HW2Hlqhf3TmGm0W1VW0ZX257w0cW4DlsZ=
    [300] => J3cp_ynN8Kzpc4mRw24DdXyXb8R1Tf4yt1Vb03" style=3D"display: inline-block; mar=
    [301] => gin-top: 32px; padding: 14px 48px; border-radius: 4px; background: #00CC83;=
    [302] =>  color: #FFFFFF; font-family: 'Helvetica Neue', Helvetica, 'Segoe UI', Aria=
    [303] => l, sans-serif; font-size: 15px; font-weight: 700; text-decoration: none; te=
    [304] => xt-align: center;" data-hs-link-id=3D"2" target=3D"_blank">Continue Reading=
    [305] => </a>
    [306] =>                                 </div>
    [307] =>                             </div>
    [308] =>                         </div>
    [309] =>                     </td>
    [310] =>                 </tr>
    [311] =>                 <tr>
    [312] =>                     <td style=3D"padding: 0;">
    [313] =>                         <div style=3D"display: block; width: 100%; backgrou=
    [314] => nd: #F3F3F3;">
    [315] =>                             <div style=3D"width: 548px; margin: 0 auto; pad=
    [316] => ding: 40px 0;">
    [317] =>                                 <h2 style=3D"margin: 0 0 20px; font-family:=
    [318] =>  'Helvetica Neue', Helvetica, 'Segoe UI', Arial, sans-serif; font-weight: 4=
    [319] => 00; font-size: 24px;">About the Author</h2>
    [320] =>                                 <div style=3D"float: right; width: 292px;">
    [321] =>                                     <h3 style=3D"margin-bottom: 32px; font-=
    [322] => family: 'Helvetica Neue', Helvetica, 'Segoe UI', Arial, sans-serif; font-we=
    [323] => ight: 400; font-size: 18px; color: #455065;">Other recommended articles:</h=
    [324] => 3>
    [325] =>                                     <ul style=3D"padding: 0 0 0 20px;">
    [326] =>                                        =20
    [327] =>                                        =20
    [328] =>                                        =20
    [329] =>                                             <li style=3D"margin: 0 0 32px;"=
    [330] => >
    [331] =>                                                 <a href=3D"https://hs-27999=
    [332] => 24.t.hubspotemail.net/e2t/c/*W3Lv-Nv3x5_DBW8x51Kp94S_Jb0/*W7HqCKG2xK3GwW1HQ=
    [333] => Wkn4SgS0Z0/5/f18dQhb0SbTY8XJ9c2N7rRy-jHyjJqW3LqXLs8q5JFzW3hHhd92P7_nXVcnTGj=
    [334] => 992gLmW4t0sSr1n3kJCW7nwMJH1xc3bNW8xGYBQ7dDZmZW2mytKR5RTccqW5Hz3cQ5lW29RW5lh=
    [335] => gkK5zD8mgW34vjNd3VqkBxW3J25ys3QtQNbW5MGDt17Psw5lW548GrJ5lKvt_N5420y5JVPWsW2=
    [336] => xqTTr328h7yW3_lZX35mZjbqN31H380c8rT8W30T_rP2Vv3csW1G8Mxx1Bb4rMW6F-Z-N2XMB1j=
    [337] => Vt-HdH2PgKcxW4cPpPz1QfT2CW58gnJF58C-zWN6mGNZdkHDb4W8XQWg347ysyMW50r5Wt4jMyc=
    [338] => NW45l0BQ1Tc8ZJW5dxdb35cNZ-3W8SQVXJ52D9fqW7lX3L_6cQKFSN7tpN01hvnG9W3Swq4p74s=
    [339] => krGW4M11334H_8kxW2Mdzgz1hsmx4W13gTRm3FsnNhVWDM002vD1bVW5Ns4Xh3TTssfW56flRB3=
    [340] => nmLvtW4C9_Rb51Y-CbW91Np7-1NwBMnN1MVsRj1pjpKf7TVg7K03" style=3D"font-family:=
    [341] =>  'Helvetica Neue', Helvetica, 'Segoe UI', Arial, sans-serif; font-size: 14p=
    [342] => x; text-decoration: none; color: #204ECF;" data-hs-link-id=3D"0" target=3D"=
    [343] => _blank">A Spectrum of Possibilities: The Go-To UI Color Guide </a>
    [344] =>                                             </li>
    [345] =>                                        =20
    [346] =>                                        =20
    [347] =>                                        =20
    [348] =>                                        =20
    [349] =>                                             <li style=3D"margin: 0 0 32px;"=
    [350] => >
    [351] =>                                                 <a href=3D"https://hs-27999=
    [352] => 24.t.hubspotemail.net/e2t/c/*W3Lv-Nv3x5_DBW8x51Kp94S_Jb0/*W1scMTP3wTZK7W4gP=
    [353] => hsh6WL1zy0/5/f18dQhb0Sq5J8XJ8NlN7rRy-jHyjJqW3LqXLs8q5JFzW3hHh8h5Cgxh0VnQ9Qq=
    [354] => 8--HBkW8Z_2Kr2K85-MW5mZ50N32pJXXW7MbyQp549vm9W5SXrhn8htXKxW9dr1642LKKL2W7JC=
    [355] => zQM8mrRhbW8lwW7v1YjLwxW9bTNXY954KlMW4N1BPY80dsqcN15SRx3T2xQ7W1bWQd05_7LR6W2=
    [356] => _1lbg5rcZX1W2-294g5J0bHmW1y7l3t5F_2JdW3XsqW05pfw1SW5mg0gg1CgtZfW5jPVDH1Rhwf=
    [357] => 9V4cNXy75WRHJVpZgcl1XRGp_W5Tsxfn5r7PCBW1sD8JT5_fDvnW4_zWtX2FK0jmW7p46r62Z40=
    [358] => g3W17zzwl7h9przW94rzfp3QbQGlW7V52FL5nVH1KVjXZhY94P7THW6pHRB067_gXDW5K3tzh1z=
    [359] => Mkb2W2QM0bK5gSHY5W6H5W1X3nTjygVVR6H24q1HYHV8hgJ41Syp30N47kQfDcVBl0W4QDcJ_1t=
    [360] => tPxdVL9ShT2RnYdNW2_ySWC6gLvJ1W1LXHqh47WGwNN6ZHqdpcYJKQW7dJ18n45fVCsf3X6Vls0=
    [361] => 4" style=3D"font-family: 'Helvetica Neue', Helvetica, 'Segoe UI', Arial, sa=
    [362] => ns-serif; font-size: 14px; text-decoration: none; color: #204ECF;" data-hs-=
    [363] => link-id=3D"0" target=3D"_blank">Design Psychology and the Neuroscience of A=
    [364] => wesome UX</a>
    [365] =>                                             </li>
    [366] =>                                        =20
    [367] =>                                        =20
    [368] =>                                        =20
    [369] =>                                        =20
    [370] =>                                             <li style=3D"margin: 0 0 32px;"=
    [371] => >
    [372] =>                                                 <a href=3D"https://hs-27999=
    [373] => 24.t.hubspotemail.net/e2t/c/*W3Lv-Nv3x5_DBW8x51Kp94S_Jb0/*W7YNy-r5rv5PDW249=
    [374] => 0Bz6Vg_Ry0/5/f18dQhb0SbTS8XJ8kFN7rRy-jHyjJqW3LqXLs8q5JFzW3hHhcB2P7_nXVcnTGj=
    [375] => 992gLmW4t0sSr1n3kJCW7nwMJH1xc3bNW8xGYBQ7dDZkwW98RG7m95S3rrW7cS-yG2lYZQrW4Bs=
    [376] => 6cn4yym9nW2nwPYk3_78LLW4JTXWy2MjL2DVsPHMl6d2lgMW6tyJbr1GmwJ3W7vPVHQ7w4nLlW3=
    [377] => yy-Cj2Rxr-sW7wVBbH5qBBjQW1BqcjB6tpJTgW5Wd0bF5-2sjBW7ZzDyK7GLjPjW2LHdpt1Z2HJ=
    [378] => 9W7n_xDv6rFpVKW7ZN28p25_bNBW1S4ggR71fjkqW7JNCMs1B5_swW7J-2sH2fWdxNW22P5cg7N=
    [379] => YqqGW2hR4jx7NS6VXW2dS1K42dPLMmW2hVQJv6Xf14dW753GZF7wQw6nW5_ZXVZ6Bn8KGW42ktn=
    [380] => R8ZsXk1VcWbVf4Wpz-0W1BbST46dwtZgW5TC_vx7wznqPVT6MS48j1VZYW5MHcPm5ycN39W20Xh=
    [381] => PR5KJp4XW8mNrjh4p34WLW8BqC5z6gVCkGw3xWwfqhzxf8GLsHX02" style=3D"font-family=
    [382] => : 'Helvetica Neue', Helvetica, 'Segoe UI', Arial, sans-serif; font-size: 14=
    [383] => px; text-decoration: none; color: #204ECF;" data-hs-link-id=3D"0" target=3D=
    [384] => "_blank">Cause and Effect =E2=80=93 Exploring Color Psychology</a>
    [385] =>                                             </li>
    [386] =>                                        =20
    [387] =>                                        =20
    [388] =>                                        =20
    [389] =>                                        =20
    [390] =>                                             <li style=3D"margin: 0 0 32px;"=
    [391] => >
    [392] =>                                                 <a href=3D"https://hs-27999=
    [393] => 24.t.hubspotemail.net/e2t/c/*W3Lv-Nv3x5_DBW8x51Kp94S_Jb0/*W6K5qt3449JQVM-Yb=
    [394] => Qb1-mmy0/5/f18dQhb0SfHC9dK7lMN7rRy-jHyjJqW3LqXLs8q5JFzW3hHhd75Cgxh0VnQ9Qq8-=
    [395] => -HBkW8Z_2Kr2K85-MW5mZ50N32pJXXW7MbyQp549nNxW8T6VND2MVlTDVXdM-k44QtFSVV9QRb8=
    [396] => q-Hk0W8tBr6R8CtcXQVTGjdK67jVjPW65x7m47Hv_hJW4cyNFY8Fdh1CN8k1dMQpSKvbN7Xd3Qs=
    [397] => k4l2_W6MjTY27lB_t5W5LMjlt2zhcvlW9dSlS635rgClW94-4T07sLfyrW520N2H7v70tSW2Hyb=
    [398] => 609dGZLlW25V5vB2jt165W3NnV4F1nJpwvW26pdfj35y0TxW6MkW8X35Gy09V_s9Gz1l-dkmW1q=
    [399] => gjz139sRCHVchr2v3hP7hWW4tfBSs34brR4N6PQjJW-C1CGW4SFjL17gJYKlW5H1MSg6TfPJbW5=
    [400] => _FSrt7c03mrW6NJpvy3k06GPW6NZB4f4YxfrdW4ZxpLT7q7-QcW6kl2SH7dr9qWW72YqDy3KQdF=
    [401] => RN2--wh37QqRQW5WSK_b4RtRwPW8mhg5w3hVGHxW9jrDtM7ZM5S0VBnvjp2gh8YpW11-FQN6Tp_=
    [402] => 6JW8B_Zvs1MWhN-W1MKdcd7z7s4x111" style=3D"font-family: 'Helvetica Neue', He=
    [403] => lvetica, 'Segoe UI', Arial, sans-serif; font-size: 14px; text-decoration: n=
    [404] => one; color: #204ECF;" data-hs-link-id=3D"0" target=3D"_blank">Design for Em=
    [405] => otion to Increase User Engagement</a>
    [406] =>                                             </li>
    [407] =>                                        =20
    [408] =>                                        =20
    [409] =>                                        =20
    [410] =>                                        =20
    [411] =>                                             <li style=3D"margin: 0 0 32px;"=
    [412] => >
    [413] =>                                                 <a href=3D"https://hs-27999=
    [414] => 24.t.hubspotemail.net/e2t/c/*W3Lv-Nv3x5_DBW8x51Kp94S_Jb0/*W5ntlMY3wmMkGW57S=
    [415] => 2Tc31bqDF0/5/f18dQhb0SbTK8Y9Xq0W5vB61F1m4DtzW7sSSsW7t5xj_W6Dk5Rq5zh-NRVnQ9Q=
    [416] => q8--HBkW8Z_2Kr2K85-MW5mZ50N32pJXXW7MbyQp549vm9W8YzV-V8Tzg0cW8Wm8_p8Fdh1CN8k=
    [417] => 1dMQpSKtRW6GmkKS6c-1lTW3y9THT32n0YgVZTj3h4DqHqzW6dgmw34yv2r0W3LmJLK20Y98hW1=
    [418] => YfY8X5hkTxhW5mg0gg3XXdf3W8xfqTq4yc3CKW3sSDqD5kmcLGW2Jb9PJ5d-Ty4W2X1mg86t_dJ=
    [419] => 4W2Jqdf53Y076kW3VY6--2YS8tKW6bLblN5Wlhn4W2X85rX5CS0WQW5YwGLg2GmxVDW4Gyc3p6P=
    [420] => kG5rW6H2RM-2H-SxCW3src1f5CRXWjW5WJrPz5khVfGW4rjdGH4cKckKW6p0MKL2tX1txW37P0d=
    [421] => 415hnZlN2-vbHlX_49wN24-7H5WyfqmW75hfNV2L5GhqW5-x53Z8Hmg-TW5Nv4T48Pq47wW7Snt=
    [422] => 797vflBTW6YdF7y6zxcXDMdSQk91_Q0Mf79SC2g11" style=3D"font-family: 'Helvetica=
    [423] =>  Neue', Helvetica, 'Segoe UI', Arial, sans-serif; font-size: 14px; text-dec=
    [424] => oration: none; color: #204ECF;" data-hs-link-id=3D"0" target=3D"_blank">The=
    [425] =>  Role of Color in UX</a>
    [426] =>                                             </li>
    [427] =>                                        =20
    [428] =>                                     </ul>
    [429] =>                                 </div>
    [430] =>                                 <div style=3D"width: 228px;">
    [431] =>                                     <div style=3D"width: 100%; overflow: hi=
    [432] => dden; background: #C6C9CD;">
    [433] =>                                         <a href=3D"" data-hs-link-id=3D"0" =
    [434] => target=3D"_blank"><img src=3D"https://cdn2.hubspot.net/hubfs/2799924/Design=
    [435] => %20Newsletters/Cameron.jpg" alt=3D"" style=3D"display: block; width: 100%;"=
    [436] => ></a>
    [437] =>                                     </div>
    [438] =>                                     <div style=3D"padding: 24px 22px; backg=
    [439] => round: #FFFFFF;">
    [440] =>                                         <h3 style=3D"margin: 0 0 6px; font-=
    [441] => family: 'Helvetica Neue', Helvetica, 'Segoe UI', Arial, sans-serif; font-we=
    [442] => ight: 400; font-size: 18px;">Cameron Chapman</h3>
    [443] =>                                         <p style=3D"margin-bottom: 1em; mar=
    [444] => gin: 0; font-family: 'Helvetica Neue', Helvetica, 'Segoe UI', Arial, sans-s=
    [445] => erif; font-weight: 700; font-size: 13px; color: #455065;">Design Blog Edito=
    [446] => r</p>
    [447] =>                                         <p style=3D"margin-bottom: 1em; lin=
    [448] => e-height: 22px; font-family: 'Helvetica Neue', Helvetica, 'Segoe UI', Arial=
    [449] => , sans-serif; font-size: 14px; color: #455065;"><span style=3D"font-weight:=
    [450] =>  400;">Cameron comes from a design background and is the author of two web =
    [451] => design books: <em>Color for Web Design</em> and <em>The Smashing Idea Book<=
    [452] => /em>.</span></p>
    [453] =>                                        =20
    [454] =>                                        =20
    [455] =>                                     </div>
    [456] =>                                 </div>
    [457] =>                                 <div style=3D"clear: both;"></div>
    [458] =>                             </div>
    [459] =>                         </div>
    [460] =>                     </td>
    [461] =>                 </tr>
    [462] =>                 <tr>
    [463] =>                     <td style=3D"padding: 0;">
    [464] =>                         <div style=3D"display: block; width: 100%; backgrou=
    [465] => nd: #FFFFFF;">
    [466] =>                             <div style=3D"width: 548px; margin: 0 auto; pad=
    [467] => ding: 40px 0;">
    [468] =>                                =20
    [469] =>                                 <h2 style=3D"margin: 0 0 20px; font-family:=
    [470] =>  'Helvetica Neue', Helvetica, 'Segoe UI', Arial, sans-serif; font-weight: 4=
    [471] => 00; font-size: 24px;">Hiring UX Designers?</h2>
    [472] =>                                 <p style=3D"margin-bottom: 1em; font-family=
    [473] => : 'Helvetica Neue', Helvetica, 'Segoe UI', Arial, sans-serif; font-size: 14=
    [474] => px; line-height: 20px;">Looking for an elite UX designer to join your team?=
    [475] =>  Get started with a Toptal account.</p>
    [476] =>                                 <a href=3D"https://hs-2799924.t.hubspotemai=
    [477] => l.net/e2t/c/*W3Lv-Nv3x5_DBW8x51Kp94S_Jb0/*W21HpRF5B75qHW8Df1XK2PrS510/5/f18=
    [478] => dQhb0Sjvk8YXN32N7rRy-jHyjJqW3LqXLs8q5JFzN3hHhdQXL0jYVnQ9Qq8--HBkW8Z_2Kr2K85=
    [479] => -MW5mZ50N4LZ65mW1L7bPx2kHlPdW676Zvd1ksGJhVDT9Nh5PydTKW6f8PsF3J25wnVtrsl_2Tl=
    [480] => Mg5W3Wdfwj7dDxTNW7mWsnX7dzcsSW51vDG61fdmZQW1x4lQB6HdqlTW7nwG0k6bnMRgW4NKqLs=
    [481] => 7P1-wWN33FK-yqPkxDVnjZC81GMlGtW7Lh92n4Qy1B_W32lnQQ5KwN7fW56TJcy1j3dxxW1hGf8=
    [482] => X1zYntxW2rb8fB4Ccz5JW11prx78grtpmW5NLs2B3p4VtwW2Qk-cN1hG59kW8kNxw96Ww7W7W5X=
    [483] => KMhl4b04gsW6d_WhM1VSk7JW2p8_TT7-cq4LW46nHYn3ygvH8N8c3mpjJ3lQsW7lb9HT7j7p6dM=
    [484] => X68QVd8rw0W2-XJ_h1smgbSW5FNrX95_5hkBW3bmx-g3tRYrJW8hQjYP4CcXzbVrVprC56gBW-W=
    [485] => 6VqqZk2L_pdx0" style=3D"display: inline-block; margin-top: 32px; padding: 1=
    [486] => 4px 48px; border: 1px solid #C4C6CA; border-radius: 4px; background: #FFFFF=
    [487] => F; color: #00CC83; font-family: 'Helvetica Neue', Helvetica, 'Segoe UI', Ar=
    [488] => ial, sans-serif; font-size: 15px; font-weight: 700; text-decoration: none; =
    [489] => text-align: center;" data-hs-link-id=3D"0" target=3D"_blank">Start Hiring</=
    [490] => a>
    [491] =>                             </div>
    [492] =>                         </div>
    [493] =>                     </td>
    [494] =>                 </tr>
    [495] =>                 <tr>
    [496] =>                     <td style=3D"padding: 0;">
    [497] =>                         <div style=3D"display: block; width: 100%; backgrou=
    [498] => nd: #262D3D;">
    [499] =>                             <div style=3D"width: 548px; margin: 0 auto; pad=
    [500] => ding: 30px;">
    [501] =>                                 <p style=3D"margin-bottom: 20px; font-famil=
    [502] => y: 'Helvetica Neue', Helvetica, 'Segoe UI', Arial, sans-serif; font-size: 1=
    [503] => 3px; line-height: 22px; color: #C4C6CA;">
    [504] =>                                     =C2=A9 2010-2019 Toptal, LLC. All right=
    [505] => s reserved. Toptal, LLC, 548 Market Street, San Francisco, California 94104=
    [506] => .
    [507] =>                                 </p>
    [508] =>                                 <p style=3D"margin-bottom: 1em; font-family=
    [509] => : 'Helvetica Neue', Helvetica, 'Segoe UI', Arial, sans-serif; font-size: 13=
    [510] => px;"><a href=3D"https://hs-2799924.s.hubspotemail.net/hs/manage-preferences=
    [511] => /unsubscribe?d=3DeyJlYSI6Imh6aGlsYW1wQDE2My5jb20iLCJlYyI6Njg4ODc0MTksInN1Yn=
    [512] => NjcmlwdGlvbklkIjozNTQ0Mjk2LCJldCI6MTU0NzEyMzc0NDA3NSwiZXUiOiIwZDM4OTNiYy05M=
    [513] => GI1LTRlNjEtYjM5YS01ODE3NDZmMjA5MDUifQ%3D%3D&amp;v=3D1&amp;utm_campaign=3DTo=
    [514] => ptal%20Design%20Blog&amp;utm_source=3Dhs_email&amp;utm_medium=3Demail&amp;u=
    [515] => tm_content=3D68887419&amp;_hsenc=3Dp2ANqtz-8LEgfLzMRs1qdtcNBEcd2eymXRPEY593=
    [516] => yqJXULyAL6GlAa3d_TU5CO_PEw524kGgX4gS_n_bJvGzZq8DlrFJz7TqiCUw&amp;_hsmi=3D68=
    [517] => 887419" style=3D"text-decoration: none; color: #FFFFFF;" data-hs-link-id=3D=
    [518] => "0" target=3D"_blank">Update your subscription preferences</a></p>
    [519] =>                             </div>
    [520] =>                         </div>
    [521] =>                     </td>
    [522] =>                 </tr>
    [523] =>             </tbody>
    [524] =>         </table>
    [525] =>     </div>
    [526] => <!-- end coded_template: id:5876930156 path:Custom/email/Engineering_Blog_E=
    [527] => mails/New_Article_v2.html -->
    [528] => <img src=3D"https://hs-2799924.t.hubspotemail.net/e2t/o/*W4Y4JBq6tby48W5gPf=
    [529] => Rn4sFhk20/*W5Bd-KH29QLlBN7LtsL2ZPz8R0/5/f18dQhb0J6s1gfPdW7CxCbq6crlb_W1f7_H=
    [530] => n22X_DlW1Q6zq82WvzRzW1RGqgd2lhw0SN2XZgmLmThQdW3R0JK93_YgH1W1-YQt143T13VN4RF=
    [531] => _rdNw158W7l1S0q5wyzxtVDjFD74V-L5bW5JWHVD6R3Pl7W1G1WVP87Tfpv101" alt=3D"" wi=
    [532] => dth=3D"1" height=3D"1" border=3D"0" style=3D"display:none!important;min-hei=
    [533] => ght:1px!important;width:1px!important;border-width:0!important;margin-top:0=
    [534] => !important;margin-bottom:0!important;margin-right:0!important;margin-left:0=
    [535] => !important;padding-top:0!important;padding-bottom:0!important;padding-right=
    [536] => :0!important;padding-left:0!important"><style>@media print{#_hs { backgroun=
    [537] => d-image: url('https://hs-2799924.t.hubspotemail.net/e2t/o/*W4Y4JBq6tby48W5g=
    [538] => PfRn4sFhk20/*W24Wlm03DBpMxW5btQL61C2k3F0/5/f18dQhb0KdhGBSCbDW7KFVlX2qwv1SMp=
    [539] => PCNfK0n-5W7Sdfkp6-_3RvN1zW07dzD-dgW1tw7R557ytxsN5Lk8VjgkPS5W6YHzwY6rDn2_W1J=
    [540] => p47H2HlqhfW3TmGm01VW0ZXW257w0c4DlsZJW3cp_yn8Kzpc4VmRsNG4NZwxn101');}} div.O=
    [541] => utlookMessageHeader {background-image:url('https://hs-2799924.t.hubspotemai=
    [542] => l.net/e2t/o/*W4Y4JBq6tby48W5gPfRn4sFhk20/*W2PFL9t6Bf3yQW6nnrXW4RLXPG0/5/f18=
    [543] => dQhb0KdhJBVg57W7KFVlX2qwv1SMpPCNfK0n-5W4kfNZl46x3G9N1h5Jfdgl_5-V1KsWQ1JN2LC=
    [544] => W57QG3z8252lrW1Vpnl09cYg06W1wlbN35cRNtSW6H4t9j4kLGYZW72l8f93l8QpJW1SJFZW8YP=
    [545] => 6mmF7wXrmK6GC9f80TrNg03')} table.moz-email-headers-table {background-image:=
    [546] => url('https://hs-2799924.t.hubspotemail.net/e2t/o/*W4Y4JBq6tby48W5gPfRn4sFhk=
    [547] => 20/*W2PFL9t6Bf3yQW6nnrXW4RLXPG0/5/f18dQhb0KdhJBVg57W7KFVlX2qwv1SMpPCNfK0n-5=
    [548] => W4kfNZl46x3G9N1h5Jfdgl_5-V1KsWQ1JN2LCW57QG3z8252lrW1Vpnl09cYg06W1wlbN35cRNt=
    [549] => SW6H4t9j4kLGYZW72l8f93l8QpJW1SJFZW8YP6mmF7wXrmK6GC9f80TrNg03')} blockquote =
    [550] => #_hs {background-image:url('https://hs-2799924.t.hubspotemail.net/e2t/o/*W4=
    [551] => Y4JBq6tby48W5gPfRn4sFhk20/*W2PFL9t6Bf3yQW6nnrXW4RLXPG0/5/f18dQhb0KdhJBVg57W=
    [552] => 7KFVlX2qwv1SMpPCNfK0n-5W4kfNZl46x3G9N1h5Jfdgl_5-V1KsWQ1JN2LCW57QG3z8252lrW1=
    [553] => Vpnl09cYg06W1wlbN35cRNtSW6H4t9j4kLGYZW72l8f93l8QpJW1SJFZW8YP6mmF7wXrmK6GC9f=
    [554] => 80TrNg03')} #MailContainerBody #_hs {background-image:url('https://hs-27999=
    [555] => 24.t.hubspotemail.net/e2t/o/*W4Y4JBq6tby48W5gPfRn4sFhk20/*W2PFL9t6Bf3yQW6nn=
    [556] => rXW4RLXPG0/5/f18dQhb0KdhJBVg57W7KFVlX2qwv1SMpPCNfK0n-5W4kfNZl46x3G9N1h5Jfdg=
    [557] => l_5-V1KsWQ1JN2LCW57QG3z8252lrW1Vpnl09cYg06W1wlbN35cRNtSW6H4t9j4kLGYZW72l8f9=
    [558] => 3l8QpJW1SJFZW8YP6mmF7wXrmK6GC9f80TrNg03')}</style><div id=3D"_hs"></div></b=
    [559] => ody></html>
    [560] => ------=_Part_1968210_2144246150.1547124410177--
    [561] => 
)

// 以第一个空行分割 header 和 body
Array
(
    [0] => Received: from pgg4ag.mail.toptal.com (unknown [54.174.63.102])
    [1] => 	by mx1 (Coremail) with SMTP id M8CowAC3UFCfPjdcE4u1Ag--.37719S15;
    [2] => 	Thu, 10 Jan 2019 20:46:55 +0800 (CST)
    [3] => Received: by 172.16.62.47 with SMTP id azlpzyulybvgvw37quuv1kafb1ikena6rwo52rn3r;
    [4] =>         Thu, 10 Jan 2019 12:46:50 GMT
    [5] => DKIM-Signature: v=1; s=hs1; d=mail.toptal.com;
    [6] =>         i=@mail.toptal.com;
    [7] =>         h=sender:from:reply-to:to:subject:mime-version:content-type:list-unsubscribe:x-report-abuse:form-sub;
    [8] =>         a=rsa-sha256; c=relaxed/relaxed;
    [9] =>         bh=Sr7c8dMnFS8BSAe1SfSfi7QRDDj8Qa9YrqQwHaHis0s=;
    [10] =>         b=bkRa1hIlLfpdlwrzk2OCvHWtHU0MC8/gJzm+0U1SUO4SJGSnOCPXDrZ/U5IUFR
    [11] =>          mcbVr3+P71feew58w6HuDe67hZoDQV5jLI1Qo3QwjaIAlQk2RA+I/RNW24DQxxq
    [12] =>          JTuI1wkHZ3tPSDZAXFhGEHcMPn3HHoNZdzQqiI5kXLyn0XAwJjL/eaRHh4o49G3
    [13] =>          zyKxDzCxIJJRrJMb0sNVoVbvJ6AxiF+DTssrWC1FOmliHXmUdaFb//cUokGeLG3
    [14] =>          3mT3Jf0Wxv2QmUhyq04X6Ukb59oAu46Em/luVOveo2JRmB5iHtmlTW6Uh0AInE4
    [15] =>          RnV4/RUlRVFDDs5r9+bA29bFaj3w==; q=dns/txt; t=1547124410;
    [16] => DKIM-Signature: v=1; s=hs1; d=toptal.com; i=@toptal.com;
    [17] =>         h=sender:from:reply-to:to:subject:mime-version:content-type:list-unsubscribe:x-report-abuse:form-sub;
    [18] =>         a=rsa-sha256; c=relaxed/relaxed;
    [19] =>         bh=Sr7c8dMnFS8BSAe1SfSfi7QRDDj8Qa9YrqQwHaHis0s=;
    [20] =>         b=K9jqmLCdxgii3sJAp3SHwmZpkybw10QQOm6794zbeJf9BL1WQjNN+8zSUbwV+G
    [21] =>          mEj+YzTbXXwXVtBrzm3/YiOOo2rfiG7MZK00J1dNiXhD/AZtbupfRPmEHSWLAB6
    [22] =>          kuhAJnxkUcHDkgQAtKauqwXYtHS1SBB6vGCxIvE+WP9TvYEDVesHukLUIGf6kNU
    [23] =>          Aq8JmMao8GRuOUfZWvaeqnL7/VUnBjxQh9LEZzDI90bjdsodEgAiRx2Z3Oxdjfz
    [24] =>          5hWsYErFfK/pN+IkxFfUgqnt6Hy7f6Zh1tvJtAU1oqyG/dyIb1PvQU8RI0Zuigz
    [25] =>          aA24wG3vTrlp+xPuwx4gf9viZF8w==; q=dns/txt; t=1547124410;
    [26] => Return-Path: <1axb06mzipx5up3rzlxc81eh16nhe81h8l7omi-hzhilamp=163.com@mail.toptal.com>
    [27] => X-HS-Cid: 1axe7t3rcjxusl6j2ajxiy9nriv74kj7tc6hc6
    [28] => List-Unsubscribe: <mailto:1axcxdq1nuanq1ngwg63bfoqiiso594ogfoq46-hzhilamp=163.com@mail.toptal.com?subject=unsubscribe>
    [29] => Date: Thu, 10 Jan 2019 07:46:50 -0500
    [30] => From: Toptal Design Blog <editor@toptal.com>
    [31] => Reply-To: editor@toptal.com
    [32] => To: hzhilamp@163.com
    [33] => Message-ID: <1547123744075.0d3893bc-90b5-4e61-b39a-581746f20905@mail.toptal.com>
    [34] => Subject: Influence with Design - a Guide to Color and Emotions
    [35] => MIME-Version: 1.0
    [36] => Content-Type: multipart/alternative;
    [37] => 	boundary="----=_Part_1968210_2144246150.1547124410177"
    [38] => X-Report-Abuse-To: abuse@hubspot.com (see
    [39] =>  https://www.hubspot.com/abuse-complaints)
    [40] => X-CM-TRANSID:M8CowAC3UFCfPjdcE4u1Ag--.37719S15
    [41] => Authentication-Results: mx1; spf=neutral smtp.mail=1axb06mzipx5up3rzlx
    [42] => 	c81eh16nhe81h8l7omi-hzhilamp=163.com@mail.toptal.com; dkim=pass header
    [43] => 	.i=@mail.toptal.com; dkim=pass header.i=@toptal.com
    [44] => X-Coremail-Antispam: 1Uf129KBjvdXoW7Wr43GF4rZr1xtrWrCw1kuFg_yoWDKrXE9r
    [45] => 	4ktr17Xw45X3WfJrWUta1j9rWjy3yUWr1kJrWfXF40q3sayws0ywnrCFykZw1fXayYgrZx
    [46] => 	Wr98Aa1fKa92vjkaLaAFLSUrUUUU2b8apTn2vfkv8UJUUUU8Yxn0WfASr-VFAUDa7-sFnT
    [47] => 	9fnUUvcSsGvfC2KfnxnUUI43ZEXa7IU5O183UUUUU==
    [48] => Sender: 1axb06mzipx5up3rzlxc81eh16nhe81h8l7omi-hzhilamp=163.com@mail.toptal.com
)

Array
(
    [0] => Received: from pgg4ag.mail.toptal.com (unknown [54.174.63.102])
by mx1 (Coremail) with SMTP id M8CowAC3UFCfPjdcE4u1Ag--.37719S15;
Thu, 10 Jan 2019 20:46:55 +0800 (CST)
    [1] => Received: by 172.16.62.47 with SMTP id azlpzyulybvgvw37quuv1kafb1ikena6rwo52rn3r;
Thu, 10 Jan 2019 12:46:50 GMT
    [2] => DKIM-Signature: v=1; s=hs1; d=mail.toptal.com;
i=@mail.toptal.com;
h=sender:from:reply-to:to:subject:mime-version:content-type:list-unsubscribe:x-report-abuse:form-sub;
a=rsa-sha256; c=relaxed/relaxed;
bh=Sr7c8dMnFS8BSAe1SfSfi7QRDDj8Qa9YrqQwHaHis0s=;
b=bkRa1hIlLfpdlwrzk2OCvHWtHU0MC8/gJzm+0U1SUO4SJGSnOCPXDrZ/U5IUFR
mcbVr3+P71feew58w6HuDe67hZoDQV5jLI1Qo3QwjaIAlQk2RA+I/RNW24DQxxq
JTuI1wkHZ3tPSDZAXFhGEHcMPn3HHoNZdzQqiI5kXLyn0XAwJjL/eaRHh4o49G3
zyKxDzCxIJJRrJMb0sNVoVbvJ6AxiF+DTssrWC1FOmliHXmUdaFb//cUokGeLG3
3mT3Jf0Wxv2QmUhyq04X6Ukb59oAu46Em/luVOveo2JRmB5iHtmlTW6Uh0AInE4
RnV4/RUlRVFDDs5r9+bA29bFaj3w==; q=dns/txt; t=1547124410;
    [3] => DKIM-Signature: v=1; s=hs1; d=toptal.com; i=@toptal.com;
h=sender:from:reply-to:to:subject:mime-version:content-type:list-unsubscribe:x-report-abuse:form-sub;
a=rsa-sha256; c=relaxed/relaxed;
bh=Sr7c8dMnFS8BSAe1SfSfi7QRDDj8Qa9YrqQwHaHis0s=;
b=K9jqmLCdxgii3sJAp3SHwmZpkybw10QQOm6794zbeJf9BL1WQjNN+8zSUbwV+G
mEj+YzTbXXwXVtBrzm3/YiOOo2rfiG7MZK00J1dNiXhD/AZtbupfRPmEHSWLAB6
kuhAJnxkUcHDkgQAtKauqwXYtHS1SBB6vGCxIvE+WP9TvYEDVesHukLUIGf6kNU
Aq8JmMao8GRuOUfZWvaeqnL7/VUnBjxQh9LEZzDI90bjdsodEgAiRx2Z3Oxdjfz
5hWsYErFfK/pN+IkxFfUgqnt6Hy7f6Zh1tvJtAU1oqyG/dyIb1PvQU8RI0Zuigz
aA24wG3vTrlp+xPuwx4gf9viZF8w==; q=dns/txt; t=1547124410;
    [4] => Return-Path: <1axb06mzipx5up3rzlxc81eh16nhe81h8l7omi-hzhilamp=163.com@mail.toptal.com>
    [5] => X-HS-Cid: 1axe7t3rcjxusl6j2ajxiy9nriv74kj7tc6hc6
    [6] => List-Unsubscribe: <mailto:1axcxdq1nuanq1ngwg63bfoqiiso594ogfoq46-hzhilamp=163.com@mail.toptal.com?subject=unsubscribe>
    [7] => Date: Thu, 10 Jan 2019 07:46:50 -0500
    [8] => From: Toptal Design Blog <editor@toptal.com>
    [9] => Reply-To: editor@toptal.com
    [10] => To: hzhilamp@163.com
    [11] => Message-ID: <1547123744075.0d3893bc-90b5-4e61-b39a-581746f20905@mail.toptal.com>
    [12] => Subject: Influence with Design - a Guide to Color and Emotions
    [13] => MIME-Version: 1.0
    [14] => Content-Type: multipart/alternative;
boundary="----=_Part_1968210_2144246150.1547124410177"
    [15] => X-Report-Abuse-To: abuse@hubspot.com (see
https://www.hubspot.com/abuse-complaints)
    [16] => X-CM-TRANSID:M8CowAC3UFCfPjdcE4u1Ag--.37719S15
    [17] => Authentication-Results: mx1; spf=neutral smtp.mail=1axb06mzipx5up3rzlx
c81eh16nhe81h8l7omi-hzhilamp=163.com@mail.toptal.com; dkim=pass header
.i=@mail.toptal.com; dkim=pass header.i=@toptal.com
    [18] => X-Coremail-Antispam: 1Uf129KBjvdXoW7Wr43GF4rZr1xtrWrCw1kuFg_yoWDKrXE9r
4ktr17Xw45X3WfJrWUta1j9rWjy3yUWr1kJrWfXF40q3sayws0ywnrCFykZw1fXayYgrZx
Wr98Aa1fKa92vjkaLaAFLSUrUUUU2b8apTn2vfkv8UJUUUU8Yxn0WfASr-VFAUDa7-sFnT
9fnUUvcSsGvfC2KfnxnUUI43ZEXa7IU5O183UUUUU==
    [19] => Sender: 1axb06mzipx5up3rzlxc81eh16nhe81h8l7omi-hzhilamp=163.com@mail.toptal.com
)
string(8) "received"
string(8) "received"
string(14) "dkim-signature"
string(14) "dkim-signature"
string(11) "return-path"
string(8) "x-hs-cid"
string(16) "list-unsubscribe"
string(4) "date"
string(4) "from"
string(8) "reply-to"
string(2) "to"
string(10) "message-id"
string(7) "subject"
string(12) "mime-version"
string(12) "content-type"
string(17) "x-report-abuse-to"
string(12) "x-cm-transid"
string(22) "authentication-results"
string(19) "x-coremail-antispam"
string(6) "sender"
Array
(
    [received] => from pgg4ag.mail.toptal.com (unknown [54.174.63.102])
by mx1 (Coremail) with SMTP id M8CowAC3UFCfPjdcE4u1Ag--.37719S15;
Thu, 10 Jan 2019 20:46:55 +0800 (CST)
Received: by 172.16.62.47 with SMTP id azlpzyulybvgvw37quuv1kafb1ikena6rwo52rn3r;
Thu, 10 Jan 2019 12:46:50 GMT
    [dkim-signature] => v=1; s=hs1; d=mail.toptal.com;
i=@mail.toptal.com;
h=sender:from:reply-to:to:subject:mime-version:content-type:list-unsubscribe:x-report-abuse:form-sub;
a=rsa-sha256; c=relaxed/relaxed;
bh=Sr7c8dMnFS8BSAe1SfSfi7QRDDj8Qa9YrqQwHaHis0s=;
b=bkRa1hIlLfpdlwrzk2OCvHWtHU0MC8/gJzm+0U1SUO4SJGSnOCPXDrZ/U5IUFR
mcbVr3+P71feew58w6HuDe67hZoDQV5jLI1Qo3QwjaIAlQk2RA+I/RNW24DQxxq
JTuI1wkHZ3tPSDZAXFhGEHcMPn3HHoNZdzQqiI5kXLyn0XAwJjL/eaRHh4o49G3
zyKxDzCxIJJRrJMb0sNVoVbvJ6AxiF+DTssrWC1FOmliHXmUdaFb//cUokGeLG3
3mT3Jf0Wxv2QmUhyq04X6Ukb59oAu46Em/luVOveo2JRmB5iHtmlTW6Uh0AInE4
RnV4/RUlRVFDDs5r9+bA29bFaj3w==; q=dns/txt; t=1547124410;
DKIM-Signature: v=1; s=hs1; d=toptal.com; i=@toptal.com;
h=sender:from:reply-to:to:subject:mime-version:content-type:list-unsubscribe:x-report-abuse:form-sub;
a=rsa-sha256; c=relaxed/relaxed;
bh=Sr7c8dMnFS8BSAe1SfSfi7QRDDj8Qa9YrqQwHaHis0s=;
b=K9jqmLCdxgii3sJAp3SHwmZpkybw10QQOm6794zbeJf9BL1WQjNN+8zSUbwV+G
mEj+YzTbXXwXVtBrzm3/YiOOo2rfiG7MZK00J1dNiXhD/AZtbupfRPmEHSWLAB6
kuhAJnxkUcHDkgQAtKauqwXYtHS1SBB6vGCxIvE+WP9TvYEDVesHukLUIGf6kNU
Aq8JmMao8GRuOUfZWvaeqnL7/VUnBjxQh9LEZzDI90bjdsodEgAiRx2Z3Oxdjfz
5hWsYErFfK/pN+IkxFfUgqnt6Hy7f6Zh1tvJtAU1oqyG/dyIb1PvQU8RI0Zuigz
aA24wG3vTrlp+xPuwx4gf9viZF8w==; q=dns/txt; t=1547124410;
    [return-path] => <1axb06mzipx5up3rzlxc81eh16nhe81h8l7omi-hzhilamp=163.com@mail.toptal.com>
    [x-hs-cid] => 1axe7t3rcjxusl6j2ajxiy9nriv74kj7tc6hc6
    [list-unsubscribe] => <mailto:1axcxdq1nuanq1ngwg63bfoqiiso594ogfoq46-hzhilamp=163.com@mail.toptal.com?subject=unsubscribe>
    [date] => Thu, 10 Jan 2019 07:46:50 -0500
    [from] => Toptal Design Blog <editor@toptal.com>
    [reply-to] => editor@toptal.com
    [to] => hzhilamp@163.com
    [message-id] => <1547123744075.0d3893bc-90b5-4e61-b39a-581746f20905@mail.toptal.com>
    [subject] => Influence with Design - a Guide to Color and Emotions
    [mime-version] => 1.0
    [content-type] => multipart/alternative;
boundary="----=_Part_1968210_2144246150.1547124410177"
    [x-report-abuse-to] => abuse@hubspot.com (see
https://www.hubspot.com/abuse-complaints)
    [x-cm-transid] => 8CowAC3UFCfPjdcE4u1Ag--.37719S15
    [authentication-results] => mx1; spf=neutral smtp.mail=1axb06mzipx5up3rzlx
c81eh16nhe81h8l7omi-hzhilamp=163.com@mail.toptal.com; dkim=pass header
.i=@mail.toptal.com; dkim=pass header.i=@toptal.com
    [x-coremail-antispam] => 1Uf129KBjvdXoW7Wr43GF4rZr1xtrWrCw1kuFg_yoWDKrXE9r
4ktr17Xw45X3WfJrWUta1j9rWjy3yUWr1kJrWfXF40q3sayws0ywnrCFykZw1fXayYgrZx
Wr98Aa1fKa92vjkaLaAFLSUrUUUU2b8apTn2vfkv8UJUUUU8Yxn0WfASr-VFAUDa7-sFnT
9fnUUvcSsGvfC2KfnxnUUI43ZEXa7IU5O183UUUUU==
    [sender] => 1axb06mzipx5up3rzlxc81eh16nhe81h8l7omi-hzhilamp=163.com@mail.toptal.com
)

Array
(
    [received] => from pgg4ag.mail.toptal.com (unknown [54.174.63.102])
by mx1 (Coremail) with SMTP id M8CowAC3UFCfPjdcE4u1Ag--.37719S15;
Thu, 10 Jan 2019 20:46:55 +0800 (CST)
Received: by 172.16.62.47 with SMTP id azlpzyulybvgvw37quuv1kafb1ikena6rwo52rn3r;
Thu, 10 Jan 2019 12:46:50 GMT
    [dkim-signature] => v=1
    [s] => hs1; d=mail.toptal.com;
i=@mail.toptal.com;
h=sender:from:reply-to:to:subject:mime-version:content-type:list-unsubscribe:x-report-abuse:form-sub;
a=rsa-sha256; c=relaxed/relaxed;
bh=Sr7c8dMnFS8BSAe1SfSfi7QRDDj8Qa9YrqQwHaHis0s=;
b=bkRa1hIlLfpdlwrzk2OCvHWtHU0MC8/gJzm+0U1SUO4SJGSnOCPXDrZ/U5IUFR
mcbVr3+P71feew58w6HuDe67hZoDQV5jLI1Qo3QwjaIAlQk2RA+I/RNW24DQxxq
JTuI1wkHZ3tPSDZAXFhGEHcMPn3HHoNZdzQqiI5kXLyn0XAwJjL/eaRHh4o49G3
zyKxDzCxIJJRrJMb0sNVoVbvJ6AxiF+DTssrWC1FOmliHXmUdaFb//cUokGeLG3
3mT3Jf0Wxv2QmUhyq04X6Ukb59oAu46Em/luVOveo2JRmB5iHtmlTW6Uh0AInE4
RnV4/RUlRVFDDs5r9+bA29bFaj3w==; q=dns/txt; t=1547124410;
DKIM-Signature: v=1; s=hs1; d=toptal.com; i=@toptal.com;
h=sender:from:reply-to:to:subject:mime-version:content-type:list-unsubscribe:x-report-abuse:form-sub;
a=rsa-sha256; c=relaxed/relaxed;
bh=Sr7c8dMnFS8BSAe1SfSfi7QRDDj8Qa9YrqQwHaHis0s=;
b=K9jqmLCdxgii3sJAp3SHwmZpkybw10QQOm6794zbeJf9BL1WQjNN+8zSUbwV+G
mEj+YzTbXXwXVtBrzm3/YiOOo2rfiG7MZK00J1dNiXhD/AZtbupfRPmEHSWLAB6
kuhAJnxkUcHDkgQAtKauqwXYtHS1SBB6vGCxIvE+WP9TvYEDVesHukLUIGf6kNU
Aq8JmMao8GRuOUfZWvaeqnL7/VUnBjxQh9LEZzDI90bjdsodEgAiRx2Z3Oxdjfz
5hWsYErFfK/pN+IkxFfUgqnt6Hy7f6Zh1tvJtAU1oqyG/dyIb1PvQU8RI0Zuigz
aA24wG3vTrlp+xPuwx4gf9viZF8w==; q=dns/txt; t=1547124410;
    [return-path] => <1axb06mzipx5up3rzlxc81eh16nhe81h8l7omi-hzhilamp=163.com@mail.toptal.com>
    [x-hs-cid] => 1axe7t3rcjxusl6j2ajxiy9nriv74kj7tc6hc6
    [list-unsubscribe] => <mailto:1axcxdq1nuanq1ngwg63bfoqiiso594ogfoq46-hzhilamp=163.com@mail.toptal.com?subject=unsubscribe>
    [date] => Thu, 10 Jan 2019 07:46:50 -0500
    [from] => Toptal Design Blog <editor@toptal.com>
    [reply-to] => editor@toptal.com
    [to] => hzhilamp@163.com
    [message-id] => <1547123744075.0d3893bc-90b5-4e61-b39a-581746f20905@mail.toptal.com>
    [subject] => Influence with Design - a Guide to Color and Emotions
    [mime-version] => 1.0
    [content-type] => multipart/alternative
    [boundary] => ----=_Part_1968210_2144246150.1547124410177
    [x-report-abuse-to] => abuse@hubspot.com (see
https://www.hubspot.com/abuse-complaints)
    [x-cm-transid] => 8CowAC3UFCfPjdcE4u1Ag--.37719S15
    [authentication-results] => mx1
    [spf] => neutral smtp.mail=1axb06mzipx5up3rzlx
c81eh16nhe81h8l7omi-hzhilamp=163.com@mail.toptal.com; dkim=pass header
.i=@mail.toptal.com; dkim=pass header.i=@toptal.com
    [x-coremail-antispam] => 1Uf129KBjvdXoW7Wr43GF4rZr1xtrWrCw1kuFg_yoWDKrXE9r
4ktr17Xw45X3WfJrWUta1j9rWjy3yUWr1kJrWfXF40q3sayws0ywnrCFykZw1fXayYgrZx
Wr98Aa1fKa92vjkaLaAFLSUrUUUU2b8apTn2vfkv8UJUUUU8Yxn0WfASr-VFAUDa7-sFnT
9fnUUvcSsGvfC2KfnxnUUI43ZEXa7IU5O183UUUUU==
    [sender] => 1axb06mzipx5up3rzlxc81eh16nhe81h8l7omi-hzhilamp=163.com@mail.toptal.com
)

// ['subject','from','sender','to','cc','return-path','reply','reply-to','name','filename'];

string(7) "subject"
string(53) "Influence with Design - a Guide to Color and Emotions"

string(4) "from"
string(38) "Toptal Design Blog <editor@toptal.com>"

string(6) "sender"
string(71) "1axb06mzipx5up3rzlxc81eh16nhe81h8l7omi-hzhilamp=163.com@mail.toptal.com"

string(2) "to"
string(16) "hzhilamp@163.com"

string(11) "return-path"
string(73) "<1axb06mzipx5up3rzlxc81eh16nhe81h8l7omi-hzhilamp=163.com@mail.toptal.com>"

string(8) "reply-to"
string(17) "editor@toptal.com"

// '/\=\?([a-z0-9\-]+)\?([a-z]{1})\?(.*)\?\=/i'
// =?GB2312?B?16O087zSyqW1rr3av+zA1n4=?=
// Q 对经过 quoted-printable 编码后的字符串进行解码
// B 对经过 base64 编码后的字符串进行解码

// GB2312 字符编码

// '/\?([a-z0-9\-]+)\?(b|q)\?(.*)\?\=/i'

// 特殊处理 content-type
string(21) "multipart/alternative"

// 特殊处理 content-transfer-encoding
// 特殊处理 charset

Array
(
    [received] => from pgg4ag.mail.toptal.com (unknown [54.174.63.102])
by mx1 (Coremail) with SMTP id M8CowAC3UFCfPjdcE4u1Ag--.37719S15;
Thu, 10 Jan 2019 20:46:55 +0800 (CST)
Received: by 172.16.62.47 with SMTP id azlpzyulybvgvw37quuv1kafb1ikena6rwo52rn3r;
Thu, 10 Jan 2019 12:46:50 GMT
    [dkim-signature] => v=1
    [return-path] => <1axb06mzipx5up3rzlxc81eh16nhe81h8l7omi-hzhilamp=163.com@mail.toptal.com>
    [x-hs-cid] => 1axe7t3rcjxusl6j2ajxiy9nriv74kj7tc6hc6
    [list-unsubscribe] => <mailto:1axcxdq1nuanq1ngwg63bfoqiiso594ogfoq46-hzhilamp=163.com@mail.toptal.com?subject=unsubscribe>
    [date] => Thu, 10 Jan 2019 07:46:50 -0500
    [from] => Toptal Design Blog <editor@toptal.com>
    [reply-to] => editor@toptal.com
    [to] => hzhilamp@163.com
    [message-id] => <1547123744075.0d3893bc-90b5-4e61-b39a-581746f20905@mail.toptal.com>
    [subject] => Influence with Design - a Guide to Color and Emotions
    [mime-version] => 1.0
    [content-type] => multipart/alternative
    [x-report-abuse-to] => abuse@hubspot.com (see
https://www.hubspot.com/abuse-complaints)
    [x-cm-transid] => 8CowAC3UFCfPjdcE4u1Ag--.37719S15
    [authentication-results] => mx1
    [x-coremail-antispam] => 1Uf129KBjvdXoW7Wr43GF4rZr1xtrWrCw1kuFg_yoWDKrXE9r
4ktr17Xw45X3WfJrWUta1j9rWjy3yUWr1kJrWfXF40q3sayws0ywnrCFykZw1fXayYgrZx
Wr98Aa1fKa92vjkaLaAFLSUrUUUU2b8apTn2vfkv8UJUUUU8Yxn0WfASr-VFAUDa7-sFnT
9fnUUvcSsGvfC2KfnxnUUI43ZEXa7IU5O183UUUUU==
    [sender] => 1axb06mzipx5up3rzlxc81eh16nhe81h8l7omi-hzhilamp=163.com@mail.toptal.com
    [s] => hs1; d=mail.toptal.com;
i=@mail.toptal.com;
h=sender:from:reply-to:to:subject:mime-version:content-type:list-unsubscribe:x-report-abuse:form-sub;
a=rsa-sha256; c=relaxed/relaxed;
bh=Sr7c8dMnFS8BSAe1SfSfi7QRDDj8Qa9YrqQwHaHis0s=;
b=bkRa1hIlLfpdlwrzk2OCvHWtHU0MC8/gJzm+0U1SUO4SJGSnOCPXDrZ/U5IUFR
mcbVr3+P71feew58w6HuDe67hZoDQV5jLI1Qo3QwjaIAlQk2RA+I/RNW24DQxxq
JTuI1wkHZ3tPSDZAXFhGEHcMPn3HHoNZdzQqiI5kXLyn0XAwJjL/eaRHh4o49G3
zyKxDzCxIJJRrJMb0sNVoVbvJ6AxiF+DTssrWC1FOmliHXmUdaFb//cUokGeLG3
3mT3Jf0Wxv2QmUhyq04X6Ukb59oAu46Em/luVOveo2JRmB5iHtmlTW6Uh0AInE4
RnV4/RUlRVFDDs5r9+bA29bFaj3w==; q=dns/txt; t=1547124410;
DKIM-Signature: v=1; s=hs1; d=toptal.com; i=@toptal.com;
h=sender:from:reply-to:to:subject:mime-version:content-type:list-unsubscribe:x-report-abuse:form-sub;
a=rsa-sha256; c=relaxed/relaxed;
bh=Sr7c8dMnFS8BSAe1SfSfi7QRDDj8Qa9YrqQwHaHis0s=;
b=K9jqmLCdxgii3sJAp3SHwmZpkybw10QQOm6794zbeJf9BL1WQjNN+8zSUbwV+G
mEj+YzTbXXwXVtBrzm3/YiOOo2rfiG7MZK00J1dNiXhD/AZtbupfRPmEHSWLAB6
kuhAJnxkUcHDkgQAtKauqwXYtHS1SBB6vGCxIvE+WP9TvYEDVesHukLUIGf6kNU
Aq8JmMao8GRuOUfZWvaeqnL7/VUnBjxQh9LEZzDI90bjdsodEgAiRx2Z3Oxdjfz
5hWsYErFfK/pN+IkxFfUgqnt6Hy7f6Zh1tvJtAU1oqyG/dyIb1PvQU8RI0Zuigz
aA24wG3vTrlp+xPuwx4gf9viZF8w==; q=dns/txt; t=1547124410;
    [boundary] => ----=_Part_1968210_2144246150.1547124410177
    [spf] => neutral smtp.mail=1axb06mzipx5up3rzlx
c81eh16nhe81h8l7omi-hzhilamp=163.com@mail.toptal.com; dkim=pass header
.i=@mail.toptal.com; dkim=pass header.i=@toptal.com
    [_type] => multipart
    [_subtype] => alternative
)

// 特殊处理 x-originating-ip
// 特殊处理 received
from pgg4ag.mail.toptal.com (unknown [54.174.63.102])
by mx1 (Coremail) with SMTP id M8CowAC3UFCfPjdcE4u1Ag--.37719S15;
Thu, 10 Jan 2019 20:46:55 +0800 (CST)
Received: by 172.16.62.47 with SMTP id azlpzyulybvgvw37quuv1kafb1ikena6rwo52rn3r;
Thu, 10 Jan 2019 12:46:50 GMT
Array
(
    [0] => Array
        (
            [0] => 54.174.63.102
            [1] => 172.16.62.47
        )

    [1] => Array
        (
            [0] => 54.174.63.102
            [1] => 172.16.62.47
        )

)
$this->head['x-originating-ip'][] = $ip;
$ip_addr = trim(exec('geoiplookup  -f /var/lib/GeoIP/GeoLiteCity.dat '.$ip.'|cut -d: -f2'));
$this->head['x-geo-ip'][ip2long($ip)] = $ip_arr;

$received_array = explode($this->_line_cut,$this->head['received']);
$this->head['date'] = trim($received_array[2]);

$this->head['from'] = $this->head['sender'];

```




