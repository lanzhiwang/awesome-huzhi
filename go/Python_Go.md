## Goodbye Python. Hello Go.

I’ve been using Go for a lot of the tasks where I used to use Python. 我一直在使用Go来完成我以前使用Python的很多任务。

Some examples:

* Processing Cloudfront logs stored in S3
* Moving Terabytes of files between buckets and/or regions in S3
* Matching up files between our database records and S3 ensuring everything is in sync.

Most are one-off tasks which is why a scripting language has been ideal. The program needs to be written quickly and then most likely thrown away. Usually the task is something new and unique, so code reuse is minimal. 大多数是一次性任务，这就是脚本语言理想的原因。 该程序需要快速编写，然后很可能被丢弃。 通常，任务是新的和独特的，因此代码重用是最小的。

Below are some advantages of using Go instead of Python. 以下是使用Go而不是Python的一些优点。

### Having a Compiler is Nice 编译器很好

I make stupid mistakes in Python constantly. I misname a variable or a function or I pass in the wrong arguments. Devtools can catch some of these, but they usually require special setup. I’ve never been able to configure pylint easily, and I’m not a fan of full blown IDEs that require their own configuration. 我经常在Python中犯下愚蠢的错误。 我错误地命名变量或函数，或者传入错误的参数。 Devtools可以捕获其中一些，但它们通常需要特殊设置。 我从来没有能够轻松配置pylint，而且我不喜欢需要自己配置的完整IDE。

The worst is if you mistype a variable that’s hidden behind conditional logic. Your script might run for hours before triggering the error, and then everything blows up, and you have to restart it. 最糟糕的是，如果您错误地键入隐藏在条件逻辑后面的变量。 您的脚本可能会在触发错误之前运行几个小时，然后一切都会爆炸，您必须重新启动它。

Unit tests would catch most of these, but it’s hard to get 100% code coverage, and I don’t want to spend time writing unit tests for a one-off script. 单元测试会捕获大部分内容，但很难获得100％的代码覆盖率，而且我不想花时间为单一脚本编写单元测试。

Compiled languages make all these problems go away. The compiler catches all the silly things you miss. Because of this, I prefer languages like Go for anything over a couple hundred lines. 编译语言会使所有这些问题消失。 编译器捕获了你错过的所有愚蠢的东西。 因此，我喜欢Go这样的语言超过几百行。

### Development Speed

The flip side to having a compiler is that usually your development speed decreases. This is especially true with C/C++ and Java. 拥有编译器的另一面是通常你的开发速度会降低。 对于C / C ++和Java来说尤其如此。

Go is simple enough where I found the development speed hit to be minimal. Don’t get me wrong, I can still write code faster in Python, but I probably achieve 85% of my Python productivity in Go. Go很简单，我发现开发速度很小。 不要误会我的意思，我仍然可以在Python中更快地编写代码，但我可能在Go中实现了85％的Python生产力。

85% isn’t bad when I consider how many fewer mistakes I’ll make with the benefit of the compiler. 当我考虑到编译器的好处会减少多少错误时，85％也不错。

### Better Parallelism 更好的并行性

As you probably know, Go was built from the ground-up for parallel execution. 您可能知道，Go是从头开始构建的，用于并行执行。

On my team, we usually need parallel programs because we’re dealing with a lot of data in S3 or in our database. 在我的团队中，我们通常需要并行程序，因为我们在S3或数据库中处理大量数据。

If the task is IO bound (which many are), then we can successfully employ Python threads. But if it’s is CPU intensive, Python will suffer because of the Global Interpreter Lock. 如果任务是IO绑定的（很多都是），那么我们就可以成功使用Python线程。 但如果它是CPU密集型的，那么Python将因全局解释器锁而受到影响。

I also enjoy how simple things “just work” in multi-threaded Go without doing anything special. Ever had that problem where you Ctrl-C your multithreaded python and it doesn’t do anything? 我也喜欢多线程Go中“简单工作”的简单事情，而不做任何特别的事情。 曾经有过这样的问题，你在哪里Ctrl-C你的多线程python并没有做任何事情？

### Easier Deployment 更容易部署

I like having a single binary. I usually run code on EC2 machines to give my scripts closer network proximity to S3 and to our database. With Python, I have to ensure all the packages I need are installed on the remote machine, and that one of my coworkers hasn’t installed anything conflicting. 我喜欢有一个二进制文件。 我通常在EC2机器上运行代码，使我的脚本更接近S3和我们的数据库。 使用Python，我必须确保我需要的所有软件包都安装在远程计算机上，并且我的一个同事没有安装任何冲突的东西。

Virtualenvs solve most of this problem, but I still find Go easier. Virtualenvs解决了大部分问题，但我仍然觉得Go更容易。

Usually I cross compile my code on my Mac to Linux, copy it to the remote machine, and I’m off and running. All my dependencies are contained in my binary. 通常我会将我的Mac上的代码交叉编译到Linux，将其复制到远程计算机，然后我就开始运行了。 我的所有依赖项都包含在我的二进制文件中。

