# -*- coding: utf-8 -*-
"""
Helper functions to format output for CLI.
"""
from __future__ import unicode_literals
from __future__ import print_function

import json
import click
from tabulate import tabulate
from pygments import highlight
from pygments.lexers.data import JsonLexer
from pygments.formatters.terminal import TerminalFormatter

# Python 3 has no 'basestring' or 'long' type we're checking for.
try:
    unicode
except NameError:
    # Python 3
    basestring = unicode = str
    long = int


class StreamFormatter(object):

    def __init__(self, data):
        """
        Initialize the formatter passing in the stream.
        :param data: generator
        """
        self.stream = data
        self.counter = 0

    def output(self):
        """
        Process and output line by line.
        :return: int
        """
        for line in self.stream:
            self.counter += 1
            line = line.strip()
            click.echo(line)
        return self.counter


class JsonStreamDumper(StreamFormatter):

    lexer = JsonLexer()
    term = TerminalFormatter()

    def output(self):
        """
        Process and output object by object.
        :return: int
        """
        for obj in self.stream:
            self.counter += 1
            text = json.dumps(obj, indent=4)
            text = self.colorize(text)
            for line in text.split('\n'):
               click.echo(line)
        return self.counter

    def colorize(self, text):
        return highlight(text, self.lexer, self.term).rstrip('\r\n')


class JsonStreamFormatter(StreamFormatter):

    progress = False

    def __init__(self, data):
        """
        Initialize the formatter passing in the stream.
        :param data: generator
        """
        StreamFormatter.__init__(self, data)

    def output(self):
        """
        Process and output line by line.
        :return: int

        Lines that contain progress information in them get special handling:

        {
            "status":"Extracting",
            "progressDetail":{
                "current":64618496,
                "total":65771329
            },
            "progress":"[======================\u003e ] 64.62 MB/65.77 MB",
            "id":"e9e06b06e14c"
        }

        """
        for line in self.stream:
            self.counter += 1
            data = json.loads(line)

            if self.is_progress(data):
                self.show_progress_line(data)
            else:
                self.show_progress_end()
                self.show_line(data)
        return self.counter

    def is_progress(self, data):
        """
        If the JSON data contains progress bar information.
        :param data: json
        """
        return 'progress' in data and data['progress']

    def show_line(self, data):
        """
        Format and output a JSON line.
        :param data: json
        """
        if 'id' in data and data['id']:
            line = "{0} {1}".format(data['status'], data['id'])
        elif 'status' in data:
            line = "{0}".format(data['status'])
        elif 'stream' in data:
            line = "{0}".format(data['stream'])
        elif 'errorDetail' in data and data['errorDetail']:
            line = "{0}".format(data['errorDetail'].get(
                'message', 'Unknown error'))
        elif 'error' in data and data['error']:
            line = "{0}".format(data['error'])
        else:
            line = "{0}".format(data)

        if line:
            line = line.rstrip()

        click.echo(line)

    def show_progress_end(self):
        """
        If we were just showing progress bar, enter a newline and unset
        the progress flag.
        """
        if self.progress:
            click.echo()
        self.progress = False

    def show_progress_line(self, data):
        """
        Output a carriage return and new progress.
        :param data: json
        """
        click.echo(b'\x0d', nl=False)

        self.progress = True

        line = "{0} {1}: {2}".format(
            data['status'],
            data['id'],
            data['progress'])

        click.echo(line, nl=False)


def format_data(command, data):
    """
    Uses tabulate to format the iterable.
    :return: string (multiline)
    """
    if command and command in DATA_FORMATTERS:
        f = DATA_FORMATTERS[command]
        assert callable(f)
        return f(data)

    if command and command in DATA_FILTERS:
        data = DATA_FILTERS[command](data)

    if isinstance(data, list) and len(data) > 0:
        if isinstance(data[0], tuple):
            if is_plain_lists(data):
                text = tabulate(data)
                return text.split('\n')
            else:
                return format_struct(data)
        elif isinstance(data[0], dict):
            if data[0].keys() == ['Id']:
                # Sometimes our 'quiet' output is a list of dicts but
                # there's only a single "Id" key in each dict. Let's simplify
                # those into plain string lists.
                return [d['Id'] for d in data]
            else:
                data = flatten_rows(data)
                data = truncate_rows(data)
                text = tabulate(data, headers='keys')
                return text.split('\n')
        elif isinstance(data[0], basestring):
            if len(data) == 1:
                return data
            elif is_plain_list(data):
                return data
            else:
                data = truncate_rows(data)
                text = tabulate(data)
                return text.split('\n')
    return data


def format_struct(data, spaces=4, indent=0, lines=None):

    if lines is None:
        lines = []

    if isinstance(data, dict):
        data = [(k, data[k]) for k in sorted(data.keys())]

    def item_to_line(current_item, current_line, is_last_item, current_list):
        """ Helper to add item to end of line """
        if len(current_line) == 0:
            current_indent = ' ' * (indent * spaces)
            current_line = current_indent

        current_line += '{0}'.format(current_item)

        if is_last_item:
            current_list.append(current_line)
            current_line = ''
        else:
            current_line += ': '
        return current_line, current_list

    for row in data:
        line = ''
        l = len(row)
        for i in range(l):
            if isinstance(row[i], dict):
                lines.append(line)
                lines = format_struct(row[i], spaces, indent + 1, lines)
            elif isinstance(row[i], list):
                if is_plain_list(row[i]):
                    item = flatten_list(row[i])
                    line, lines = item_to_line(item, line, i == (l - 1), lines)
                else:
                    lines.append(line)
                    lines = format_struct(row[i], spaces, indent + 1, lines)
            else:
                line, lines = item_to_line(row[i], line, i == (l - 1), lines)

    return lines


