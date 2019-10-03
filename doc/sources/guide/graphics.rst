.. _graphics:

显卡绘图
========

介绍画布
----------------------

一个挂件的显卡表现形式就是翻译成一张画布，在渲染画布的时候你即可以看到
一个最终的画板，也可以看到一套绘画指令集。有许多指令你可以使用（增加）
到你的画布上，但主要是2个不同的模块：

- :mod:`语境指令 <kivy.graphics.context_instructions>`
- :mod:`顶部指令 <kivy.graphics.vertex_instructions>`

语境指令不会做出绘画动作，但语境指令改变顶部指令的结果。

许多画布可以包含2个子指令集。它们是
:mod:`canvas.before <kivy.graphics.Canvas.before>` 模块和
:mod:`canvas.after <kivy.graphics.Canvas.after>` 模块的指令组。
在这两个指令组中指令会分别有 :mod:`~kivy.graphics.canvas` 模块
之前和之后执行的指令。意味着画布会出现在指令代码的下面（指令先执行后绘制）
和指令代码的上面（先绘制后执行指令）。
那些指令组不会被建立，要等待用户访问指令才可以。

要把一个画布指令增加到一个挂件上，你使用画布语境即可：

.. code-block:: python

    class MyWidget(Widget):
        def __init__(self, **kwargs):
            super(MyWidget, self).__init__(**kwargs)
            with self.canvas:
                # add your instruction for main canvas here

            with self.canvas.before:
                # you can use this to add instructions rendered before

            with self.canvas.after:
                # you can use this to add instructions rendered after

语境指令
--------------------

语境指令是对 OpenGL 语境进行操作。你可以旋转、翻译和标量你的画布。
你也可以附着上一个结构或改变绘制颜色。这是最共性的用法，但其它也真的有用::

   with self.canvas.before:
       Color(1, 0, .4, mode='rgb')

绘画指令
--------------------

绘画指令范围非常直接，就像画一条线或画一个多边形一样，
太多层化的指令例如是网格化或者是弧形曲线::

    with self.canvas:
       # draw a line using the default color
       Line(points=(x1, y1, x2, y2, x3, y3))

       # lets draw a semi-transparent red square
       Color(1, 0, 0, .5, mode='rgba')
       Rectangle(pos=self.pos, size=self.size)

操作指令
-------------------------

有时候你想要更新或移除你已经增加到画布上的指令。实现的方法许多，要根据你的需求：

你可以保留一个指向你的指令的参考对象后更新这些指令::

    class MyWidget(Widget):
        def __init__(self, **kwargs):
            super(MyWidget, self).__init__(**kwargs)
            with self.canvas:
                self.rect = Rectangle(pos=self.pos, size=self.size)
    
            self.bind(pos=self.update_rect)
            self.bind(size=self.update_rect)
    
        def update_rect(self, *args):
            self.rect.pos = self.pos
            self.rect.size = self.size


或者你可以清除你的画布后启动刷新::

    class MyWidget(Widget):
        def __init__(self, **kwargs):
            super(MyWidget, self).__init__(**kwargs)
            self.draw_my_stuff()

            self.bind(pos=self.draw_my_stuff)
            self.bind(size=self.draw_my_stuff)

        def draw_my_stuff(self):
            self.canvas.clear()

            with self.canvas:
                self.rect = Rectangle(pos=self.pos, size=self.size)

注意更新指令是最好的实行，因为这种方式触发较少的负荷并且避免建立新的指令。
