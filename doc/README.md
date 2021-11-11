Kivy - 文档
====================

你可以访问最新的文档内容，网址是：

* http://kivy.org/docs

贡献
------------

如果你对编辑文档感兴趣，又想做出一些贡献，
请确保 kivy 源代码更新成最新内容后再开始工作。
如果你的文档过期了，可能会导致合并时出现冲突问题。

安装 Sphinx
--------------

- 使用 pip 安装：
  
  ``pip install sphinx``

- 使用 apt-get 安装：
    
  ``apt-get install python-sphinx``

- 使用 MacPorts 安装：
  
  ``port install py34-sphinx``

- 在 Windows 系统上 (或在虚拟环境下)：

  先获得 pip 程序 (https://pypi.python.org/pypi/pip). 你需要使用这个来安装依赖库。

  要想安装 pip 程序，在 pip 目录命令行中运行 ``python setup.py install`` 命令。然后运行：
    
  ``pip install sphinxcontrib-blockdiag sphinxcontrib-seqdiag``
  
  ``pip install sphinxcontrib-actdiag sphinxcontrib-nwdiag``
    
  或者使用提供的 *doc-requirements.txt* 文件用 pip 来进行安装：
    
  ``pip install -r doc-requirements.txt``
  
建立文档
--------------------------

生成文档使用 make 命令： ``make html``

生成的文档存放在 ``build/html/`` 目录里，可以直接访问。
