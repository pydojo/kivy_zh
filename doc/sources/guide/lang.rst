.. _lang:

Kv 设计语言
===========

设计语言背后的概念
---------------------------

由于你的应用会成长为更加多层化的形式，挂件树的建造和明确地绑定声明变得
冗长和难于维护，这是共性的问题。那么 `KV` 设计语言就是弥补这种缺陷的解决方案。

对于 `KV` 设计语言来说，有时候会叫 kvlang 或 kivy 语言，让你建立挂件树的时候
采用一种声明的方式，并且把挂件财产相互绑定，或者用一种自然的方法来回调。 ``KV``
在迅速建立原型和与你的 UI 变化保持一起变化方面都是有效的。它也方便了把你的应用逻辑
和应用的用户界面分离开来。

如何加载 KV
--------------

有2种方法来加载 `KV` 代码到你的应用中：

- 通过命名转换：

  Kivy 查看一个 Kv 文件使用的是与你的 ``App`` 类相同的文件名，不过是全小写形式，
  如果你的应用子类以 App 结尾的话还要去掉 App 部分。例如::

    MyApp -> my.kv

  如果这个文件定义了一个 `根挂件` ，那么还要跟在 App 的 `root` 属性之后，
  并且作为应用挂件树的基础。

- :obj:`~kivy.lang.Builder` 对象：
  你可以告诉 Kivy 直接夹在一个字符串或一个文件。如果字符串或文件定义了一个根挂件，
  根挂件会通过方法返回::

    Builder.load_file('path/to/file.kv')

  或者::

    Builder.load_string(kv_string)

规则语境
------------

一个 Kv 代码源是由许多 `规则` 组成的，规则都是描述一个挂件的内容。
你可以有一个 `根` 规则，然后任何数量的 `类` 或任何数量的 `模版` 规则。

`根` 规则的描述是通过描述你的根挂件的类来实现，不需要任何缩进，以冒号 `:` 结束，
然后被设置成 ``App`` 类实例的 `root` 属性了::

    Widget:

一个 `类` 规则的描述是通过使用一对儿尖括号 `< >` 包裹着一个挂件的名字后以冒号 `:` 结束， 
然后定义该类任何一个实例的外观和表现::

    <MyWidget>:

下面的规则都是用缩进来进行分隔，就像 Python 一样。缩进每一层都是用4个空格，
遵循了 Python 风格指导的建议
`缩进用法 <https://www.python.org/dev/peps/pep-0008/#indentation>`_

对于 Kv 设计语言来说有 3 个具体的关键字：

- `app`：一直指向你的应用类的实例。
- `root`：指向当前规则中基础挂件/模版。
- `self`：一直指向当前挂件。

特殊句法
----------------

有一种特殊句法是为整个 Kv 语境定义众多值的。

要想从 kv 文件访问 Python 模块和类，使用 ``#:import`` ::

    #:import name x.y.z
    #:import isdir os.path.isdir
    #:import np numpy

等效于 Python 中的句法::

    from x.y import z as name
    from os.path import isdir
    import numpy as np


要想设置一个全局变量值，使用 ``#:set`` ::

    #:set name value

等效于 Python 中的句法::

    name = value


实例化子挂件
--------------------

要想把某个类的一个挂件实例声明称一个子挂件，只需要把那个子挂件声明在根挂件规则里：

.. code-block:: kv

    MyRootWidget:
        BoxLayout:
            Button:
            Button:

上面这个例子定义了我们的根挂件，就是一个 `MyRootWidget` 类的实例，
所拥有的一个子挂件就是 :class:`~kivy.uix.boxlayout.BoxLayout` 类的实例，
然后 ``BoxLayout`` 下面又有2个子挂件是 :class:`~kivy.uix.button.Button` 类的实例。

用 Python 代码写同样效果的代码也许是：

.. code-block:: python

    root = MyRootWidget()
    box = BoxLayout()
    box.add_widget(Button())
    box.add_widget(Button())
    root.add_widget(box)

你可以看到两种代码都具有可读性和良好地书写能力，而 Kv 代码量更少。

当然，在 Python 中，你可以在建立描述这些行为时代入关键字参数。
例如，设置一个 :mod:`~kivy.uix.gridlayout` 网格图层的列数，我们可以这样做::

    grid = GridLayout(cols=3)

在 kv 中做同样的事情，你可以在规则中直接设置子挂件的财产：

