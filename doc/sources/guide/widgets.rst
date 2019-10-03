.. _widgets:

挂件
=======

.. |size_hint| replace:: :attr:`~kivy.uix.widget.Widget.size_hint`
.. |pos_hint| replace:: :attr:`~kivy.uix.widget.Widget.pos_hint`
.. |size_hint_x| replace:: :attr:`~kivy.uix.widget.Widget.size_hint_x`
.. |size_hint_y| replace:: :attr:`~kivy.uix.widget.Widget.size_hint_y`
.. |pos| replace:: :attr:`~kivy.uix.widget.Widget.pos`
.. |size| replace:: :attr:`~kivy.uix.widget.Widget.size`
.. |width| replace:: :attr:`~kivy.uix.widget.Widget.width`
.. |height| replace:: :attr:`~kivy.uix.widget.Widget.height`
.. |children| replace:: :attr:`~kivy.uix.widget.Widget.children`
.. |parent| replace:: :attr:`~kivy.uix.widget.Widget.parent`
.. |x| replace:: :attr:`~kivy.uix.widget.Widget.x`
.. |y| replace:: :attr:`~kivy.uix.widget.Widget.y`
.. |left| replace:: :attr:`~kivy.uix.widget.Widget.left`
.. |right| replace:: :attr:`~kivy.uix.widget.Widget.right`
.. |top| replace:: :attr:`~kivy.uix.widget.Widget.top`
.. |center_x| replace:: :attr:`~kivy.uix.widget.Widget.center_x`
.. |center_y| replace:: :attr:`~kivy.uix.widget.Widget.center_y`
.. |orientation| replace:: :attr:`~kivy.uix.boxlayout.BoxLayout.orientation`
.. |Widget| replace:: :class:`~kivy.uix.widget.Widget`
.. |Spinner| replace:: :class:`~kivy.uix.spinner.Spinner`
.. |Button| replace:: :class:`~kivy.uix.button.Button`
.. |Image| replace:: :class:`~kivy.uix.image.Image`
.. |Canvas| replace:: :class:`~kivy.graphics.Canvas`
.. |ListProperty| replace:: :class:`~kivy.properties.ListProperty`
.. |ObjectProperty| replace:: :class:`~kivy.properties.ObjectProperty`
.. |ReferenceListProperty| replace:: :class:`~kivy.properties.ReferenceListProperty`
.. |Layout| replace:: :mod:`~kivy.uix.layout`
.. |RelativeLayout| replace:: :mod:`~kivy.uix.relativelayout`
.. |BoxLayout| replace:: :mod:`~kivy.uix.boxlayout`
.. |FloatLayout| replace:: :mod:`~kivy.uix.floatlayout`
.. |GridLayout| replace:: :mod:`~kivy.uix.gridlayout`
.. |StackLayout| replace:: :mod:`~kivy.uix.stacklayout`
.. |AnchorLayout| replace:: :mod:`~kivy.uix.anchorlayout`
.. |add_widget| replace:: :meth:`~kivy.uix.widget.Widget.add_widget`
.. |remove_widget| replace:: :meth:`~kivy.uix.widget.Widget.remove_widget`

介绍挂件
----------------------

在 Kivy 中一个 |Widget| 就是 GUI 界面的基础建造砖块。挂件提供一个 |Canvas| 画布，
画布是用来在屏幕上绘画用的。挂件接收事件后并把事件响应给画布。对于深度解释 |Widget| 类，
阅读挂件模块文档。

操作挂件树
----------------------------

在 Kivy 中许多挂件都组织成圣诞树形式。你的应用有一个 `root widget` 根挂件，
根挂件常常有 |children| 子挂件，子挂件可以有自己的 |children| 子挂件。
一个挂件的子挂件都表示成 |children| 属性，一种 Kivy |ListProperty| 财产列表。

挂件树可以有如下操作方法：

- :meth:`~kivy.uix.widget.Widget.add_widget` 方法是把一个挂件作为子挂件加入一个挂件中
- :meth:`~kivy.uix.widget.Widget.remove_widget` 方法是从子挂件列表中移除一个挂件
- :meth:`~kivy.uix.widget.Widget.clear_widgets` 方法是从一个挂件中移除其所有子挂件

