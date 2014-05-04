#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------------------------------------
# file: textgrid.py
# date: Tue August 06 16:55:34 2013
# author:
# Maarten Versteegh
# cls.ru.nl/~versteegh
# maartenversteegh AT gmail DOT com
# Centre for Language Studies
# Radboud University Nijmegen
#
# Licensed under GPLv3
# ------------------------------------
"""textgrid: parse Praat textgrid files

"""

from __future__ import division
__all__ = ['Tier', 'Interval', 'Point', 'TextGrid']

from pyparsing import *
import cStringIO as StringIO
import json

# pyparsing elements
line = Group(Regex(".*") + lineEnd)
line.setParseAction(lambda t: t[0][0])
marker = quotedString.setParseAction(removeQuotes)
decimal = Regex(r'[-+]?\d+(\.\d*)?([Ee][-+]?\d+)?')
decimal.setParseAction(lambda t: ''.join(t), lambda t: float(t[0]))
integer = Regex(r'\d+').setParseAction(lambda t: int(t[0]))


class Interval(object):
    def __init__(self, start, end, mark):
        self.start = start
        self.end = end
        self.mark = mark

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.__dict__)

    def __str__(self, ):
        return '<Interval ({start}, {end}, {mark})>'.format(
            start=self.start,
            end=self.end,
            mark=self.mark)

    def __eq__(self, other):
        return all(getattr(self, k) == getattr(other, k)
                   for k in self.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)


class Point(object):
    def __init__(self, time, mark):
        self.time = time
        self.mark = mark

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.__dict__)

    def __eq__(self, other):
        return all(getattr(self, k) == getattr(other, k)
                   for k in self.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self, ):
        return '<Point ({time}, {mark})>'.format(
            time=time,
            mark=mark)


class HeaderParseException(ParseFatalException):
    def __init__(self, s, loc, msg):
        super(HeaderParseException, self).__init__(
            s, loc, "parse error in header '{0}'".format(msg))


class ContentParseException(ParseFatalException):
    def __init__(self, s, loc, msg):
        super(ContentParseException, self).__init__(
            s, loc, "parse error in tier '{0}'".format(msg))


class SizeException(Exception):
    pass


def error(exceptionclass):
    def raise_exception(s, l, t):
        raise exceptionclass(s, l, t[0])
    return Word(alphas, alphanums).setParseAction(raise_exception)


