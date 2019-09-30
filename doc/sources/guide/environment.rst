.. _environment:

控制环境变量
===========================

在系统中有许多环境变量是可以使用的，
环境变量都可以用来控制 Kivy 的初始化过程和行为。

例如，要想限制文字渲染到 PIL 中实现图像效果，
先要在系统终端里设置环境变量::

    $ KIVY_TEXT=pil python main.py

环境变量都要在导入 kivy 之前进行设置，
然后在程序中先引用环境变量再写导入kivy的代码::

    import os
    os.environ['KIVY_TEXT'] = 'pil'
    import kivy

路径控制的环境变量
------------

.. versionadded:: 1.0.7

你可以控制含有配置文件、模块和 kivy 数据所在的默认目录。

KIVY_DATA_DIR
    是 Kivy 数据的路径环境变量，默认值是 `<kivy path>/data`

KIVY_MODULES_DIR
    是 Kivy 模块的路径环境变量，默认值是 `<kivy path>/modules`

KIVY_HOME
    是 Kivy 主目录的路径环境变量，这个目录是提供给本地配置用的，
    并且必须具有可写权限。

    默认值是：
     - 桌面应用: `<user home>/.kivy`
     - 安卓应用: `<android app path>/.kivy`
     - 苹果应用: `<user home>/Documents/.kivy`

    .. versionadded:: 1.9.0

KIVY_SDL2_PATH
    如果设置这个环境变量的话，来自这个路径的 SDL2 库和头部文件都会被使用，
    在编译 kivy 是要用到，这样就不会使用安装在系统中的内容。
    当运行一个 kivy 应用时要使用相同的库，这个路径必须加入到 PATH 环境变量
    的开头。

    .. versionadded:: 1.9.0

    .. warning::

        要编译 Kivy 必须要有这个路径。要执行 Kivy 程序不需要这个路径。


配置的环境变量
-------------

KIVY_USE_DEFAULTCONFIG
    如果在环境变量中有这个名字的话， Kivy 不会读取用户配置的文件。

KIVY_NO_CONFIG
    如果设置这个环境变量的话，不会读取配置文件，也不会写配置文件。
    这个环境变量也会作用在用户配置的目录上。

KIVY_NO_FILELOG
    如果设置这个环境变量，日志不会输出到文件中。

KIVY_NO_CONSOLELOG
    如果设置这个环境变量，日志不会输出到终端里。

KIVY_NO_ARGS
    如果设置这个环境变量，不会对命令行中的参数进行语法分析，
    也不会被 Kivy 使用。例如，你可以安全地建立一个脚本或
    一个含有你自己参数的应用，而不需要用 `--` 来区分参数::

        import os
        os.environ["KIVY_NO_ARGS"] = "1"
        import kivy

    .. versionadded:: 1.9.0

KCFG_section_key
    如果发现这种格式的环境变量名的话，它会映射给 Config 对象。
    当导入 `kivy` 时只会加载一次。
    使用 `KIVY_NO_ENV_CONFIG` 可以禁用这种行为。

    ::

        import os
        os.environ["KCFG_KIVY_LOG_LEVEL"] = "warning"
        import kivy
        # during import it will map it to:
        # Config.set("kivy", "log_level", "warning")

    .. versionadded:: 1.11.0

KIVY_NO_ENV_CONFIG
    如果设置这个环境变量，不会把环境变量名映射给配置对象。
    如果不设置的话，
    任何一个 `KCFG_section_key=value` 键值对儿都会映射给 Config 对象。

    .. versionadded:: 1.11.0

把 kivy 核心限制成具体实现方式的环境变量
----------------------------------------

对于你所使用的操作系统来说 :mod:`kivy.core` 模块会尝试选择最好的可用实现方式。
对于测试或自定义安装来说，你也许想要把选择器设置成一个具体的实现方式。

KIVY_WINDOW
    建立窗口的实现方式

    环境变量值有： sdl2, pygame, x11, egl_rpi

