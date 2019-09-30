.. _configure kivy:

配置 Kivy
==============

对于 kivy 应用的配置文件来说，就是名叫 `config.ini` 的文件，
这种配置文件的标准格式如下 `标准 INI 格式 <http://en.wikipedia.org/wiki/INI_file>`_ 

配置文件的存放位置
-------------------------------

配置文件所在位置是由环境变量 `KIVY_HOME` 来控制::

    <KIVY_HOME>/config.ini

桌面应用默认值是::

    <HOME_DIRECTORY>/.kivy/config.ini

因此，如果你的操作系统用户名是 "tito" 的话，
那么配置文件会在：

- Windows: ``C:\Users\tito\.kivy\config.ini``
- OS X: ``/Users/tito/.kivy/config.ini``
- Linux: ``/home/tito/.kivy/config.ini``

在安卓操作系统上，配置文件的默认位置是::

    <ANDROID_APP_PATH>/.kivy/config.ini

如果你的 kivy 应用名字是 "org.kivy.launcher" 的话，
配置文件的位置是::

    /data/data/org.kivy.launcher/files/.kivy/config.ini

在苹果 iOS 系统上，配置文件的默认位置是::

    <HOME_DIRECTORY>/Documents/.kivy/config.ini


本地配置文件
-------------------

有时候想要给某些应用只改变配置，或者在测试期间对 Kivy 的局部做测试，例如输入测试。
那么要建立一个单独的配置文件，你可以直接在程序中使用如下这些命令来实现::

    from kivy.config import Config

    Config.read(<file>)
    # set config
    Config.write()

当只有一个本地配置文件 ``.ini`` 是不够的，例如，当你想要给 `garden` 提供一个
单独环境来记录 kivy 日志和其它事物，你会需要改变 ``KIVY_HOME`` 环境变量，那
就要在程序中来获得需要的结果::

    import os
    os.environ['KIVY_HOME'] = <folder>

或者在应用每次运行之前在终端里手动改变这个环境变量值：

#. Windows::

    set KIVY_HOME=<folder>

#. Linux & OSX::

    export KIVY_HOME=<folder>

改变 ``KIVY_HOME`` 环境变量值后，所指向的文件夹与上面提到过的
默认 ``.kivy/`` 目录在行为上是一样的。

理解配置令牌
---------------------------

所有配置令牌都解释在 :mod:`kivy.config` 模块中。