### Consistent Styling 风格一致

At first, the gofmt tool annoyed me, particularly their choice of using tabs instead of spaces. I thought that was insane. 起初，gofmt工具让我烦恼，特别是他们选择使用制表符而不是空格。 我以为这太疯狂了。

But as I use it more, I’ve come to depend on it. I get free formatting right out of the box. All of my code is always styled consistently, regardless of what project I’m working on because the formatting is a feature of the standard Go tooling. 但是当我更多地使用它时，我开始依赖它。 我开箱即可免费格式化。 无论我正在处理什么项目，我的所有代码都始终保持一致的样式，因为格式化是标准Go工具的一项功能。

I have to put in more effort to get the same effect in Python. I have to configure pylint correctly and then ensure it’s used in every single project. 我必须付出更多努力才能在Python中获得相同的效果。 我必须正确配置pylint，然后确保它在每个项目中使用。

### Better Tooling

Gofmt is just one example of a general theme. All of the editors I love – VSCode, vim, and Sublime Text, all have great Golang extensions that take advantage of the standard Go tooling. Gofmt只是一般主题的一个例子。 我喜欢的所有编辑器 -  VSCode，vim和Sublime Text都有很好的Golang扩展，可以利用标准的Go工具。

As a result I get intellisense similar to Java, but without using a real IDE. I’ve never come close to that ability with Python. 因此，我得到类似于Java的intellisense，但没有使用真正的IDE。 我从来没有接近过Python的这种能力。

### Disadvantages

Whenever I read posts criticizing Go, it’s usually because of the obvious features that are missing, like generics. I’ve never had much trouble with missing generics – you’d be surprised how much you can do with maps and slices, but I have had numerous other problems. 每当我阅读批评Go的帖子时，通常都是因为缺少明显的功能，比如泛型。 我从来没有遇到过丢失泛型的麻烦 - 你会惊讶于你能用地图和切片做多少，但我还有很多其他问题。

#### Go is opinionated Go是固执己见的

First, Go is probably the most opinionated language I’ve ever used. From forcing you to use tabs instead of spaces (assuming you’re using gofmt), to forcing you to use a certain directory structure, to making you code within the GOPATH environment variable, there are many features of Go which are not easy to change. 首先，Go可能是我用过的最自以为是的语言。 从迫使你使用制表符而不是空格（假设你正在使用gofmt），强迫你使用某个目录结构，使你在GOPATH环境变量中编写代码，Go的许多功能都不容易改变。

One of the reasons it’s so easy to learn is because you can’t change these features. If you don’t want to export every name that starts with a capital letter, then too bad for you. Fortunately, none of these are deal breakers for me, but I could understand if they are for others. 这么容易学习的原因之一是因为你无法改变这些功能。 如果您不想导出以大写字母开头的每个名称，那么对您来说太糟糕了。 幸运的是，这些都不是我的交易破坏者，但我能理解他们是否适合其他人。

Python is much more flexible. Python更灵活。

#### Somewhat Poor library support 缺少一些库的支持

It’s not fair to compare Python and Go in this arena. Go is a lot newer, but I’m still baffled when I find features that Go doesn’t support out of the box. I’m even more baffled when people on StackOverflow post code which should be a built-in function, and then act like there’s no problem with every person copying and pasting that code into their project. 在这个领域比较Python和Go是不公平的。 Go是一个更新的，但当我发现Go不支持开箱即用的功能时，我仍然感到困惑。 当StackOverflow上的人发布应该是内置函数的代码时，我更加困惑，然后就像每个人复制并将代码粘贴到他们的项目中一样没有问题。

2 examples that come to mind in the last couple of years: 在过去几年中浮现的两个例子：

* Sorting a slice (fortunately this was made easier in Go 1.8) 对切片进行排序（幸运的是，这在Go 1.8中变得更容易）
* Math.round only working with integers and not allowing you to Round to float values (e.g. if you want to round to the nearest .5). And before Go 1.10 there wasn’t even a math.round. Math.round只使用整数而不允许你舍入到浮点值（例如，如果你想舍入到最接近的.5）。 在Go 1.10之前，甚至没有math.round。

Granted, some of these are because Go doesn’t have generics, and some are because the developers of Go are following the strategy of only adding things to the standard libraries which are absolutely necessary. 当然，其中一些是因为Go没有泛型，有些是因为Go的开发人员遵循的策略是只向标准库中添加绝对必要的东西。

I understand both points, but it’s still annoying when you encounter trivial functionality that you have to code yourself. 我理解这两点，但是当你遇到必须自己编写代码的琐碎功能时，它仍然很烦人。

Hopefully as the language continues to evolve, these pain points become fewer and fewer. 希望随着语言的不断发展，这些痛点越来越少。



参考：

* https://thinkfaster.co/2018/07/goodbye-python-hello-go/