.. code-block:: kv

    GridLayout:
        cols: 3

写财产值时会被评估成一个 Python 表达式，然后所有用在表达式中的财产都会被看到，
这意味着，如果你在 Python 中有类似这样的代码（这就假定 `self` 就是一个含有
一项 `data` :class:`~kivy.property.ListProperty` 类数据的挂件）::

    grid = GridLayout(cols=len(self.data))
    self.bind(data=grid.setter('cols'))

当你的数据有变化时要显示更新后的效果，你可以在 kv 中写成：

.. code-block:: kv

    GridLayout:
        cols: len(root.data)

.. note::
    挂件名字都应该以大写字母开头，同时财产名都应该以小写开头。
    遵循 `PEP8 命名指导 <https://www.python.org/dev/peps/pep-0008/#naming-conventions>`_
    是我们鼓励你们这样做的最好实行。

事件绑定
--------------

在 Kv 中你可以使用冒号 ":" 句法来绑定事件，就这样把一个回调函数与一个事件关联起来了：

.. code-block:: kv

    Widget:
        on_size: my_callback()

你可以使用 `args` 关键字参数信号把值调度进函数中：

.. code-block:: kv

    TextInput:
        on_text: app.search(args[1])

更多层化的表达式可以像下面这样用：

.. code-block:: kv

    pos: self.center_x - self.texture_size[0] / 2., self.center_y - self.texture_size[1] / 2.

这种表达式监听了 ``center_x``, ``center_y``, 和 ``texture_size`` 中的变化。
如果其中一项有了变化，表达式会重新进行评估来更新 ``pos`` 区域。

你也可以在 kv 语言中处理 ``on_`` 类型事件。例如，
``TextInput`` 类有一个 ``focus`` 财产，这个财产自动生成 ``on_focus`` 事件，
在 kv 代码中可以访问这个事件：

.. code-block:: kv

    TextInput:
        on_focus: print(args)


扩展画布
-------------

Kv 语言可以用来定义你挂件的画布指令，例如：

.. code-block:: kv

    MyWidget:
        canvas:
            Color:
                rgba: 1, .3, .8, .5
            Line:
                points: zip(self.data.x, self.data.y)

当财产值变化时画布得到更新。

当然你可以使用 `canvas.before` 和 `canvas.after` 指令。

指向挂件
-------------------

在一个挂件树中常常需要 访问/指向 其它的挂件。那么 Kv 语言提供了一个方法来实现，
就是使用 `id` 做到的。把这些 `id` 想成类级别的变量（不是类实例级别的变量），
这些类的变量之一用在 Kv 语言里。思考如下代码：

.. code-block:: kv

    <MyFirstWidget>:
        Button:
            id: f_but
        TextInput:
            text: f_but.state

    <MySecondWidget>:
        Button:
            id: s_but
        TextInput:
            text: s_but.state

一个 ``id`` 使用的限制范围是在声明规则里，所以在上面的代码中的 ``s_but`` 类变量
不能被 ``<MySecondWidget>`` 类规则以外的范围访问。

.. warning:: 当给一个 ``id`` 分配一个值的时候，记住值不能是字符串。
   也不能用引号，例如，好的用法是 -> ``id: value``，坏的用法是 -> ``id: 'value'``

一个 ``id`` 是一种 ``weakref`` 方式（为描述器存储属性值）指向挂件，而不是挂件本身。
作为一种结果，存储 ``id`` 来保持挂件被垃圾回收机制处理是不够的。示范代码如下：

.. code-block:: kv

    <MyWidget>:
        label_widget: label_widget
        Button:
            text: 'Add Button'
            on_press: root.add_widget(label_widget)
        Button:
            text: 'Remove Button'
            on_press: root.remove_widget(label_widget)
        Label:
            id: label_widget
            text: 'widget'

代码中尽管指向的 ``label_widget`` 存储在 ``MyWidget`` 类中，但无法保存对象一直存在，
一旦其它指向删除后就会消失，因为这只是一种 `weakref` 方式。
因此，点击移除按钮之后（就会删除任何一个直接指向挂件）以及窗口大小改变之后（调用了垃圾回收器
导致删除 ``label_widget`` 结果），当点击增加按钮时，就又把挂件增加回来，那么会抛出一个
 ``ReferenceError: weakly-referenced object no longer exists`` 指向错误例外。

