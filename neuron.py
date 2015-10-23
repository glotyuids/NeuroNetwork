# -*- coding:utf-8 -*-
"""
Y = F(sum(X)) -> u = sum(X); y = F(u)
"""

import math
import random
from params import *

DEPTH = 5
PS = ' '
PST = PS * DEPTH


class Neuron(object):
    """simple implementation of neuron model"""

    def __init__(self, alpha=None, is4alpha=False, af=None):
        super(Neuron, self).__init__()
        self.af = af
        if af is None:
            self.af = DEFAULT_TYPE  # type of F-function
        self.alpha = alpha
        if alpha is None:
            self.alpha = 0.75
        self.axon = {}  # y - axon; neuron:weight
        self.input = 0.0  # signal from synapse
        self.value = 0.0
        self.constant_input = 0.0
        self.delta = 0.0
        self.is4alpha = is4alpha
        if is4alpha:
            self.value = 1.0
        self.funcs = {
            TYPE_SIGMOID_BP: (self.sigmoid_h, [self.alpha]),
            TYPE_SIGMOID_UP: (self.sigmoid_e, [self.alpha]),
            TYPE_LINEAR_BP: (self.linear, [-1, 1, self.alpha]),
            TYPE_LINEAR_UP: (self.linear, [0, 1, self.alpha]),
            TYPE_RELAY_BP: (self.relay, [-1, 1]),
            TYPE_RELAY_UP: (self.relay, [0, 1])
        }
        # print self.funcs

    """
    Проверка на вхождение _val_ в диапазон (mn .. mx), иначе - возврат mx или mn
    """

    def __check_range(self, mn, mx, val):
        if val < mn:
            return mn
        if val > mx:
            return mx
        return val

    """
    Установка нового значения для alpha
    """

    def set_alpha(self, value):
        if MIN_VALUE_ALPHA <= value <= MAX_VALUE_ALPHA:
            self.alpha = value
        return True

    """
    Добавление значения нейрону
    """

    def add(self, value):
        self.input += value
        return True

    """
    Соединение нейронов
    """

    def connect(self, neuron=None, val=None):
        if val == None:
            val = DEFAULT_WEIGHT
        self.axon[neuron] = val

    """
    Рассоединение нейронов
    """

    def disconnect(self, neuron):  # """ WRONG! Cant find error!"""
        # try:
        del self.axon[neuron]
        # except Exception, e:
        # pass
        return True

    """
    Сигмоида (логистическая функция)
    """

    def sigmoid_e(self, alpha, x):
        return 1.0 / (1 + math.exp(-1 * (1. / alpha) * x))

    """
    Сигмоида (гиперболический тангенс)
    """

    def sigmoid_h(self, alpha, x):
        # print x
        return math.tanh(x / float(self.alpha))

    """
    Линейная функция с зоной насыщения
    """

    def linear(self, mn, mx, alpha, x):
        return self.__check_range(mn, mx, alpha * x)

    """
    Релейная функция
    """

    def relay(self, mn, mx, x):
        if x < 0:
            return mn
        return mx

    """
    Отработка функции активации
    """

    def f(self, x):
        if self.af in self.funcs:
            return self.funcs[self.af][0](*(self.funcs[self.af][1] + [x]))
        return self.relay(-1, 1, x)  # if error if

    """
    Установка нового значения alpha для следующих нейронов
    """

    def process_alpha(self):
        for i in self.axons:
            i.set_alpha(self.axons[i] * i.value)

    """
    Обработка дендрита каждого соединенного нейрона следующего слоя
    """

    def process_neurons(self):
        for i in self.axon:
            i.add(self.value * self.axon[i])

    """
    Соединение аксона с дендритами следующего слоя
    """

    def add_next_layer(self, neurons, wg=None):
        if wg == None:
            wg = DEFAULT_WEIGHT
        for i in neurons:
            self.axon[i] = wg

    """
    Удаление связи аксона с нейронами следующего слоя
    """

    def delete_next_layer(self, neurons):
        # try:
        for i in neurons:
            self.disconnect(i)
            # except Exception, e:
            # print self
            # print neurons
            # print i
            #   raise e

    """
    Вычисление текущего значения нейрона и установка аксона
    """

    def calculate(self):
        if self.is4alpha:
            for i in self.axon:
                i.set_alpha(self.axon[i])
            return True
        # print 'input neuron',self.input
        # if self.delta:
        #   print self.delta
        self.value = self.f(self.input + self.delta)
        self.input = self.constant_input
        self.process_neurons()
        return True

    def set_delta(self, c):
        self.delta = float(c)

    """
    Модификация нейрона (генетический алгоритм)
    """

    def modify(self, tp):
        if tp == 0:
            for i in self.axon:
                self.axon[i] = random.random() * 2 - 1
            return True
        elif tp == 1:
            self.af == random.randint(1, MAX_TYPE)
            return True
        return False

    """
    Todo: Gauss connection
    """

    def set_input(self, n):
        self.constant_input = n

    def __str__(self):
        s = ''
        s += PST + 'Is alpha:'.ljust(14) + `self.is4alpha` + '\n'
        s += PST + 'Input:'.ljust(14) + `self.input` + '\n'
        s += PST + 'Value:'.ljust(14) + `self.value` + '\n'
        s += PST + 'Weights:'.ljust(14) + `self.axon` + '\n'
        s += PST + 'Activation:'.ljust(14) + `self.af` + '\n'
        s += PST + 'Alpha:'.ljust(14) + `self.alpha`
        return s


if __name__ == '__main__':
    N1 = Neuron()
    N2 = Neuron()
    N1.connect(N1)
    N1.add(1)
    for i in xrange(10):
        N1.calculate()
        print N1.value
