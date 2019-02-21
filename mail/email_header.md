## Email Header

An email consists of three vital components: the envelope, the header(s), and the body of the message. The envelope is something that an email user will never see since it is part of the internal process by which an email is routed. The body is the part that we always see as it is the actual content of the message contained in the email. The header(s), the third component of an email, is perhaps a little more difficult to explain, though it is arguably the most interesting part of an email.  电子邮件由三个重要组成部分组成：信封，标题和邮件正文。 信封是电子邮件用户永远不会看到的，因为它是电子邮件路由的内部流程的一部分。 正文是我们总是看到的部分，因为它是电子邮件中包含的消息的实际内容。 标题（电子邮件的第三个组成部分）可能稍微难以解释，尽管它可以说是电子邮件中最有趣的部分。

### Header

In an e-mail, the body (content text) is always preceded by header lines that identify particular **routing information** of the message, including the **sender**, **recipient**, **date** and **subject**. Some headers are mandatory, such as the **FROM**, **TO** and **DATE** headers. Others are optional, but very commonly used, such as **SUBJECT** and **CC**. Other headers include **the sending time** stamps and **the receiving time** stamps of all mail transfer agents that have received and sent the message. In other words, any time a message is transferred from one user to another (i.e. when it is sent or forwarded), the message is date/time stamped by a mail transfer agent (MTA) - a computer program or software agent that facilitates the transfer of email message from one computer to another. This date/time stamp, like FROM, TO, and SUBJECT, becomes one of the many headers that precede the body of an email.  在电子邮件中，正文（内容文本）前面总是标题行标识消息的特定路由信息，包括发件人，收件人，日期和主题。 某些标头是必需的，例如FROM，TO和DATE标头。 其他是可选的，但非常常用，例如SUBJECT和CC。 其他标头包括已接收和发送消息的所有邮件传输代理的发送时间戳和接收时间戳。 换句话说，无论何时将消息从一个用户传送到另一个用户（即，当它被发送或转发时），该消息都是由邮件传输代理（MTA）标记的日期/时间 - 用于促进该消息的计算机程序或软件代理。 将电子邮件从一台计算机传输到另一台计算机 此日期/时间戳（如FROM，TO和SUBJECT）将成为电子邮件正文之前的众多标题之一。

To really understand what an email header is, you must see one. Here is an example of a full email header*:  要真正了解电子邮件标题是什么，您必须看到一个。 以下是完整电子邮件标题*的示例：