要想保持挂件一直存在，一个直接指向 ``label_widget`` 挂件必须保存下来。在这里实现就是使用
 ``id.__self__`` 或者使用 ``label_widget.__self__`` 。那么纠正以后的代码会是：

.. code-block:: kv

    <MyWidget>:
        label_widget: label_widget.__self__

在你的 Python 代码里的 Kv 语言定义访问挂件
------------------------------------------------------------

思考 `my.kv` 文件中的代码：

.. code-block:: kv

    <MyFirstWidget>:
        # both these variables can be the same name and this doesn't lead to
        # an issue with uniqueness as the id is only accessible in kv.
        txt_inpt: txt_inpt
        Button:
            id: f_but
        TextInput:
            id: txt_inpt
            text: f_but.state
            on_text: root.check_status(f_but)


在 `myapp.py` 文件里：

.. code-block:: py

    ...
    class MyFirstWidget(BoxLayout):

        txt_inpt = ObjectProperty(None)

        def check_status(self, btn):
            print('button state is: {state}'.format(state=btn.state))
            print('text input text is: {txt}'.format(txt=self.txt_inpt))
    ...

其中 `txt_inpt` 定义成一个 :class:`~kivy.properties.ObjectProperty` 类的实例，
初始化时使用 `None` 值 ::

    txt_inpt = ObjectProperty(None)

这时候 self.txt_inpt 的值就是 `None` 了。在 Kv 语言中这项财产更新成
保存 :class:`~kivy.uix.TextInput` 类的实例由 `id` 指向 `txt_inpt`::

    txt_inpt: txt_inpt

从这点继续看， `self.txt_inpt` 保存了一个指向挂件，通过 id `txt_input` 来识别，
然后可以用在类中的任何地方，与在方法 `check_status` 中一样。与这个方法对比而言，
你可以只把 `id` 代入到你需要使用的函数中，就像上面代码中的 `f_but` 一样。

这里有一种更简单的方法来访问含有 `id` 标签的对象，那就是在 Kv 语言中使用 `ids` 来找到对象。
你可以像下面一样来实现：

.. code-block:: kv

    <Marvel>
      Label:
        id: loki
        text: 'loki: I AM YOUR GOD!'
      Button:
        id: hulk
        text: "press to smash loki"
        on_release: root.hulk_smash()

在你的 Python 代码中要写：

.. code-block:: python

    class Marvel(BoxLayout):

        def hulk_smash(self):
            self.ids.hulk.text = "hulk: puny god!"
            self.ids["loki"].text = "loki: >_<!!!"  # alternative syntax

当你的 kv 文件经过语法分析时，kivy 收集了所有含有 id 标签的挂件，
然后把这些 id 放在 `self.ids` 字典类型财产中。那就意味着你也可以
迭代这些挂件后访问字典风格的内容::

    for key, val in self.ids.items():
        print("key={0}, val={1}".format(key, val))

.. Note::

    虽然 `self.ids` 是非常简明的方法，但通用中视为使用 ``ObjectProperty`` 类的最好实行。
    这样建立了一个直接指向，提供了更快地访问而且更加明确。

动态类
---------------
思考如下代码：

.. code-block:: kv

    <MyWidget>:
        Button:
            text: "Hello world, watch this text wrap inside the button"
            text_size: self.size
            font_size: '25sp'
            markup: True
        Button:
            text: "Even absolute is relative to itself"
            text_size: self.size
            font_size: '25sp'
            markup: True
        Button:
            text: "Repeating the same thing over and over in a comp = fail"
            text_size: self.size
            font_size: '25sp'
            markup: True
        Button:

要想代替每个按钮中重复的一样值部分，我们可以使用一个模版来代替重复地写法，如下：

.. code-block:: kv

    <MyBigButt@Button>:
        text_size: self.size
        font_size: '25sp'
        markup: True

    <MyWidget>:
        MyBigButt:
            text: "Hello world, watch this text wrap inside the button"
        MyBigButt:
            text: "Even absolute is relative to itself"
        MyBigButt:
            text: "repeating the same thing over and over in a comp = fail"
        MyBigButt:

这个类，是通过这种规则写法建立的，实现了继承自 ``Button`` 类后允许我们
改变默认值和建立所有实例的绑定，而且不需要在 Python 后端增加任何新代码。

在多挂件中复用风格
-----------------------------------

思考 `my.kv` 中的如下代码：