class Tier(object):
    """ Container class for IntervalTier and TextTier tiers.
    """

    def __init__(self, name, start, end, entries):
        """

        Arguments:
        :param name: identifier of the tier
        :param start: start time in seconds (float)
        :param end: end time in seconds (float)
        :param entries: list of either Interval or Point objects
        """
        self.name = name
        self.start = start
        self.end = end
        self.entries = entries
        self._sort_entries()

    def _sort_entries(self):
        if not self.entries:
            return
        if isinstance(self.entries[0], Point):
            cmp = lambda x: (x.time, x.mark)
        else:
            cmp = lambda x: (x.start, x.end, x.mark)
        self.entries = sorted(self.entries, key=cmp)

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.__dict__)

    def __eq__(self, other):
        return all(getattr(self, k) == getattr(other, k)
                   for k in self.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __iter__(self):
        return iter(self.entries)

    def __len__(self):
        return self.size

    def __getitem__(self, k):
        return self.entries[k]

    def __setitem__(self, k, v):
        self.entries[k] = v
        self._sort_entries()

    def __delitem__(self, k):
        del self.entries[k]
        self._sort_entries()

    @property
    def size(self):
        return len(self.entries)

    @property
    def transcription(self):
        """
        """
        s = StringIO.StringIO()
        for entry in self.entries:
            if not entry.mark in ['', ' ']:
                s.write(entry.mark + ' ')
        return s.getvalue().strip()


class TextGrid(object):
    """Represents TextGrid files.

    Attributes:
    start: start time of the \c TextGrid object
    end: end time of the \c TextGrid object
    size: number of tiers
    tiers: list of tiers
    """

    def __init__(self, start=0.0, end=0.0, tiers=None):
        """

        Arguments:
        :param start: start time in seconds [default: 0.0]
        :param end: end time in seconds [default: 0.0]
        :param tiers: list of \c Tier objects
        """
        self.start = start
        self.end = end
        if tiers is None:
            tiers = []
        self.tiers = tiers

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.__dict__)

    def __str__(self):
        return '<TextGrid with %d tiers>' % len(self.tiers)

    def __eq__(self, other):
        return all(getattr(self, k) == getattr(other, k)
                   for k in self.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def size(self):
        return len(self.tiers)

    def append_tier(self, tier):
        self.tiers.append(tier)
        if tier.end > self.end:
            self.end = tier.end

    def keys(self):
        for t in self.tiers:
            yield t.name

    def __iter__(self):
        return iter(self.tiers)

    def __len__(self):
        return self.size

    def __getitem__(self, i):
        k = self._check_key(i)
        return self.tiers[k]

    def __setitem__(self, i, tier):
        k = self._check_key(i)
        self.tiers[k] = tier

    def __delitem__(self, i):
        k = self._check_key(i)
        del self.tiers[k]

    def _check_key(self, key):
        if isinstance(key, int):
            if key < self.size:
                return key
            else:
                raise KeyError('{0} is not a valid key'.format(key))
        elif isinstance(key, basestring):
            _tier_map = dict(zip([t.name for t in self.tiers],
                                 range(self.size)))
            try:
                return _tier_map[key]
            except KeyError:
                raise KeyError('{0} is not a valid key'.format(key))
        else:
            raise TypeError('key needs to be either int or string'
                            ', not {0}'.format(type(key)))

    def __contains__(self, k):
        return k in self.keys()

    @staticmethod
    def read(f):
        """
        :param f: string or file
        """
        if isinstance(f, basestring):
            with open(f, 'r') as fid:
                text = fid.read()
        elif isinstance(f, file):
            text = f.read()
        else:
            raise ValueError('`f` needs to be either string or file, not %s'
                             % type(f))

        # 1. figure out the type of textgrid; long, short or chrono
        type_info = Group(line('type') + Suppress(line) + line('xmin'))
        token_type_info = type_info.parseString(text)[0]
        if 'chron' in token_type_info.type:
            ttype = 'chronological'
        elif 'xmin' in token_type_info.xmin:
            ttype = 'long'
        else:
            ttype = 'short'

        r = TextGrid()
        r.start = 0
        r.end = 0
        # 2. parse the file
        if ttype == 'chronological':
            r._parse_chron(text, marker, integer, line, decimal)
        elif ttype == 'short':
            r._parse_short(text)
        else:  # ttype == 'long'
            r._parse_long(text)
        return r

    def _parse_long(self, text):
        prelude = Group(Suppress(line) +
                        Suppress(line) +
                        Suppress(Literal('xmin =')) +
                        decimal('start') +
                        Suppress(Literal('xmax =')) +
                        decimal('end') +
                        Suppress(line) +
                        Suppress(Literal('size =')) +
                        integer('size') +
                        Suppress(line)) | error(HeaderParseException)
        interval = Group(Suppress(line) +
                         Suppress(Literal('xmin =')) +
                         decimal('start') +
                         Suppress(Literal('xmax =')) +
                         decimal('end') +
                         Suppress('text =') +
                         marker('mark'))
        interval.setParseAction(lambda t:
                                Interval(*t[0]))
        point = Group(Suppress(line) +
                      Suppress(Literal('number =')) +
                      decimal('time') +
                      Suppress('mark =') +
                      marker('mark'))
        point.setParseAction(lambda t: Point(*t[0]))
        entry = (interval ^ point)
        tier = Group(Suppress(line) +
                     Suppress(line) +
                     Suppress(Literal('name =')) + marker('name') +
                     Suppress(Literal('xmin =')) + decimal('start') +
                     Suppress(Literal('xmax =')) + decimal('end') +
                     Suppress(Regex('.*: ') +
                              Literal('size =')) + integer('size') +
                     OneOrMore(entry)('entries')) \
            | error(ContentParseException)

        def validate_tier(t):
            if t[0].size != len(t[0].entries.asList()):
                raise SizeException('inconsistent number of entries.'
                                    ' expected: {0}, got: {1}'.format(
                                        t[0].size,
                                        len(t[0].entries.asList())))

        tier.setParseAction(validate_tier,
                            lambda t:
                            Tier(t[0].name,
                                 t[0].start,
                                 t[0].end,
                                 t[0].entries.asList()))

        def validate_grid(t):
            if t[0].prelude.size != len(t[0].tiers):
                raise ParseException('inconsistent number of tiers.'
                                     ' expected: {0}, got: {1}'.format(
                                         t[0].prelude.size,
                                         len(t[0].tiers)))

        grid = Group(prelude('prelude') + OneOrMore(tier)('tiers'))
        grid.setParseAction(validate_grid)

        g = grid.parseString(text)
        self.start = float(g[0].prelude.start)
        self.end = float(g[0].prelude.end)
        self.tiers = g[0].tiers.asList()

    def _parse_short(self, text):
        prelude = Group(Suppress(line) +
                        Suppress(line) +
                        decimal('start') +
                        decimal('end') +
                        Suppress(line) +
                        integer('size')) | error(HeaderParseException)
        interval = Group(decimal('start') +
                         decimal('end') +
                         marker('mark'))
        interval.setParseAction(lambda t:
                                Interval(*t[0]))
        point = Group(decimal('time') +
                      marker('mark'))
        point.setParseAction(lambda t:
                             Point(*t[0]))
        entry = (interval ^ point)
        tier = Group((Suppress(Literal('"IntervalTier"')) ^
                      Suppress(Literal('"TextTier"'))) +
                     marker('name') +
                     decimal('start') +
                     decimal('end') +
                     integer('size') +
                     OneOrMore(entry)('entries')) \
            | error(ContentParseException)

        def validate_tier(t):
            if t[0].size != len(t[0].entries.asList()):
                raise SizeException('inconsistent number of entries.'
                                    ' expected: {0}, got: {1}'.format(
                                        t[0].size,
                                        len(t[0].entries.asList())))

        tier.setParseAction(validate_tier,
                            lambda t:
                            Tier(t[0].name,
                                 t[0].start,
                                 t[0].end,
                                 t[0].entries.asList()))

        def validate_grid(t):
            if t[0].prelude.size != len(t[0].tiers):
                raise SizeException('inconsistent number of tiers.'
                                    ' expected: {0}, got: {1}'.format(
                                        t[0].prelude.size,
                                        len(t[0].entries.asList())))

        grid = Group(prelude('prelude') + OneOrMore(tier)('tiers'))
        grid.setParseAction(validate_grid)

        g = grid.parseString(text)

        self.start = float(g[0].prelude.start)
        self.end = float(g[0].prelude.end)
        self.tiers = g[0].tiers.asList()

    def _parse_chron(self, text):
        tiers = []
        time_line = Group(decimal('start') +
                          decimal('end') +
                          Suppress(restOfLine)) | error(HeaderParseException)
        size_line = Group(integer('size') +
                          Suppress(restOfLine)) | error(HeaderParseException)
        size_line.setParseAction(lambda t: t[0].size)
        tier_id = Group(quotedString('type') +
                        quotedString('name') +
                        decimal('start') +
                        decimal('end'))
        tier_id.setParseAction(lambda t:
                               tiers.append(Tier(t[0].name,
                                                 t[0].start,
                                                 t[0].end,
                                                 [])))
        tier_ids = Group(OneOrMore(tier_id))
        prelude = Group(Suppress(line) +
                        time_line('time') +
                        size_line('size') +
                        tier_ids('tier_ids')) | error(HeaderParseException)

        interval = Group(Suppress(line) +
                         integer('tier_id') +
                         decimal('start') +
                         decimal('end') +
                         marker('mark'))
        interval.setParseAction(lambda t: (t[0].tier_id,
                                           Interval(t[0].start,
                                                    t[0].end,
                                                    t[0].mark)))
        point = Group(Suppress(line) +
                      integer('tier_id') +
                      decimal('time') +
                      marker('mark'))
        point.setParseAction(lambda t: (t[0].tier_id,
                                        Point(t[0].time,
                                              t[0].mark)))
        entry = (interval ^ point)
        entry.setParseAction(lambda t:
                             tiers[t[0][0] - 1].entries.append(t[0][1]))
        entries = OneOrMore(entry) | error(ContentParseException)
        g = Group(prelude('prelude') + entries('entries')).parseString(text)
        if g[0].prelude.size != len(tiers):
            print g[0].prelude.size
            raise SizeException('inconsistent number of tiers.'
                                ' expected: {0}, got: {1}'.format(
                                    g[0].prelude.size,
                                    len(tiers)))

        self.start = float(min(x.start for x in tiers))
        self.end = float(max(x.end for x in tiers))
        self.tiers = tiers

    def to_json(self, sort_keys=True, indent=2):
        class Encoder(json.JSONEncoder):
            def default(self, obj):
                d = {'_TYPE': obj.__class__.__name__}
                d.update(obj.__dict__)
                return d
        return json.dumps(self, sort_keys=sort_keys,
                          indent=indent, cls=Encoder)

    @staticmethod
    def from_json(text):
        class Decoder(json.JSONDecoder):
            def __init__(self):
                json.JSONDecoder.__init__(self,
                                          object_hook=self.dict_to_object)

            def dict_to_object(self, d):
                if '_TYPE' in d:
                    class_name = d.pop('_TYPE')
                    module = __import__('textgrid')
                    class_ = getattr(module, class_name)
                    args = {key.encode('utf-8'): value
                            for key, value in d.items()}
                    inst = class_(**args)
                else:
                    inst = d
                return inst
        return Decoder().decode(text)

    def write(self, stream, fmt='long'):
        """Write \c TextGrid object out in long format

        :params stream: stream to write to
        """
        # TODO implement formats
        if fmt == 'long':
            self._write_long(stream)
        elif fmt == 'short':
            self._write_short(stream)
        elif fmt == 'chron':
            self._write_chron(stream)
        else:
            raise ValueError('invalid format: {0}'.format(fmt))

    def _write_short(stream):
        # TODO implement
        raise NotImplementedError

    def _write_chron(stream):
        # TODO implement
        raise NotImplementedError

    def _write_long(self, stream):
        print >>stream, 'File type = "ooTextFile"'
        print >>stream, 'Object class = "TextGrid"'
        print >>stream, ''
        print >>stream, 'xmin = {0}'.format(self.start)
        print >>stream, 'xmax = {0}'.format(self.end)
        print >>stream, 'tiers? <exists>'
        print >>stream, 'size = {0}'.format(len(self.tiers))
        print >>stream, 'item []:'
        for tdx, tier in enumerate(self.tiers):
            print >>stream, '\titem [{0}]:'.format(tdx+1)
            print >>stream, '\t\tclass = "IntervalTier"'
            print >>stream, '\t\tname = "{0}"'.format(tier.name)
            print >>stream, '\t\txmin = {0:.3f}'.format(tier.start)
            print >>stream, '\t\txmax = {0:.3f}'.format(tier.end)
            print >>stream, '\t\tintervals: size = {0}'.format(
                len(tier.intervals))
            for idx, interval in enumerate(tier.intervals):
                print >>stream, '\t\tintervals [{0}]'.format(idx+1)
                print >>stream, '\t\t\txmin = {0:.3f}'.format(interval.start)
                print >>stream, '\t\t\txmax = {0:.3f}'.format(interval.end)
                print >>stream, '\t\t\ttext = "{0}"'.format(interval.mark)
