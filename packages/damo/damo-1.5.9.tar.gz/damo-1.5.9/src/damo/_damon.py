#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0

"""
Contains core functions for DAMON control.
"""

import os
import time

import _damo_fmt_str
import _damo_fs
import _damon_dbgfs
import _damon_sysfs

# Core data structures

class DamonIntervals:
    sample = None
    aggr = None
    ops_update = None

    def __init__(self, sample, aggr, ops_update):
        self.sample = _damo_fmt_str.text_to_us(sample)
        self.aggr = _damo_fmt_str.text_to_us(aggr)
        self.ops_update = _damo_fmt_str.text_to_us(ops_update)

    def __str__(self):
        return 'sample %s, aggr %s, update %s' % (
                _damo_fmt_str.format_time_us(self.sample, False),
                _damo_fmt_str.format_time_us(self.aggr, False),
                _damo_fmt_str.format_time_us(self.ops_update, False))

    def __eq__(self, other):
        return self.__str__() == other.__str__()

    def to_kvpairs(self):
        return {
                'sample': _damo_fmt_str.format_time_us(self.sample, False),
                'aggr': _damo_fmt_str.format_time_us(self.aggr, False),
                'ops_update': _damo_fmt_str.format_time_us(self.ops_update,
                    False),
                }

def kvpairs_to_DamonIntervals(kvpairs):
    return DamonIntervals(
            kvpairs['sample'], kvpairs['aggr'], kvpairs['ops_update'])

default_DamonIntervals = DamonIntervals(5000, 100000, 1000000)

class DamonNrRegionsRange:
    min_nr_regions = None
    max_nr_regions = None

    def __init__(self, min_, max_):
        self.min_nr_regions = _damo_fmt_str.text_to_nr(min_)
        self.max_nr_regions = _damo_fmt_str.text_to_nr(max_)

    def __str__(self):
        return '[%s, %s]' % (
                _damo_fmt_str.format_nr(self.min_nr_regions, False),
                _damo_fmt_str.format_nr(self.max_nr_regions, False))

    def __eq__(self, other):
        return self.__str__() == other.__str__()

    def to_kvpairs(self):
        return {
                'min_nr_regions':
                _damo_fmt_str.format_nr(self.min_nr_regions, False),
                'max_nr_regions':
                _damo_fmt_str.format_nr(self.max_nr_regions, False),
                }

def kvpairs_to_DamonNrRegionsRange(kvpairs):
    return DamonNrRegionsRange(
            kvpairs['min_nr_regions'], kvpairs['max_nr_regions'])

default_DamonNrRegionsRange = DamonNrRegionsRange(10, 1000)

class DamonRegion:
    # [star, end)
    start = None
    end = None

    def __init__(self, start, end):
        self.start = _damo_fmt_str.text_to_nr(start)
        self.end = _damo_fmt_str.text_to_nr(end)

    def __str__(self):
        return _damo_fmt_str.format_addr_range(self.start, self.end, False)

    def __eq__(self, other):
        return self.__str__() == other.__str__()

    def to_kvpairs(self):
        return {'start': _damo_fmt_str.format_nr(self.start, False),
                'end': _damo_fmt_str.format_nr(self.end, False)}

def kvpairs_to_DamonRegion(kvpairs):
    return DamonRegion(kvpairs['start'], kvpairs['end'])

class DamonTarget:
    name = None
    pid = None
    regions = None

    def __init__(self, name, pid, regions):
        self.name = name
        self.pid = pid
        self.regions = regions

    def __str__(self):
        lines = ['%s (pid: %s)' % (self.name, self.pid)]
        for region in self.regions:
            lines.append('region %s' % region)
        return '\n'.join(lines)

    def __eq__(self, other):
        return self.__str__() == other.__str__()

    def to_kvpairs(self):
        kvp = {attr: getattr(self, attr) for attr in ['name', 'pid']}
        kvp['regions'] = [r.to_kvpairs() for r in self.regions]
        return kvp

