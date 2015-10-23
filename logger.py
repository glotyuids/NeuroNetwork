# -*- coding: utf-8 -*-
import time,os

class Logger(object):
    """docstring for Logger"""
    def __init__(self, score, history, tm, logfile = 'log',folder = 'Logs'):
        super(Logger, self).__init__()
        self.log_folder = folder
        if self.log_folder[-1] != os.sep:
            self.log_folder += os.sep
        try:
            os.mkdir(self.log_folder)
        except:
            pass
        self.logfile = logfile+'.txt'
        self.f = open(self.log_folder+self.logfile,'w')
        #score = neuronet,position,field,porson,score
        self.dv = '#'
        self.history = history
        self.time = tm
        if score is None:
            self.neuronet, self.position, self.field, self.person, self.score = None, None, None, None, None
        else:
            self.neuronet, self.position, self.field, self.person, self.score = score

    def log_neuronet(self):
        self.f.write(str(self.neuronet)+'\n')

    def log_divider(self,l = 20):
        self.f.write(self.dv*l+'\n')

    def header(self,str,l = 20):
        self.log_divider()
        self.f.write(self.dv + ' '*(l-len(self.dv)*2)+self.dv+'\n')
        self.f.write(self.dv +str.center(l-len(self.dv)*2)+self.dv+'\n' )
        self.f.write(self.dv + ' '*(l-len(self.dv)*2)+self.dv+'\n')
        self.log_divider()
        self.f.write('\n')

    def log_field(self):
        a = ''
        # print len(self.field.layers[2])
        for n,i in enumerate(self.field.layers[2][:]):
            for j in i:
                a += str(j).rjust(3)
            a+='\n'
        self.f.write(str(a))
        self.f.write('\n')

    def log_history(self):
        self.f.write('Person score:'.ljust(14)+str(self.score)+'\n')
        self.f.write('Scores:'.ljust(14)+str(self.history)+'\n')
        self.f.write('Time:'.ljust(14)+str(self.time))
        # self.f.write('Scores:'.ljust(14)+str(self.history))

    def log_person(self):
        self.f.write(str(self.person)+'\n')

    def log(self):
        if self.neuronet:
            self.header('Neuronet')
            self.log_neuronet()
        if self.field:
            self.header('Field')
            self.log_field()
        if self.person:
            self.header('Person')
            self.log_person()
        if self.history:
            self.header('History')
            self.log_history()

    def __del__(self):
        self.f.close()

if __name__ == '__main__':
    a = Logger(None,[1,2,3,4,5],100,'test', folder = os.path.join('test'))
    a = Logger(None,[1,2,3,4,5],100,'test', folder = os.path.join('test','test2'))
    del a
        