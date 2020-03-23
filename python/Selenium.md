# Selenium

## Selenium.webdriver 和 RemoteWebDriver 是什么？

《Selenium自动化测试 基于 Python 语言》P54

## InternetExplorerDriver

《Selenium自动化测试 基于 Python 语言》P59

## ChromeDriver

《Selenium自动化测试 基于 Python 语言》P63


## unittest

* unittest 基础
* 断言
* 测试套件
* HTML 报告

《Selenium自动化测试 基于 Python 语言》P67











selenium 是一套完整的web应用程序测试系统，包含了测试的录制（selenium IDE）,编写及运行（Selenium Remote Control）和测试的并行处理（Selenium Grid）。Selenium的核心Selenium Core基于JsUnit，完全由JavaScript编写，因此可以用于任何支持JavaScript的浏览器上。

selenium可以模拟真实浏览器，自动化测试工具，支持多种浏览器，爬虫中主要用来解决JavaScript渲染问题。

### 相关组件

* Selenium IDE：一个Firefox插件，可以录制用户的基本操作，生成测试用例。随后可以运行这些测试用例在浏览器里回放，可将测试用例转换为其他语言的自动化脚本。

* Selenium WebDriver：浏览器驱动

* Selenium 1 (Selenium RC)：Selenium Remote Control (RC) ：支持多种平台(Windows，Linux，Solaris)和多种浏览器(IE，Firefox，Opera，Safari)，可以用多种语言(Java，Ruby，Python，Perl，PHP，C#)编写测试用例。

* Selenium-Grid：允许Selenium-RC 针对规模庞大的测试案例集或者需要在不同环境中运行的测试案例集进行扩展。


### Appium
Appium is an open source test automation framework for use with native, hybrid and mobile web apps.
It drives iOS, Android, and Windows apps using the WebDriver protocol.