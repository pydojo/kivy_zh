建立 OS X 打包程序
==========================

.. note::

    本指导描述了许多方法来为 OS X 操作系统打包 Kivy 程序。
    使用 `PyInstaller` 打包是通用中建议使用的解决方案。

.. _osx_pyinstaller:

使用 PyInstaller 和 Homebrew
------------------------------
.. note::
    在最老旧的 OS X 系统版本上打包你需要一些支持。

完整指导
~~~~~~~~~~~~~~
#. 安装 `Homebrew <http://brew.sh>`_
#. 安装 Python::

    $ brew install python

   .. note::
     要使用 Python 3 版本， ``brew install python3`` 后在下面的指导内容中
     要用 ``pip3`` 来代替 ``pip`` 命令。

#. 使用 ``--build-bottle`` 来安装或重新安装你的依赖包，
   确保依赖包可以用在其它机器上::

    $ brew reinstall --build-bottle sdl2 sdl2_image sdl2_ttf sdl2_mixer

   .. note::
       如果你的项目根据 GStreamer 或其它额外的库，也要使用
        ``--build-bottle`` 来安装或重新安装，与
       `below <additional libraries_>`_ 描述的一样。

#. 安装 Cython 和 Kivy：

    .. parsed-literal::

        $ pip install |cython_install|
        $ pip install -U kivy

#. 安装 PyInstaller::

    $ pip install -U pyinstaller

#. 使用指向 ``main.py`` 的路径来打包你的应用::

    $ pyinstaller -y --clean --windowed --name touchtracer \
      --exclude-module _tkinter \
      --exclude-module Tkinter \
      --exclude-module enchant \
      --exclude-module twisted \
      /usr/local/share/kivy-examples/demo/touchtracer/main.py

   .. note::
     这不会复制额外的图片或音频文件。你需要在 ``.spec`` 描述文件中来实现。


编辑描述文件
~~~~~~~~~~~~~~~~~~~~~
描述文件名叫做 `touchtracer.spec` 并且在执行 `pyinstaller` 命令时
所写的目录中可以找到。

你需要改变 `COLLECT()` 语句部分增加 touchtracer 的数据文件
（`touchtracer.kv`, `particle.png`, 等等）。还要增加一个
 `Tree()` 树结构对象。这个树结构对象会搜索并发现 `touchtracer`
 目录里的每个文件，增加到你的最终程序包里。你的 `COLLECT` 语句部分
应该写成如下一样的代码::


    coll = COLLECT(exe, Tree('/usr/local/share/kivy-examples/demo/touchtracer/'),
                   a.binaries,
                   a.zipfiles,
                   a.datas,
                   strip=None,
                   upx=True,
                   name='touchtracer')

这会增加所需要的钩子，所以 PyInstaller 能得到需要的 Kivy 文件。
我们完成这部分工作后，你的描述文件就准备好了，下一步就是执行描述文件。

建立描述文件和创建一个 DMG 程序
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. 打开一个终端。
#. 进入描述文件所在的目录，执行如下命令::

    $ pyinstaller -y --clean --windowed touchtracer.spec

#. 然后运行如下命令::

    $ pushd dist
    $ hdiutil create ./Touchtracer.dmg -srcfolder touchtracer.app -ov
    $ popd

#. 在 `dist` 目录中此时会有一个 `Touchtracer.dmg` 程序了。


额外的库
~~~~~~~~~~~~~~~~~~~~
GStreamer
^^^^^^^^^
如果你的项目有依赖库 GStreamer 的话，要重新执行如下命令::

    $ brew reinstall --build-bottle gstreamer gst-plugins-{base,good,bad,ugly}

.. note::
    如果你的项目需要 Ogg Vorbis 支持，就要确保在上面命令中增加
    ``--with-libvorbis`` 可选项来执行。

如果你使用的 Python 来自 Homebrew 的话，你也需要遵循如下步骤，直到
 `this pull request <https://github.com/Homebrew/homebrew/pull/46097>`_
