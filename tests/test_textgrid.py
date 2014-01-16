#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_textgrid
----------------------------------

Tests for `textgrid` module.
"""

import unittest

from textgrid import TextGrid, Tier, Interval, Point, \
    HeaderParseException, SizeException, ParseException

from example_textgrids import valid_long_1, valid_long_2, \
    invalid_header_long, invalid_entry_long, valid_short_1, \
    valid_short_2, invalid_header_short, invalid_entry_short, \
    valid_chron_1, valid_chron_2, invalid_header_chron, invalid_entry_chron

expected_textgrid = TextGrid(0.0, 3.5,
                             [Tier('First_Interval_Tier',
                                   0.0,
                                   3.5,
                                   [Interval(0.0,
                                             0.5207695865651463,
                                             "word1"),
                                    Interval(0.5207695865651463,
                                             2.054427880167936,
                                             "word2"),
                                    Interval(2.054427880167936,
                                             3.5,
                                             "word3")]),
                              Tier('First_Point_Tier',
                                   0.0,
                                   3.5,
                                   [Point(1.7253166583647621,
                                          "here is a point"),
                                    Point(2.3045524087383478,
                                          "and here's another one")])])

expected_keys = list(expected_textgrid.keys())


class TestLong(unittest.TestCase):
    def test_valid_1(self):
        tg = TextGrid()
        try:
            tg._parse_long(valid_long_1)
        except Exception as exc:
            print exc
            self.fail('_parse_long raised unexpected exception: %s' % exc)
        self.assertEqual(expected_textgrid, tg)

    def test_valid_2(self):
        tg = TextGrid()
        try:
            tg._parse_long(valid_long_2)
        except Exception as exc:
            self.fail('_parse_long raised unexpected exception: %s' % exc)
        self.assertEqual(expected_textgrid, tg)

    def test_invalid_header(self):
        tg = TextGrid()
        self.assertRaises(HeaderParseException,
                          tg._parse_long, invalid_header_long)

    def test_invalid_entry(self):
        tg = TextGrid()
        self.assertRaises(SizeException,
                          tg._parse_long, invalid_entry_long)


class TestShort(unittest.TestCase):
    def test_valid_1(self):
        tg = TextGrid()
        try:
            tg._parse_short(valid_short_1)
        except Exception as exc:
            self.fail('_parse_short raised unexpected exception: %s' % exc)
        self.assertEqual(expected_textgrid, tg)

    def test_valid_2(self):
        tg = TextGrid()
        try:
            tg._parse_short(valid_short_2)
        except Exception as exc:
            self.fail('_parse_short raised unexpected exception: %s' % exc)
        self.assertEqual(expected_textgrid, tg)

    def test_invalid_header(self):
        tg = TextGrid()
        self.assertRaises(HeaderParseException,
                          tg._parse_short, invalid_header_short)

    def test_invalid_entry(self):
        tg = TextGrid()
        # tg._parse_short(invalid_entry_short)
        # print tg.__repr__()
        self.assertRaises(SizeException,
                          tg._parse_short, invalid_entry_short)


class TestChron(unittest.TestCase):
    def test_valid_1(self):
        tg = TextGrid()
        try:
            tg._parse_chron(valid_chron_1)
        except Exception as exc:
            self.fail('_parse_chron raised unexpected exception: %s' % exc)
        if expected_textgrid != tg:
            print expected_textgrid.__repr__()
            print
            print tg.__repr__()
        self.assertEqual(expected_textgrid, tg)

    def test_valid_2(self):
        tg = TextGrid()
        try:
            tg._parse_chron(valid_chron_2)
        except Exception as exc:
            self.fail('_parse_chron raised unexpected exception: %s' % exc)
        self.assertEqual(expected_textgrid, tg)

    def test_invalid_header(self):
        tg = TextGrid()
        self.assertRaises(ParseException,
                          tg._parse_chron, invalid_header_chron)

    def test_invalid_entry(self):
        tg = TextGrid()
        self.assertRaises(SizeException,
                          tg._parse_chron, invalid_entry_chron)


class TestTextGrid(unittest.TestCase):
    def setUp(self):
        tg = TextGrid()
        tg._parse_long(valid_long_1)
        self.tg = tg

    def test_correct_key_in(self):
        for k in expected_keys:
            self.assertIn(k, self.tg)

    def test_keys(self):
        self.assertEqual(list(self.tg.keys()), expected_keys)

    def test_incorrect_key_in(self):
        for k in ['incorrect key 1', 'incorrect key 2']:
            self.assertRaises(KeyError, self.tg.__getitem__, k)


class TestJSON(unittest.TestCase):
    def setUp(self):
        tg = TextGrid()
        tg._parse_long(valid_long_1)
        self.tg = tg

    def test_json(self):
        self.tg.from_json(self.tg.to_json())
        self.assertEqual(self.tg, expected_textgrid)


if __name__ == '__main__':
    unittest.main()
