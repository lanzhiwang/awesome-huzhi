# Writing Vim plugin in Python

Writing a Vim script for own use is easy. Writing a plugin, compatible with pathogen, Vundle or other, and making it top quality user experience is just a bit more complicated. But is still easy and fun. Here I show just how to do so.  编写自己的Vim脚本很容易。 编写与病原体，Vundle或其他兼容的插件，并使其具有最高质量的用户体验，只是稍微复杂一点。 但是还是容易和有趣的。 在这里，我展示了如何做到这一点。

Only prerequisites are: Vim, some Python knowledge and lots of curiosity (more on that later). Some sample commands here are for `bash`, so, Linux or Mac. You will need to adjust a bit if you use Windows, but the general idea and all the rest is same in any case.  只有先决条件是：Vim，一些Python知识和很多好奇心（稍后会进一步介绍）。 这里的一些示例命令适用于bash，适用于Linux或Mac。 如果使用Windows，则需要进行一些调整，但是总体思路和所有其他方法在任何情况下都是相同的。

Final source code is available on … TODO: share source code

TODO: links to Vim wiki, documentation, etc. Links to other blogs.

Let’s go!

## Vim Python support

There are many ways to create a Vim plugin. Classic one - use VimL. Or you can also use Lua. Or Python. This particular guide uses Python, and Python may be a great language to write a plugin for Vim because:  有多种创建Vim插件的方法。 经典之一-使用VimL。 或者，您也可以使用Lua。 或Python。 本特定指南使用Python，Python可能是为Vim编写插件的绝佳语言，因为：

- it is “*natively*” supported by Vim  它被Vim“本地”支持
- you most likely already know it, in contrast to VimL  与VimL相比，您很可能已经知道了
- and it simple; you know, in contract to VimL  而且很简单； 你知道，与VimL签约

Certainly, a plugin written in Python will only run in Vim compiled with Python support. Vim’s default distribution is compiled with Python support, and nowadays finding the opposite is actually harder. There is also a number of widely used Vim plugins written in Python and you shouldn’t worry about Python support - it is not going anywhere.  当然，用Python编写的插件只能在通过Python支持编译的Vim中运行。 Vim的默认发行版是在Python支持下编译的，如今发现相反的事实实际上更加困难。 还有许多使用Python编写的广泛使用的Vim插件，您不必担心Python的支持-它不会随处可见。

To make sure that your Vim has Python support, run `vim --version`, and look for a line marked `+python` or `+python3`. Note that all code below is designed for Python 2 (`+python`) which is how Vim is distributed by default. If your Vim uses Python 3 (`+python3`) - you will need to update the source code accordingly.  为确保您的Vim具有Python支持，请运行vim --version，并查找标记为+ python或+ python3的行。 请注意，以下所有代码都是针对Python 2（+ python）设计的，这是默认情况下Vim的分发方式。 如果您的Vim使用Python 3（+ python3）-您将需要相应地更新源代码。

## Principles and minimal template  原则和最小模板

Vim plugins actually *have to* be written in VimL and not in Python. Good news is that Vim plugin can execute arbitrary Python scripts from withing VimL code. With this knowledge, basic idea of the plugin is to:  Vim插件实际上必须使用VimL而不是Python编写。 好消息是Vim插件可以使用VimL代码执行任意Python脚本。 有了这些知识，插件的基本思想是：

- create a wrapper script in VimL
- which will declare Vim commands
- and import and run Python code
- while latter implements those commands

Before going into Python code, let’s prepare the basic project structure, development environment, and ensure that our plugin is ready for plugin managers.

### Plugin structure

If we want our plugin to work with Vim plugin managers, like pathogen, Vundle and many others, it needs to follow some basic structure:

```
sampleplugin/
├── doc/
│   └── sampleplugin.doc
└── plugin/
    └── sampleplugin.vim
```

This is self-explanatory. It is a good idea to provide an integrated documentation for a plugin, and we will addres this later on. If we are to publish the plugin, say, on GitHub, it makes sense to also add two more files:  这是不言自明的。 为插件提供集成文档是个好主意，稍后我们将对此进行补充。 如果要在GitHub上发布插件，那么还可以添加两个文件：

```
sampleplugin/
├── ...
├── LICENSE
└── README
```