例如，如果你想要把一个按钮增加到一个 BoxLayout 里的话，你可以这样做::

    layout = BoxLayout(padding=10)
    button = Button(text='My first button')
    layout.add_widget(button)

按钮加入到图层：意思就是按钮的父财产会设置给图层；图层有了加入的按钮后放在了图层的子列表里。
要删除按钮就要在图层上操作::

    layout.remove_widget(button)

删除后，按钮的父财产会被设置成 `None` 值，然后图层把已经删除的按钮从图层的子列表里清除。

如果你想要清空一个挂件中的子列表的话，使用
 :meth:`~kivy.uix.widget.Widget.clear_widgets` 方法::

    layout.clear_widgets()

.. warning::

    永远不要你自己来操作子列表，除非你真的知道自己在做什么，会有什么效果。
    挂件树是与一颗显卡树关联在一起的。例如，如果你把一个挂件加入到子列表里，
    而没有把关键的画布增加到显卡树上，挂件虽然会是一个子挂件，但在屏幕上却看不到。
    更甚者，你也许在后面调用 `add_widget`, `remove_widget` 和 `clear_widgets`
    这些方法时会产生问题。

爬树处理
-------------------

挂件类的实例 :attr:`~kivy.uix.widget.Widget.children` 属性列出了所含的全部子挂件。
你可以容易地在树上爬上爬下::

    root = BoxLayout()
    # ... add widgets to root ...
    for child in root.children:
        print(child)

不管如何做到的，必须小心这种用法，爬树有危险。如果你想要用前面部分中介绍的方法之一修改子列表，
你必须使用列表副本来操作，就像::

    for child in root.children[:]:
        # manipulate the tree. For example here, remove all widgets that have a
        # width < 100
        if child.width < 100:
            root.remove_widget(child)

挂件默认行为不会影响其子关键的尺寸/位置。其 |pos| 属性是屏幕坐标系的绝对坐标值
（除非你使用了 |RelativeLayout| 相对图层，后面会介绍）并且 |size| 属性是绝对尺寸。

挂件 Z 索引
---------------

挂件绘制的顺序是根据在挂件树中的挂件位置。其中 :attr:`~kivy.uix.widget.Widget.add_widget`
方法得到一个 `index` 参数，这个参数是用来描述挂件在挂件数中的位置用的::

    root.add_widget(widget, index)

较低索引位上的挂件会绘制在较高索引位挂件的上面。记住默认 `index` 值是 0，所以后加入的挂件
都优先绘制，除非反向描述。默认采用后进先出层叠图层！

用图层来组织
---------------------

图层 |Layout| 是一种具体的挂件，图层是控制挂件子挂件的尺寸和位置用的。有许多不同类型的图层，
针对不同的自动化子挂件的摆放。图层使用 |size_hint| 和 |pos_hint| 财产来确定图层的子挂件
|children| 的 |size| 尺寸和 |pos| 位置。

**BoxLayout** 类：
以一种挨着的方式摆放挂件（垂直或水平方向），填满所有空间。子挂件的 `size_hint` 财产
可以用来改变每个子挂件的尺寸，或设置固定尺寸给某些子挂件。

.. only:: html

    .. image:: ../images/boxlayout.gif
    .. image:: ../images/gridlayout.gif
    .. image:: ../images/stacklayout.gif
    .. image:: ../images/anchorlayout.gif
    .. image:: ../images/floatlayout.gif

.. only:: latex

    .. image:: ../images/boxlayout.png
    .. image:: ../images/gridlayout.png
    .. image:: ../images/stacklayout.png
    .. image:: ../images/anchorlayout.png
    .. image:: ../images/floatlayout.png


**GridLayout** 类：
以一种网格阵列方式摆放挂件。你必须至少描述网格阵列的一个空间，这样 Kivy 可以计算
每个挂件的尺寸后来摆放它们。

**StackLayout** 类：
以一种堆栈的方式一个接一个的摆放挂件，但要在众多空间之一里含有一个集合大小，不用把所有
挂件都放在整个空间里。这对于显示具有相同预定义尺寸的子挂件是有用的。

