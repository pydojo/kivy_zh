输入管理
================

输入的架构
------------------

Kivy 能够处理绝大部分的输入类型：鼠标、触碰屏、加速器、陀螺仪，等等输入硬件。
它天生能处理的多触摸协议是如下操作系统上的协议：
Tuio, WM_Touch, MacMultitouchSupport, MT Protocol A/B 和 Android。

全局架构可以视为::

    输入供应器 -> 运动事件 -> 发布进程 -> 调度给窗口

所有输入事件属于 :class:`~kivy.input.motionevent.MotionEvent` 类。
它生成 2 种事件类型：

    - 触碰事件：一种运动型事件含有至少X和Y位置的坐标值。
      所有触碰类事件都通过挂件树来调度。
    - 非触碰事件：所有剩下的事件类型。例如加速器是一种连续性的事件，不含位置坐标。
      它不会有静止的起点或终点。这些类型事件都不是通过挂件树来调度的。


一个运动型事件是通过一个 :mod:`输入供应器 <kivy.input.providers>` 生成的。
一个输入供应器负责读取来自操作系统、网络、或其它应用程序的输入事件。有许多种
输入供应器，例如：

    - :class:`~kivy.input.providers.tuio.TuioMotionEventProvider` 类：是建立
      一个 UDP 服务器后监听 TUIO/OSC 消息。
    - :class:`~kivy.input.providers.wm_touch.WM_MotionEventProvider` 类：是
      使用 windows API 来读取多触碰信息后发送给 Kivy。
    - :class:`~kivy.input.providers.probesysfs.ProbeSysfsHardwareProbe` 类：是
      在 Linux 里迭代所有连接到电脑的硬件，然后找到每个多触碰设备，提供给一个多触碰输入供应器。
    - 还有更多的输入供应器类型！

当你写一个应用的时候，你不需要建立输入供应器。Kivy 尝试自动检测可用的硬件。
不管如何做到的，如果你想要支持自定义硬件的话，你会需要配置 Kivy 来生效。

在新建立的运动型事件传递给用户之前，Kivy 会开启发布进程给输入。
每个运动型事件经过分析后完成检测，然后纠正错误的输入，同时做出有意义的解释，例如：

    - 双击/三击检测，根据一个距离和时间阀值。
    - 当硬件不准确的时候让事件更准确
    - 如果原生触碰硬件在相同位置附近正在发送事件的话，会减少事件生成的数量

处理过后，运动型事件就调度给窗口。由于前面完成了解释，不是所有的事件都调度给
整个挂件树：窗口会过滤一些事件。对于给出一个事件来说：

    - 如果只是一个运动型事件的话，会调度给
      :meth:`~kivy.core.window.WindowBase.on_motion` 方法。
    - 如果是一个触碰事件，那么触碰（范围是0到1）的位置 (x,y) 坐标
      会经过标量成窗口尺寸（宽/高），然后再调度给：

      - :meth:`~kivy.uix.widget.Widget.on_touch_down` 方法
      - :meth:`~kivy.uix.widget.Widget.on_touch_move` 方法
      - :meth:`~kivy.uix.widget.Widget.on_touch_up` 方法


运动型事件侧写情况
---------------------

根据你的硬件和输入供应器的使用，可能为你产生更多可用的信息。
例如，一个触碰输入有一个 (x,y) 位置坐标，也许还有压力信息、
面积尺寸、一个加速向量，等等信息。

一个侧写就是一个字符串类型，指明在运动型事件中可用的特性都是哪些。
我们想象一下，你此时站在一个 ``on_touch_move`` 方法里::

    def on_touch_move(self, touch):
        print(touch.profile)
        return super(..., self).on_touch_move(touch)

输出结果会是::

    ['pos', 'angle']

.. warning::

    许多人会把侧写的名字和相关财产名混为一谈。
    正因为 ``'angle'`` 是在可用的侧写中，
    但不意味着触碰事件对象会有一个 ``angle`` 财产。

对于 ``'pos'`` 侧写来说，财产 ``pos``, ``x``, 和 ``y`` 会是可以使用的。
含有 ``'angle'`` 侧写，财产 ``a`` 会是可用的。因为我们说过，对于触碰事件来说，
 ``'pos'`` 是一种必须有的侧写，而 ``'angle'`` 不是非有不可。你可以通过检查
是否有 ``'angle'`` 侧写来扩展你的互动。

    def on_touch_move(self, touch):
        print('The touch is at position', touch.pos)
        if 'angle' in touch.profile:
            print('The touch angle is', touch.a)

你可以在 :mod:`~kivy.input.motionevent` 文档中找到一份可用的侧写清单。

触碰事件
------------

一个触碰事件就是一个特殊的 :class:`~kivy.input.motionevent.MotionEvent` 类，
其中财产 :attr:`~kivy.input.motionevent.MotionEvent.is_touch` 属性评估成 `True`。
对于所有触碰事件来说，你自动拥有 X 和 Y 位置坐标值，标量给窗口的宽和高。换句话说，
所有触碰事件都有一个 ``'pos'`` 侧写。