```
Received: from em.oreilly.com (unknown [192.28.152.137])
	by mx40 (Coremail) with SMTP id WsCowABXjR0B_Ehc5+UEDw--.38557S9;
	Thu, 24 Jan 2019 07:43:07 +0800 (CST)
Return-Path: <reply@oreilly.com>
X-MSFBL: aHpoaWxhbXBAMTYzLmNvbUBkdnAtMTkyLTI4LTE1Mi0xMzdAYmctYWJkLTYyMkAx
	MDctRk1TLTA3MDozOTc1Ojc5MzM6MjUzNTk6MDo1Mzc1Ojk6MTY1MTY6MTA5NTQ4
	MTk=
Received: from [10.1.87.249] ([10.1.87.249:45085] helo=abmas01.marketo.org)
	by abmta05.marketo.org (envelope-from <reply@oreilly.com>)
	(ecelerity 3.6.8.47404 r(Core:3.6.8.0)) with ESMTP
	id 4C/85-48062-B0CF84C5; Wed, 23 Jan 2019 17:43:07 -0600
DKIM-Signature: v=1; a=rsa-sha256; q=dns/txt; c=relaxed/relaxed; t=1548286987;
	s=m1; d=oreilly.com; i=@oreilly.com;
	h=Date:From:To:Subject:MIME-Version:Content-Type;
	bh=YFLvxCec3AzEl2iLqLizFofQAjKsWrc9L4/HdqmkFlQ=;
	b=fRyQxVeWI5xGH7iNk5fvYfekQMpmwc9sW/lXijhGRsyA+g1zjnLGGwQxtH0v38BQ
	wJ+9konTWjhqNdWM3b6QDmb3ZFmgF6UMoW1kY/5SXwlBpy31VsflaqFldEPhMqo8v3c
	6B+cr2O8npjzNl7L9JS/og5OXMOf3wQYkmh1vc+M=
DKIM-Signature: v=1; a=rsa-sha256; q=dns/txt; c=relaxed/relaxed; t=1548286987;
	s=m1; d=mktdns.com; i=@mktdns.com;
	h=Date:From:To:Subject:MIME-Version:Content-Type;
	bh=YFLvxCec3AzEl2iLqLizFofQAjKsWrc9L4/HdqmkFlQ=;
	b=V6SWlm8ZRFO9V1i+lARAk/rjfPqMOQrTvVx0AHjeNzyP0bmd1Ag1lDWNc56icZaY
	aBseqclA+2VsDlm8X5zU/vcssN2oqR/E/9DluoJ09awYV8nMbKTZAPyJCi4I8ovxNb+
	ETrK/izEC++0LCl1VNHUJnwES2xSMdUKyhG21MmY=
Date: Wed, 23 Jan 2019 17:43:07 -0600 (CST)
From: O'Reilly Web Newsletter <reply@oreilly.com>
Reply-To: reply@oreilly.com
To: hzhilamp@163.com
Message-ID: <1140434236.-958832893.1548286987105.JavaMail.root@abmas01.marketo.org>
Subject: React, Angular, Vue, var, let, and const (and more)
MIME-Version: 1.0
Content-Type: multipart/alternative; 
	boundary="----=_Part_-958832894_1297831561.1548286987104"
X-PVIQ: mkto-107FMS070-000001-000000-016516
X-Binding: bg-abd-622
X-MarketoID: 107-FMS-070:3975:7933:25359:0:5375:9:16516:10954819
X-MktArchive: false
List-Unsubscribe: <mailto:KVRDK6KYKEZGM4SWPBXVSZLHHBRXITSXMJAT2PI.16516.5375.9@unsub-ab.mktomail.com>
X-Mailfrom: 107-FMS-070.0.16516.0.0.5375.9.10954819@em.oreilly.com
X-MSYS-API: {"options":{"open_tracking":false,"click_tracking":false}}
X-MktMailDKIM: true
X-CM-TRANSID:WsCowABXjR0B_Ehc5+UEDw--.38557S9
Authentication-Results: mx40; spf=pass smtp.mail=107-fms-070.0.16516.0
	.0.5375.9.10954819@em.oreilly.com; dkim=pass header.i=@oreilly.com; dk
	im=pass header.i=@mktdns.com
X-Coremail-Antispam: 1Uf129KBjvJXoWxCr4fAFyDZrWxKw47tw4UXFb_yoW5AF17pF
	Z3K34Yyr4vqry0k340y3WxXF4F93yktF45KryUJryvyw45CF93Zry3KrWYyFW5AFWkAw12
	v3yjvFy7Za909aDanT9S1TB71UUUbYJqnTZGkaVYY2UrUUUUjbIjqfuFe4nvWSU5nxnvy2
	9KBjDUYxBIdaVFxhVjvjDU0xZFpf9x07U7sqXUUUUU=
Sender: 107-fms-070.0.16516.0.0.5375.9.10954819@em.oreilly.com
```

email headers should always be read from bottom to top.  电子邮件标题应始终从下到上阅读。

Fortunately, most of this information is hidden inside the email with only the most relevant or mandatory headers appearing to the user. Those headers that we most often see and recognize are bolded in the above example.  幸运的是，大部分信息都隐藏在电子邮件中，只有最相关或最强的标题出现在用户身上。 我们最常见到并识别的标题在上面的示例中以粗体显示。 

### Header Characteristics 标题特征

A single email header has some important characteristics, including perhaps the most important part of an email - this is the KEY:VALUE pairs contained in the header. Looking at the above, you can tell some of the KEY:VALUE pairs used. Here is a breakdown of the most commonly used and viewed headers, and their values:  单个电子邮件标题具有一些重要特征，包括可能是电子邮件中最重要的部分 - 这是标题中包含的KEY：VALUE对。 看看上面的内容，您可以了解一些使用的KEY：VALUE对。 以下是最常用和查看的标题及其值的细分:

* From: sender's name and email address (IP address here also, but hidden) 发件人：发件人姓名和电子邮件地址（此处也是IP地址，但隐藏）
* To: recipient's name and email address 收件人：收件人的姓名和电子邮件地址
* Date: sent date/time of the email 日期：发送电子邮件的日期/时间
* Subject: whatever text the sender entered in the Subject heading before sending 主题：发送者在主题标题中输入的任何文本

### Headers Provide Routing Information

