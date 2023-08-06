# -*- encoding:utf-8 -*-
"""
    横截面下因子评估方式
"""
import copy, functools, pdb
import numpy as np
from collections import namedtuple
from ultron.utilities.logger import kd_logger
from ultron.kdutils.progress import Progress

DALIY_PER_YEAR = 252
WEEKLY_PER_YEAR = 52
MONTHLY_PER_YEAR = 12
QUARTERLY_PER_YEAR = 4
YEARLY_PER_YEAR = 1

OLNY_LONG = 'long'
OLNY_SHORT = 'short'
BOTH_SIDE = 'both'

POSITIVE = 1
NEGATIVE = -1


class EvaluateTuple(
        namedtuple('EvaluateTuple',
                   ('returns_mean', 'returns_std', 'sharp', 'turnover',
                    'maxdd', 'returns_mdd', 'win_rate', 'ic', 'ir', 'fitness',
                    'category', 'freq'))):

    __slots__ = ()

    def __repr__(self):
        return "\nreturns_mean:{}\nreturns_std:{}\nsharp:{}\nturnover:{}\n" \
                "maxdd:{}\nreturns_mdd:{}\nwin_rate:{}\nic:{}\nir:{}\nfitness:{}\n" \
                "category:{}\nfreq:{}".format(self.returns_mean,self.returns_std,
                    self.sharp,self.turnover,self.maxdd,self.returns_mdd,self.win_rate,
                    self.ic,self.ir,self.fitness,self.category,self.freq)


class MetricsTuple(
        namedtuple(
            'EvaluateTuple',
            ('long_evaluate', 'short_evaluate', 'both_evaluate', 'freq'))):
    __slots__ = ()

    def __repr__(self):
        return "long_evaluate:{}\nshort_evaluate:{}\nboth_evaluate:{},freq:{}".format(
            self.long_evaluate, self.short_evaluate, self.both_evaluate,
            self.freq)


def valid_check(func):
    """检测度量的输入是否正常，非正常显示info，正常继续执行被装饰方法"""

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.valid:
            return func(self, *args, **kwargs)
        else:
            kd_logger.info('metrics input is invalid or zero order gen!')

    return wrapper


class Metrics(object):

    @classmethod
    def general(cls, returns, factors, freq=DALIY_PER_YEAR, show_log=True):
        metrics = cls(returns=returns,
                      factors=factors,
                      freq=freq,
                      show_log=show_log)
        return metrics.fit_metrics()

    def __init__(self, returns, factors, freq=DALIY_PER_YEAR, show_log=True):
        # 验证输入的数据是否可度量，便于valid_check装饰器工作
        self.valid = False
        self.returns = returns
        self.factors = factors
        self.freq = freq
        self.show_log = show_log
        if self.returns is not None and self.factors is not None:
            self.valid = True

    @valid_check
    def fit_metrics(self):
        with Progress(3, 0, label='factor fit metrics') as progress:
            long_weight, short_weight, both_weight = self.create_weight()
            if self.show_log: progress.show(a_progress=1)
            long_evaluate = self.evaluate(returns=self.returns,
                                          weight=long_weight,
                                          freq=self.freq,
                                          category=OLNY_LONG)
            if self.show_log: progress.show(a_progress=2)
            short_evaluate = self.evaluate(returns=self.returns,
                                           weight=short_weight,
                                           freq=self.freq,
                                           category=OLNY_SHORT)
            if self.show_log: progress.show(a_progress=3)
            both_evaluate = self.evaluate(returns=self.returns,
                                          weight=both_weight,
                                          freq=self.freq,
                                          category=BOTH_SIDE)

            self.show_log: progress.show(a_progress=4)
        return MetricsTuple(long_evaluate=long_evaluate,
                            short_evaluate=short_evaluate,
                            both_evaluate=both_evaluate,
                            freq=self.freq)

    def create_weight(self):
        right_weight = copy.deepcopy(self.factors)
        right_weight[right_weight <= 0] = np.nan
        right_weight = right_weight.div(right_weight.sum(axis=1, min_count=1),
                                        axis='rows')

        left_weight = copy.deepcopy(self.factors)
        left_weight[left_weight >= 0] = np.nan
        left_weight = left_weight.div(left_weight.sum(axis=1, min_count=1),
                                      axis='rows')

        both_weight = right_weight.sub(left_weight, fill_value=0)
        ret_diff = (self.returns * right_weight).sum(
            axis=1).mean() - (self.returns * left_weight).sum(axis=1).mean()
        if ret_diff > 0:
            self.direction = POSITIVE
            long_weight = copy.deepcopy(right_weight)
            short_weight = copy.deepcopy(left_weight)
        else:
            self.direction = NEGATIVE
            long_weight = copy.deepcopy(left_weight)
            short_weight = copy.deepcopy(right_weight)
            both_weight = copy.deepcopy(-both_weight)

        return long_weight, short_weight, both_weight

    def evaluate(self,
                 returns,
                 weight,
                 freq=DALIY_PER_YEAR,
                 category=OLNY_LONG):
        rets_sum = (returns * weight).sum(axis=1)
        rets_mean = rets_sum.mean() * freq
        rets_std = rets_sum.std() * np.sqrt(freq)
        sharp = rets_mean / rets_std
        tv = abs(weight.sub(weight.shift(1), fill_value=0)).sum(
            axis=1, min_count=1).mean() * 0.5
        pnl = rets_sum.cumsum()
        maxdd = (pnl.expanding().max() - pnl).max()
        ret2mdd = rets_mean / maxdd
        win_rate = rets_sum[
            rets_sum > 0].count() / rets_sum[~rets_sum.isna()].count()
        ic_series = weight.corrwith(returns, axis=1, method='spearman')
        ic = ic_series.mean()
        ir = ic / ic_series.std()
        fitness = sharp * np.sqrt(abs(rets_mean) / tv)

        return EvaluateTuple(returns_mean=rets_mean,
                             returns_std=rets_std,
                             sharp=sharp,
                             turnover=tv,
                             maxdd=maxdd,
                             returns_mdd=ret2mdd,
                             win_rate=win_rate,
                             ic=ic,
                             ir=ir,
                             fitness=fitness,
                             category=category,
                             freq=freq)