触碰事件的基础
~~~~~~~~~~~~~~~~~~

默认情况下，触碰事件都调度给所有当前显示的挂件。这意味着挂件接收触碰事件不管是否发生在硬件上。

如果你有其它 GUI 工具体验的话，这是一种计数器的感知。典型来说，如果坐标落在挂件区域内，
这些是把屏幕分解成许多几何面积，并且只调度触碰事件或鼠标事件给挂件。

当与触碰输入一起工作时，这种需求变得非常具有限制性。扫动、捏动和长按也可以对挂件区域以外
的坐标做出良好地获得和响应。

为了提供最大化地灵活性，Kivy 调度这类事件给所有的挂件，然后让挂件来决定如何做出反应。
如果你只想要对挂件以内的面积做出响应，你直接检查即可::

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            # The touch has occurred inside the widgets area. Do stuff!
            pass

            
坐标系
~~~~~~~~~~~

在你使用含有矩阵转换的挂件时，必须小心对待矩阵转换操作。一些挂件，例如
:class:`~kivy.uix.scatter.Scatter` 类有它们自己的矩阵转换，意味着
触碰必须乘以离散矩阵才能正确地调度触碰位置坐标给 `Scatter` 的子挂件。

    - 得到父空间的坐标给本地空间使用：
      :meth:`~kivy.uix.widget.Widget.to_local` 方法
    - 得到本地空间的坐标给父空间使用：
      :meth:`~kivy.uix.widget.Widget.to_parent` 方法
    - 得到本地空间的坐标给窗口空间使用：
      :meth:`~kivy.uix.widget.Widget.to_window` 方法
    - 得到窗口空间的坐标给本地空间使用：
      :meth:`~kivy.uix.widget.Widget.to_widget` 方法

你必须使用其中一种来把坐标正确地标量给语境。看一下离散矩阵的实现::

    def on_touch_down(self, touch):
        # push the current coordinate, to be able to restore it later
        touch.push()

        # transform the touch coordinate to local space
        touch.apply_transform_2d(self.to_local)

        # dispatch the touch as usual to children
        # the coordinate in the touch is now in local space
        ret = super(..., self).on_touch_down(touch)

        # whatever the result, don't forget to pop your transformation
        # after the call, so the coordinate will be back in parent space
        touch.pop()

        # return the result (depending what you want.)
        return ret


触碰形状
~~~~~~~~~~~~

如果触碰有一个形状的话，会反映在 'shape' 财产中。目前只有一个
 :class:`~kivy.input.shape.ShapeRect` 类被曝光::

    from kivy.input.shape import ShapeRect

    def on_touch_move(self, touch):
        if isinstance(touch.shape, ShapeRect):
            print('My touch have a rectangle shape of size',
                (touch.shape.width, touch.shape.height))
        # ...

双击
~~~~~~~~~~

双击是在一定时间内和一段距离里按两次的动作。计算双击是由双击发布进程模块负责。
你可以测试当前的触碰是否是两类双击中的一种::

    def on_touch_down(self, touch):
        if touch.is_double_tap:
            print('Touch is a double tap !')
            print(' - interval is', touch.double_tap_time)
            print(' - distance between previous is', touch.double_tap_distance)
        # ...

三击
~~~~~~~~~~

三击是在一定时间内和一段距离里按三次的动作。计算三击是由三击发布进程模块负责。
你可以测试当前触碰是否是两类三击中的一种::

    def on_touch_down(self, touch):
        if touch.is_triple_tap:
            print('Touch is a triple tap !')
            print(' - interval is', touch.triple_tap_time)
            print(' - distance between previous is', touch.triple_tap_distance)
        # ...

抓取触碰事件
~~~~~~~~~~~~~~~~~~~~~

对于父挂件可能调度一种触碰事件给子挂件，是来自 ``on_touch_down`` 的触碰，
而不是来自 ``on_touch_move`` 的触碰，也不是来自 ``on_touch_up`` 的触碰。
这是在某种情节下发生的，可能当一个触碰动作超出了绑定的父盒子范围，所以父挂件决定
不提醒其子挂件超出范围的运动。

但你也许想要在 ``on_touch_up`` 方法中要做点什么。比如说在你开始要做的是在
 ``on_touch_down`` 方法里产生的事件，可能是播放一个声音，然后你可能要在
 ``on_touch_up`` 方法里发生完成事件。抓取触碰事件就是你的需求了。

当你抓取一个触碰事件时，你会一直接收移动和放手事件。但对于抓取触碰事件也有一些限制：

    - 你会接收至少两次事件：一次来自你的父挂件（正常的事件），
      另一次来自窗口挂件（抓取的事件）。
    - 你也许接收一个含有抓取触碰的事件，但不是来自你的：这是因为父挂件已经发送
      触碰事件给了自己的子挂件，同时事件曾处于被抓取的状态。

