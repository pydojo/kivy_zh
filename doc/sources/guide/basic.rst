.. _basic:

Kivy 基础内容
===========

安装 Kivy 环境
------------------------------------

Kivy 是依据许多 Python 库建立起来的框架，例如 pygame, gstreamer, PIL,
Cairo, 等等。 并不是都需要安装，可以根据你所使用的操作系统来选择安装，
否则会让你感到痛苦。对于 Windows 和 MacOS 系统来说，我们提供了一种可
移植的包，你可以解压后使用。

阅读下面安装参考文档了解安装细节：

* :ref:`installation_windows`
* :ref:`installation_osx`
* :ref:`installation_linux`
* :ref:`installation_rpi`

另外，对于开发版本可以在如下参考文档中找到安装指令：

* :ref:`installation`

.. _quickstart:

建立一个应用
---------------------

要想写一个 kivy 应用需要明白：

- 使用 :class:`~kivy.app.App` 类的一个子类
- 在子类的实例上使用 :meth:`~kivy.app.App.build` 方法会返回一个
  :class:`~kivy.uix.Widget` 类的实例 (返回的实例作为挂件树的根)
- 在子类的实例上使用 :meth:`~kivy.app.App.run` 方法来执行应用的实例化过程。

下面是一个实现上面三步的应用例子::

    import kivy
    kivy.require('1.11.1') # 声明当前你所使用的kivy版本号

    from kivy.app import App
    from kivy.uix.label import Label


    class MyApp(App):

        def build(self):
            return Label(text='Hello Python3')


    if __name__ == '__main__':
        MyApp().run()

例如上面的代码保存在文本文件 `main.py` 中后运行即可看到效果。

Kivy 应用的生命周期
-------------------

首先，我们要熟悉一下 Kivy 应用的生命周期。

.. image:: ../images/Kivy_App_Life_Cycle.png

上图显示了整个生命周期的工作流，告诉我们一个应用使用了 run() 方法所涉及的
所有环节，在我们上面的例子中就是与 "MyApp().run()" 有关的所有内容。我们
总会要回顾这个工作流，但我们先看看第三行代码::

    from kivy.app import App

导入建立一个应用所需的 `App` 基类，所在位置是在kivy安装目录中：
<kivy安装目录>/kivy/app.py

.. 注意::
    如果你想要深入开发 App 类都能做什么的话，可以进入这个文件自行开发。
    我们鼓励你打开源代码并通篇阅读。Kivy 是根据 Python 和 Sphinx 来
    实现文档化工作，所以对于每个类的文档字符串来说都是文档的组成内容。

那么第四行代码::

    from kivy.uix.label import Label

注意重要的一件事，导入的方法是 包名/类名 这种结构。其中
:class:`~kivy.uix` 是目录模块化技术实现的，而 `label`
是一个模块文件，`Label`是这个模块文件中的一个类。相当于在
`uix` 中保存了许多用户接口元素，就像许多图层和挂件一样。

看一下第五行代码::

    class MyApp(App):

这就是我们自己定义的一个应用子类，继承自 App 这个基类。
你应该一直这样来建立应用，因为可以修改调试你自己的应用，
例如你可以把 `MyApp` 类名改成你想用的名字一样。

第六行代码::

    def build(self):

在生命周期中这是一项重点，这个函数形式是你在自己的子类中
必须要覆写的一项内容，因为它会初始化完成后返回一个根源挂件。
所以我们要在第七行代码明确写一个 return 语句::

    return Label(text='Hello Python3')

这里我们返回了一个标签挂件，其中含有文字 'Hello Python3'，
这里我们用一行来完成刚才所说的两个步骤，先用 Label 类完成
建立一个挂件实例后返回这个实例。那么此处应用的根源挂件就是
一个含有文字的标签了。

.. 注意::
    Python 使用缩进来形成块代码，因此上面所定义的类和函数
    要注意缩进问题。

那么我们作为执行区域的代码就是运行应用所需要的第八和第九行::

    if __name__ == '__main__':
        MyApp().run()

这里的 `MyApp()` 类完成初始化建立了一个实例，然后在实例上
调用了 `run()` 方法，从而启动了我们的 Kivy 应用。


运行应用
-----------------------
要运行应用针对不同操作系统有不同的指令:

    Linux
        参考如下文档了解指令
        :ref:`running a Kivy application on Linux <linux-run-app>`::

            $ python main.py

    Windows
        参考如下文档了解指令
        :ref:`running a Kivy application on Windows <windows-run-app>`::

            $ python main.py
            # or
            C:\appdir>kivy.bat main.py

    Mac OS X
        参考如下文档了解指令
        :ref:`running a Kivy application on OS X <osx-run-app>`::

            $ kivy main.py

    Android
        在安卓系统上运行应用需要一些补充文件才可以。
        阅读 :doc:`/guide/packaging-android` 文档了解细节。

运行成功后会有一个窗口出现，显示了一个含有文字的标签，
这个标签覆盖了整个窗口区域。基础部分就这些了。

.. image:: ../guide/images/quickstart.png
    :align: center


自定义应用
-------------------------

要想扩展你的应用，例如提供一个用户名/密码的登陆界面。

.. code-block:: python

    from kivy.app import App
    from kivy.uix.gridlayout import GridLayout
    from kivy.uix.label import Label
    from kivy.uix.textinput import TextInput


    class LoginScreen(GridLayout):

        def __init__(self, **kwargs):
            super(LoginScreen, self).__init__(**kwargs)
            self.cols = 2
            self.add_widget(Label(text='User Name'))
            self.username = TextInput(multiline=False)
            self.add_widget(self.username)
            self.add_widget(Label(text='password'))
            self.password = TextInput(password=True, multiline=False)
            self.add_widget(self.password)


    class MyApp(App):

        def build(self):
            return LoginScreen()


    if __name__ == '__main__':
        MyApp().run()

第二行我们导入了一个 :class:`~kivy.uix.gridlayout.Gridlayout` 类::

    from kivy.uix.gridlayout import GridLayout

这个类是给我们的根源挂件提供了一个放置的平台，
那就是定义在第五行上的 (LoginScreen) 子类::

    class LoginScreen(GridLayout):

第六行我们覆写了 :meth:`~kivy.widget.Widget.__init__` 方法，
这样可以自己增加一些挂件后重新定义一些行为::

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

这里不要忘记写调用 super 代码，这是为了把父类的初始化功能
可以让我们来覆写。同样要注意一项良好的实际代码，那就是调用
super 时别忽略 `**kwargs` 多关键字参数，因为可以确保提供
内部使用。

接下来下面的这些 self 代码行::

    self.cols = 2
    self.add_widget(Label(text='User Name'))
    self.username = TextInput(multiline=False)
    self.add_widget(self.username)
    self.add_widget(Label(text='password'))
    self.password = TextInput(password=True, multiline=False)
    self.add_widget(self.password)

都是 GridLayout 网格图层管理其子类的内容，其中我们设定了两列，
然后增加了一个 :class:`~kivy.uix.label.Label` 类和一个
 :class:`~kivy.uix.textinput.TextInput` 类提供用户名和密码区域。

最后运行这个应用会显示一个窗口，类似如下样子：

.. image:: ../guide/images/guide_customize_step1.png
   :align: center

你可以用鼠标来调整窗口大小，你会看到挂件会根据窗口的大小自动地进行调整。
这是因为挂件默认使用了尺寸提示功能。

如上代码目前不能处理用户的输入和验证，或其它事情。
我们会深入这个示例程序并且了解 :class:`~kivy.widget.Widget`
挂件的尺寸和位置问题。
