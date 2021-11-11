''' 建立 examples 目录中的 rst 文档。

这会使用源代码中 screenshots_dir 目录里的截图
(目前路径是 doc/sources/images/examples) 而且
在 examples/ 目录中的文件都会建立成 rst 文件存放在 generation_dir 目录里
(doc/sources/examples) 例如，gallery.rst, index.rst, 和 gen__*.rst

'''


import os
import re
from os.path import sep
from os.path import join as slash  # 命名成斜杠的意思更好一点
from os.path import dirname, abspath
from kivy.logger import Logger
import textwrap

# 从当前路径移步到 kivy 所在位置
base_dir = dirname(dirname(abspath(__file__)))
examples_dir = slash(base_dir, 'examples')
screenshots_dir = slash(base_dir, 'doc/sources/images/examples')
generation_dir = slash(base_dir, 'doc/sources/examples')

image_dir = "../images/examples/"  # relative to generation_dir
gallery_filename = slash(generation_dir, 'gallery.rst')


# Info 信息是一个字典，直接从文件名信息中建立到，
# 更多信息从读取文档字符串中建立，
# 以及更多信息从语义分析描述文字中建立。常常显示到错误消息都是
# 通过设置字典键 'error' 对应到值作为错误消息内容。
#
# 对于一个类来说不是非常符合需求，
# 但在这个模块里就是一个词汇。

def iter_filename_info(dir_name):
    """
    产生每个匹配截图的信息 (字典) ，通过遍历目录
     dir_name 找到的截图。一张匹配的截图使用2个下划线
    来分隔区域，例如， path__to__filename__py.png 就是
    examples/path/to/filename.py 的一张截图。

    没有用 .png 结尾的文件名都会被忽略，其它类型的图片格式经过语义分析后
    抛出一个错误。

    如果没有 'error' 错误的话，信息区域是 'dunder', 'dir', 'file', 'ext', 'source'
    """
    pattern = re.compile(r'^((.+)__(.+)__([^-]+))\.png')
    for t in os.walk(dir_name):
        for filename in t[2]:
            if filename.endswith('.png'):
                m = pattern.match(filename)
                if m is None:
                    yield {'error': 'png filename not following screenshot'
                                    ' pattern: {}'.format(filename)}
                else:
                    d = m.group(2).replace('__', sep)
                    yield {'dunder': m.group(1),
                           'dir': d,
                           'file': m.group(3),
                           'ext': m.group(4),
                           'source': slash(d, m.group(3) + '.' + m.group(4))
                           }


def parse_docstring_info(text):
    ''' 对文档字符串内容进行语义分析 (正常的字符串中含有 '\n' 换行符) 后返回一个信息字典。
    一个文档字符串应该用三引号对儿来建立，要有一个标题，后面跟着一个换行符，然后至少要有一句话。

    如果没有 'error' 的话，信息区域有 'docstring', 'title', 和 'first_sentence'
    'first_sentence' 是没有换行符的单行内容。
    '''
    q = '\"\"\"|\'\'\''
    p = r'({})\s+([^\n]+)\s+\=+\s+(.*?)(\1)'.format(q)
    m = re.search(p, text, re.S)
    if m:
        comment = m.group(3).replace('\n', ' ')
        first_sentence = comment[:comment.find('.') + 1]
        return {'docstring': m.group(0), 'title': m.group(2),
                'description': m.group(3), 'first_sentence': first_sentence}
    else:
        return {'error': 'Did not find docstring with title at top of file.'}


def iter_docstring_info(dir_name):
    ''' 迭代目录中的截图，从文件名生成信息，并且初始化文档字符串语义分析。
     错误都会被记录下来，但会跳过含有错误的文件。
    '''
    for file_info in iter_filename_info(dir_name):
        if 'error' in file_info:
            Logger.error(file_info['error'])
            continue
        source = slash(examples_dir, file_info['dir'],
                       file_info['file'] + '.' + file_info['ext'])
        if not os.path.exists(source):
            Logger.error('Screen shot references source code that does '
                         'not exist:  %s', source)
            continue
        with open(source) as f:
            text = f.read()
            docstring_info = parse_docstring_info(text)
            if 'error' in docstring_info:
                Logger.error(docstring_info['error'] + '  File: ' + source)
                continue  # don't want to show ugly entries
            else:
                file_info.update(docstring_info)
        yield file_info


