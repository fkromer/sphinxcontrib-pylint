# -*- coding: utf-8 -*-
"""
    sphinxcontrib.pylint
    ~~~~~~~~~~~~~~~~~~~~

    Allow pylint static analysis results to be included in Sphinx-generated
    documents inline.

    :copyright: Copyright 2016 by the contributers, see AUTHORS.
    :license: MIT.
"""

import os.path
import re
import subprocess
from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.util.compat import Directive

options = []

class message_list(nodes.General, nodes.Element):
    pass

class package_diagram(nodes.General, nodes.Element):
    pass

class class_diagram(nodes.General, nodes.Element):
    pass

class MessageListDirective(Directive):
    """
    Directive to insert the pylint message list as table.

    Syntax::

        .. message_list:: title

    """
    optional_arguments = 1
    final_argument_whitespace = True
    has_content = False
    def run(self):
        message_list_node = message_list('')
        
        if len(self.arguments) > 0:
            message_list_node['title'] = self.arguments[0]
        else:
            message_list_node['title'] = 'pylint message list'

        return [message_list_node]

class PackageDiagramDirective(Directive):
    """
    Directive to insert the pyreverse package diagram as dot inlined.

    Syntax::
    
        .. package-diagram::

    """
    def run(self):
        return [package_diagram('')]

class ClassDiagramDirective(Directive):
    """
    Directive to insert the pyreverse class diagram as dot inlined.

    Syntax::
    
        .. class-diagram:: class_name
           :ancestor_depth:
           :class_depth:
           :attribute_filtering:
           :classes_only:
           :builtins:

    """
    required_arguments = 1  # class_name
    option_spec = {'class': directives.class_option,
                   'ancestor_depth': directives.unchanged,
                   'class_depth': directives.unchanged,
                   'attribute_filtering': directives.unchanged,
                   'classes_only': directives.unchanged,
                   'builtins': directives.unchanged}
    def run(self):
        class_diagram_node = class_diagram('')
        class_diagram_node['class_name'] = self.arguments[0]
        if 'ancestor_depth' in self.options:
            class_diagram_node['ancestor_depth'] = self.options['ancestor_depth']
        else:
            class_diagram_node['ancestor_depth'] = None
        if 'class_depth' in self.options:
            class_diagram_node['class_depth'] = self.options['class_depth']
        else:
            class_diagram_node['class_depth'] = None
        if 'attribute_filtering' in self.options:
            class_diagram_node['attribute_filtering'] = self.options['attribute_filtering']
        else:
            class_diagram_node['attribute_filtering'] = None
        if 'classes_only' in self.options:
            class_diagram_node['classes_only'] = self.options['classes_only']
        else:
            class_diagram_node['classes_only'] = None
        if 'builtins' in self.options:
            class_diagram_node['builtins'] = self.options['builtins']
        else:
            class_diagram_node['builtins'] = None
        return [class_diagram_node]

class Pyreverse(object):
    def __init__(self, file_or_dir, output_format='dot', output_name=None, ancestor_depth=None, class_depth=None, module_consideration=False, filtering=None, classes_only=False, builtins=False, project=None):
        self.output_format = output_format
        self.output_name = output_name
        self.ancestor_search_depth = ancestor_depth
        self.associated_classes_depth = class_depth
        self.module_name_consideration = module_consideration
        self.attribute_filtering = filtering
        self.__attribute_filters = ['PUB_ONLY', 'SPECIAL', 'OTHER', 'ALL']
        self.show_classes_only = classes_only
        self.show_builtin_objects = builtins
        self.file_or_directory = file_or_dir
        self.project_name = project
        self.__option_list = []
        self.__command_list = []

    def _create_command(self):
        """
        >>> p = Pyreverse('test.py')
        >>> p._create_command()
        ['pyreverse', '-odot', '-mn', 'test.py']

        >>> p1 = Pyreverse('test.py', 'dot', 'test', 'ALL', 'ALL', True, "PUB_ONLY", True, True)
        >>> p1._create_command()
        ['pyreverse', '-odot', '-ctest', '-A', '-S', '-my', '-fPUB_ONLY', '-k', '-b', 'test.py']


        >>> p2 = Pyreverse('../tests/package/test.py', 'svg', 'test', 3, 2, False, 'SPECIAL', False, False, 'package')
        >>> p2._create_command()
        ['pyreverse', '-osvg', '-ctest', '-a3', '-s2', '-mn', '-fSPECIAL', '../tests/package/test.py', 'package']
        """
        if self.output_format:
            self.__option_list.append("-o"+self.output_format)
        if self.output_name:
            self.__option_list.append("-c"+self.output_name)
        if self.ancestor_search_depth == 'ALL':
            self.__option_list.append("-A")
        elif isinstance(self.ancestor_search_depth, int):
            self.__option_list.append("-a"+str(self.ancestor_search_depth))
        else:
            pass
        if self.associated_classes_depth == 'ALL':
            self.__option_list.append("-S")
        elif isinstance(self.associated_classes_depth, int):
            self.__option_list.append("-s"+str(self.associated_classes_depth))
        else:
            pass
        if self.module_name_consideration:
            self.__option_list.append("-my")
        else:
            self.__option_list.append("-mn")
        if self.attribute_filtering in self.__attribute_filters:
            self.__option_list.append("-f"+self.attribute_filtering)
        if self.show_classes_only:
            self.__option_list.append("-k")
        if self.show_builtin_objects:
            self.__option_list.append("-b")
        self.__command_list.append("pyreverse")
        for o in self.__option_list:
            self.__command_list.append(o)
        self.__command_list.append(self.file_or_directory)
        if self.project_name:
            self.__command_list.append(self.project_name)
        return self.__command_list

    def run(self):
        """
        >>> p = Pyreverse('../tests/package/test.py', 'png', 'TestClass', 'ALL', 'ALL', True, "PUB_ONLY", True, True )
        >>> p.run() 
        """
        command = self._create_command()
        console_output = subprocess.check_output(command).decode("utf-8")

