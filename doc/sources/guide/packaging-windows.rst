建立一个 Windows 程序包
============================

.. note::

    本文档只对 kivy ``1.9.1`` 以上的版本有效。

为 Windows 系统打包你的应用只能在 Windows 操作系统上来操作。
下面的过程已经在 Windows 系统上使用 Kivy **wheels** 安装测试过了，
对于另外一种安装阅读结尾部分内容。

打包程序会分32位或64位，这要根据你运行的 Python 版本来决定。

.. _packaging-windows-requirements:

前提条件
------------

    * 最新的 Kivy （安装描述在 :ref:`installation_windows` 文档中）。
    * 安装 PyInstaller 3.1以上的版本 (``pip install --upgrade pyinstaller``)

.. _Create-the-spec-file:

PyInstaller 的默认钩子
========================

这部分内容对 PyInstaller (>= 3.1) 有效，包括了 kivy 钩子。
要覆写默认的钩子，下面的例子需要稍微做些修改。阅读 :ref:`overwrite-win-hook` 文档了解。

打包一个简单的应用
----------------------

对于这个例子来说，我们会打包 **touchtracer** 示例项目和嵌入一个自定义图标。
kivy 示例的位置是，当使用轮子时，安装在 ``python\\share\\kivy-examples`` ，
并且当使用 github 源代码时会安装在 ``kivy\\examples`` 位置上。我们只要指向
完整路径到示例 ``examples-path`` 位置。那么 touchtracer 示例就是在
``examples-path\\demo\\touchtracer`` 位置上，并且主文件名叫 ``main.py`` 。

#. 打开你的命令行窗口后确保 python 在环境变量 PATH 中（例如在命令行里
   直接输入 ``python`` 回车就可以有效）。
#. 建立一个文件夹用来打包应用。例如，建立一个 ``TouchApp`` 文件夹后 `进入这个目录
   <http://www.computerhope.com/cdhlp.htm>`_ 使用 ``cd TouchApp`` 命令。
   然后输入如下命令::

    > pyinstaller --name touchtracer examples-path\demo\touchtracer\main.py

   你也可以增加一个 `icon.ico` 图标文件到应用文件夹中，这样可以建立一个程序图标。
   如果你没有 `.ico` 文件，你可以把 `icon.png` 转换成图标文件，使用这个网络应用
   `ConvertICO <http://www.convertico.com>`_ 就可以。保存 `icon.ico` 到
   `touchtracer` 目录中后在命令行里输入::

    > pyinstaller --name touchtracer --icon examples-path\demo\touchtracer\icon.ico examples-path\demo\touchtracer\main.py

   对于更多的打包选项可以参考
   `PyInstaller Manual <http://pythonhosted.org/PyInstaller/>`_

#. 建立好打包程序后会在 ``TouchApp`` 目录中有一个 ``touchtracer.spec`` 文件，
   需要编辑这个描述文件来增加依赖包钩子才能正确地建立 `exe` 文件。用你喜欢的文本编辑器
   打开这个描述文件后，在文件起始行增加如下语句（本示例程序默认假设使用 sdl2）::

    from kivy_deps import sdl2, glew

   然后找到 ``COLLECT()`` 语句部分，给 touchtracer 增加要使用的数据，例如
   (`touchtracer.kv`, `particle.png`, 等等)：增加一个 ``Tree()`` 对象。
   就是 ``Tree('examples-path\\demo\\touchtracer\\')`` 这句话。这是一个
   树结构，用来搜索发现 touchtracer 目录中的每个文件并加入到最终的程序包里。

   要增加依赖包，要写在第一个关键字参数之前，为依赖包的每条路径增加一个树结构对象。
   例如， ``*[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)]`` 这句话，
   那么最后 ``COLLECT()`` 语句部分看起来像下面一样::

    coll = COLLECT(exe, Tree('examples-path\\demo\\touchtracer\\'),
                   a.binaries,
                   a.zipfiles,
                   a.datas,
                   *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
                   strip=False,
                   upx=True,
                   name='touchtracer')

#. 此时我们在命令行中根据 ``TouchApp`` 目录里的描述文件来建立可执行程序，输入::

    > pyinstaller touchtracer.spec

#. 编译完的程序包会放在 `TouchApp\\dist\\touchtracer` 目录中。

使用 gstreamer 打包含视频功能的应用
------------------------------------

下面的指导内容与上面的例子稍有不同，我们要为含有视频功能的应用使用 gstreamer 来打包程序。
我们会使用 ``videoplayer`` 示例，位置在 ``examples-path\widgets\videoplayer.py``。
建立一个名叫 ``VideoPlayer`` 的文件夹后在命令行中进入到这个目录里，再输入如下命令::

    > pyinstaller --name gstvideo examples-path\widgets\videoplayer.py

打开 ``gstvideo.spec`` 文件后这次导入语句部分包含了 `gstreamer` 依赖包::

    from kivy_deps import sdl2, glew, gstreamer

然后这次增加 ``Tree()`` 时包含了视频文件。 ``Tree('examples-path\\widgets')`` 语句
也要增加 `gstreamer` 依赖包部分，最后看起来像下面一样::

    coll = COLLECT(exe, Tree('examples-path\\widgets'),
                   a.binaries,
                   a.zipfiles,
                   a.datas,
                   *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins + gstreamer.dep_bins)],
                   strip=False,
                   upx=True,
                   name='gstvideo')

