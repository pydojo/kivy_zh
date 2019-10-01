.. _events:
.. _properties:

事件与财产
=====================

事件都是 Kivy 编程中的一项重要组成部分。对那些 GUI 开发老手来说没有什么理解困难，
但对于新手来说是一个重要概念。一旦你理解了事件是如何工作的，以及理解如何绑定事件的话，
你会在 Kivy 代码中看到事件都是无处不在的。不管你想要的行为是什么，在 Kivy 中建立
事件并没有你想象的那么难，也没有你认为的那么容易。

下面的图片解释了事件都是如何在 Kivy 框架中进行处理的。

.. image:: images/Events.*


介绍事件调度器
------------------------------------

这是框架中最重要的基础类之一，那就是 :class:`~kivy.event.EventDispatcher` 类。
这个类允许你注册事件类型，然后调度给感兴趣的部分（常常是调度给其它事件调度器）。
其中 :class:`~kivy.uix.widget.Widget` 类，
:class:`~kivy.animation.Animation` 类和 :obj:`~kivy.clock.Clock` 对象都是
事件调度器的示例。

事件调度器根据主循环来产生和处理事件。

主循环
---------

在上面的图示中，Kivy 有一个 `main loop` ，这种循环会一直运行在所有应用的生命周期中，
并且只在退出程序时才会终止循环。

在主循环里，每一次迭代，都会从用户输入、硬件传感器、或其它源头生成事件，并且帧都被翻译
给显示器。

你的应用会描述一些回调（稍后再多说一点回调的事儿），这些回调都被主循环调用。如果一个回调
花费的事件太长，或无法退出一次回调的话，主循环就断裂了，然后你的应用就无法正常工作了。

在 Kivy 应用里，你要想避免太长的循环等待或无限循环等待，甚至进入无响应。例如下面的示例
代码会进入这种麻烦中::

    while True:
        animate_something()
        time.sleep(.10)

当你运行类似这样的一种代码时，程序永远不会退出循环，那么 Kivy 处了这个循环什么其它事也
做不了了。由于这种结果，你会看到一个黑色的窗口，不会显示任何互动产生的变化。相反，你需要
对重复调用的 ``animate_something()`` 函数做一份*时间安排*。


对重复的事件做时间安排
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

你可以调用一个函数或方法，安排在每秒调用多少次，那就要使用
:meth:`~kivy.clock.Clock.schedule_interval` 这个方法来实现。
这里有一个例子，安排 `my_callback` 函数每条调用 30 次::

    def my_callback(dt):
        print('My callback is called', dt)
    event = Clock.schedule_interval(my_callback, 1 / 30.)

要想取消一个时间计划完的事件，你有许多方法。其中一个就是使用
 :meth:`~kivy.clock.ClockEvent.cancel` 方法或 :meth:`~kivy.clock.Clock.unschedule` 方法::

    event.cancel()

或::

    Clock.unschedule(event)

另外，你可以在回调函数中返回 `False` 值，那么当返回这个值的时候会自动取消时间计划::

    count = 0
    def my_callback(dt):
        global count
        count += 1
        if count == 10:
            print('Last call of my callback, bye bye !')
            return False
        print('My callback is called')
    Clock.schedule_interval(my_callback, 1 / 30.)


对一次性事件做时间计划
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

使用 :meth:`~kivy.clock.Clock.schedule_once` 方法你可以实现下一个调用的函数是什么，
就像下一帧要什么画面，或在 X 秒内调用::

    def my_callback(dt):
        print('My callback is called !')
    Clock.schedule_once(my_callback, 1)

这个例子告诉我们 ``my_callback`` 函数在1秒内调用。其中第二个参数的意思是
在调用函数前等待时间不能超过1秒。不管如何做到的，你可以用第二个参数值实现一个
指定的时间计划：

- 如果 X 大于 0，回调会在 X 秒内被调用。即限时模式！
- 如果 X 等于 0，回调会在下一帧完成后被调用。即后天模式！
- 如果 X 等于 -1，回调函数会在下一帧之前被调用。即明天模式！