def run_pylint(builder, options):
    for el in options:
        if el is None:
            builder.info('sphinxcontrib.pylint: option dicarded {}'.format(el))
            options.remove(el)
        if el is isinstance(el, bool):
            builder.info('sphinxcontrib.pylint: option dicarded {}'.format(el))
            options.remove(el)
        if el is isinstance(el, int):
            builder.info('sphinxcontrib.pylint: option dicarded {}'.format(el))
            options.remove(el)
    if builder.config.pylint_debug:
        builder.info('sphinxcontrib.pylint: {}'.format(options))

    try:
        [el for el in options if isinstance(el, str)]
    except:
        raise ValueError('unknown format: {}'.format(el))

    #print('{}'.format(os.getcwd()))
    command = 'pylint --reports=no --output-format=parseable ' + ' '.join(options) + ' ' + 'bzr.py'
    if builder.config.pylint_debug:
        builder.info('sphinxcontrib.pylint: command - {}'.format(command))
    # TODO pass the sphinx-doc source root directory as cwd to Popen
    pylint_output = subprocess.Popen(['pylint', '--reports=no', '--msg-template={path}:{line}: [{msg_id}({symbol}), {obj}] {msg}', '../bzr.py'], stdout=subprocess.PIPE)
    output = pylint_output.stdout.read().decode("utf-8")
    if builder.config.pylint_debug:
        builder.info('sphinxcontrib.pylint: output - {}'.format(output))
    
    # GitHub Gist of andialbrecht about regex to parse errors from pylint output:
    # https://gist.github.com/andialbrecht/917126
    PYLINT_ERROR_REGEX = re.compile(r"""^(?P<file>.+?):(?P<line>[0-9]+):\ # file name and line number
\[(?P<type>[a-z])(?P<errno>\d+)   # message type and error number, e.g. E0101
(,\ (?P<hint>.+))?\]\             # optional class or function name
(?P<msg>.*)                       # finally, the error message
""", re.IGNORECASE|re.VERBOSE)
    #PYLINT_ERROR_REGEX = regexp.MustCompile('^(?P<file>.+?):(?P<line>[0-9]+): \[(?P<code>[A-Z][0-9]+)\((?P<key>.*)\), \] (?P<msg>.*)')
    pylint_messages = re.match(PYLINT_ERROR_REGEX, output)
    #for m in re.finditer(PYLINT_ERROR_REGEX, output):
    #    builder.info('{}'.format(m.groups()))
    if builder.config.pylint_debug:
        builder.info('sphinxcontrib.pylint: messages - {}'.format(pylint_messages))

def get_general_options(builder):
    general_options = ['--ignore=' + builder.config.pylint_ignore, '--jobs=' + builder.config.pylint_jobs]
    return general_options

def get_message_control_options(builder):
    if builder.config.pylint_confidence not in ('HIGH', 'INFERENCE', 'INFERENCE_FAILURE', 'UNDEFINED'):
        raise ValueError('Unsupported option value: %s' % builder.config.pylint_confidence)
    message_control_options = ['--confidence=' + builder.config.pylint_confidence, '--enable=' + builder.config.pylint_enable, '--disable=' + builder.config.pylint_disable]
    return message_control_options

def on_builder_inited(self):
    """
    Reads the pylint configuration values from sphinx-doc conf.py into a module
    global data 'options'.
    """
    if self.builder.config.pylint_debug:
        self.builder.info('sphinxcontrib.pylint: execute on_builder_inited()...')
    [options.append(o) for o in get_general_options(self.builder)]
    [options.append(o) for o in get_message_control_options(self.builder)]
    if self.builder.config.pylint_debug:
        self.builder.info('sphinxcontrib.pylint:   config values {}'.format(options))