def is_plain_lists(lst):
    """
    Check if all items in list of lists are strings or numbers
    :param lst:
    :return: boolean
    """
    for x in lst:
        if not is_plain_list(x):
            return False
    return True


def is_plain_list(lst):
    """
    Check if all items in list are strings or numbers
    :param lst:
    :return: boolean
    """
    for item in lst:
        if not isinstance(item, basestring) and \
                not isinstance(item, (int, long, float, complex)):
            return False
    return True


def flatten_list(data):
    """
    Format and return a comma-separated string of list items.
    :param data:
    :return:
    """
    return ', '.join(["{0}".format(x) for x in data])


def flatten_dict(data):
    """
    Format and return a comma-separated string of dict items.
    :param data:
    :return:
    """
    return ', '.join(["{0}: {1}".format(x, y) for x, y in data.iteritems()])


def format_port_lines(ports):
    """
    Return ports as list of strings
    :param ports: list of dicts
    :return: list of strings
    """
    port_s = format_ports(ports)
    result = port_s.split(', ')
    return result


def format_ports(ports):
    """
    Ports get special treatment.

    They are a list that looks like this:
       [{u'Type': u'tcp', u'PrivatePort': 3306}]

    We return this:
       "3306/tcp"

    Or instead of this:
       [{
       u'IP': u'0.0.0.0',
       u'Type': u'tcp',
       u'PublicPort': 3000,
       u'PrivatePort': 3306}]

    We return:
        "0.0.0.0:3000->3306/tcp"

    :param ports: list of dicts
    :return: string
    """

    def format_port_list(l):
        if isinstance(l, list):
            return ', '.join([format_port(x) for x in l])
        return '{0}'.format(l)

    def format_port(port):
        """
        Format port dictionary and return string.
        """
        if 'PublicPort' in port:
            return '{0}:{1}->{2}/{3}'.format(
                port.get('IP', '0.0.0.0'),
                port.get('PublicPort', '0000'),
                port.get('PrivatePort', '0000'),
                port.get('Type', 'type'))
        if 'HostPort' in port:
            return "{0}:{1}".format(
                port.get('HostIp', '0.0.0.0'),
                port.get('HostPort', '0000')
            )
        if 'PrivatePort' in port:
            return '{0}/{1}'.format(
                port.get('PrivatePort', '0000'),
                port.get('Type', 'type'))
        # Fallback to formatting "as is"
        return "{0}".format(port)

    if isinstance(ports, dict):
        return ', '.join(['{0}->{1}'.format(k, format_port_list(v))
                          for k, v in ports.items()])
    return ', '.join(format_port(x) for x in ports)


def flatten_rows(rows):
    """
    Transform all list or dict values in a dict into comma-separated strings.
    :param rows: iterable of dictionaries
    :return:
    """

    for row in rows:
        for k in row.keys():
            if k in ROW_FORMATTERS:
                row[k] = ROW_FORMATTERS[k](row[k])
            elif isinstance(row[k], list):
                row[k] = flatten_list(row[k])
            elif isinstance(row[k], dict):
                row[k] = flatten_dict(row[k])
    return rows


def truncate_rows(rows, length=30, length_id=10):
    """
    Truncate every string value in a dictionary up to a certain length.
    :param rows: iterable of dictionaries
    :param length: int
    :param length_id: length for dict keys that end with "Id"
    :return:
    """

    def trimto(s, l):
        """
        Trim string to length.
        :param s: string to trim
        :param l: length
        """
        if isinstance(s, basestring):
            return s[:l + 1]
        return s

    result = []
    for row in rows:
        if isinstance(row, dict):
            updated = {}
            for k, v in row.items():
                if k.endswith('Id'):
                    updated[k] = trimto(v, length_id)
                else:
                    updated[k] = trimto(v, length)
            result.append(updated)
        elif isinstance(row, basestring):
            result.append(trimto(row, length))
        else:
            result.append(row)
    return result


def format_top(data):
    """
    Format "top" output
    :param data: dict
    :return: list
    """
    result = []
    if data:
        if 'Titles' in data:
            result.append(data['Titles'])
        if 'Processes' in data:
            for process in data['Processes']:
                result.append(process)
    result = tabulate(result, headers='firstrow').split('\n')
    return result


def filter_ps(data):
    """
    Strip out some of the dictionary fields.
    :param data: dict
    :return: dict
    """
    display_keys = [
        'status', 'created', 'image', 'id', 'command', 'names', 'ports']
    if data and isinstance(data, list) and isinstance(data[0], dict):
        result = []
        for item in data:
            filtered = {}
            for k, v in item.items():
                if k.lower() in display_keys:
                    filtered[k] = v
            result.append(filtered)
        return result
    return data


DATA_FILTERS = {
    'ps': filter_ps
}


DATA_FORMATTERS = {
    'top': format_top,
    'port': format_port_lines
}

ROW_FORMATTERS = {
    'Ports': format_ports
}

STREAM_FORMATTERS = {
    'pull': JsonStreamFormatter,
    'push': JsonStreamFormatter,
    'build': JsonStreamFormatter,
    'inspect': JsonStreamDumper,
}


def output_stream(command, stream, logs):
    """
    Take the iterable and output line by line using click.echo.
    :param command: string command
    :param stream: generator
    :param logs: callable
    :return: None
    """
    if command and command in STREAM_FORMATTERS:
        formatter = STREAM_FORMATTERS[command](stream)
    else:
        formatter = StreamFormatter(stream)

    stream_count = formatter.output()

    if stream_count == 0 and logs and callable(logs):
        # Something nasty has happened and we got an empty
        # output stream. But we have logs. Let's show those.
        lines = logs()
        if lines:
            lines = lines.split('\n')
            for line in lines:
                click.echo(line)