第二个参数值最多使用的是 -1，因为你正位于当前帧，就是在下一个事件发生*之前*安排一件事。

第二个方法对于重复调用一个函数来说，就是使用 :meth:`~kivy.clock.Clock.schedule_once`
方法先计划一次回调函数，然后在回调函数自身中第二次调用这个函数::


    def my_callback(dt):
        print('My callback is called !')
        Clock.schedule_once(my_callback, 1)
    Clock.schedule_once(my_callback, 1)

同时主循环会尝试把事件计划保留成已请求过的，当一个计划完的回调正好被调用时，
会有一些不明情况发生。有时候应用中另一个回调，或某个其它任务所花费的时间要
比已经参与的回调或任务更长，因此计时可以稍微短一点儿。

对于这种重复回调问题来说，解决方案是最新的迭代结束之后下一次迭代的调用至少是一秒。
使用 :meth:`~kivy.clock.Clock.schedule_interval` 方法，不管如何做到的，
回调都是按照每秒来被调用。

发动事件
~~~~~~~~~~~~~~

有时候你也许想要为下一帧只对一个函数做一次性计划，这样可以防止重复调用。
你可以像下面一样来实现::

    # First, schedule once.
    event = Clock.schedule_once(my_callback, 0)
    
    # Then, in another place you will have to unschedule first
    # to avoid duplicate call. Then you can schedule again.
    Clock.unschedule(event)
    event = Clock.schedule_once(my_callback, 0)

这种编程方法是发动事件的昂贵做法，因为你总要先调用取消计划，
即使事件已经完成了，也要做一步没有意义的操作。另外，每次都会
产生一个新事件。那么使用一个触发器来替换昂贵的做法::

    trigger = Clock.create_trigger(my_callback)
    # later
    trigger()

每次你调用 `trigger()` 的时候，它会对你的 `my_callback` 函数做单次调用。
如果已经计划过这个函数了，就不会重复做计划。


挂件事件
-------------

一个挂件有 2 种默认事件类型：

- 财产事件： 如果你的挂件改变了自身的位置或尺寸，一个事件就被触发了。
- 用挂件定义事件：: 例如一个会被按钮触发的事件，当按下或松开按钮时就会产生一种挂件事件。

对于挂件触碰事件是如何管理的讨论，以及挂件触碰事件是如何传播的讨论，
请阅读 :ref:`挂件触碰事件冒泡 <widget-event-bubbling>` 参考文档。

建立自定义事件
----------------------

要建立一个事件调度器含有自定义的事件，你需要用类来注册事件的名字，然后建立一个同名方法。

自定义事件例子::

    class MyEventDispatcher(EventDispatcher):
        def __init__(self, **kwargs):
            self.register_event_type('on_test')
            super(MyEventDispatcher, self).__init__(**kwargs)

        def do_something(self, value):
            # when do_something is called, the 'on_test' event will be
            # dispatched with the value
            self.dispatch('on_test', value)

        def on_test(self, *args):
            print("I am dispatched", args)


把回调附着在事件上
-------------------

要使用事件，你还要把回调函数绑定到事件上。当事件被调度时，
你的回调函数才会使用事件的参数进行调用。

一个回调函数可以是任何一种 Python 可调用对象，但你需要确保
可调用对象能够接收多参数，这样事件发出的参数才可以被接收。
对于这个来说，常常最安全的做法就是使用 `*args` 多参数形式，
它会捕获所有位于 `args` 列表中的参数。

绑定事件的回调例子::

    def my_callback(value, *args):
        print("Hello, I got an event!", args)


    ev = MyEventDispatcher()
    ev.bind(on_test=my_callback)
    ev.do_something('test')

请阅读 :meth:`kivy.event.EventDispatcher.bind` 方法的文档了解
更多如何把回调附着在事件上的示例。

介绍财产
--------------------------

财产都是定义事件和绑定事件回调的困难方法。虽然不可缺少，但财产生产的
事件都是一个对象的属性有变化时发生的事情，所有财产指向的属性都会被自动更新。