def kvpairs_to_DamonTarget(kvpairs):
    regions = [kvpairs_to_DamonRegion(kvp) for kvp in kvpairs['regions']]
    return DamonTarget(kvpairs['name'], kvpairs['pid'], regions)

class DamosAccessPattern:
    min_sz_bytes = None
    max_sz_bytes = None
    min_nr_accesses = None
    max_nr_accesses = None
    nr_accesses_unit = None # 'percent' or 'sample_intervals'
    min_age = None
    max_age = None
    age_unit = None # 'usec' or 'aggr_intervals'

    def __init__(self, min_sz_bytes, max_sz_bytes,
            min_nr_accesses, max_nr_accesses, nr_accesses_unit,
            min_age, max_age, age_unit):
        self.min_sz_bytes = _damo_fmt_str.text_to_bytes(min_sz_bytes)
        self.max_sz_bytes = _damo_fmt_str.text_to_bytes(max_sz_bytes)

        if nr_accesses_unit == 'percent':
            self.min_nr_accesses = _damo_fmt_str.text_to_percent(
                    min_nr_accesses)
            self.max_nr_accesses = _damo_fmt_str.text_to_percent(
                    max_nr_accesses)
        else:
            self.min_nr_accesses = min_nr_accesses
            self.max_nr_accesses = max_nr_accesses
        self.nr_accesses_unit = nr_accesses_unit

        if age_unit == 'usec':
            self.min_age = _damo_fmt_str.text_to_us(min_age)
            self.max_age = _damo_fmt_str.text_to_us(max_age)
        else:
            self.min_age = min_age
            self.max_age = max_age
        self.age_unit = age_unit

    def __str__(self):
        lines = [
            'sz: [%s, %s]' % (_damo_fmt_str.format_sz(self.min_sz_bytes, False),
                _damo_fmt_str.format_sz(self.max_sz_bytes, False)),
            ]
        if self.nr_accesses_unit == 'percent':
            unit = '%'
        else:
            unit = self.nr_accesses_unit
        lines.append('nr_accesses: [%s %s, %s %s]' % (
                _damo_fmt_str.format_nr(self.min_nr_accesses, False), unit,
                _damo_fmt_str.format_nr(self.max_nr_accesses, False), unit))
        if self.age_unit == 'usec':
            min_age = _damo_fmt_str.format_time_us_exact(self.min_age, False)
            max_age = _damo_fmt_str.format_time_us_exact(self.max_age, False)
        else:
            min_age = '%s %s' % (
                    _damo_fmt_str.format_nr(self.min_age, False),
                    self.age_unit)
            max_age = '%s %s' % (
                    _damo_fmt_str.format_nr(self.max_age, False),
                    self.age_unit)
        lines.append('age: [%s, %s]' % (min_age, max_age))
        return '\n'.join(lines)

    def __eq__(self, other):
        return (type(self) == type(other) and
                self.min_sz_bytes ==
                other.min_sz_bytes and self.max_sz_bytes == other.max_sz_bytes
                and self.min_nr_accesses == other.min_nr_accesses and
                self.max_nr_accesses == other.max_nr_accesses and
                self.nr_accesses_unit == other.nr_accesses_unit and
                self.min_age == other.min_age and self.max_age == other.max_age
                and self.age_unit == other.age_unit)

    def to_kvpairs(self):
        if self.nr_accesses_unit == 'percent':
            unit = '%'
        min_nr_accesses = '%s %s' % (
                _damo_fmt_str.format_nr(self.min_nr_accesses, False), unit)
        max_nr_accesses = '%s %s' % (
                _damo_fmt_str.format_nr(self.max_nr_accesses, False), unit)
        if self.age_unit == 'usec':
            min_age = _damo_fmt_str.format_time_us_exact(self.min_age, False)
            max_age = _damo_fmt_str.format_time_us_exact(self.max_age, False)
        else:
            min_age = '%s %s' % (
                    _damo_fmt_str.format_nr(self.min_age, False), self.age_unit)
            max_age = '%s %s' % (
                    _damo_fmt_str.format_nr(self.max_age, False), self.age_unit)

        return {
                'min_sz_bytes':
                    _damo_fmt_str.format_sz(self.min_sz_bytes, False),
                'max_sz_bytes':
                    _damo_fmt_str.format_sz(self.max_sz_bytes, False),
                'min_nr_accesses': min_nr_accesses,
                'max_nr_accesses': max_nr_accesses,
                'min_age': min_age,
                'max_age': max_age
                }

