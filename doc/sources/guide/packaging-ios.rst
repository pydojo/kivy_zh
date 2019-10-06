.. _packaging_ios:

建立一个 IOS 包程序
========================

.. note::

    目前， kivy-iOS 使用 Python 2.7 和 3.7 来建立打包程序。

整个过程对于 IOS 来说，建立一个打包程序要用4个步骤来做出解释：

#. :ref:`Compile the distribution` 编译分发包(python + modules for IOS)
#. :ref:`Create an Xcode project` 建立一个Xcode项目(and link your source code)
#. :ref:`Update the Xcode project` 更新Xcode项目
#. :ref:`Customize` 自定义

前置条件
-------------

你需要安装一些依赖包，就像安装 Cython, autotools, 等等依赖包一样。
我们鼓励你使用 `Homebrew <http://mxcl.github.com/homebrew/>`_ 来安装如下依赖包：

.. parsed-literal::

    brew install autoconf automake libtool pkg-config
    brew link libtool
    sudo easy_install pip
    sudo pip install |cython_install|

对于更多细节，阅读 :ref:`IOS 前期准备 <packaging_ios_prerequisites>` 文档。
这样确保在第二个步骤之前每件事都没问题！

.. _Compile the distribution:

编译分发包
------------------------

打开一个终端，然后输入如下命令::

    $ git clone git://github.com/kivy/kivy-ios
    $ cd kivy-ios
    $ pip install -r requirements.txt
    $ ./toolchain.py build python3
    $ ./toolchain.py build kivy

大部分 python 分发包都打包成 `python27.zip` 形式。如果你的体验中有任何一个问题，
请访问我们的
`用户组 <https://groups.google.com/forum/#!forum/kivy-users>`_ 或者访问
`kivy-ios 项目页面 <https://github.com/kivy/kivy-ios>`_ 来沟通。

.. _Create an Xcode project:

建立一个 Xcode 项目
-----------------------

继续执行下一步之前，确保你的应用入口是一个名叫 `main.py` 的文件。

我们提供了一个脚本来建立一个初始化的 Xcode 项目已做启动准备。在如下命令行中，
用你自己的项目名字替换 `test` 部分。项目名字必须不能含有任何一个空格或非法字符::

    $ ./toolchain.py create <title> <app_directory>
    $ ./toolchain.py create Touchtracer ~/code/kivy/examples/demo/touchtracer

.. Note::
    你必须使用一个完整路径指向你的应用程序目录。

一个名叫 `<title>-ios` 的目录会被建立，其中含有一个 Xcode 项目。
你可以打开 Xcode 项目::

    $ open touchtracer-ios/touchtracer.xcodeproj

然后点击 `Play` 就可以与 IOS 应用一起玩耍了。

.. Note::

    每次你按下 `Play` 的时候，你的应用目录都会同步到 `<title>-ios/YourApp` 目录。
    不要直接在 -ios 目录中做任何变更。

.. _Update the Xcode project:

Update the Xcode project
------------------------

Let's say you want to add numpy to your project but you did not compile it
prior to creating your XCode project. First, ensure it is built::

    $ ./toolchain.py build numpy

Then, update your Xcode project::

    $ ./toolchain.py update touchtracer-ios

All the libraries / frameworks necessary to run all the compiled recipes will be
added to your Xcode project.

.. _Customize:

Customize the Xcode project
---------------------------

There are various ways to customize and configure your app. Please refer
to the `kivy-ios <http://www.github.com/kivy/kivy-ios>`_ documentation
for more information.

.. _Known issues:

Known issues
------------

All known issues with packaging for iOS are currently tracked on our
`issues <https://github.com/kivy/kivy-ios/issues>`_  page. If you encounter
an issue specific to packaging for iOS that isn't listed there, please feel
free to file a new issue, and we will get back to you on it.

While most are too technical to be written here, one important known issue is
that removing some libraries (e.g. SDL_Mixer for audio) is currently not
possible because the kivy project requires it. We will fix this and others
in future versions.

.. _ios_packaging_faq:

FAQ
---

Application quit abnormally!
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, all the print statements to the console and files are ignored. If
you have an issue when running your application, you can activate the log by
commenting out this line in `main.m`::

    putenv("KIVY_NO_CONSOLELOG=1");

Then you should see all the Kivy logging on the Xcode console.

How can Apple accept a python app ?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We managed to merge the app binary with all the libraries into a single binary,
called libpython. This means all binary modules are loaded beforehand, so
nothing is dynamically loaded.

Have you already submited a Kivy application to the App store ?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Yes, check:

- `Defletouch on iTunes <http://itunes.apple.com/us/app/deflectouch/id505729681>`_,
- `ProcessCraft on iTunes <http://itunes.apple.com/us/app/processcraft/id526377075>`_

For a more complete list, visit the
`Kivy wiki <https://github.com/kivy/kivy/wiki/List-of-Kivy-Projects>`_.