**AnchorLayout** 类：
一种只在乎子挂件位置的简单图层。允许把子挂件放在相对图层边缘的一个位置上。
不按照 `size_hint` 来摆放。

**FloatLayout** 类：
用任意位置和大小来摆放子挂件，即可是绝对图层尺寸，也可以是相对图层尺寸。
默认 `size_hint` 值是 (1, 1) ，这会让每个子挂件都有一样的尺寸，所以
如果你有多个子挂件的话，你可能想要改变这个值。你可以把 `size_hint` 设置
成 (None, None) 后使用绝对 `size` 尺寸值。这种挂件也会根据 `pos_hint`
作为一个字典来设置相对于图层位置的位置值。

**RelativeLayout** 类：
行为上类似 `FloatLayout` 类，但子挂件的位置都是相对于图层位置，而不是屏幕位置。

阅读各自图层的文档来进一步深入理解。

|size_hint| 和 |pos_hint|:

- |FloatLayout|
- |BoxLayout|
- |GridLayout|
- |StackLayout|
- |RelativeLayout|
- |AnchorLayout|

|size_hint| 是 |size_hint_x| 和 |size_hint_y| 的
一种 |ReferenceListProperty| 形式。它接收的值范围是从 `0` 到 `1` 或是 `None`，
默认值是 `(1, 1)` 。如果挂件在一个图层中的话，这说明图层会给挂件两边分配足够的空间
（相对于图层尺寸来说）。

例如把 |size_hint| 设置成 (0.5, 0.8) 的时候，会让挂件有一个 |layout| 图层可用
大小的  50% 宽和 80% 高。

思考如下示例：

.. code-block:: kv

    BoxLayout:
        Button:
            text: 'Button 1'
            # default size_hint is 1, 1, we don't need to specify it explicitly
            # however it's provided here to make things clear
            size_hint: 1, 1

现在输入下面指令可以加载 kivy 目录，但要把 $KIVYDIR 替换成你所安装的目录
（通过 :py:mod:`os.path.dirname(kivy.__file__)` 可以找到）::

    cd $KIVYDIR/examples/demo/kivycatalog
    python main.py

一个新的窗口会出现，点击下面左边 'Welcome' |Spinner| 区域后用上面的 kv 代码
替换默认的全部 kv 文本内容。

.. image:: images/size_hint[B].jpg

你会看到如同上面的图片所示， `Button` 得到了 100% 的图层 |size| 尺寸。

改变 |size_hint_x|/|size_hint_y| 的值为 0.5 后会让挂件 |widget| 得到
 50% 的图层 |layout| |width|/|height| 宽高比。

.. image:: images/size_hint[b_].jpg

你看到这里尽管我们描述了 |size_hint_x| 和 |size_hint_y| 的值都为 0.5 后，
但只有 |size_hint_y| 按照这个值做出改变。那是因为 |BoxLayout| 类控制着
 |size_hint_y| 方向 |orientation| 是 `垂直的` 以及 |size_hint_x|
方向 |orientation| 是 '水平的'。所控制的空间尺寸是根据 |BoxLayout| 中的
所有 |children| 子挂件数量计算的。在这里的例子中，一个子挂件的 |size_hint_y| 
被控制着 (.5/.5 = 1) ，因此挂件能够得到 100% 的父图层高。

我们再增加一个 |Button| 到 |layout| 图层上，看看会发生什么。

.. image:: images/size_hint[bb].jpg

|BoxLayout| 盒子图层天生默认均分空间给它的 |children| 子挂件使用。
在我们的例子中，比例是 50/50 因为我们有了2个 |children| 按钮。我们
在其中一个子挂件上使用 ``size_hint`` 后看看结果是什么。

.. image:: images/size_hint[oB].jpg

如果一个子挂件描述了 |size_hint| 值的话，那就描述了 |Widget| 会得到
多少 |BoxLayout| 提供的 |size| 空间大小。在我们的例子里，第一个按钮
 |Button| 的 |size_hint_x| 是 0.5，那么挂件的空间计算是::

    第一个子挂件的 ``size_hint`` 除以
    第一个子挂件的 ``size_hint`` + 第二个子挂件的 ``size_hint`` + ...n(第n个子挂件)
    
    .5/(.5+1) = .333...