def enhance_info_description(info, line_length=79):
    ''' 使用 info['description'] 字典键值操作，增加信息区域。

    info['files'] 就是源文件和描述中所指的任何一个文件名，例如，
     'the file xxx.py' 或 'The image this.png' 。
    与描述中所写的内容一样，不允许使用 ../dir 符号，
    以及源文件目录的相对路径。

    info['enhanced_description'] 是描述成段落组成的阵列，
    其中每段都是有许多行组成的，并按照 line_length 行宽度打包内容。
    这种增强的描述信息包含了 info['files'] 中文件的 rst 链接。
    '''

    # 建立许多行形成的文集，每段内容是一个文集。
    paragraphs = info['description'].split('\n\n')
    lines = [
        paragraph.replace('\n', '$newline$')
        for paragraph in paragraphs
    ]
    text = '\n'.join(lines)

    info['files'] = [info['file'] + '.' + info['ext']]
    regex = r'[tT]he (?:file|image) ([\w\/]+\.\w+)'
    for name in re.findall(regex, text):
        if name not in info['files']:
            info['files'].append(name)

    # 增加参考文件链接
    folder = '_'.join(info['source'].split(sep)[:-1]) + '_'
    text = re.sub(r'([tT]he (?:file|image) )([\w\/]+\.\w+)',
                  r'\1:ref:`\2 <$folder$\2>`', text)
    text = text.replace('$folder$', folder)

    # 此时把文本分解成由段落组成的阵列，每个阵列是有许多行组成的。
    lines = [line.replace('$newline$', '\n') for line in text.split('\n')]
    paragraphs = [
        textwrap.wrap(line, line_length)
        # 如果 rst 文件中有 .. note:: 这样类似的块内容就不做打包处理
        if not line.startswith(' ') else [line]
        for line in lines
    ]
    info['enhanced_description'] = paragraphs


def get_infos(dir_name):
    ''' 返回许多信息内容，
    目录中每张匹配的截图都是一个阵列信息字典，
    按照源文件名进行排序，而且在这个阵列字典中增加 'num' 数据区域
    作为唯一的序号。

    '''
    infos = [i for i in iter_docstring_info(dir_name)]
    infos.sort(key=lambda x: x['source'])
    for num, info in enumerate(infos):
        info['num'] = num
        enhance_info_description(info)
    return infos


def make_gallery_page(infos):
    ''' 返回画廊页面的 rst (Restructured Text) 文件字符串内容，
    显示所有找到的截图信息。
    '''

    def a(s=''):
        ''' 对 s 格式化后加入到输出结果中，会以追加方式增加内容 '''
        output.append(s.format(**info))

    def t(left='', right=''):
        ''' 把左边格式化字符串和右边格式化字符串追加到一张表的行上 '''
        l = left.format(**info)
        r = right.format(**info)
        if len(l) > width1 or len(r) > width2:
            Logger.error('items to wide for generated table: "%s" and "%s"',
                         l, r)
            return
        output.append('| {0:{w1}} | {1:{w2}} |'
                      .format(l, r, w1=width1, w2=width2))

    gallery_top = '''
画廊
-------

.. _Tutorials:  ../tutorials-index.html

.. container:: title

    这个画廊是让你查看使用 Kivy 的许多示例用的。
    点击任何一张截图来查看代码。

本画廊含有:

    * 来自 examples/ 目录的示例，都是展示不同库所拥有的具体能力
      以及展示 Kivy 的那些特性用的。
    * 示范 examples/demos/ 目录中的内容，可以看到许多 Kivy 的能力。

在其它地方还有更多的 Kivy 程序:

    * Tutorials_ 教程会带你走遍完整的 Kivy 应用程序开发过程。
    * 在源代码中找到的单元测试位于 kivy/tests/ 子目录中，
      这也是对你有用的。

我们希望你的学习 Kivy 旅程是激动且有趣的一件事！

'''
    output = [gallery_top]

    for info in infos:
        a("\n.. |link{num}|  replace:: :doc:`{source}<gen__{dunder}>`")
        a("\n.. |pic{num}| image:: ../images/examples/{dunder}.png"
          "\n    :width:  216pt"
          "\n    :align:  middle"
          "\n    :target: gen__{dunder}.html")
        a("\n.. |title{num}|  replace:: **{title}**")

    # 写表格
    width1, width2 = 20, 50  # 不包含2个结束位空格
    head = '+-' + '-' * width1 + '-+-' + '-' * width2 + '-+'
    a()
    a(head)

    for info in infos:
        t('| |pic{num}|', '| |title{num}|')
        t('| |link{num}|', '')
        paragraphs = info['description'].split("\n\n")
        for p in paragraphs:
            for line in textwrap.wrap(p, width2):
                t('', line)
            t()  # 段落之间的空行
        t()
        a(head)
    return "\n".join(output) + "\n"


