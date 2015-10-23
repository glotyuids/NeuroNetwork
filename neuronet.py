# -*- coding:utf-8 -*-
from layer import Layer
import random

MIN_LAYERS_NUM = 3
MAX_LAYERS_NUM = 10

DEPTH = 0
PS = '-'
PST = PS * DEPTH


class NeuroNet(object):
    """network over neurons"""

    def __init__(self, input_num, output_num, lnum=3, delta=0):
        super(NeuroNet, self).__init__()
        self.input_layer = Layer(input_num)
        self.output_layer = Layer(output_num)

        self.layers = [Layer()]
        self.connect_layers(self.input_layer, self.layers[0])
        for i in xrange(lnum - 1):
            self.layers.append(Layer())
            self.connect_layers(self.layers[-2], self.layers[-1])

        self.connect_layers(self.layers[-1], self.output_layer)
        for i in self.layers:
            i.modify(-1)
            # for i in i.neurons:
            #   print i
        self.set_input_delta(delta)

    def set_input(self, inp_arr):
        self.input_layer.set_input(inp_arr)
        # return False

    def calculate(self, steps=10):
        for i in xrange(steps):
            self.input_layer.calculate()
            for j in self.layers:
                j.calculate()
            self.output_layer.calculate()
        return self.output_layer.get_value()

    """
    Соединить два слоя последовательно
    """

    def connect_layers(self, l1, l2):
        l1.connect(l2)
        return True

    """
    Добавить новый слой между двумя существующими, заданных индексами позиции
    """

    def add_layer_indx(self, layer=None, prev_layer_indx=0, next_layer_indx=0):
        # if len(self.layers) >= MAX_LAYERS_NUM:
        #   return False
        if not (0 <= prev_layer_indx < len(self.layers) and 0 <= next_layer_indx < len(self.layers)):
            return False
        # if layer == None:
        #   layer = Layer(next = self.layers[next_layer_indx])
        # self.layers.append(layer)
        # self.connect_layers(self.layers[prev_layer_indx],layer)
        self.add_layer(layer, self.layers[prev_layer_indx], self.layers[next_layer_indx])
        return True

    """
    Добавить слой в случайное место
    """

    def rand_add_layer_indx(self, layer=None, np=0):  # 0 - both, 1 - only directly, 2 - only backward
        if len(self.layers) < 2:
            pli = self.layers
        pli, nli = random.sample(range(len(self.layers)), 2)
        if ((np == 1) and (nli < pli)) or ((np == 2) and (nli > pli)):
            pli, nli = nli, pli
        self.add_layer_indx(layer, pli, nli)
        return True

    """
    Добавить слой между двумя заданными слоями, заданных объектами (main)
    """

    def add_layer(self, layer=None, prev_layer=None, next_layer=None):
        if len(self.layers) >= MAX_LAYERS_NUM:
            return False
        if (prev_layer is None) or (next_layer is None):
            return False
        if layer == None:
            layer = Layer(next=next_layer)
        else:
            if (next_layer in layer.next_layer) or (prev_layer in layer.prev_layer):
                print 'DA',
                return False
        self.layers.append(layer)
        self.connect_layers(prev_layer, layer)
        layer.modify(-1)  # add random weight
        return True

    """ 
    Получить слой из общей карты слоев, включая:
    - входной (0); 
    - промежуточные (1..n);
    - выходной (n+1); """

    def get_layer(self, num):
        if num == 0:
            return self.input_layer
        if num == len(self.layers) + 1:
            return self.output_layer
        return self.layers[num - 1]

    """
    Удалить слой, заданный объектом
    """

    def del_layer(self, layer):
        layer.remove_connections()
        if layer in self.layers:
            self.layers.remove(layer)
        return True

    """
    Удалить слой, заданный индексом
    """

    def delete(self, num):
        if len(self.layers) <= MIN_LAYERS_NUM:
            return False
        if 0 <= num <= len(self.layers) - 1:
            # try:
            self.del_layer(self.layers[num])
            # except Exception, e:
            #   print self.layers[num].history
            #   raise e
            return True
        else:
            return False

    """
    Изменение случайного слоя
    """

    def rand_modify_layer(self, tp):
        random.choice(self.layers).modify(tp)
        return True

    """
    Добавление случайного слоя
    """

    def rand_add_layer(self, layer=None, np=0):  # 0 - both, 1 - only directly, 2 - only backward
        pli, nli = random.sample(range(len(self.layers) + 2), 2)
        print pli, nli
        if ((np == 1) and (nli < pli)) or ((np == 2) and (nli > pli)):
            pli, nli = nli, pli
        self.add_layer(layer, self.get_layer(pli), self.get_layer(nli))
        return True

    """
    Удаление случайного слоя
    """

    def rand_del_layer(self):
        return self.delete(random.randint(0, len(self.layers) - 1))

    """
    Изменение параметров нейросети
    tp - type of modify neuronet; 1-add,2-del,3-modify layers
    atp1 - additional type
    """

    def modify(self, tp, atp=0, atp1=0):
        # print tp,atp,atp1
        if tp == 0:
            self.rand_add_layer(np=atp)
        elif tp == 1:
            self.rand_del_layer()
        elif tp == 2:
            self.rand_modify_layer(atp)
        return True

    def set_input_delta(self, const):
        self.input_layer.set_delta(const)
        # self.input_layer.neurons[n].constant_input = float(const)

    def __str__(self):
        s = ''
        s += PST + 'Input  Layer:'.ljust(14) + `self.input_layer` + '\n' + str(self.input_layer) + '\n\n'
        s += PST + 'Output Layer:'.ljust(14) + `self.output_layer` + '\n' + str(self.output_layer) + '\n\n'
        s += PST + 'Other  Layers:\n'
        for n, i in enumerate(self.layers):
            s += PST + '>Layer' + `n` + ': ' + `i` + '\n' + str(i) + '\n'
        return s


if __name__ == '__main__':
    nn = NeuroNet(8, 4)
    print nn
    c = []
    # c.append([0]*8)
    c.append([1] * 8)
    c.append([0] * 8)
    c.append([0, 0, 0, 0, 0, 0, 0, 1])
    nn.set_input_delta(-0.5)
    for i in c:
        nn.set_input(i)  # set input for neuronet
        # print '\n\n'+'#'*20+'\n\n'
        # print nn
        out = nn.calculate(steps=10)  # calculate output for neuronet
        print out


        # for i in xrange(3):
        #   nn.rand_add_layer()
        # for i in nn.layers:
        #   print `i`,':\n',i,'\n'
        # print '-- DELETED --'
        # nn.delete(2)
        # for i in nn.layers:
        #   print `i`,':\n',i,'\n'
        # print nn