那么 ``BoxLayout`` 的宽 |width| 是除以剩下的 |children| 子挂件。
在我们的例子中，意味着第二个 |Button| 按钮得到了 66.66% 的图层 |layout|
宽 |width| 。有例如增加到3个按钮时，那么就是 0.5/(0.5+1+1) = 0.2 因此
第一个按钮得到 20% 而第二和第三按钮共得到 80%，第二和第三按钮分别均分后得到
的就是 40% 了。

你可以用这个示范程序来与 |size_hint| 做一些实验，直到你理解空间的百分比分配。

如果你想要控制一个挂件 |Widget| 的绝对 |size| 尺寸的话，你可以设置所有挂件的
|size_hint_x|/|size_hint_y| 值，或都设置成 `None` 值，如此一来会按照挂件的
宽 |width| 和或高 |height| 属性值来分配空间了。

|pos_hint| 是一个字典数据格式，默认是空字典。与 |size_hint| 相比，图层按照
|pos_hint| 值的机制是不一样的，但通用中你可以增加值到任何一个 |pos| 属性里
 (|x|, |y|, |right|, |top|, |center_x|, |center_y|) 这样挂件 |Widget| 
的位置是相对于其父挂件 |parent| 来说的。

我们用如下 kv 代码来做一下实验，就好理解 |pos_hint| 的效果。点击 ``Welcome``
菜单选择 ``FloatLayout`` 游动图层，替换成如下 kv 代码：

.. code-block:: kv

    FloatLayout:
        Button:
            text: "We Will"
            pos: 100, 100
            size_hint: .2, .4
        Button:
            text: "Wee Wiill"
            pos: 200, 200
            size_hint: .4, .2

        Button:
            text: "ROCK YOU!!"
            pos_hint: {'x': .3, 'y': .6}
            size_hint: .5, .2

翻译过后的效果是：

.. image:: images/pos_hint.jpg

由于使用了 |size_hint| 后，你应该用 |pos_hint| 来理解对挂件位置效果的影响。

.. _adding_widget_background:

增加一个背景到图层
-------------------------------

最常问到图层问题之一就是::

    “如何给图层增加一个背景图片/背景色/背景视频，等等？"”

图层天生不具备可视化表现形式：默认情况图层没有画布指令。不管如何做到的，你可以
给一个图层增加画布指令，直接用增加一个背景色的例子是：

在 Python 代码里::

    from kivy.graphics import Color, Rectangle

    with layout_instance.canvas.before:
        Color(0, 1, 0, 1) # green; colors range from 0-1 instead of 0-255
        self.rect = Rectangle(size=layout_instance.size,
                               pos=layout_instance.pos)