def make_detail_page(info):
    ''' 返回信息中文件详细页面的 rst 文本字符串。 '''

    def a(s=''):
        ''' 以追加方式把格式化过的 s 内容增加到输出结果里 '''
        output.append(s.format(**info))

    output = []
    a('{title}')
    a('=' * len(info['title']))
    a('\n.. |pic{num}| image:: /images/examples/{dunder}.png'
      '\n   :width: 50%'
      '\n   :align: middle')
    a('\n|pic{num}|')
    a()
    for paragraph in info['enhanced_description']:
        for line in paragraph:
            a(line)
        a()

    # 包括图片
    last_lang = '.py'
    for fname in info['files']:
        full_name = slash(info['dir'], fname)
        ext = re.search(r'\.\w+$', fname).group(0)
        a('\n.. _`' + full_name.replace(sep, '_') + '`:')
        # 如果在 Windows 操作系统上建立的话 (sphinx 跳过反斜杠) ，使用2个分隔符
        if '\\' in full_name:
            full_name = full_name.replace(sep, sep*2)

        if ext in ['.png', '.jpg', '.jpeg']:
            title = 'Image **' + full_name + '**'
            a('\n' + title)
            a('~' * len(title))
            a('\n.. image:: ../../../examples/' + full_name)
            a('    :align:  center')
        else:  # code
            title = 'File **' + full_name + '**'
            a('\n' + title)
            a('~' * len(title))
            if ext != last_lang and ext != '.txt':
                a('\n.. highlight:: ' + ext[1:])
                a('    :linenothreshold: 3')
                last_lang = ext
            # 防止使用 'none' 时出现高亮错误
            elif ext == '.txt':
                a('\n.. highlight:: none')
                a('    :linenothreshold: 3')
                last_lang = ext
            a('\n.. include:: ../../../examples/' + full_name)
            a('    :code:')
    return '\n'.join(output) + '\n'


def write_file(name, s):
    ''' 把字符串写到文件里 '''
    with open(name, 'w') as f:
        f.write(s)


def make_index(infos):
    ''' 返回画廊 index.rst 文件的 rst 字符串内容。 '''
    start_string = '''
画廊示例
===================

.. toctree::
    :maxdepth: 1

    gallery'''
    output = [start_string]
    for info in infos:
        output.append('    gen__{}'.format(info['dunder']))
    return '\n'.join(output) + '\n'


def write_all_rst_pages():
    ''' 负责写画廊，细节和索引 rst 页面这项主要任务。 '''
    infos = get_infos(screenshots_dir)
    s = make_gallery_page(infos)
    write_file(gallery_filename, s)

    for info in infos:
        s = make_detail_page(info)
        detail_name = slash(generation_dir,
                            'gen__{}.rst'.format(info['dunder']))
        write_file(detail_name, s)

    s = make_index(infos)
    index_name = slash(generation_dir, 'index.rst')
    write_file(index_name, s)
    Logger.info('gallery.py: Created gallery rst documentation pages.')


if __name__ == '__main__':
    write_all_rst_pages()
