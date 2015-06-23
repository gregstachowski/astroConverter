from time import sleep, time


def start():
    return time() * 1000


def end(t):
    return time()*1000 - t


#@perftest
def perftest(f):
    def new_f(*args, **kws):
        _t = start()
        returns = f(*args, **kws)
        _t = end(_t)
        print("%s took %s ms" % (f.__name__, _t)) 
        return returns
    return new_f

@perftest
def bum():
    sleep(1)
    
if __name__ == '__main__':
    pass