然后根据 ``VideoPlayer`` 目录中的描述文件建立打包程序，在命令中输入::

    > pyinstaller gstvideo.spec

完成后在 ``VideoPlayer\dist\gstvideo`` 目录里会找到 ` gstvideo.exe` 可执行程序，
当你双击这个程序时就会播放一段视频了。

.. note::

    如果你使用了 Pygame 并且需要打包 PyGame 到你的应用中，你要增加如下代码到你的描述文件中，
    由于 kivy 的 #1638 问题在导入语句下面增加如下代码::

        def getResource(identifier, *args, **kwargs):
            if identifier == 'pygame_icon.tiff':
                raise IOError()
            return _original_getResource(identifier, *args, **kwargs)

        import pygame.pkgdata
        _original_getResource = pygame.pkgdata.getResource
        pygame.pkgdata.getResource = getResource

.. _overwrite-win-hook:

覆写默认的钩子
============================

包含视频音频/不包含视频音频，以及为应用程序瘦身
---------------------------------------------------------

PyInstaller 为 kivy 提供了一个钩子，默认增加 **所有** kivy 使用的核心模块，
例如， audio, video, spelling 等等（你仍然需要手动打包 gstreamer 的 dll
 文件，使用的就是 ``Tree()`` 树结构对象 - 上面的例子已经见过了）以及其它依赖包。
如果这个狗子没有安装的话，或要瘦身应用不包含那些没使用的模块，例如不使用 audio/video
 模块，那就要含有另一项钩子来实现。

Kivy 提供了另一个钩子位置在 :func:`~kivy.tools.packaging.pyinstaller_hooks.hookspath`，
另外，如果 PyInstaller 没有默认钩子，那么
 :func:`~kivy.tools.packaging.pyinstaller_hooks.runtime_hooks` 也必须提供。
当覆写默认钩子时，后面的钩子典型来说是不用覆写的。

那么这个另一个 :func:`~kivy.tools.packaging.pyinstaller_hooks.hookspath` 钩子
不包含任何一个 kivy 供应器。要增加供应器，那就要用
:func:`~kivy.tools.packaging.pyinstaller_hooks.get_deps_minimal` 或者用
:func:`~kivy.tools.packaging.pyinstaller_hooks.get_deps_all` 来增加。
阅读钩子的文档和 :mod:`~kivy.tools.packaging.pyinstaller_hooks` 模块文档了解
更多细节。但不可缺少的是
:func:`~kivy.tools.packaging.pyinstaller_hooks.get_deps_all` 钩子增加了所有
供应器，与默认钩子类似，而
:func:`~kivy.tools.packaging.pyinstaller_hooks.get_deps_minimal` 钩子只增加
那些应用运行时被加载的供应器。每个方法提供了隐藏 kivy 导入列表，并且不包含的导入可以代入
到描述文件里的 ``Analysis`` 部分。

也可以生成一种逐项罗列的另一种钩子，每个 kivy 供应器模块和那些不需要的供应器可以注释掉。
阅读 :mod:`~kivy.tools.packaging.pyinstaller_hooks` 模块文档了解。

上面的例子中要使用这种另一个钩子，那就要做一些描述文件的修改，增加 ``hookspath()`` 
和 ``runtime_hooks`` （如果需要的话）以及 ``**get_deps_minimal()`` 或
 ``**get_deps_all()`` 来描述供应器。

例如，增加的导入语句是::

 from kivy.tools.packaging.pyinstaller_hooks import get_deps_minimal, get_deps_all, hookspath, runtime_hooks

然后修改描述文件中 ``Analysis`` 部分::

    a = Analysis(['examples-path\\demo\\touchtracer\\main.py'],
                 ...
                 hookspath=hookspath(),
                 runtime_hooks=runtime_hooks(),
                 ...
                 **get_deps_all())

要包含像默认钩子一样的东西。或者写成::

    a = Analysis(['examples-path\\demo\\touchtracer\\main.py'],
                 ...
                 hookspath=hookspath(),
                 runtime_hooks=runtime_hooks(),
                 ...
                 **get_deps_minimal(video=None, audio=None))

例如，不包含音频和视频供应器，然后对其它核心模块只使用加载的那些模块。

这里的关键点就是提供那个另一个
:func:`~kivy.tools.packaging.pyinstaller_hooks.hookspath` 钩子，
它默认不会列出所有 kivy 供应器，并且要手动对 `hiddenimports` 增加需要的
供应器，同时也就移除了不想要的供应器（例子中的音频和视频），使用的就是
:func:`~kivy.tools.packaging.pyinstaller_hooks.get_deps_minimal` 钩子。

另一种安装程序打包方法
-----------------------

前面的例子使用了树结构对象
``*[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins + gstreamer.dep_bins)],``
来让 PyInstaller 增加所有 dll 文件，这些 dll 文件都是这些依赖包要使用的文件。
如果没有安装 kivy 的话，使用轮子方法时，这些命令都是无效的，并且例如
``kivy_deps.sdl2`` 在导入时也会失败。相反，要找到这些 dll 文件所在位置是必须的，
并且手动把这些 dll 文件代入到 ``Tree`` 类中也是用一种与示例一样的类似模式。