def on_doctree_resolved(self, doctree, docname):
    if self.builder.config.pylint_debug:
        self.builder.info('sphinxcontrib.pylint: execute on_doctree_resolved()...')
    
    # TODO remove the message overriding with the fake messages
    # pylints default message format: {path}:{line}: [{msg_id}({symbol}), {obj}] {msg}
    messages =  run_pylint(self.builder, options) 
    messages = [['bzr.py', '10', 'E0401', 'import-error', '', 'Unable to import \'paver.options\''], ['bzr.py', '16', 'C0111', 'missing-docstring', 'do_bzr_cmd', 'Missing function docstring']]

    # output message list into table
    for node in doctree.traverse(message_list):
        if self.builder.config.pylint_debug:
            self.builder.info('sphinxcontrib.pylint:   process message list directive...')
        table = nodes.table()
        tgroup = nodes.tgroup()
        path_colspec = nodes.colspec(colwidth=5)
        line_colspec = nodes.colspec(colwidth=5)
        msg_id_colspec = nodes.colspec(colwidth=5)
        symbol_colspec = nodes.colspec(colwidth=5)
        obj_colspec = nodes.colspec(colwidth=5)
        msg_colspec = nodes.colspec(colwidth=5)
        tgroup += [path_colspec, line_colspec, msg_id_colspec, symbol_colspec, obj_colspec, msg_colspec]
        tgroup += nodes.thead('', nodes.row(
            '',
            nodes.entry('', nodes.paragraph('', 'path')),
            nodes.entry('', nodes.paragraph('', 'line')),
            nodes.entry('', nodes.paragraph('', 'msg_id')),
            nodes.entry('', nodes.paragraph('', 'symbol')),
            nodes.entry('', nodes.paragraph('', 'obj')),
            nodes.entry('', nodes.paragraph('', 'msg'))))
        tbody = nodes.tbody()
        tgroup += tbody
        table += tgroup
        for m in messages:
            if self.builder.config.pylint_debug:
                self.builder.info('sphinxcontrib.pylint:      process message...')
            row = nodes.row()
            path = nodes.entry('', nodes.paragraph('', m[0]))
            line = nodes.entry('', nodes.paragraph('', m[1]))
            msg_id = nodes.entry('', nodes.paragraph('', m[2]))
            symbol = nodes.entry('', nodes.paragraph('', m[3]))
            obj = nodes.entry('', nodes.paragraph('', m[4]))
            msg = nodes.entry('', nodes.paragraph('', m[5]))
            row += path
            row += line
            row += msg_id
            row += symbol
            row += obj
            row += msg
            tbody += row
            if self.builder.config.pylint_debug:
                self.builder.info('sphinxcontrib.pylint:      ... message processed')
        node.replace_self(table)
        if self.builder.config.pylint_debug:
            self.builder.info('sphinxcontrib.pylint:   ... message list directive processed')

    # output package diagrams TODO replace string fake output with dot code
    for node in doctree.traverse(package_diagram):
        content = nodes.paragraph('', 'FAKE PACKAGE DIAGRAM OUTPUT')
        node.replace_self(content)

    # output class diagrams TODO replace string fake output with dot code
    for node in doctree.traverse(class_diagram):
        content = nodes.paragraph('', 'FAKE CLASS DIAGRAM OUTPUT')
        content.append(nodes.paragraph('', 'class name: {}'.format(node['class_name'])))
        if node['ancestor_depth']:
            content.append(nodes.paragraph('', 'ancestor depth: {}'.format(node['ancestor_depth'])))
        if node['class_depth']:
            content.append(nodes.paragraph('', 'class depth: {}'.format(node['class_depth'])))
        if node['attribute_filtering']:
            content.append(nodes.paragraph('', 'attribute_filtering: {}'.format(node['attribute_filtering'])))
        if node['classes_only']:
            content.append(nodes.paragraph('', 'classes_only: {}'.format(node['classes_only'])))
        if node['builtins']:
            content.append(nodes.paragraph('', 'builtins: {}'.format(node['builtins'])))
        node.replace_self(content)

def setup(app):
    app.add_node(message_list)
    app.add_node(package_diagram)
    app.add_node(class_diagram)
    app.add_directive('message-list', MessageListDirective)
    app.add_directive('package-diagram', PackageDiagramDirective)
    app.add_directive('class-diagram', ClassDiagramDirective)
    app.add_config_value('pylint_debug', None, 'html')
    app.add_config_value('pylint_ignore', None, 'html')
    app.add_config_value('pylint_jobs', None, 'html')
    app.add_config_value('pylint_confidence', None, 'html')
    app.add_config_value('pylint_enable', None, 'html')
    app.add_config_value('pylint_disable', None, 'html')
    app.connect("builder-inited", on_builder_inited)
    app.connect("doctree-resolved", on_doctree_resolved)