def kvpairs_to_DamosAccessPattern(kv):
    try:
        min_nr_accesses = _damo_fmt_str.text_to_percent(kv['min_nr_accesses'])
        max_nr_accesses = _damo_fmt_str.text_to_percent(kv['max_nr_accesses'])
        nr_accesses_unit = 'percent'
    except:
        min_nr_accesses, nr_accesses_unit = _damo_fmt_str.text_to_nr_unit(
                kv['min_nr_accesses'])
        max_nr_accesses, nr_accesses_unit = _damo_fmt_str.text_to_nr_unit(
                kv['max_nr_accesses'])

    try:
        min_age = _damo_fmt_str.text_to_us(kv['min_age'])
        max_age = _damo_fmt_str.text_to_us(kv['max_age'])
        age_unit = 'usec'
    except:
        min_age, age_unit = _damo_fmt_str.text_to_nr_unit(kv['min_age'])
        max_age, age_unit = _damo_fmt_str.text_to_nr_unit(kv['max_age'])

    return DamosAccessPattern(_damo_fmt_str.text_to_bytes(kv['min_sz_bytes']),
            _damo_fmt_str.text_to_bytes(kv['max_sz_bytes']), min_nr_accesses,
            max_nr_accesses, nr_accesses_unit, min_age, max_age, age_unit)

# every region.  could be used for monitoring
default_DamosAccessPattern =  DamosAccessPattern(
        'min', 'max', 'min', 'max', 'percent', 'min', 'max', 'usec')

class DamosQuotas:
    time_ms = None
    sz_bytes = None
    reset_interval_ms = None
    weight_sz_permil = None
    weight_nr_accesses_permil = None
    weight_age_permil = None

    def __init__(self, time_ms, sz_bytes, reset_interval_ms, weight_sz_permil,
            weight_nr_accesses_permil, weight_age_permil):
        self.time_ms = _damo_fmt_str.text_to_ms(time_ms)
        self.sz_bytes = _damo_fmt_str.text_to_bytes(sz_bytes)
        self.reset_interval_ms = _damo_fmt_str.text_to_ms(reset_interval_ms)
        self.weight_sz_permil = weight_sz_permil
        self.weight_nr_accesses_permil = weight_nr_accesses_permil
        self.weight_age_permil = weight_age_permil

    def __str__(self):
        return '\n'.join([
            '%s / %s per %s' % (
                _damo_fmt_str.format_sz(self.time_ms * 1000000, False),
                _damo_fmt_str.format_time_ns(self.sz_bytes, False),
                _damo_fmt_str.format_time_ms(self.reset_interval_ms, False)),
            'priority: sz %d permil, nr_accesses %d permil, age %d permil' % (
                self.weight_sz_permil, self.weight_nr_accesses_permil,
                self.weight_age_permil),
            ])

    def __eq__(self, other):
        return (type(self) == type(other) and self.time_ms == other.time_ms and
                self.sz_bytes == other.sz_bytes and self.reset_interval_ms ==
                other.reset_interval_ms and self.weight_sz_permil ==
                other.weight_sz_permil and self.weight_nr_accesses_permil ==
                other.weight_nr_accesses_permil and self.weight_age_permil ==
                other.weight_age_permil)

    def to_kvpairs(self):
        return {attr: getattr(self, attr) for attr in [
            'time_ms', 'sz_bytes', 'reset_interval_ms', 'weight_sz_permil',
            'weight_nr_accesses_permil', 'weight_age_permil']}

def kvpairs_to_DamosQuotas(kv):
    return DamosQuotas(kv['time_ms'], kv['sz_bytes'], kv['reset_interval_ms'],
            kv['weight_sz_permil'], kv['weight_nr_accesses_permil'],
            kv['weight_age_permil'])

# no limit
default_DamosQuotas = DamosQuotas(0, 0, 0, 0, 0, 0)

class DamosWatermarks:
    metric = None
    interval_us = None
    high_permil = None
    mid_permil = None
    low_permil = None

    def __init__(self, metric, interval_us, high, mid, low):
        # 'none' or 'free_mem_rate'
        self.metric = metric
        self.interval_us = _damo_fmt_str.text_to_us(interval_us)
        self.high_permil = high
        self.mid_permil = mid
        self.low_permil = low

    def __str__(self):
        return '\n'.join([
            '%s/%s/%s permil' % (self.high_permil, self.mid_permil,
                self.low_permil),
            'metric %s, interval %s' % (self.metric,
                _damo_fmt_str.format_time_us(self.interval_us, False))
            ])

    def __eq__(self, other):
        return (type(self) == type(other) and self.metric == other.metric and
                self.interval_us == other.interval_us and self.high_permil ==
                other.high_permil and self.mid_permil == other.mid_permil and
                self.low_permil == other.low_permil)

    def to_kvpairs(self):
        return {attr: getattr(self, attr) for attr in [
            'metric', 'interval_us', 'high_permil', 'mid_permil',
            'low_permil']}

def kvpairs_to_DamosWatermarks(kv):
    return DamosWatermarks(*[kv[x] for x in
        ['metric', 'interval_us', 'high_permil', 'mid_permil', 'low_permil']])

# no limit
default_DamosWatermarks = DamosWatermarks('none', 0, 0, 0, 0)

class DamosFilter:
    name = None
    filter_type = None  # anon or memcg
    memcg_path = None
    matching = None

    def __init__(self, name, filter_type, memcg_path, matching):
        self.name = name
        self.filter_type = filter_type
        self.memcg_path = memcg_path
        self.matching = matching

    def __str__(self):
        memcg_path_str = ''
        if self.filter_type == 'memcg':
            memcg_path_str = 'memcg_path %s, ' % self.memcg_path
        return 'filter_type %s, %smatching %s' % (
                self.filter_type, memcg_path_str, self.matching)

    def __eq__(self, other):
        return '%s' % self == '%s' % other

    def to_kvpairs(self):
        return {attr: getattr(self, attr) for attr in [
            'name', 'filter_type', 'memcg_path', 'matching']}

def kvpairs_to_DamosFilter(kv):
    return DamosFilter(kv['name'], kv['filter_type'],
            kv['memcg_path'] if kv['filter_type'] == 'memcg' else '',
            kv['matching'])

class DamosStats:
    nr_tried = None
    sz_tried = None
    nr_applied = None
    sz_applied = None
    qt_exceeds = None

    def __init__(self, nr_tried, sz_tried, nr_applied, sz_applied, qt_exceeds):
        self.nr_tried = nr_tried
        self.sz_tried = sz_tried
        self.nr_applied = nr_applied
        self.sz_applied = sz_applied
        self.qt_exceeds = qt_exceeds

    def __str__(self):
        return '\n'.join([
            'tried %d times (%s)' % (self.nr_tried,
            _damo_fmt_str.format_sz(self.sz_tried, False)),
            'applied %d times (%s)' % (self.nr_applied,
            _damo_fmt_str.format_sz(self.sz_applied, False)),
            'quota exceeded %d times' % self.qt_exceeds,
            ])

class DamosTriedRegion:
    start = None
    end = None
    nr_accesses = None
    age = None

    def __init__(self, start, end, nr_accesses, age):
        self.start = start
        self.end = end
        self.nr_accesses = nr_accesses
        self.age = age

    def __str__(self):
        return '%s: nr_accesses: %s, age: %s' % (
                _damo_fmt_str.format_addr_range(self.start, self.end, False),
                _damo_fmt_str.format_nr(self.nr_accesses, False),
                _damo_fmt_str.format_nr(self.age, False))

class Damos:
    name = None
    access_pattern = None
    action = None
    quotas = None
    watermarks = None
    filters = None
    stats = None
    tried_regions = None

    def __init__(self, name, access_pattern, action, quotas, watermarks,
            filters, stats, tried_regions=None):
        self.name = name
        self.access_pattern = access_pattern
        self.action = action
        self.quotas = quotas
        self.watermarks = watermarks
        self.filters = filters
        self.stats = stats
        self.tried_regions = tried_regions

    def __str__(self):
        lines = ['%s (action: %s)' % (self.name, self.action)]
        lines.append('target access pattern')
        lines.append(_damo_fmt_str.indent_lines('%s' % self.access_pattern, 4))
        lines.append('quotas')
        lines.append(_damo_fmt_str.indent_lines('%s' % self.quotas, 4))
        lines.append('watermarks')
        lines.append(_damo_fmt_str.indent_lines('%s' % self.watermarks, 4))
        lines.append('filters')
        for damos_filter in self.filters:
            lines.append(_damo_fmt_str.indent_lines('%s' % damos_filter, 8))
        lines.append('statistics')
        lines.append(_damo_fmt_str.indent_lines('%s' % self.stats, 4))
        if self.tried_regions != None:
            lines.append('tried regions')
            for region in self.tried_regions:
                lines.append(_damo_fmt_str.indent_lines('%s' % region, 4))
        return '\n'.join(lines)

    def __eq__(self, other):
        return (type(self) == type(other) and self.name == other.name and
                self.access_pattern == other.access_pattern and self.action ==
                other.action and self.quotas == other.quotas and
                self.watermarks == other.watermarks)

    def to_kvpairs(self):
        kv = {attr: getattr(self, attr) for attr in ['name', 'action']}
        kv['access_pattern'] = self.access_pattern.to_kvpairs()
        kv['quotas'] = self.quotas.to_kvpairs()
        kv['watermarks'] = self.watermarks.to_kvpairs()
        filters = []
        for damos_filter in self.filters:
            filters.append(damos_filter.to_kvpairs())
        kv['filters'] = filters
        return kv

def kvpairs_to_Damos(kv):
    filters = []
    if 'filters' in kv:
        for damos_filter_kv in kv['filters']:
            filters.append(kvpairs_to_DamosFilter(damos_filter_kv))
    return Damos(kv['name'],
            kvpairs_to_DamosAccessPattern(kv['access_pattern'])
                if 'access_pattern' in kv else default_DamosAccessPattern,
            kv['action'] if 'action' in kv else 'stat',
            kvpairs_to_DamosQuotas(kv['quotas'])
                if 'quotas' in kv else default_DamosQuotas,
            kvpairs_to_DamosWatermarks(kv['watermarks'])
                if 'watermarks' in kv else default_DamosWatermarks,
            filters,
            None, None)

default_Damos = kvpairs_to_Damos({'name': '0'})

class DamonRecord:
    rfile_buf = None
    rfile_path = None

    def __init__(self, rfile_buf, rfile_path):
        self.rfile_buf = _damo_fmt_str.text_to_bytes(rfile_buf)
        self.rfile_path = rfile_path

    def __str__(self):
        return 'path: %s, buffer sz: %s' % (self.rfile_path,
                _damo_fmt_str.format_sz(self.rfile_buf))

    def __eq__(self, other):
        return self.__str__() == other.__str__()

    def to_kvpairs(self):
        return {attr: getattr(self, attr) for attr in ['rfile_buf',
            'rfile_path']}

def kvpairs_to_DamonRecord(kv):
    return DamonRecord(kv['rfile_buf'], kv['rfile_path'])

class DamonCtx:
    name = None
    intervals = None
    nr_regions = None
    ops = None
    targets = None
    schemes = None
    # For old downstream kernels that supports record feature
    record_request = None

    def __init__(self, name, intervals, nr_regions, ops, targets, schemes):
        self.name = name
        self.intervals = intervals
        self.nr_regions = nr_regions
        self.ops = ops
        self.targets = targets
        self.schemes = schemes

    def __str__(self):
        lines = ['%s (ops: %s)' % (self.name, self.ops)]
        lines.append('intervals: %s' % self.intervals)
        lines.append('nr_regions: %s' % self.nr_regions)
        lines.append('targets')
        for target in self.targets:
            lines.append(_damo_fmt_str.indent_lines('%s' % target, 4))
        lines.append('schemes')
        for scheme in self.schemes:
            lines.append(_damo_fmt_str.indent_lines('%s' % scheme, 4))
        return '\n'.join(lines)

    def __eq__(self, other):
        return self.__str__() == other.__str__()

    def to_kvpairs(self):
        kv = {}
        kv['name'] = self.name
        kv['intervals'] = self.intervals.to_kvpairs()
        kv['nr_regions'] = self.nr_regions.to_kvpairs()
        kv['ops'] = self.ops
        kv['targets'] = [t.to_kvpairs() for t in self.targets]
        kv['schemes'] = [s.to_kvpairs() for s in self.schemes]
        if self.record_request:
            kv['record_request'] = self.record_request.to_kvpairs()
        return kv

def kvpairs_to_DamonCtx(kv):
    ctx = DamonCtx(kv['name'],
            kvpairs_to_DamonIntervals(kv['intervals'])
                if 'intervals' in kv else default_DamonIntervals,
            kvpairs_to_DamonNrRegionsRange(kv['nr_regions'])
                if 'nr_regions' in kv else default_DamonNrRegionsRange,
            kv['ops'],
            [kvpairs_to_DamonTarget(t) for t in kv['targets']],
            [kvpairs_to_Damos(s) for s in kv['schemes']]
                if 'schemes' in kv else [])
    if 'record_request' in kv:
        ctx.record_request = kvpairs_to_DamonRecord(kv['record_request'])
    return ctx

def target_has_pid(ops):
    return ops in ['vaddr', 'fvaddr']

class Kdamond:
    name = None
    state = None
    pid = None
    contexts = None

    def __init__(self, name, state, pid, contexts):
        self.name = name
        self.state = state
        self.pid = pid
        self.contexts = contexts

    def summary_str(self):
        return '%s (state: %s, pid: %s)' % (self.name, self.state, self.pid)

    def __str__(self):
        lines = [self.summary_str()]
        for ctx in self.contexts:
            lines.append('contexts')
            lines.append(_damo_fmt_str.indent_lines('%s' % ctx, 4))
        return '\n'.join(lines)

    def __eq__(self, other):
        return self.__str__() == other.__str__()

    def to_kvpairs(self):
        kv = {}
        kv['name'] = self.name
        kv['state'] = self.state
        kv['pid'] = self.pid
        kv['contexts'] = [c.to_kvpairs() for c in self.contexts]
        return kv

def kvpairs_to_Kdamond(kv):
    return Kdamond(kv['name'],
            kv['state'] if 'state' in kv else 'off',
            kv['pid'] if 'pid' in kv else None,
            [kvpairs_to_DamonCtx(c) for c in kv['contexts']])

# System check

features = ['record',       # was in DAMON patchset, but not merged in mainline
            'schemes',      # merged in v5.16
            'init_regions', # merged in v5.16 (90bebce9fcd6)
            'vaddr',        # merged in v5.15, thebeginning
            'fvaddr',       # merged in v5.19 (b82434471cd2)
            'paddr',        # merged in v5.16 (a28397beb55b)
            'init_regions_target_idx',  # merged in v5.18 (144760f8e0c3)
            'schemes_speed_limit',      # merged in v5.16 (2b8a248d5873)
            'schemes_quotas',           # merged in v5.16 (1cd243030059)
            'schemes_prioritization',   # merged in v5.16 (38683e003153)
            'schemes_wmarks',           # merged in v5.16 (ee801b7dd782)
            'schemes_stat_succ',        # merged in v5.17 (0e92c2ee9f45)
            'schemes_stat_qt_exceed',   # merged in v5.17 (0e92c2ee9f45)
            'schemes_tried_regions',    # developing on top of v6.0
            'schemes_filters',          # developing on top of v6.0
            ]

_damon_fs = None

pr_debug_log = False

def ensure_root_permission():
    if os.geteuid() != 0:
        print('Run as root')
        exit(1)

def feature_supported(feature):
    return _damon_fs.feature_supported(feature)

def initialize(args):
    global _damon_fs
    if args.damon_interface == 'sysfs':
        _damon_fs = _damon_sysfs
    elif args.damon_interface == 'debugfs':
        _damon_fs = _damon_dbgfs
    elif args.damon_interface == 'auto':
        if _damon_sysfs.supported():
            _damon_fs = _damon_sysfs
        else:
            _damon_fs = _damon_dbgfs

    global pr_debug_log
    if args.debug_damon:
        pr_debug_log = True

    return _damon_fs.update_supported_features()

initialized = False
def ensure_initialized(args):
    global initialized

    if initialized:
        return
    err = initialize(args)
    if err != None:
        print(err)
        exit(1)
    initialized = True

def damon_interface():
    if _damon_fs == _damon_sysfs:
        return 'sysfs'
    elif _damon_fs == _damon_dbgfs:
        return 'debugfs'
    print('something wrong')
    raise Exception

# DAMON fs read/write

def _damon_fs_root():
    if _damon_fs == _damon_dbgfs:
        return _damon_dbgfs.debugfs_damon
    return _damon_sysfs.admin_dir

def read_damon_fs():
    return _damo_fs.read_files_recursive(_damon_fs_root())

def write_damon_fs(contents):
    return _damo_fs.write_files({_damon_fs_root(): contents})

# DAMON status reading

def is_kdamond_running(kdamond_name):
    return _damon_fs.is_kdamond_running(kdamond_name)

def current_kdamonds():
    return _damon_fs.current_kdamonds()

def current_kdamond_names():
    return _damon_fs.current_kdamond_names()

def any_kdamond_running():
    for kd_name in current_kdamond_names():
        if is_kdamond_running(kd_name):
            return True
    return False

def every_kdamond_turned_off():
    return not any_kdamond_running()

def wait_current_kdamonds_turned(on_off):
    if not on_off in ['on', 'off']:
        print('wait_current_kdamonds_turned() called with \'%s\'' % on_off)
        exit(1)
    for kd_name in current_kdamond_names():
        running = is_kdamond_running(kd_name)
        while (on_off == 'on' and not running) or (
                on_off == 'off' and running):
            time.sleep(1)
            running = is_kdamond_running(kd_name)

# DAMON control

def apply_kdamonds(kdamonds):
    _damon_fs.apply_kdamonds(kdamonds)

def commit_inputs(kdamonds):
    if _damon_fs == _damon_dbgfs:
        print('debugfs interface unsupport commit_inputs()')
        exit(1)
    return _damon_fs.commit_inputs(kdamonds)

def update_schemes_stats(kdamond_name):
    return _damon_fs.update_schemes_stats(kdamond_name)

def update_schemes_tried_regions(kdamond_name):
    if _damon_fs == _damon_dbgfs:
        return 'DAMON debugfs doesn\'t support schemes tried regions'
    return _damon_fs.update_schemes_tried_regions(kdamond_name)

def turn_damon(on_off, kdamonds_names):
    err = _damon_fs.turn_damon(on_off, kdamonds_names)
    if err:
        return err
    # Early version of DAMON kernel turns it on/off asynchronously
    wait_current_kdamonds_turned(on_off)