KIVY_TEXT
    渲染文本的实现方式

    环境变量值有： sdl2, pil, pygame, sdlttf

KIVY_VIDEO
    渲染视频的实现方式

    环境变量值有： gstplayer, ffpyplayer, ffmpeg, null

KIVY_AUDIO
    播放音频的实现方式

    环境变量值有： sdl2, gstplayer, ffpyplayer, pygame, avplayer

KIVY_IMAGE
    读取图片的实现方式

    环境变量值有： sdl2, pil, pygame, imageio, tex, dds, gif

KIVY_CAMERA
    读取摄像头的实现方式

    环境变量值有： avfoundation, android, opencv

KIVY_SPELLING
    魔法效果的实现方式

    环境变量值有： enchant, osxappkit

KIVY_CLIPBOARD
    剪贴板管理的实现方式

    环境变量值有： sdl2, pygame, dummy, android

度量衡的环境变量
-------

KIVY_DPI
    如果设置这个环境变量，变量值会提供给 :attr:`Metrics.dpi` 属性使用。

    .. versionadded:: 1.4.0

KIVY_METRICS_DENSITY
    如果设置这个环境变量，变量值会提供给 :attr:`Metrics.density` 属性使用。

    .. versionadded:: 1.5.0

KIVY_METRICS_FONTSCALE

    如果设置这个环境变量，变量值会提供给 :attr:`Metrics.fontscale` 属性使用。

    .. versionadded:: 1.5.0

显卡的环境变量
--------

KIVY_GL_BACKEND
    后端使用 OpenGL 显卡驱动。阅读 :mod:`~kivy.graphics.cgl` 文档。

KIVY_GL_DEBUG
    是否对 OpenGL 调用做日志记录。阅读 :mod:`~kivy.graphics.cgl` 文档。

KIVY_GRAPHICS
    是否使用 OpenGL ES2 驱动。阅读 :mod:`~kivy.graphics.cgl` 文档。

KIVY_GLES_LIMITS
    是否限制强制使用 GLES2 驱动（默认开启，或设置成 1）。
    如果设置成禁用的话， Kivy 无法实现兼容 GLES2 驱动。

    如果设置成开启的话，如下是一份潜在不兼容的清单。

==============	====================================================
Mesh indices	If true, the number of indices in a mesh is limited
                to 65535
Texture blit    When blitting to a texture, the data (color and
                buffer) format must be the same format as the one
                used at the texture creation. On desktop, the
                conversion of different color is correctly handled
                by the driver, while on Android, most of devices
                fail to do it.
                Ref: https://github.com/kivy/kivy/issues/1600
==============	====================================================

    .. versionadded:: 1.8.1

KIVY_BCM_DISPMANX_ID
    改变默认使用 Raspberry Pi 驱动的环境变量。可用的变量值是来自
     `vc_dispmanx_types.h` 文件。默认值是 0：

    - 0: DISPMANX_ID_MAIN_LCD
    - 1: DISPMANX_ID_AUX_LCD
    - 2: DISPMANX_ID_HDMI
    - 3: DISPMANX_ID_SDTV
    - 4: DISPMANX_ID_FORCE_LCD
    - 5: DISPMANX_ID_FORCE_TV
    - 6: DISPMANX_ID_FORCE_OTHER

KIVY_BCM_DISPMANX_LAYER
    改变默认使用 Raspberry Pi dispmanx layer 驱动的环境变量。默认值是 0。

    .. versionadded:: 1.10.1

事件循环的环境变量
----------

KIVY_EVENTLOOP
    当应用采用异步机制运行时，必须要用 async 标准库。
    阅读 :mod:`kivy.app` 模块了解实例用法。

    ``'asyncio'``: 异步模式运行应用时要使用 Python 的 asyncio 异步标准库。
        默认是不进行此环境变量的设置。
    ``'trio'``: 异步模式运行应用时也要使用 `trio` 库。

    .. versionadded:: 2.0.0
