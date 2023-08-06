#! /usr/bin/env python
# -*- coding:Utf-8 -*-

""" Tools python.
    Keyword arguments:
        none
    Return self
"""
# ============================================================
#    Linux python path and Library import
# ============================================================

import calendar
import datetime
import arrow
from collections import OrderedDict


from typing import Iterable, Any, Tuple

# ============================================================
#    Variables and Constants
# ============================================================

# None

# ============================================================
#     Functions and Procedures
# ============================================================


# ||||||||||||||||||||||||||||||||||||||||||||||||||
#    signal_first
# ||||||||||||||||||||||||||||||||||||||||||||||||||
def signal_first(it: Iterable[Any]) -> Iterable[Tuple[bool, Any]]:
    """Get the first element in iterable loop :
    for is_first_element, var in signal_first(fib(10)):
    if is_first_element:
        special_function(var)
    else:
        not_so_special_function(var)
    """
    iterable = iter(it)
    yield True, next(iterable)
    for val in iterable:
        yield False, val


# ||||||||||||||||||||||||||||||||||||||||||||||||||
#    signal_last
# ||||||||||||||||||||||||||||||||||||||||||||||||||
def signal_last(it: Iterable[Any]) -> Iterable[Tuple[bool, Any]]:
    """Get the first element in iterable loop :
    for is_last_element, var in signal_last(fib(10)):
    if is_last_element:
        special_function(var)
    else:
        not_so_special_function(var)
    """
    iterable = iter(it)
    ret_var = next(iterable)
    for val in iterable:
        yield False, ret_var
        ret_var = val
    yield True, ret_var


# ||||||||||||||||||||||||||||||||||||||||||||||||||
#    add_months
# ||||||||||||||||||||||||||||||||||||||||||||||||||
def add_months(pdate, pmonths):
    cal_month = pdate.month - 1 + pmonths
    cal_year = pdate.year + cal_month // 12
    cal_month = cal_month % 12 + 1
    cal_day = min(pdate.day, calendar.monthrange(cal_year, cal_month)[1])
    return pdate.replace(year=cal_year, month=cal_month, day=cal_day)


# ||||||||||||||||||||||||||||||||||||||||||||||||||
#    iso_date_info
# ||||||||||||||||||||||||||||||||||||||||||||||||||
def iso_date_info(pdate):
    isoYEAR, isoWEEK, isoDAY = pdate.isocalendar()
    del isoDAY
    isoYEAR = str(isoYEAR)
    isoWEEK = str(isoWEEK).rjust(2, "0")
    return (isoYEAR, isoWEEK)


# ||||||||||||||||||||||||||||||||||||||||||||||||||
#    convertHeaders_ToList
# ||||||||||||||||||||||||||||||||||||||||||||||||||
def convertHeaders_ToList(
    pheaders,
    pdecoding=None,
    pencoding=None,
    pdoublequote=False,
    ptobind=False,
    pnone=None,
    pdictconv={},
    pcase=None,
    pstrip=False,
    pisdttutc=False,
):
    new_headers = []
    for header in pheaders:
        v = header[0]
        v = pdictconv.get(v, v)
        v = val_convert(
            v,
            pdecoding=pdecoding,
            pencoding=pencoding,
            pdoublequote=pdoublequote,
            ptobind=ptobind,
            pnone=pnone,
            pcase=pcase,
            pstrip=pstrip,
            pisdttutc=pisdttutc,
        )
        if v is not None:
            new_headers.append(v)
    return new_headers


# ||||||||||||||||||||||||||||||||||||||||||||||||||
#    convertRows_ToDicts
# ||||||||||||||||||||||||||||||||||||||||||||||||||
def convertRows_ToDicts(
    prows,
    pdecoding=None,
    pencoding=None,
    pdoublequote=False,
    ptobind=False,
    pnone=None,
    pcase=None,
    pstrip=False,
    pisdttutc=False,
):
    new_rows = []
    for row in prows:
        new_rows.append(
            convertRow_ToDict(
                row,
                pdecoding=pdecoding,
                pencoding=pencoding,
                pdoublequote=pdoublequote,
                ptobind=ptobind,
                pnone=pnone,
                pcase=pcase,
                pstrip=pstrip,
                pisdttutc=pisdttutc,
            )
        )
    return new_rows


