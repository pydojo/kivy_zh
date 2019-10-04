.. _other_frameworks:

与其它框架集成
=================================

.. versionadded:: 1.0.8

在 Kivy 中使用 Twisted
-------------------------

.. note::
    你可以使用 `kivy.support.install_twisted_reactor` 函数来安装一个
    twisted 反应器，这样能在 kivy 事件循环中运行反应器。

    任何代入到这个函数中的多参数或多关键字参数，都会传递给线程选择的反应器插入函数。
    这些函数常常传递给 twisted 的 reactor.startRunning

.. warning::
    与默认的 twisted 反应器不一样，安装完的反应器不会处理任何信号，除非你明确地
    把 'installSignalHandlers' 关键字参数值设置成1。完成这步才允许 kivy 如
    往常一样去处理信号，否则你的意思就是让 twisted 反应器去处理信号（例如， SIGINT）。



在 kivy 示例中含有一个 twisted 服务器和客户端的小示例。
服务器应用有一个简单的 twisted 服务器运行和日志记录任何消息功能。
客户端应用是发送消息给服务器，然后输出消息和得到的响应内容。
这个例子是根据 twisted 文档中简单的 Echo 例子写的，你可以在如下地方找到：

- http://twistedmatrix.com/documents/current/_downloads/simpleserv.py
- http://twistedmatrix.com/documents/current/_downloads/simpleclient.py

要像试用一下这个例子，先运行 `echo_server_app.py` 服务器应用文件，然后启动
`echo_client_app.py` 客户端应用文件。服务器会直接用 echo 消息来回应任何客户端
发送的消息，在文本框中输入一些内容后按下回车键看看效果吧。

服务器应用
~~~~~~~~~~

.. include:: ../../../examples/frameworks/twisted/echo_server_app.py
   :literal:

客户端应用
~~~~~~~~~~

.. include:: ../../../examples/frameworks/twisted/echo_client_app.py
   :literal:

