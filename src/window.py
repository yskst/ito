#!/bin/env python

def get_window(srate, wsize, shift):
    """
    get window queue
    srate: sampling rate[khz]
    wsize: window size[msec]
    shift: shift width[msec]
    """
    queue_size = srate * wsize
    queue_shift = srate * shift
    q = windowQueue(queue_size)
    return q, queue_size, queue_shift


class windowQueue:
    def __init__(self, size):
        self.__queue__ = [0 for i in range(size)]
        self.__size__ = size
    
    def push(self, elem):
            self.__queue__.append(elem)
            return self.__queue__.pop(0)

    def npush(self, elems):
        """
        push multiple emlements
        """
        self.__queue__.extends(elems)
        while len(self.__queue__) != self.size:
            self.__queue__.pop(0)
    
    def get_queue(self):
        return self.__queue__

def main(argv):
    from optparse import OptionParser
    import fileinput
    parser = OptionParser(description="segmentation")
    parser.add_option('-r', '--srate', type=int, default=16, help="sampling rate(unit: khz)")
    parser.add_option('-w', '--wsize', type=int, default=25, help="window size(unit: ms)")
    parser.add_option('-s', '--shift', type=int, default=10, help="window shift size(uniq: ms)")
    (opts, args) = parser.parse_args(argv)

    (w, w_nsample, w_nshift) = get_window(opts.srate, opts.wsize, opts.shift)
    with fileinput.input(files=args[1:]) as f:
        # とりあえずキューを満たす
        for i in range(w_nsample):
            data = next(f).strip()
            if data[0] == '#':
                continue
            w.push(data)

        try:
            while True:
                print(' '.join(w.get_queue()))
                for i in range(w_nshift):
                    data = next(f).strip()
                    if data[0] == '#':
                        continue
                    w.push(data)
        except StopIteration:
            # 入力がEOFに達したら終了
            pass

if __name__=='__main__':
    import sys
    main(sys.argv)