# ||||||||||||||||||||||||||||||||||||||||||||||||||
#    convertRows_ToLists
# ||||||||||||||||||||||||||||||||||||||||||||||||||
def convertRows_ToLists(
    prows,
    pdecoding=None,
    pencoding=None,
    pdoublequote=False,
    ptobind=False,
    pnone=None,
    pcase=None,
    pstrip=False,
    pisdttutc=False,
):
    new_rows = []
    for row in prows:
        new_rows.append(
            convertRow_ToList(
                row,
                pdecoding=pdecoding,
                pencoding=pencoding,
                pdoublequote=pdoublequote,
                ptobind=ptobind,
                pnone=pnone,
                pcase=pcase,
                pstrip=pstrip,
                pisdttutc=pisdttutc,
            )
        )
    return new_rows


# ||||||||||||||||||||||||||||||||||||||||||||||||||
#    convertRow_ToDict
# ||||||||||||||||||||||||||||||||||||||||||||||||||
def convertRow_ToDict(
    prow,
    pdecoding=None,
    pencoding=None,
    pdoublequote=False,
    ptobind=False,
    pnone=None,
    pcase=None,
    pstrip=False,
    pisdttutc=False,
):
    new_dict = OrderedDict()
    for (k, v) in zip(prow.cursor_description, prow):
        v = val_convert(
            v,
            pdecoding=pdecoding,
            pencoding=pencoding,
            pdoublequote=pdoublequote,
            ptobind=ptobind,
            pnone=pnone,
            pcase=pcase,
            pstrip=pstrip,
            pisdttutc=pisdttutc,
        )
        new_dict[k[0]] = v
    return new_dict


# ||||||||||||||||||||||||||||||||||||||||||||||||||
#    convertRow_ToList
# ||||||||||||||||||||||||||||||||||||||||||||||||||
def convertRow_ToList(
    prow,
    pdecoding=None,
    pencoding=None,
    pdoublequote=False,
    ptobind=False,
    pnone=None,
    pcase=None,
    pstrip=False,
    pisdttutc=False,
):
    new_list = []
    for v in prow:
        v = val_convert(
            v,
            pdecoding=pdecoding,
            pencoding=pencoding,
            pdoublequote=pdoublequote,
            ptobind=ptobind,
            pnone=pnone,
            pcase=pcase,
            pstrip=pstrip,
            pisdttutc=pisdttutc,
        )
        new_list.append(v)
    return new_list


# ||||||||||||||||||||||||||||||||||||||||||||||||||
#    convertDict_ToDict
# ||||||||||||||||||||||||||||||||||||||||||||||||||
def convertDict_ToDict(
    pdict,
    pdecoding=None,
    pencoding=None,
    pdoublequote=False,
    ptobind=False,
    pnone=None,
    pdictconv={},
    pcase=None,
    pstrip=False,
    pisdttutc=False,
):
    new_dict = OrderedDict()
    for (k, v) in pdict.items():
        v = val_convert(
            v,
            pdecoding=pdecoding,
            pdoublequote=pdoublequote,
            ptobind=ptobind,
            pnone=pnone,
            pcase=pcase,
            pstrip=pstrip,
            pisdttutc=pisdttutc,
        )
        new_dict[pdictconv.get(k, k)] = v
    return new_dict


# ||||||||||||||||||||||||||||||||||||||||||||||||||
#    val_convert
# ||||||||||||||||||||||||||||||||||||||||||||||||||
def val_convert(
    pval,
    pdecoding=None,
    pencoding=None,
    pdoublequote=False,
    ptobind=False,
    pnone=None,
    pcase=None,
    pstrip=False,
    pisdttutc=False,
):
    v = pval
    if pnone is not None:
        if v is None:
            v = pnone
    if pstrip:
        if isinstance(v, str):
            v = v.strip()
    if pdoublequote:
        if isinstance(v, str):
            v = v.replace("'", "''")
    if ptobind:
        if v is None:
            v = "NULL"
        elif isinstance(v, str):
            v = "'%s'" % v
    if pisdttutc:
        if isinstance(v, datetime.date):
            v = arrow.get(v).datetime
    if pdecoding is not None:
        try:
            v = v.decode(pdecoding)
        except Exception:
            pass
    if pencoding is not None:
        try:
            v = v.encode(pencoding)
        except Exception:
            pass
    if pcase is not None:
        if isinstance(v, str):
            if "UP" in pcase.upper():
                v = v.upper()
            if "LOW" in pcase.upper():
                v = v.lower()
    return v
