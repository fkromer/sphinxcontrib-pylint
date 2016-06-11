# -*- coding: utf-8 -*-
"""
    sphinxcontrib.pylint
    ~~~~~~~~~~~~~~~~~~~~

    Allow pylint static analysis results to be included in Sphinx-generated
    documents inline.

    :copyright: Copyright 2016 by the contributers, see AUTHORS.
    :license: MIT.
"""

#from pylint import epylint as lint
import os.path
from docutils import nodes
from sphinx.util.compat import Directive

options = []

class message_list(nodes.General, nodes.Element):
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


def get_general_options(builder):
    general_options = [builder.config.pylint_ignore, builder.config.pylint_jobs]
    return general_options

def get_message_control_options(builder):
    if builder.config.pylint_confidence not in ('HIGH', 'INFERENCE', 'INFERENCE_FAILURE', 'UNDEFINED'):
        raise ValueError('Unsupported option value: %s' % builder.config.pylint_confidence)
    message_control_options = [builder.config.pylint_confidence, builder.config.pylint_enable, builder.config.pylint_disable]
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
    # run pylint
    #pylint_options = ['report=no', 'output-format=parseable', '../tests/brz.py']
    #lint.py_run(pylint_options)
    if self.builder.config.pylint_debug:
        self.builder.info('sphinxcontrib.pylint: execute on_doctree_resolved()...')
    
    self.builder.info('sphinxcontrib.pylint: TODO run pylint with options {}'.format(options))

    # TODO replace this fake message list with the messages from pylint
    messages = [['C', 'test1.py', 'warning', '14', '15', '16'], ['F', 'test2.py', 'fatal', '24', '25', '26']]

    # output message list into table
    for node in doctree.traverse(message_list):
        if self.builder.config.pylint_debug:
            self.builder.info('sphinxcontrib.pylint:   process message list directive...')
        table = nodes.table()
        tgroup = nodes.tgroup()
        category_colspec = nodes.colspec(colwidth=5)
        module_colspec = nodes.colspec(colwidth=5)
        object_colspec = nodes.colspec(colwidth=5)
        line_colspec = nodes.colspec(colwidth=5)
        column_colspec = nodes.colspec(colwidth=5)
        message_colspec = nodes.colspec(colwidth=5)
        tgroup += [category_colspec, module_colspec, object_colspec, line_colspec, column_colspec, message_colspec]
        tgroup += nodes.thead('', nodes.row(
            '',
            nodes.entry('', nodes.paragraph('', 'Category')),
            nodes.entry('', nodes.paragraph('', 'Module')),
            nodes.entry('', nodes.paragraph('', 'Object')),
            nodes.entry('', nodes.paragraph('', 'Line')),
            nodes.entry('', nodes.paragraph('', 'Column')),
            nodes.entry('', nodes.paragraph('', 'Message'))))
        tbody = nodes.tbody()
        tgroup += tbody
        table += tgroup
        for m in messages:
            if self.builder.config.pylint_debug:
                self.builder.info('sphinxcontrib.pylint:      process message...')
            row = nodes.row()
            category = nodes.entry('', nodes.paragraph('', m[0]))
            module = nodes.entry('', nodes.paragraph('', m[1]))
            obj = nodes.entry('', nodes.paragraph('', m[2]))
            line = nodes.entry('', nodes.paragraph('', m[3]))
            column = nodes.entry('', nodes.paragraph('', m[4]))
            message = nodes.entry('', nodes.paragraph('', m[5]))
            row += category
            row += module
            row += obj
            row += line
            row += column
            row += message
            tbody += row
            if self.builder.config.pylint_debug:
                self.builder.info('sphinxcontrib.pylint:      ... message processed')
        node.replace_self(table)
        if self.builder.config.pylint_debug:
            self.builder.info('sphinxcontrib.pylint:   ... message list directive processed')


def setup(app):
    app.add_node(message_list)
    app.add_directive('message-list', MessageListDirective)
    app.add_config_value('pylint_debug', None, 'html')
    app.add_config_value('pylint_ignore', None, 'html')
    app.add_config_value('pylint_jobs', None, 'html')
    app.add_config_value('pylint_confidence', None, 'html')
    app.add_config_value('pylint_enable', None, 'html')
    app.add_config_value('pylint_disable', None, 'html')
    app.connect("builder-inited", on_builder_inited)
    app.connect("doctree-resolved", on_doctree_resolved)