获得了合并功能::

    $ brew reinstall --with-python --build-bottle https://github.com/cbenhagen/homebrew/raw/patch-3/Library/Formula/gst-python.rb


使用 PyInstaller 不用 Homebrew
----------------------------------
第一次安装 Kivy 和其依赖包不使用 Homebrew 的提示内容在下面链接地址中。
http://kivy.org/docs/installation/installation.html#development-version.

一旦你完成了 kivy 和其 deps 依赖包的安装，你需要安装 PyInstaller 打包库。

我们假设使用一个 `testpackaging` 文件夹::

    cd testpackaging
    git clone http://github.com/pyinstaller/pyinstaller

在这个目录里建立一个名叫 `touchtracer.spec` 的文件，然后在文件里写如下代码::

    # -*- mode: python -*-

    block_cipher = None
    from kivy.tools.packaging.pyinstaller_hooks import get_deps_all, hookspath, runtime_hooks

    a = Analysis(['/path/to/yout/folder/containing/examples/demo/touchtracer/main.py'],
                 pathex=['/path/to/yout/folder/containing/testpackaging'],
                 binaries=None,
                 win_no_prefer_redirects=False,
                 win_private_assemblies=False,
                 cipher=block_cipher,
                 hookspath=hookspath(),
                 runtime_hooks=runtime_hooks(),
                 **get_deps_all())
    pyz = PYZ(a.pure, a.zipped_data,
                 cipher=block_cipher)
    exe = EXE(pyz,
              a.scripts,
              exclude_binaries=True,
              name='touchtracer',
              debug=False,
              strip=False,
              upx=True,
              console=False )
    coll = COLLECT(exe, Tree('../kivy/examples/demo/touchtracer/'),
                   Tree('/Library/Frameworks/SDL2_ttf.framework/Versions/A/Frameworks/FreeType.framework'),
                   a.binaries,
                   a.zipfiles,
                   a.datas,
                   strip=False,
                   upx=True,
                   name='touchtracer')
    app = BUNDLE(coll,
                 name='touchtracer.app',
                 icon=None,
             bundle_identifier=None)