有各种不同类型的财产，都是用来描述你想要处理的数据类型。

- :class:`~kivy.properties.StringProperty`
- :class:`~kivy.properties.NumericProperty`
- :class:`~kivy.properties.BoundedNumericProperty`
- :class:`~kivy.properties.ObjectProperty`
- :class:`~kivy.properties.DictProperty`
- :class:`~kivy.properties.ListProperty`
- :class:`~kivy.properties.OptionProperty`
- :class:`~kivy.properties.AliasProperty`
- :class:`~kivy.properties.BooleanProperty`
- :class:`~kivy.properties.ReferenceListProperty`


一项财产的声明
-------------------------

要声明财产，你必须声明在类的层次上。当你建立完对象时，
类才会做实例化成属性的工作。这些财产都不是属性：它们都是根据属性来建立事件的机制::

    class MyWidget(Widget):

        text = StringProperty('')


当覆写 `__init__` 方法时，*一直* 要接收 `**kwargs` 多关键字参数，
并且使用 `super()` 内置函数来让子类调用父类的 `__init__` 方法，
总要使用明确地代入参数方式写在你的子类初始化方法中::

        def __init__(self, **kwargs):
            super(MyWidget, self).__init__(**kwargs)


调度一个财产事件
----------------------------

Kivy 的财产，默认提供一个 `on_<property_name>` 事件。
当财产值改变时，这个事件就会被调用。

.. Note::
    如果财产的新值等于当前值的话，`on_<property_name>` 事件不会被调用。

例如思考如下代码：

.. code-block:: python
   :linenos:

    class CustomBtn(Widget):

        pressed = ListProperty([0, 0])

        def on_touch_down(self, touch):
            if self.collide_point(*touch.pos):
                self.pressed = touch.pos
                return True
            return super(CustomBtn, self).on_touch_down(touch)

        def on_pressed(self, instance, pos):
            print('pressed at {pos}'.format(pos=pos))

上面第3行代码::

    pressed = ListProperty([0, 0])

是我们定义了 `pressed` 财产类型为 :class:`~kivy.properties.ListProperty` 类，
并给出了默认值 `[0, 0]`。继续向下看，不管什么时候这个财产值改变了
 `on_pressed` 事件都会被调用。

在第5行开始::

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.pressed = touch.pos
            return True
        return super(CustomBtn, self).on_touch_down(touch)

我们覆写了 `Widget`类的 :meth:`on_touch_down` 方法。此处我们检查了
触碰我们挂件时发生 `touch` 的状态。

如果触碰落在了我们挂件范围中，我们改变了 `pressed` 的值指向 `touch.pos` 后
返回 `True` 值，这说明我们已经消化掉了触碰后并不想继续传播下去。

最后，如果触碰落在挂件范围以外的话，我们使用 `super(...)` 部分代码来调用
原来的事件后返回结果。这允许触碰事件继续传播，说明事件会正常地出现。

最后从第11行代码看::

    def on_pressed(self, instance, pos):
        print('pressed at {pos}'.format(pos=pos))

我们定义了一个 `on_pressed` 方法，这个方法会在财产值变化时被调用。

.. Note::
    这里的 `on_<prop_name>` 类型事件被调用都是在类里定义财产的位置上发生。
    要监视/观察任何一项定义在类范围以外的财产变化，你就要按照下面方法来绑定到财产了。


**绑定到财产**

如何监视所有从外部访问一项财产的变化？例如通过挂件实例来访问另一个类的财产。
那你就要*绑定*到财产::

    your_widget_instance.bind(property_name=function_name)

根据上面的例子，思考如下代码：

.. code-block:: python
   :linenos:

    class RootWidget(BoxLayout):

        def __init__(self, **kwargs):
            super(RootWidget, self).__init__(**kwargs)
            self.add_widget(Button(text='btn 1'))
            cb = CustomBtn()
            cb.bind(pressed=self.btn_pressed)
            self.add_widget(cb)
            self.add_widget(Button(text='btn 2'))

        def btn_pressed(self, instance, pos):
            print('pos: printed from root widget: {pos}'.format(pos=.pos))

