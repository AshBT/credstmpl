# -*- coding: utf-8 -*-
import os
import logging

import jinja2

from jinja2.exceptions import TemplateSyntaxError

from . exceptions import CredsNotFoundException, LastPassNotFoundException

from . import creds
from . import lastpass

__log = logging.getLogger(__name__)


class TemplateContents(object):
    """ This class represents the contents of a template file. It also
        carries extra metadata along with it, such as the name of the
        source file and its eventual destination.
    """
    def __init__(self, filename, contents):
        self.src            = filename
        self.data           = contents
        self.dst, _ext_     = os.path.splitext(filename)


def is_a_template(filename):
    """ This function checks if the filename ends with the proper
        extension ('j2').

        :param str filename:    The filename to check
        :return:                True if valid template; False otherwise
    """
    ext = os.path.splitext(filename)[-1]
    return ext == '.j2'

def get_template_contents(filenames):
    """ This generator reads valid files and yields their contents.

        :param list filenames:  The list of files to render
        :return:                A generator which yields the contents
                                of valid files.
    """
    for filename in filenames:
        try:
            with open(filename, 'r') as f:
                if is_a_template(filename):
                    yield TemplateContents(filename, f.read())
                else:
                    __log.info("We expected '{}' to end with a .j2 extension. Skipping...".format(filename))
        except IOError:
            __log.info("Could not open file. Skipping '{}'.".format(os.path.abspath(filename)))

def create_template(contents):
    """ This function creates a jinja2 template using the given
        string contents.

        :param TemplateContents contents:   The template contents
        :return:                            A Jinja2 template object
    """
    # attempt to create the template
    try:
        return jinja2.Template(contents.data)
    except TemplateSyntaxError as e:
        __log.error("Encountered syntax error in '{}' on line {}: {}".format(contents.src, e.lineno, e.message))
        raise e

def render_template(template, dest):
    """ This function renders the jinja2 template and writes it to an
        output file that can only be read by the current user.

        :param template:    The Jinja2 template to render
        :param dest:        The destination filename
    """
    try:
        # create file with specific permissions
        #   http://stackoverflow.com/questions/5624359/write-file-with-specific-permissions-in-python
        dest_abs_path = os.path.abspath(dest)
        handle = os.open(dest_abs_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(handle, 'wb') as f:
            __log.debug("Writing template to '{}'".format(dest))
            # note that for each reference to any credstash lookup
            # has to hit AWS, this can be slow for files with lots of
            # credentials
            result = template.render(credstash = creds.lookup, lastpass = lastpass.lookup)
            if isinstance(result, str):
                f.write(result.encode('utf-8'))
            else:
                f.write(result)
    except IOError as e:
        __log.error("Encountered an error writing '{}': {}. Aborting...".format(output, e))
        raise e
    except CredsNotFoundException as e:
        __log.error(str(e).strip())
        __log.error("Sorry, but '{}' was not found. Aborting...".format(e.secret))
        raise e
    except LastPassNotFoundException as e:
        __log.error(str(e).strip())
        __log.error("Sorry, but we could not find the `lpass` binary on your system.")
        __log.error("If you wish to use Last Pass in your templates, please install the Last Pass CLI. (https://github.com/lastpass/lastpass-cli)")
        __log.error("Aborting...")
        raise e

def render(filenames):
    """ This function renders the templates and writes them to the
        filesystem.

        :param list filenames:  The list of files to render
        :return:                A tuple of two lists: the first is a
                                list of rendered templates, the second a
                                list of skipped templates.
    """
    rendered, skipped = [], []
    for contents in get_template_contents(filenames):
        try:
            template = create_template(contents)
            render_template(template, contents.dst)
        except (IOError, CredsNotFoundException, LastPassNotFoundException, TemplateSyntaxError) as e:
            skipped.append(contents.dst)
            continue
        rendered.append(contents.dst)
    return rendered, skipped
