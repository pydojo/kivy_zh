'''
从源代码生成 Kivy API 用的脚本。

代码有点乱，但有效。
如果你要改变任何代码就要小心了！

'''

ignore_list = (
    'kivy._clock',
    'kivy._event',
    'kivy.factory_registers',
    'kivy.graphics.buffer',
    'kivy.graphics.vbo',
    'kivy.graphics.vertex',
    'kivy.uix.recycleview.__init__',
    'kivy.setupconfig',
    'kivy.version'
)

import os
import sys
from glob import glob

import kivy

# 强制加载 kivy 一些模块
import kivy.app
import kivy.metrics
import kivy.atlas
import kivy.context
import kivy.core.audio
import kivy.core.camera
import kivy.core.clipboard
import kivy.core.gl
import kivy.core.image
import kivy.core.spelling
import kivy.core.text
import kivy.core.text.markup
import kivy.core.video
import kivy.core.window
import kivy.geometry
import kivy.graphics
import kivy.graphics.shader
import kivy.graphics.tesselator
import kivy.animation
import kivy.modules.console
import kivy.modules.keybinding
import kivy.modules.monitor
import kivy.modules.touchring
import kivy.modules.inspector
import kivy.modules.recorder
import kivy.modules.screen
import kivy.modules.joycursor
import kivy.storage
import kivy.storage.dictstore
import kivy.storage.jsonstore
import kivy.storage.redisstore
import kivy.network.urlrequest
import kivy.modules.webdebugger
import kivy.support
try:
    import kivy.tools.packaging.pyinstaller_hooks
except ImportError:
    pass
import kivy.input.recorder
import kivy.interactive
import kivy.garden
from kivy.factory import Factory
from kivy.lib import ddsfile, mtdev

# 检查静默建立
BE_QUIET = True
if os.environ.get('BE_QUIET') == 'False':
    BE_QUIET = False

# 强制加载来自工厂的所有类
for x in list(Factory.classes.keys())[:]:
    getattr(Factory, x)

# 目录 doc
base_dir = os.path.dirname(__file__)
dest_dir = os.path.join(base_dir, 'sources')
examples_framework_dir = os.path.join(base_dir, '..', 'examples', 'framework')

# 检查建立的空文件
base = 'autobuild.py-done'
with open(os.path.join(base_dir, base), 'w') as f:
    f.write('')


def writefile(filename, data):
    global dest_dir
    # 如果内容没有变化不会重写文件
    f = os.path.join(dest_dir, filename)
    if not BE_QUIET:
        print('write', filename)
    if os.path.exists(f):
        with open(f) as fd:
            if fd.read() == data:
                return
    h = open(f, 'w')
    h.write(data)
    h.close()


# 激活 Kivy 模块
'''
for k in kivy.kivy_modules.list().keys():
    kivy.kivy_modules.import_module(k)
'''


# 搜索所有 kivy 模块
l = [(x, sys.modules[x],
      os.path.basename(sys.modules[x].__file__).rsplit('.', 1)[0])
      for x in sys.modules if x.startswith('kivy') and sys.modules[x]]


# 从模块中提取包
packages = []
modules = {}
api_modules = []
for name, module, filename in l:
    if name in ignore_list:
        continue
    if not any([name.startswith(x) for x in ignore_list]):
        api_modules.append(name)
    if filename == '__init__':
        packages.append(name)
    else:
        if hasattr(module, '__all__'):
            modules[name] = module.__all__
        else:
            modules[name] = [x for x in dir(module) if not x.startswith('__')]

packages.sort()

# 建立索引
api_index = '''API 参考手册
-------------

本 API 参考手册是以文字形式列出所有不同的类，
方法和 Kivy 提供的特性。

.. toctree::
    :maxdepth: 1

'''
api_modules.sort()
for package in api_modules:
    api_index += "    api-%s.rst\n" % package

writefile('api-index.rst', api_index)


# 建立所有包的索引
# 注意显示继承成员关系；
#     增加 ':inherited-members:' 指令到自动模块来实现这个功能
#     但不总是希望这样做。请参阅
#         https://github.com/kivy/kivy/pull/3870

template = '\n'.join((
    '=' * 100,
    '$SUMMARY',
    '=' * 100,
    '''
$EXAMPLES_REF

.. automodule:: $PACKAGE
    :members:
    :show-inheritance:

.. toctree::

$EXAMPLES
'''))


template_examples = '''.. _example-reference%d:

示例
--------

%s
'''

template_examples_ref = ('# :ref:`Jump directly to Examples'
                         ' <example-reference%d>`')


def extract_summary_line(doc):
    """
    :param doc: 一个模块的 __doc__ 数据区域
    :return: 为只有一个标题或空字符串情况返回一个文档字符串
    """
    if doc is None:
        return ''
    for line in doc.split('\n'):
        line = line.strip()
        # 不要空行
        if len(line) < 1:
            continue
        # ref mark 参考标记
        if line.startswith('.. _'):
            continue
        return line

for package in packages:
    summary = extract_summary_line(sys.modules[package].__doc__)
    if summary is None or summary == '':
        summary = 'NO DOCUMENTATION (package %s)' % package
    t = template.replace('$SUMMARY', summary)
    t = t.replace('$PACKAGE', package)
    t = t.replace('$EXAMPLES_REF', '')
    t = t.replace('$EXAMPLES', '')

    # 搜索包
    for subpackage in packages:
        packagemodule = subpackage.rsplit('.', 1)[0]
        if packagemodule != package or len(subpackage.split('.')) <= 2:
            continue
        t += "    api-%s.rst\n" % subpackage

    # 搜索模块
    m = list(modules.keys())
    m.sort(key=lambda x: extract_summary_line(sys.modules[x].__doc__).upper())
    for module in m:
        packagemodule = module.rsplit('.', 1)[0]
        if packagemodule != package:
            continue
        t += "    api-%s.rst\n" % module

    writefile('api-%s.rst' % package, t)


# 为所有模块建立索引
m = list(modules.keys())
m.sort()
refid = 0
for module in m:
    summary = extract_summary_line(sys.modules[module].__doc__)
    if summary is None or summary == '':
        summary = 'NO DOCUMENTATION (module %s)' % package

    # 搜索示例
    example_output = []
    example_prefix = module
    if module.startswith('kivy.'):
        example_prefix = module[5:]
    example_prefix = example_prefix.replace('.', '_')

    # 尝试在框架目录中找到任何一个示例
    list_examples = glob('%s*.py' % os.path.join(
        examples_framework_dir, example_prefix))
    for x in list_examples:
        # 提取不含目录到文件名
        xb = os.path.basename(x)

        # 增加一个区域
        example_output.append('File :download:`%s <%s>` ::' % (
            xb, os.path.join('..', x)))

        # 把文件放进区域中
        with open(x, 'r') as fd:
            d = fd.read().strip()
            d = '\t' + '\n\t'.join(d.split('\n'))
            example_output.append(d)

    t = template.replace('$SUMMARY', summary)
    t = t.replace('$PACKAGE', module)
    if len(example_output):
        refid += 1
        example_output = template_examples % (
                refid, '\n\n\n'.join(example_output))
        t = t.replace('$EXAMPLES_REF', template_examples_ref % refid)
        t = t.replace('$EXAMPLES', example_output)
    else:
        t = t.replace('$EXAMPLES_REF', '')
        t = t.replace('$EXAMPLES', '')
    writefile('api-%s.rst' % module, t)


# 自动生成结束
print('Auto-generation finished')
