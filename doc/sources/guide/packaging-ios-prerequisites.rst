.. _packaging_ios_prerequisites:

打包成 IOS 应用的前提条件
=================

本指导是建立在如下假设基础上的：

    * XCode 5.1 or above
    * OS X 10.9 or above

你可以与不同的版本做体验。

前期准备
---------------

要像提交任何应用到 iTunes 商店，你需要一份
`iOS 开发者协议 <https://developer.apple.com/programs/ios/>`_。
对于测试来说，你可以使用一台苹果设备或用 XCode iOS 模拟器。

请注意要在苹果设备上做测试，你需要注册这台设备后安装你的 "供应侧写" 到设备上。
请参考苹果的
`前期准备 <https://developer.apple.com/programs/ios/gettingstarted/>`_
指导文档了解更多信息。

Homebrew
--------

我们使用 `Homebrew <http://brew.sh/>`_ 程序包管理器来为 OSX 系统安装一些
依赖库和工具，这些都是 Kivy 要用到的内容。`Homebrew` 是真正有帮助的工具，
并且是一项开源项目，服务在 `Github <https://github.com/Homebrew/homebrew>`_ 上。

由于包管理的实质（因操作系统与版本的混乱），管理过程会有已经证实的错误，
并且在建造过程导致失败。典型来说会出现这样的错误消息：
**Missing requirement: <pkg> is not installed!**

第一件要做的事就是确保你已经运行了下面的命令：

.. parsed-literal::

    brew install autoconf automake libtool pkg-config mercurial
    brew link libtool
    brew link mercurial
    sudo easy_install pip
    sudo pip install |cython_install|

如果你依然收到建造错误的话，用一种健康模式检查你的 `Homebrew`::

    brew doctor

进一步帮助请阅读
`Homebrew 维基 <https://github.com/Homebrew/homebrew/wiki>`_ 信息。

最后，你还是感到绝望，那就是执行删除依赖包和 `Homebrew` ，重新安装最新版本
 `Homebrew` 后再安装依赖包。

    `针对 Mac OSX 系统如何卸载和删除 Homebrew
    <http://www.curvve.com/blog/guides/2013/uninstall-homebrew-mac-osx/>`_