如果你运行这类代码，你会在终端里注意到执行了两个print函数。
一个是来自 `on_pressed` 事件，这个事件是调用在 `CustomBtn` 类里，
另一个是来自 `btn_pressed` 方法，这是我们绑定外部财产变化产生的。

这两个函数都直接被调用的原因是，绑定不代表覆写。
这两个函数可以选择其一，通用中你应该只使用其中
一种监听/响应方式来检测财产的变化。

你也应该注意得到的参数，这些参数都被代入到 `on_<property_name>` 事件中，
或者代入绑定到财产的函数里。

.. code-block:: python

    def btn_pressed(self, instance, pos):

第一参数必须是 `self`，这代表的就是定义这个函数的所在类的实例。
你可以使用函数式面向对象方法来实现，例如：

.. code-block:: python
   :linenos:

    cb = CustomBtn()

    def _local_func(instance, pos):
        print ('pos: printed from root widget: {pos}'.format(pos=pos))

    cb.bind(pressed=_local_func)
    self.add_widget(cb)

第一参数会成为定义财产类的实例了。

第二个参数会是财产的新值 `value` 。

下面是一个完整的示例，综合应用了上面的代码片段，
你可以复制粘贴到你的文本编辑器中做一下实验。

.. code-block:: python
   :linenos:

    from kivy.app import App
    from kivy.uix.widget import Widget
    from kivy.uix.button import Button
    from kivy.uix.boxlayout import BoxLayout
    from kivy.properties import ListProperty

    class RootWidget(BoxLayout):

        def __init__(self, **kwargs):
            super(RootWidget, self).__init__(**kwargs)
            self.add_widget(Button(text='btn 1'))
            cb = CustomBtn()
            cb.bind(pressed=self.btn_pressed)
            self.add_widget(cb)
            self.add_widget(Button(text='btn 2'))

        def btn_pressed(self, instance, pos):
            print ('pos: printed from root widget: {pos}'.format(pos=pos))

    class CustomBtn(Widget):

        pressed = ListProperty([0, 0])

        def on_touch_down(self, touch):
            if self.collide_point(*touch.pos):
                self.pressed = touch.pos
                # we consumed the touch. return False here to propagate
                # the touch further to the children.
                return True
            return super(CustomBtn, self).on_touch_down(touch)

        def on_pressed(self, instance, pos):
            print ('pressed at {pos}'.format(pos=pos))

    class TestApp(App):

        def build(self):
            return RootWidget()


    if __name__ == '__main__':
        TestApp().run()


运行上面示例代码会产生如下结果：

.. image:: images/property_events_binding.png

这里我们的 CustomBtn 类没有可视化表现形式因此显示的是黑色屏幕。
你可以在黑色区域测试触碰/点击，看看终端里会输出什么内容。

复合财产
-------------------

当定义一个 :class:`~kivy.properties.AliasProperty` 类的时候，
你要正常地自己定义一个 `getter` 和 `setter` 函数。这样，当使用 
`bind` 参数时才会调用你定义的财产控制属性。

思考一下如下代码：

.. code-block:: python
   :linenos:

    cursor_pos = AliasProperty(_get_cursor_pos, None,
                               bind=('cursor', 'padding', 'pos', 'size',
                                     'focus', 'scroll_x', 'scroll_y',
                                     'line_height', 'line_spacing'),
                               cache=True)
    '''Current position of the cursor, in (x, y).

    :attr:`cursor_pos` is an :class:`~kivy.properties.AliasProperty`,
    read-only.
    '''

其中 `cursor_pos` 是一个 :class:`~kivy.properties.AliasProperty` 类的实例对象，
它使用了 `getter` `_get_cursor_pos` 和 `setter` 部分设置成 `None`，隐含地表达了
这个对象是只读财产。

其中 `bind=` 参数定义了 `on_cursor_pos` 事件被调用的情况，就是当任何一项用在
 `bind=` 参数值里的财产有变化的时候。