这是一个如何使用抓取触碰事件的示例::

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):

            # if the touch collides with our widget, let's grab it
            touch.grab(self)

            # and accept the touch.
            return True

    def on_touch_up(self, touch):
        # here, you don't check if the touch collides or things like that.
        # you just need to check if it's a grabbed touch event
        if touch.grab_current is self:

            # ok, the current touch is dispatched for us.
            # do something interesting here
            print('Hello world!')

            # don't forget to ungrab ourself, or you might have side effects
            touch.ungrab(self)

            # and accept the last up
            return True
            
触碰事件管理
~~~~~~~~~~~~~~~~~~~~~~

要想明白触碰事件都是如何被控制与在挂件之间进行传播的，
请阅读 :ref:`挂件触碰事件冒泡 <widget-event-bubbling>` 文档部分。

手柄事件
---------------

手柄的输入表示成生食值，都直接来自硬件，或虚拟控制器，通过 SDL2 供应器获得这类事件：

* SDL_JOYAXISMOTION
* SDL_JOYHATMOTION
* SDL_JOYBALLMOTION
* SDL_JOYBUTTONDOWN
* SDL_JOYBUTTONUP

每个运动事件都有最小、最大和默认值可以获得：

+-------------+----------+---------+---------+
| Event       | Minimum  | Maximum | Default |
+=============+==========+=========+=========+
| on_joy_axis | -32767   |  32767  |    0    |
+-------------+----------+---------+---------+
| on_joy_hat  | (-1, -1) |  (1, 1) |  (0, 0) |
+-------------+----------+---------+---------+
| on_joy_ball | Unknown  | Unknown | Unknown |
+-------------+----------+---------+---------+

手柄上的每个按键都基本表示成按钮事件的一个状态，例如 `up` 和 `down`，因此没有其它的值形式。

* on_joy_button_up
* on_joy_button_down

手柄事件基础
~~~~~~~~~~~~~~~~~~~~~

.. |dropexpl| replace:: Multiple dropfile example
.. _dropexpl:
   https://github.com/kivy/kivy/blob/master/examples/miscellaneous/multiple_dropfile.py

与触碰事件不一样，手柄事件都直接调度给窗口挂件，意味着只有单个值被传递，
例如一个具体的坐标轴，而不是多个坐标值。如果你要分解输入给不同的挂件就更困难了，
而且也不是不可能。你可以使用 |dropexpl|_ 作为一项灵感自行研究。

要获得一个手柄事件，你首先需要把某个函数绑定到窗口挂件，像下面的手柄事件一样::

    Window.bind(on_joy_axis=self.on_joy_axis)

然后你需要针对你使用的每个事件得到描述在 :class:`~kivy.core.window.Window` 类
中的参数，例如::

    def on_joy_axis(self, win, stickid, axisid, value):
        print(win, stickid, axisid, value)

变量 `stickid` 是发送 `value` 的控制器ID， `axisid` 是 `value` 所属坐标轴的ID。

手柄输入
~~~~~~~~~~~~~~

Kivy 负责获得来自任何一种手柄设备的输入，这些设备描述成 `gamepad`、 `joystick` 或基本上
能被 SDL2 供应器识别的其它类型游戏手柄。要想变得更容易些，例如下面的控制器ID数据表。

Xbox 360
^^^^^^^^

.. |xbox_ctr| image:: ../images/input_xbox.png
   :width: 300

+------------+------+---------+-----+--------+
|            |  #   |ID       |  #  | ID     |
|            +------+---------+-----+--------+
|            |  1   |axis 1   |  2  |axis 0  |
|            +------+---------+-----+--------+
|            |  3   |hat Y    |  4  |hat X   |
|            +------+---------+-----+--------+
|            |  5   |axis 4   |  6  |axis 3  |
|            +------+---------+-----+--------+
|            |  7   |axis 2   |  8  |axis 5  |
| |xbox_ctr| +------+---------+-----+--------+
|            |  9   |button 4 | 10  |button 5|
|            +------+---------+-----+--------+
|            |  X   |button 2 |  Y  |button 3|
|            +------+---------+-----+--------+
|            |  A   |button 0 |  B  |button 1|
|            +------+---------+-----+--------+
|            | back |button 6 |start|button 7|
|            +------+---------+-----+--------+
|            |center|button 10|     |        |
+------------+------+---------+-----+--------+

手柄调试
~~~~~~~~~~~~~~~~~~

.. |vjoy| replace:: vJoy
.. _vjoy: http://vjoystick.sourceforge.net

大部分情况你想要与多种控制器来调试你的应用，或测试是否适用于 _other_ 类型的控制器
（例如，不同品牌的手柄）。作为另一种方案，你也许想要使用一些可用的控制器模拟器，例如 |vjoy|_ 。