Besides the most common identifications (from, to, date, subject), email headers also provide information on the route an email takes as it is transferred from one computer to another. As mentioned earlier, mail transfer agents (MTA) facilitate email transfers. When an email is sent from one computer to another it travels through a MTA. Each time an email is sent or forwarded by the MTA, it is stamped with a date, time and recipient. This is why some emails, if they have had several destinations, may have several **RECEIVED** headers: there have been multiple recipients since the origination of the email. In a way it is much like the same way the post office would route a letter: every time the letter passes through a post office on its route, or if it is forwarded on, it will receive a stamp. In this case the stamp is an email header.  除了最常见的标识（从，到，日期，主题），电子邮件标题还提供有关电子邮件从一台计算机传输到另一台计算机时所采用的路由的信息。 如前所述，邮件传输代理（MTA）有助于电子邮件传输。 当电子邮件从一台计算机发送到另一台计算机时，它将通过MTA传输。 每次MTA发送或转发电子邮件时，都会标记日期，时间和收件人。 这就是为什么有些电子邮件，如果它们有多个目的地，可能有几个RECEIVED标题：自电子邮件发起以来就有多个收件人。 在某种程度上，它与邮局路由信件的方式非常相似：每当信件通过其路线上的邮局时，或者如果邮件被转发，它将收到一张邮票。 在这种情况下，邮票是电子邮件标题。

When viewed in their entirety, these multiple recipient headers will look like this in an email:  从整体上看，这些多个收件人标题在电子邮件中将如下所示：

```
Received: from tom.bath.dc.uk ([138.38.32.21] ident=yalrla9a1j69szla2ydr)
        by steve.wrath.dc.uk with esmtp (Exim 3.36 #2)id 19OjC3-00064B-00
        for example_to@imaps.bath.dc.uk; Sat, 07 Jun 2005 20:17:35 +0100

Received: from write.example.com ([205.206.231.26])
        by tom.wrath.dc.uk with esmtp id 19OjBy-0001lb-3V
        for example_to@bath.ac.uk; Sat, 07 Jun 2005 20:17:30 +0100

Received: from master.example.com (lists.example.com [205.206.231.19])
        by write.example.com (Postfix) with QMQP
        id F11418F2C1; Sat, 7 Jun 2005 12:34:34 -0600 (MDT)
```
or
```
Received: from m12-17.163.com (unknown [220.181.12.17])
	by newmx33.qq.com (NewMx) with SMTP id 
	for <774126846@qq.com>; Thu, 24 Jan 2019 16:47:53 +0800
Received: from huzhi (unknown [111.172.4.57])
	by smtp13 (Coremail) with SMTP id EcCowABXS7g6e0lcQjIvDA--.60931S2;
	Thu, 24 Jan 2019 16:47:04 +0800 (CST)
```
or
```
Received: from em.oreilly.com (unknown [192.28.152.137])
	by mx40 (Coremail) with SMTP id WsCowABXjR0B_Ehc5+UEDw--.38557S9;
	Thu, 24 Jan 2019 07:43:07 +0800 (CST)
Received: from [10.1.87.249] ([10.1.87.249:45085] helo=abmas01.marketo.org)
	by abmta05.marketo.org (envelope-from <reply@oreilly.com>)
	(ecelerity 3.6.8.47404 r(Core:3.6.8.0)) with ESMTP
	id 4C/85-48062-B0CF84C5; Wed, 23 Jan 2019 17:43:07 -0600

# IP address 10.1.87.249 was ignored because it is a Private-Use Network address.
```

In the example shown above, there are three Received: stamps. **Reading from the bottom upwards**, you can see who sent the message first, next and last, and you can see when it was done. This is because every MTA that processed the email message added a Received: line to the email's header. These Received: lines provide information on where the message originated and what stops it made (what computers) before reaching its final destination. As the example shows, these Received: lines provide the email and IP address of each sender and recipient. They also provide the date and time of each transfer. The lines also indicate if the email address was part of an email list. It is all this information that is valued by computer programmers and IT department associates when making efforts to track and stop SPAM email message. And it is this information that arguable makes headers the most important part of an email. 在上面显示的示例中，有三个Received：戳记。 从下往上阅读，您可以看到谁先发送消息，下一次和最后发送消息，您可以看到它何时完成。 这是因为处理电子邮件的每个MTA都在电子邮件的标题中添加了Received：行。 这些Received：行提供了有关消息源自何处以及在到达其最终目的地之前停止了什么（哪些计算机）的信息。 如示例所示，这些Received：行提供每个发件人和收件人的电子邮件和IP地址。 它们还提供每次转移的日期和时间。 这些行还指示电子邮件地址是否是电子邮件列表的一部分。 在努力跟踪和停止垃圾邮件时，计算机程序员和IT部门员工都会重视这些信息。 正是这些信息可以说标题是电子邮件中最重要的部分。 