Once our project structure is ready, let’s try and install it.

### Development process and our first Vim command

Let’s configure the development environment at once, so that we can test and run the plugin in a Vim instance regularly. How this set-up is made depends largely on the plugin manager you use with Vim.  让我们立即配置开发环境，以便我们可以定期在Vim实例中测试和运行插件。 如何进行此设置很大程度上取决于与Vim一起使用的插件管理器。

Some plugin managers require all plugins to be installed under same root directory, which for most users is `~/.vim/bundle`. If you are concerned, and don’t want to change your plugins root directory, you can create a symbolic link from your source code:  一些插件管理器要求所有插件都安装在同一根目录下，对于大多数用户来说，该目录是〜/ .vim / bundle。 如果您担心并且不想更改插件的根目录，则可以从源代码创建符号链接：

```
$ cd ~/.vim/bundle
$ ln -s ~/src/sampleplugin sampleplugin
```

Check you Vim’s plugin manager documentation on how to declare and load the plugin. For example, I use [Vundle](https://github.com/VundleVim/Vundle.vim), my plugin source code is in `~/src/sampleplugin`, and thus I have following in my `~/.vimrc`:

```
Plugin 'file:///home/candidtim/src/sampleplugin'
```

Now, let’s make sure this actually works. Let’s add following content to `sampleplugin.vim`:

```
echo "It worked!"
```

And start new Vim instance where we will test the plugin. Upon startup you should see “hello vim!” printed out in the terminal. It worked!

> If at this point it doesn’t work, try to load the plugin manually. For this, execute following command from Vim: `:source ~/.vim/bundle/sampleplugin/plugin/sampleplugin.vim`. Now, if this finally works, it means that your plugin manager doesn’t load the plugin automatically on Vim startup - refer to your plugin manager documentation to find out how to configure it correctly. If however this doesn’t work either - Vim should normally print out an error message, which should give you a better idea. Most likely you need to check that file actually exists and symbolic link works as expected, and that file content (syntax) is correct.

All set! Let’s write some Python!

## Use Python in Vim plugin

As noted above, the idea now is to execute Python code from VimL. VimL exposes specific syntax for this. Let’s change our plugin source to the following:  如上所述，现在的想法是从VimL执行Python代码。 VimL为此公开了特定的语法。 让我们将插件源更改为以下内容：

```
python << EOF
    print "Hello from Vim's Python!"
EOF
```

(Re-)start test Vim instance and you should see the new message.

Now, I don’t mind writing few simple commands inline like this, but our actual goal is to make Python code to live in Python source files, and VimL code in .vim source files. So, let’s actually make Vim “import” our code from Python source files. Change the code to:  现在，我不介意像这样内联地编写一些简单的命令，但是我们的实际目标是使Python代码可以驻留在Python源文件中，而VimL代码可以驻留在.vim源文件中。 因此，实际上让Vim从Python源文件“导入”我们的代码。 将代码更改为：

```
1  let s:plugin_root_dir = fnamemodify(resolve(expand('<sfile>:p')), ':h')
2  
3  python << EOF
4  import sys
5  from os.path import normpath, join
6  import vim
7  plugin_root_dir = vim.eval('s:plugin_root_dir')
8  python_root_dir = normpath(join(plugin_root_dir, '..', 'python'))
9  sys.path.insert(0, python_root_dir)
10 import sample
11 EOF
```

Vim doesn’t know where your Python plugin code lives, so if we are to import it, we need to add its root directory to `sys.path` in the interpreter running inside Vim. For this:

- (1) we first save plugin’s directory path into a local variable in plugin’s Vim script
- (7) then acces its value from within Python script
- (8) use it to build the path to the directory where our Python code lives
- (9) and finally add it to `sys.path`
- (10) so that we can now import our Python module

To extract value from Vim’s `plugin_root_dir` variable we use `vim` Python module. This is available inside Vim and provides an interface to the Vim environment. We will revist this in details later.  要从Vim的plugin_root_dir变量中提取值，我们使用vim Python模块。 这在Vim内部可用，并提供了Vim环境的接口。 我们稍后将详细讨论。

Now, let’s actually add this Python code we talk about. Let’s add a file:

```
$ touch /sampleplugin/python/sample.py
```

With following content:

```
print "Hello from Python source code!"
```

Restart test Vim instance, see the new message, all done!

## Declare commands and implement them in Python

Now, you likely want to add some commands to the Plugin, or it risks to not to be very useful. Let’s implement a simple command which would print out the country you are in, based on your IP. I mean, why not?  现在，您可能想要向该插件添加一些命令，否则可能会变得不太有用。 让我们实现一个简单的命令，该命令将根据您的IP打印出您所在的国家/地区。 我的意思是，为什么不呢？

Let’s implement it first: TODO: fix for Python 2

```
import urllib, urllib.request
import json
import vim

def _get(url):
    return urllib.request.urlopen(url, None, 5).read().strip().decode()

def _get_country():
    try:
        ip = _get('http://ipinfo.io/ip')
        json_location_data = _get('http://api.ip2country.info/ip?%s' % ip)
        location_data = json.loads(json_location_data)
        return location_data['countryName']
    except Exception as e:
        print 'Error in sample plugin (%s)' % e.msg

def print_country():
    print 'You seem to be in %s' % _get_country()
```

Now, the buty of this implementation is in that it is plain Python code. You can test and debug it outside Vim with whatever tools you typically use. You can write Python unit tests and execute code from Python REPL, for example:  现在，此实现的关键在于它是纯Python代码。 您可以使用通常使用的任何工具在Vim外部对其进行测试和调试。 您可以编写Python单元测试并从Python REPL执行代码，例如：

```
$ python
>>> import sample
>>> sample.print_country()
France
```

Now, if we want to call it from Vim, some VimL is necessary again. Let’s declare a Vim function which will call our Python function. Add this to the end of `sampleplugin.vim` file:  现在，如果要从Vim调用它，则再次需要一些VimL。 让我们声明一个Vim函数，它将调用我们的Python函数。 将此添加到sampleplugin.vim文件的末尾：

```
function! PrintCountry()
    python print_country()
endfunction
```

Restart test Vim instance, and type: `:call PrintCountry()`. I’m in France, and where are you?

It is not very convenient however to use the `:call` syntax. Typically, Vim plugins provide commands instead, so let’s do just that. Add this line after the function declaration:  但是，使用：call语法不是很方便。 通常，Vim插件会提供命令，因此就让我们开始吧。 在函数声明后添加以下行：

```
command! -nargs=0 PrintCountry call PrintCountry()
```

Rinse, repeat and type `:PrintCountry` and it still should print the same country. Well done!

## Accessing Vim functionality from Python plugin

Our plugin is quite limited so far: it only spits some text to Vim message area, but doesn’t do a lot otherwise. If we want to do more interesting thins - we need to use `vim` module. It provides Python interface to various Vim functinality.  到目前为止，我们的插件非常有限：它只会向Vim消息区域吐出一些文本，否则不会做很多事情。 如果我们想做更多有趣的Thins-我们需要使用vim模块。 它提供了各种Vim功能的Python接口。

For starters, it can simply evalaute expressions writtern in VimL. This is what we previously did to extract a value of a variable declared in VimL:  首先，我可以简化用VimL编写的评估表达式。 这是我们以前提取VimL中声明的变量的值所执行的操作：

```
plugin_root_dir = vim.eval('s:plugin_root_dir')
```

`eval` can evalaute any VimL expression and is certinaly not limited to accessing vars. But more often it will be more convenient to use other `vim` interfaces instead of `eval`.  eval可以代表任何VimL表达，并且从实际意义上讲，它不限于访问var。 但是更多时候使用其他vim接口代替eval会更方便。

For example, you can access and modify text in current buffer like so:

```
vim.current.buffer.append('I was added by a Python plugin!')
```

As an example, let’s implement another command, `InsertCountry`, which would insert the name of the country you are in at current cursor position. Here is the Python code to add:

```
def insert_country():
    row, col = vim.current.window.cursor
    current_line = vim.current.buffer[row-1]
    new_line = current_line[:col] + _get_country() + current_line[col:]
    vim.current.buffer[row-1] = new_line
```

And, same way as before, let’s add according function and command to VimL wrapper script:

```
function! InsertCountry()
    python3 insert_country()
endfunction
command! -nargs=0 InsertCountry call InsertCountry()
```

Try it out in a new Vim instance. Position a cursor somewhere in a buffer and run `:InsertCountry`. You can now even map a key combination for this. For example, run

```
:map <Leader>c :InsertCountry<CR>
```

and press `<Leader> c` to run the command! Hey, our plugin just got a major upgrade! Our users can add the mapping to `~/.vimrc` and their country name is just two key presses away!

Vim plugin can do a lot more interesing things. What is possible and how to use `vim` module is well documented in Vim itself. Check out help: `:help python-vim` - this is why I mentioned curiosity as a prerequisite previously.

## Configuration

Now this is simple. We already saw everything we need to provide a configuration for our plugin. Typically, users will configure the plugin in `~/.vimrc` file and set some global variables, which we will later access in a plugin and use to adjust its behaviour. Say, we want to configure our plugin to provide either country names, or ISO codes. Add following to your `~/.vimrc`:  现在，这很简单。 我们已经看到了为插件提供配置所需的一切。 通常，用户将在〜/ .vimrc文件中配置插件并设置一些全局变量，我们稍后将在插件中访问它们并用于调整其行为。 假设我们要配置插件以提供国家名称或ISO代码。 将以下内容添加到您的〜/ .vimrc中：

```
let g:SamplePluginUseCountryCodes = 1
```

And then, access it in Python code:

```
vim.eval('g:SamplePluginUseCountryCodes')
```

Heads up! `eval` will only return a string, list or a dict, depending on type of data used in VimL. In this case, it is a string, so normally you would actually use it like so:  小心！ eval将仅返回字符串，列表或字典，具体取决于VimL中使用的数据类型。 在这种情况下，它是一个字符串，因此通常您实际上会像这样使用它：

```
use_codes = vim.eval('g:SamplePluginUseCountryCodes').strip() != '0'
```

You can technically ask users to use ‘true’ and ‘false’ in this case for example, but it is good idea to stick to the behaviour users are already used to with the majority of other plugins, which is using 0 and 1 for this.  例如，您可以在技术上要求用户在这种情况下使用'true'和'false'，但是最好还是坚持用户已经习惯了大多数其他插件的行为，为此，使用0和1 。

## Getting a bit more sophisticated  变得更加复杂

We are almost done. Let’s just finalize our VimL wrapper. It makes sense to add two more features to it:  我们快完成了。 让我们最后确定VimL包装器。 向其中添加两个功能是有意义的：

- ensure that our plugin is only started when Python is actually available in Vim (this prevents Vim from spitting too many errors to the user when Python is not available)  确保仅当Python在Vim中实际可用时才启动我们的插件（这可防止Vim在Python不可用时向用户吐出太多错误）
- and ensure that plugin is initialized once and only once.

Following does precisely that:

```
if !has("python3")
    echo "vim has to be compiled with +python3 to run this"
    finish
endif

if exists('g:sample_plugin_loaded')
    finish
endif

; the rest of plugin VimL code goes here

let g:sample_plugin_loaded = 1
```

Now, for example, if our user does something like `:source ~/.vimrc`, we are sure our plugin won’t try to run the initialization code again: won’t change `sys.path` again, won’t import python modules or execute mode-level code. Having said that, you don’t have any code at module level except for declarations, do you?  现在，例如，如果我们的用户执行了诸如：source〜/ .vimrc之类的操作，我们可以确定我们的插件不会尝试再次运行初始化代码：不会再次更改sys.path，不会导入python模块或 执行模式级代码。 话虽如此，除了声明，您在模块级别没有任何代码，是吗？

## Provide documentation

TODO: how to document?

## Publish a plugin

TODO: publish to GitHub

## TODO: ?

- testing with vim and not (split code, unittest without vim module)
- not relaunching vim? (re-source ~/.vimrc ?)

## That’s it!

You can find final source code in this sample repository. TODO: add link. Certainly check out `:help python` which contanins a lot of important details.

If you know of other important tricks, or have a good advice - please, leave a comment below. I’m very interested in further improvments of my Vim plugin development workflow and implementation.

Hope it was useful. Have fun with Vim!

## 参考

* http://candidtim.github.io/vim/2017/08/11/write-vim-plugin-in-python.html
* http://candidtim.github.io/vim/2017/08/11/write-vim-plugin-in-python.html
* https://www.oschina.net/translate/how-to-write-vim-plugins-with-python