不幸的是这段代码只在图层的初始化位置和尺寸上绘制了一个四边形。
要确保 ``rect`` 绘制在图层里面，那么当图层的大小/位置变化时，
我们需要对四边形的尺寸和位置上的任何一次变化和更新都做监听。那
我们要写如下代码来实现::

    with layout_instance.canvas.before:
        Color(0, 1, 0, 1) # green; colors range from 0-1 instead of 0-255
        self.rect = Rectangle(size=layout_instance.size,
                               pos=layout_instance.pos)

    def update_rect(instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

    # listen to size and position changes
    layout_instance.bind(pos=update_rect, size=update_rect)

在 kv 设计语言中写：

.. code-block:: kv

    FloatLayout:
        canvas.before:
            Color:
                rgba: 0, 1, 0, 1
            Rectangle:
                # self here refers to the widget i.e BoxLayout
                pos: self.pos
                size: self.size

在 kv 中的声明设置了一项隐含绑定：最后两行确保了四边形的 |pos| 位置和尺寸 |size| 值
在浮动图层的 |pos| 变化时能够得到更新。

现在我们把上面的代码片段放到 Kivy ``App`` 里面。

纯 Python 实现的方法是::

    from kivy.app import App
    from kivy.graphics import Color, Rectangle
    from kivy.uix.floatlayout import FloatLayout
    from kivy.uix.button import Button
    
    
    class RootWidget(FloatLayout):
    
        def __init__(self, **kwargs):
            # make sure we aren't overriding any important functionality
            super(RootWidget, self).__init__(**kwargs)
    
            # let's add a Widget to this layout
            self.add_widget(
                Button(
                    text="Hello World",
                    size_hint=(.5, .5),
                    pos_hint={'center_x': .5, 'center_y': .5}))
    
    
    class MainApp(App):
    
        def build(self):
            self.root = root = RootWidget()
            root.bind(size=self._update_rect, pos=self._update_rect)

            with root.canvas.before:
                Color(0, 1, 0, 1)  # green; colors range from 0-1 not 0-255
                self.rect = Rectangle(size=root.size, pos=root.pos)
            return root
    
        def _update_rect(self, instance, value):
            self.rect.pos = instance.pos
            self.rect.size = instance.size
    
    if __name__ == '__main__':
        MainApp().run()

要在 Python 代码里使用 kv 语言::

    from kivy.app import App
    from kivy.lang import Builder


    root = Builder.load_string('''
    FloatLayout:
        canvas.before:
            Color:
                rgba: 0, 1, 0, 1
            Rectangle:
                # self here refers to the widget i.e FloatLayout
                pos: self.pos
                size: self.size
        Button:
            text: 'Hello World!!'
            size_hint: .5, .5
            pos_hint: {'center_x':.5, 'center_y': .5}
    ''')

    class MainApp(App):

        def build(self):
            return root

    if __name__ == '__main__':
        MainApp().run()

这两种 ``App`` 风格的编程结果看起来如下图一样：

.. image:: images/layout_background.png

给 **自定义图层规则/类** 的背景色着色
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

如果我们需要使用多个图层的话，我们给背景色着色的方法很快就变得笨重起来。
要轻松面对着色问题，你可以用图层的子类建立你自己的图层，增加一个背景。

使用纯 Python 方式::

    from kivy.app import App
    from kivy.graphics import Color, Rectangle
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.floatlayout import FloatLayout
    from kivy.uix.image import AsyncImage
    
    
    class RootWidget(BoxLayout):
        pass
    
    
    class CustomLayout(FloatLayout):
    
        def __init__(self, **kwargs):
            # make sure we aren't overriding any important functionality
            super(CustomLayout, self).__init__(**kwargs)
    
            with self.canvas.before:
                Color(0, 1, 0, 1)  # green; colors range from 0-1 instead of 0-255
                self.rect = Rectangle(size=self.size, pos=self.pos)
    
            self.bind(size=self._update_rect, pos=self._update_rect)
    
        def _update_rect(self, instance, value):
            self.rect.pos = instance.pos
            self.rect.size = instance.size
    
    
    class MainApp(App):
    
        def build(self):
            root = RootWidget()
            c = CustomLayout()
            root.add_widget(c)
            c.add_widget(
                AsyncImage(
                    source="http://www.everythingzoomer.com/wp-content/uploads/2013/01/Monday-joke-289x277.jpg",
                    size_hint= (1, .5),
                    pos_hint={'center_x':.5, 'center_y':.5}))
            root.add_widget(AsyncImage(source='http://www.stuffistumbledupon.com/wp-content/uploads/2012/05/Have-you-seen-this-dog-because-its-awesome-meme-puppy-doggy.jpg'))
            c = CustomLayout()
            c.add_widget(
                AsyncImage(
                    source="http://www.stuffistumbledupon.com/wp-content/uploads/2012/04/Get-a-Girlfriend-Meme-empty-wallet.jpg",
                    size_hint= (1, .5),
                    pos_hint={'center_x':.5, 'center_y':.5}))
            root.add_widget(c)
            return root
    
    if __name__ == '__main__':
        MainApp().run()

结合 kv 设计语言的方式::

    from kivy.app import App
    from kivy.uix.floatlayout import FloatLayout
    from kivy.uix.boxlayout import BoxLayout
    from kivy.lang import Builder


    Builder.load_string('''
    <CustomLayout>
        canvas.before:
            Color:
                rgba: 0, 1, 0, 1
            Rectangle:
                pos: self.pos
                size: self.size

    <RootWidget>
        CustomLayout:
            AsyncImage:
                source: 'http://www.everythingzoomer.com/wp-content/uploads/2013/01/Monday-joke-289x277.jpg'
                size_hint: 1, .5
                pos_hint: {'center_x':.5, 'center_y': .5}
        AsyncImage:
            source: 'http://www.stuffistumbledupon.com/wp-content/uploads/2012/05/Have-you-seen-this-dog-because-its-awesome-meme-puppy-doggy.jpg'
        CustomLayout
            AsyncImage:
                source: 'http://www.stuffistumbledupon.com/wp-content/uploads/2012/04/Get-a-Girlfriend-Meme-empty-wallet.jpg'
                size_hint: 1, .5
                pos_hint: {'center_x':.5, 'center_y': .5}
    ''')

    class RootWidget(BoxLayout):
        pass

    class CustomLayout(FloatLayout):
        pass

    class MainApp(App):

        def build(self):
            return RootWidget()

    if __name__ == '__main__':
        MainApp().run()


两种给自定义图层着色的代码效果看起来如下一样：

.. image:: images/custom_layout_background.png

在自定义图层类中定义背景，确保在每个 ``CustomLayout`` 类的子类中都能够被使用。

现在要把一张图片或一个颜色增加到一个内置 Kivy 图层背景上，**全局范围里**，
我们需要覆写图层的 kv 规则。
思考一下 ``GridLayout`` 类::

    <GridLayout>
        canvas.before:
            Color:
                rgba: 0, 1, 0, 1
            BorderImage:
                source: '../examples/widgets/sequenced_images/data/images/button_white.png'
                pos: self.pos
                size: self.size

然后我们把这个片段放到一个 Kivy 应用代码中::

    from kivy.app import App
    from kivy.uix.floatlayout import FloatLayout
    from kivy.lang import Builder


    Builder.load_string('''
    <GridLayout>
        canvas.before:
            BorderImage:
                # BorderImage behaves like the CSS BorderImage
                border: 10, 10, 10, 10
                source: '../examples/widgets/sequenced_images/data/images/button_white.png'
                pos: self.pos
                size: self.size

    <RootWidget>
        GridLayout:
            size_hint: .9, .9
            pos_hint: {'center_x': .5, 'center_y': .5}
            rows:1
            Label:
                text: "I don't suffer from insanity, I enjoy every minute of it"
                text_size: self.width-20, self.height-20
                valign: 'top'
            Label:
                text: "When I was born I was so surprised; I didn't speak for a year and a half."
                text_size: self.width-20, self.height-20
                valign: 'middle'
                halign: 'center'
            Label:
                text: "A consultant is someone who takes a subject you understand and makes it sound confusing"
                text_size: self.width-20, self.height-20
                valign: 'bottom'
                halign: 'justify'
    ''')

    class RootWidget(FloatLayout):
        pass


    class MainApp(App):

        def build(self):
            return RootWidget()

    if __name__ == '__main__':
        MainApp().run()

最后结果看起来像下面一样：

.. image:: images/global_background.png

因为我们覆写了 ``GridLayout`` 类的 kv 规则，任何一个这个类都会使用 kv 语言的效果，
在应用代码中就会显示资源指定的图片。

那么如何增加一个 **动画背景** 呢？

你可以设置绘画指令，像 Rectangle/BorderImage/Ellipse/... 来使用
一个特殊的 ``texture`` 属性::

    Rectangle:
        texture: reference to a texture

我们使用这种结构属性来显示一种动画背景::

    from kivy.app import App
    from kivy.uix.floatlayout import FloatLayout
    from kivy.uix.gridlayout import GridLayout
    from kivy.uix.image import Image
    from kivy.properties import ObjectProperty
    from kivy.lang import Builder


    Builder.load_string('''
    <CustomLayout>
        canvas.before:
            BorderImage:
                # BorderImage behaves like the CSS BorderImage
                border: 10, 10, 10, 10
                texture: self.background_image.texture
                pos: self.pos
                size: self.size

    <RootWidget>
        CustomLayout:
            size_hint: .9, .9
            pos_hint: {'center_x': .5, 'center_y': .5}
            rows:1
            Label:
                text: "I don't suffer from insanity, I enjoy every minute of it"
                text_size: self.width-20, self.height-20
                valign: 'top'
            Label:
                text: "When I was born I was so surprised; I didn't speak for a year and a half."
                text_size: self.width-20, self.height-20
                valign: 'middle'
                halign: 'center'
            Label:
                text: "A consultant is someone who takes a subject you understand and makes it sound confusing"
                text_size: self.width-20, self.height-20
                valign: 'bottom'
                halign: 'justify'
    ''')


    class CustomLayout(GridLayout):

        background_image = ObjectProperty(
            Image(
                source='../examples/widgets/sequenced_images/data/images/button_white_animated.zip',
                anim_delay=.1))


    class RootWidget(FloatLayout):
        pass


    class MainApp(App):

        def build(self):
            return RootWidget()

    if __name__ == '__main__':
        MainApp().run()

要尽力理解这里的代码发生了什么，从第 13 行代码开始看::

    texture: self.background_image.texture

这句 kv 代码描述了 `BorderImage` 的 `texture` 财产值，
不管 `background_image` 的 `texture` 什么时候更新都会
更新 kv 中所描述的财产值。我们定义 ``background_image`` 是在第 40 行::

    background_image = ObjectProperty(...

这句 python 代码让 `background_image` 变量名指向了一个 |ObjectProperty| 实例对象，
在这个对象财产类中我们增加了一个 |Image| 挂件类的实例。一个图片挂件具有一项 `texture` 财产；
所以你看到 `self.background_image.texture` 就是 python 代码中所实现的，这种 kv 设置指向
了 `texture` 这个财产项。
由于 |Image| 类挂件支持动画：图片的结构财产更新是在动画变化时产生的，并且 ``BorderImage``
指令中的 ``texture`` 也是在这个过程中进行更新。

你也可以把自定义数据提供给 ``texture`` ，对于这部分细节阅读
 :class:`~kivy.graphics.texture.Texture` 类的文档内容。

嵌入式图层
---------------

没错！要明白如何扩展这个过程是非常有趣的一件事。


尺寸和位置的度量衡
-------------------------

.. |Transitions| replace:: :class:`~kivy.uix.screenmanager.TransitionBase`
.. |ScreenManager| replace:: :class:`~kivy.uix.screenmanager.ScreenManager`
.. |Screen| replace:: :class:`~kivy.uix.screenmanager.Screen`
.. |screen| replace:: :mod:`~kivy.modules.screen`
.. |metrics| replace:: :mod:`~kivy.metrics`
.. |pt| replace:: :attr:`~kivy.metrics.pt`
.. |mm| replace:: :attr:`~kivy.metrics.mm`
.. |cm| replace:: :attr:`~kivy.metrics.cm`
.. |in| replace:: :attr:`~kivy.metrics.inch`
.. |dp| replace:: :attr:`~kivy.metrics.dp`
.. |sp| replace:: :attr:`~kivy.metrics.sp`

Kivy 默认的长度单位是像素，所有尺寸和位置都默认用像素来表达。你可以用其它单位来表达，
其中比较有用的地方是使用不同的设备时能保持一致的理解（实际上任何其它单位都要最终转换成像素）。

可用的其它单位有 |pt|, |mm|, |cm|, |in|, |dp| 和 |sp| 。你可以在 |metrics| 度量衡文档中学习。

你也可以用 |screen| 屏幕用法来实验，为你的应用程序模拟各种设备的屏幕。

使用屏幕管理器来实现分屏功能
-------------------------------------

如果你的应用由各种不同的屏幕界面组成，你可能想要容易地从一个 |Screen| 指向到另一个。
幸运的是，我们有 |ScreenManager| 类，这个类允许你定义许多独立的屏幕，然后设置
传输 |Transitions| 类实现从一个屏幕到另一个屏幕的效果。