把路径部分改写成你要使用的路径::

    a = Analysis(['/path/to/yout/folder/containing/examples/demo/touchtracer/main.py'],
                pathex=['/path/to/yout/folder/containing/testpackaging'],
    ...
    ...
    coll = COLLECT(exe, Tree('../kivy/examples/demo/touchtracer/'),

然后运行如下命令::

    pyinstaller/pyinstaller.py touchtracer.spec

Replace `touchtracer` with your app where appropriate.
This will give you a <yourapp>.app in the dist/ folder.


.. _osx_kivy-sdk-packager:

Using Buildozer
---------------

    pip install git+http://github.com/kivy/buildozer
    cd /to/where/I/Want/to/package
    buildozer init

.. note::
    Packaging Kivy applications with the following method must be done inside
    OS X, 32-bit platforms are no longer supported.

Edit the buildozer.spec and add the details for your app.
Dependencies can be added to the `requirements=` section.

By default the kivy version specified in the requirements is ignored.

If you have a Kivy.app at /Applications/Kivy.app then that is used,
for packaging. Otherwise the latest build from kivy.org using Kivy
master will be downloaded and used.

If you want to package for python 3.x.x simply download the package
named Kivy3.7z from the download section of kivy.org and extract it
to Kivy.app in /Applications, then run::

    buildozer osx debug

Once the app is packaged, you might want to remove unneeded
packages like gstreamer, if you don't need video support.
Same logic applies for other things you do not use, just reduce
the package to its minimal state that is needed for the app to run.

As an example we are including the showcase example packaged using
this method for both Python 2 (9.xMB) and 3 (15.xMB), you can find the
packages here:
https://drive.google.com/drive/folders/0B1WO07-OL50_alFzSXJUajBFdnc .

That's it. Enjoy!

Buildozer right now uses the Kivy SDK to package your app.
If you want to control more details about your app than buildozer
currently offers then you can use the SDK directly, as detailed in the
section below.

Using the Kivy SDK
------------------

.. note::
    Kivy.app is not available for download at the moment. For details,
    see `this <https://github.com/kivy/kivy/issues/5211>`_ issue.

.. note::
    Packaging Kivy applications with the following method must be done inside
    OS X, 32-bit platforms are no longer supported.

Since version 1.9.0, Kivy is released for the OS X platform in a
self-contained, portable distribution.

Apps can be packaged and distributed with the Kivy SDK using the method
described below, making it easier to include frameworks like SDL2 and
GStreamer.

1. Make sure you have the unmodified Kivy SDK (Kivy.app) from the download page.

2. Run the following commands::

    > mkdir packaging
    > cd packaging
    packaging> git clone https://github.com/kivy/kivy-sdk-packager
    packaging> cd kivy-sdk-packager/osx
    osx> cp -a /Applications/Kivy.app ./Kivy.App

  .. note::
    This step above is important, you have to make sure to preserve the paths
    and permissions. A command like ``cp -rf`` will copy but make the app
    unusable and lead to error later on.

3. Now all you need to do is to include your compiled app in the Kivy.app
   by running the following command::

    osx> ./package-app.sh /path/to/your/<app_folder_name>/

  Where <app_folder_name> is the name of your app.

  This copies Kivy.app to `<app_folder_name>.app` and includes a compiled copy
  of your app into this package.

4. That's it, your self-contained package is ready to be deployed!
   You can now further customize your app as described bellow.

Installing modules
~~~~~~~~~~~~~~~~~~

Kivy package on osx uses its own virtual env that is activated when you run
your app using `kivy` command.
To install any module you need to install the module like so::

    $ kivy -m pip install <modulename>

Where are the modules/files installed?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Inside the portable venv within the app at::

    Kivy.app/Contents/Resources/venv/

If you install a module that installs a binary for example like kivy-garden
That binary will be only available from the venv above, as in after you do::

    kivy -m pip install kivy-garden

The garden lib will be only available when you activate this env.

    source /Applications/Kivy.app/Contents/Resources/venv/bin/activate
    garden install mapview
    deactivate

To install binary files
~~~~~~~~~~~~~~~~~~~~~~~

Just copy the binary to the Kivy.app/Contents/Resources/venv/bin/ directory.

To include other frameworks
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Kivy.app comes with SDL2 and Gstreamer frameworks provided.
To include frameworks other than the ones provided do the following::

    git clone http://github.com/tito/osxrelocator
    export PYTHONPATH=~/path/to/osxrelocator
    cd Kivy.app
    python -m osxrelocator -r . /Library/Frameworks/<Framework_name>.framework/ \
    @executable_path/../Frameworks/<Framework_name>.framework/

Do not forget to replace <Framework_name> with your framework.
This tool `osxrelocator` essentially changes the path for the
libs in the framework such that they are relative to the executable
within the .app, making the Framework portable with the .app.


Shrinking the app size
^^^^^^^^^^^^^^^^^^^^^^
The app has a considerable size right now, however the unneeded parts can be
removed from the package.

For example if you don't use GStreamer, simply remove it from
YourApp.app/Contents/Frameworks.
Similarly you can remove the examples folder from
/Applications/Kivy.app/Contents/Resources/kivy/examples/ or kivy/tools,
kivy/docs etc.

This way the package can be made to only include the parts that are needed for
your app.

Adjust settings
^^^^^^^^^^^^^^^
Icons and other settings of your app can be changed by editing
YourApp/Contents/info.plist to suit your needs.

Create a DMG
^^^^^^^^^^^^
To make a DMG of your app use the following command::

    osx> ./create-osx-dmg.sh YourApp.app

Note the lack of `/` at the end.
This should give you a compressed dmg that will further shrink the size of your
distributed app.