.. code-block:: kv

    <MyFirstWidget>:
        Button:
            on_press: root.text(txt_inpt.text)
        TextInput:
            id: txt_inpt

    <MySecondWidget>:
        Button:
            on_press: root.text(txt_inpt.text)
        TextInput:
            id: txt_inpt

在 `myapp.py` 文件中的代码：

.. code-block:: py

    class MyFirstWidget(BoxLayout):

        def text(self, val):
            print('text input text is: {txt}'.format(txt=val))

    class MySecondWidget(BoxLayout):

        writing = StringProperty('')

        def text(self, val):
            self.writing = val

因为这两个类都分享了相同的 kv 风格，如果你重复使用一样的风格给这2个挂件的话，
这种设计语言可以简化成如下形式。在 `my.kv` 文件中改写成：

.. code-block:: kv

    <MyFirstWidget,MySecondWidget>:
        Button:
            on_press: root.text(txt_inpt.text)
        TextInput:
            id: txt_inpt

用一个逗号 ``,`` 分隔两个类名，所有列在声明中的类会使用相同的 kv 财产。

用 Kivy 语言进行外观设计
--------------------------------

开发出 Kivy 语言的目的之一就是考虑逻辑与外观的
`实现分离 <https://en.wikipedia.org/wiki/Separation_of_concerns>`_
这种外观（图层）前端由你的 `.kv` 文件来解释，后端逻辑由你的 `.py` 文件来解释。

在 `.py` 文件中的代码
~~~~~~~~~~~~~~~~~~~~~~~~~

我们用一个小例子来开启前后端分离思维：一个名叫 `main.py` 的 Python 文件位于：

.. include:: ../../../examples/guide/designwithkv/main.py
   :literal:

在这里例子中，我们建立了一个含有2项财产的 ``Controller`` 类：

    * ``info`` 是接收一些文本
    * ``label_wid`` 是接收标签挂件

另外，我们建立了一个 ``do_action()`` 方法，它会使用这2项财产。
它也会改变 ``info`` 文本和 ``label_wid`` 挂件中的文字。

前端图层代码写在 `controller.kv` 文件里
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

单独执行这个应用没有问题，但不会在屏幕上显示任何内容，因为还没有相关的 `.kv` 文件。
这是必然的，因为在 ``Controller`` 类中没有任何挂件存在，这个类此时只是一个 ``FloatLayout`` 类。
我们可以围绕着 ``Controller`` 类来建立 UI 内容，文件命名为 `controller.kv`，
当我们运行 ``ControllerApp`` 类时这个文件会被加载。如何实现这个文件呢？以及都需要
加载什么文件呢？那就要描述在 :meth:`kivy.app.App.load_kv` 方法中。

.. literalinclude:: ../../../examples/guide/designwithkv/controller.kv
    :language: kv
    :linenos:

一个标签和一个按钮都是垂直摆放的 ``BoxLayout`` 形式。看起来非常简单，但包含了3件事：

    1. 从 ``Controller`` 类使用数据时：控制器类里的 ``info`` 财产立即产生变化，
       表达式 ``text: 'My controller info is: ' + root.info`` 会自动重新评估，
       改变 ``Button`` 类中的文字内容。

    2. 提供给 ``Controller`` 类数据的时候：表达式 ``id: my_custom_label``
       正在发送信号来建立 ``Label`` 的 id ``my_custom_label`` 内容。然后把
       表达式中的 ``my_custom_label`` 提供给 ``label_wid: my_custom_label``
       ，这样就把 ``Label`` 挂件的实例给了你的 ``Controller`` 类。

    3. 在 ``Button`` 类中建立一个自定义回调函数，就是用 ``Controller`` 类的
       ``on_press`` 方法实现。

        * ``root`` 和 ``self`` 都是保留关键字，可以用在任何地方。
          ``root`` 代表了规则中的顶层挂件，而 ``self`` 代表当前挂件。

        * 你可以使用任何声明在规则里的一个 id ，用起来与 ``root`` 和
          ``self`` 一样。例如，你可以在 ``on_press()`` 中来用：

        .. code-block:: kv

            Button:
                on_press: root.do_action(); my_custom_label.font_size = 18

就这些看起来简单的事情也不要轻视。现在当你运行 `main.py` 文件时， `controller.kv` 会
被自动加载，所以 ``Button`` 和 ``Label`` 类都能显示在屏幕上并做出触碰事件的响应效果。
