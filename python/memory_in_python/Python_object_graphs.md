# Python object graphs

My post on [hunting memory leaks in Python](https://mg.pov.lt/blog/hunting-python-memleaks.html) received *a lot* of feedback via email. And both most of them asked for the source code.  我在Python中寻找内存泄漏的帖子通过电子邮件收到了很多反馈。 他们大多数都要求提供源代码。

So, here's the mysterious `checks` module I used in the post. There's nothing complicated in it, just a bunch of ad-hoc functions I wrote in an afternoon. I'm sure you could do better.  因此，这是我在帖子中使用的神秘检查模块。 没什么复杂的，只是我在一个下午写的一堆临时功能。 我相信你可以做得更好。

```
import gc
import inspect
```

The [gc](http://python.org/doc/current/lib/module-gc.html) module gives us access to the Python garbage collector, which tracks object references. The [inspect](http://python.org/doc/current/lib/module-inspect.html) module has useful functions for distinguishing certain kinds of built-in objects such as modules or call stack frames.  gc模块使我们可以访问Python垃圾收集器，该垃圾收集器跟踪对象引用。 检查模块具有有用的功能，用于区分某些内置对象，例如模块或调用堆栈框架。

```
def count(typename):
    return sum(1 for o in gc.get_objects() if type(o).__name__ == typename)
```

A very simple function that counts the number of objects by the class or type name. If you happen to use [old-style classes](http://docs.python.org/ref/node33.html), well, it won't work for you. Before the great class and type unification in Python 2.2, all instances of all classes were of type 'instance', and that's what you'll see today if you still use old-style classes.  一个非常简单的函数，它通过类或类型名称对对象的数量进行计数。 如果您碰巧使用旧式的类，那么它将对您不起作用。 在Python 2.2中实现出色的类和类型统一之前，所有类的所有实例均为“实例”类型，如果您仍在使用旧式类，那么今天将看到这些。

Also, this simple function doesn't distinguish between classes with the same name defined in different modules. I didn't need it — I prefer to have unique class names, so that I can easily navigate my source tree with [ctags](http://localhost/blog/hacking-tools.html).  而且，此简单函数无法区分在不同模块中定义的具有相同名称的类。 我不需要它-我更喜欢使用唯一的类名，这样我就可以使用ctags轻松导航我的源代码树。

```
def by_type(typename):
    return [o for o in gc.get_objects() if type(o).__name__ == typename]
```

Essentially the same thing, but this function returns a list of objects instead of counting them.  本质上是相同的，但是此函数返回对象列表，而不是对它们进行计数。

```
def at(addr):
    for o in gc.get_objects():
        if id(o) == addr:
            return o
    return None
```

This is a way to "dereference" a "pointer" in Python, the reverse to [id](http://python.org/doc/current/lib/built-in-funcs.html#l2h-39)(). If you see an interesting object in the graph, and want to get hold of it in the pdb prompt to do some manual looking, you can do that by calling  `at` and passing the id shown in the graph.  这是在Python中“解除引用”“指针”的一种方法，与 id() 相反。 如果您在图形中看到一个有趣的对象，并且想要在pdb提示符中获取它以进行一些手动查找，则可以通过调用并传递图形中所示的id来实现。

> Actually, it's not a true reverse of id(). It can only find objects tracked by the garbage collector, such as lists, dicts, instances, functions and so on, but not trivial value objects (such as strings or ints) that never contain references to other objects  实际上，这并不是id（）的真正反向。 它只能找到由垃圾收集器跟踪的对象，例如列表，字典，实例，函数等，而不能找到从不包含对其他对象的引用的琐碎值对象（例如字符串或整数）

```
def find_backref_chain(obj, predicate, max_depth=20, extra_ignore=()):
```

This function, given an object and a predicate, finds the shortest chain of object references from some source object such that predicate(source_object) is true. It does a bog-standard [Breadth-first search](http://en.wikipedia.org/wiki/Breadth-first_search) in a graph. The max_depth argument limits the search so that I wouldn't have to wait too long to get a negative answer (I'm pretty sure any such chain should be shorter than 20 references).  给定一个对象和一个谓词的该函数从某个源对象中查找最短的对象引用链，从而谓词（source_object）为true。 它在图形中进行沼泽标准的广度优先搜索。 max_depth参数限制了搜索范围，因此我不必等待太久就可以获得否定答案（我很确定任何这样的链都应少于20个引用）。

The extra_ignore argument lets me specify additional ids of objects that I want to be ignored. For example, if I stored the results of by_type('Foo') in a variable, I'd have an extra list object referencing each of the Foo objects. If I don't want that list to clutter up my searches, I can pass extra_ignore=[id(my_list)].  extra_ignore参数使我可以指定要忽略的对象的其他ID。 例如，如果我将by_type（'Foo'）的结果存储在变量中，则将有一个额外的列表对象引用每个Foo对象。 如果我不希望该列表使搜索混乱，可以传递extra_ignore = [id（my_list）]。

```
    queue = [obj]
    depth = {id(obj): 0}
    parent = {id(obj): None}
```

The standard BFS elements: a FIFO queue, the mapping from a node to its depth (depth[x] = the length of the shortest path from obj to x), and the mapping that lets me construct the shortest path easily (parent[x] = the next node on the shortest path from x to node).

```
    ignore = set(extra_ignore)
    ignore.add(id(extra_ignore))
    ignore.add(id(queue))
    ignore.add(id(depth))
    ignore.add(id(parent))
    ignore.add(id(ignore))
```

The objects that implement the search should not themselves become part of the search!

```
    gc.collect()
```

Just to make sure we have no collectable garbage lying around.

```
    while queue:
        target = queue.pop(0)
        if predicate(target):
```

Found it! Let's reconstruct the reference chain now

```
            chain = [target]
            while parent[id(target)] is not None:
                target = parent[id(target)]
                chain.append(target)
            return chain
```

Otherwise, continue looking...

```
        tdepth = depth[id(target)]
        if tdepth < max_depth:
```

... but don't dive deeper than the user asked.

```
            referrers = gc.get_referrers(target)
            ignore.add(id(referrers))
```

We definitely don't want new objects created during the search to become part of the search space (you could easily get into an infinite loop). And even if the referrers list got garbage collected at the end of the inner loop, this doesn't hurt our search. Even if the same id got reused by a different *new* object, we don't want *any* new objects to become a part of the search space.

```
            for source in referrers:
```

We look at each source object referring to the current target object...

```
                if inspect.isframe(source) or id(source) in ignore:
                    continue
```

... ignoring ones that we want to ignore. Note that here I also ignore call-stack frames, even though I probably shouldn't. Frame objects contain references to local variables in a function. It is entirely plausible that some long-running function is the source of your memory leak, so I shouldn't do that. However, in my particular case it wasn't, and all the frame objects appeared in my graph solely because of locals I defined in the pdb prompt. Adding this check simplified my object graphs without affecting the outcome.

```
                if id(source) not in depth:
                    depth[id(source)] = tdepth + 1
                    parent[id(source)] = target
                    queue.append(source)
```

The standard BFS steps again.

```
    return None # not found
```

And if we ever get out of that loop, it means the search failed.

Since this post is getting excessively long, I'll describe the show_backrefs function that you all really wanted to see in the next post.

**Update:** [continue reading](https://mg.pov.lt/blog/object-graphs-with-graphviz.html).

**Update 2:** the 'checks' module was open-sourced as [objgraph](https://mg.pov.lt/objgraph/).

[« Hunting memory leaks in Python](https://mg.pov.lt/blog/hunting-python-memleaks.html)

[Out of touch with reality »](https://mg.pov.lt/blog/out-of-touch.html)