### Headers Fields

It is important to know that when reading an email header every line can be forged, so only the **Received**: lines that are created by your service or computer should be completely trusted.  重要的是要知道，在阅读电子邮件标题时，每行都可以伪造，因此只有您的服务或计算机创建的Received：行才应该完全受信任。

* From

This displays who the message is from, however, this can be easily forged and can be the least reliable.  这显示了消息的来源，但是，这可以很容易伪造，并且可能是最不可靠的。

* Subject

This is what the sender placed as a topic of the email content.

* Date

This shows the date and time the email message was composed.

* To

This shows to whom the message was addressed, but may not contain the recipient's address.  这表明邮件已向谁发送，但可能不包含收件人的地址。

* CC

A cc means that other recipients of the email can see the cc recipient listed

* BCC

A bcc means that other recipients of the email do not see the bcc recipient listed

* Sender

```
Sender: 107-fms-070.0.16516.0.0.5375.9.10954819@em.oreilly.com
```

* Return-Path

The email address for return mail. This is the same as "Reply-To:".  返回邮件的电子邮件地址。 这与“回复：”相同。
```
Return-Path: <reply@oreilly.com>
Reply-To: reply@oreilly.com
```

* Envelope-To（？？）

This header shows that this email was delivered to the mailbox of a subscriber whose email address is user@example.com.

* Delivery Date

This shows the date and time at which the email was received by your (mt) service or email client.

* Received

The received is the most important part of the email header and is usually the most reliable. They form a list of all the servers/computers through which the message traveled in order to reach you.  received是电子邮件标题中最重要的部分，通常是最可靠的部分。 它们形成了所有服务器/计算机的列表，消息通过这些服务器/计算机与您联系。

The received lines are best read from bottom to top. That is, the first "Received:" line is your own system or mail server. The last "Received:" line is where the mail originated. Each mail system has their own style of "Received:" line. A "Received:" line typically identifies the machine that received the mail and the machine from which the mail was received.  收到的行最好从下到上阅读。 也就是说，第一个“已接收：”行是您自己的系统或邮件服务器。 最后一个“已接收：”行是邮件发送的位置。 每个邮件系统都有自己的“Received：”行样式。 “已接收：”行通常标识接收邮件的计算机和从中接收邮件的计算机。

* X-Originating-IP

The easiest way for finding the original sender is by looking for the X-Originating-IP header. This header is important since it tells you the IP address of the computer that had sent the email.

* Dkim-Signature & Domainkey-Signature（？？）

These are related to domain keys which are currently not supported by (mt) Media Temple services. You can learn more about these by visiting: http://en.wikipedia.org/wiki/DomainKeys.

* Message-id

A unique string assigned by the mail system when the message is first created. These can easily be forged.

* Mime-Version

Multipurpose Internet Mail Extensions (MIME) is an Internet standard that extends the format of email. Please see http://en.wikipedia.org/wiki/MIME for more details.

* Content-Type

Generally, this will tell you the format of the message, such as html or plaintext.

* X-Spam-Status

Displays a spam score created by your service or mail client.  显示由服务或邮件客户端创建的垃圾邮件分数。

* X-Spam-Level

Displays a spam score usually created by your service or mail client.

* spf

SPF：Sender Policy Framework，发件人保证框架。出现的主要原因是SMTP协议的缺陷。SMTP协议中，发件人的邮箱地址是可以伪造的，因而SPF的出现就是防止伪造发件人。SPF的记录实际上就是DNS服务器上面的一个记录。

* dkim-signature

Domain Keys Identified Mail。功能与SPF相似，主要是让收件人可以通过加密解密的方式来得知发件人是否是真实的。原理就是在电子邮件的开头插入一段签名，然后接收方通过从DNS查询得到公钥以后，以进行验证，与SSH的公钥和密钥类似。


### 参考

* https://whatismyipaddress.com/email-header
* https://mediatemple.net/community/products/dv/204643950/understanding-an-email-header
* https://www.iana.org/assignments/message-headers/message-headers.xhtml














