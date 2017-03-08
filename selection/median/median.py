#!/usr/bin/env python3

import heapq


class Median(object):
    def __init__(self):
        self.heap_low = []
        self.heap_high = []
        self._median = 0

    def _update(self):
        self._balance()
        self.median()

    def _push_to_heap_low(self, num):
        self.heap_low.append(num)
        heapq._siftdown_max(self.heap_low, 0, len(self.heap_low) - 1)

    def _heapified_heap_low(self):
        self.heap_low_heapified = list(self.heap_low)
        heapq._heapify_max(self.heap_low_heapified)
        return self.heap_low_heapified

    def _push_to_heap_high(self, num):
        heapq.heappush(self.heap_high, num)

    def heappush(self, num):
        if num < self._median:
            self._push_to_heap_low(num)
            # self.heap_low = self._heapified_heap_low()
        else:
            self._push_to_heap_high(num)
        self._update()

    def _balance(self):
        while len(self.heap_high) - len(self.heap_low) > 1:
            self.heap_low.append(heapq.heappop(self.heap_high))
            heapq._siftdown_max(self.heap_low, 0, len(self.heap_low) - 1)
        while len(self.heap_low) - len(self.heap_high) > 1:
            heapq.heappush(self.heap_high, heapq.heappop(self.heap_low))
            heapq._siftup_max(self.heap_low, 0)

    def median(self):
        heaps_same_size = len(self.heap_high) == len(self.heap_low)
        if heaps_same_size:
            if len(self.heap_low) or len(self.heap_high):
                self._median = self.heap_low[0] if len(self.heap_low) else self.heap_high[0]
        else:
            larger = self.heap_high if len(self.heap_high) > len(self.heap_low) else self.heap_low
            self._median = larger[0]
        return self._median

    def heappushmedian(self, num):
        self.heappush(num)
        return self.median()


if __name__ == '__main__':
    medians = []
    heap = Median()
    import ipdb; ipdb.set_trace()
    with open('median.txt') as f:
        for lineno, line in enumerate(f):
            print(lineno, int(line.strip()))
            median = heap.heappushmedian(int(line.strip()))
            medians.append(median)
    print(len(medians))
    print(sum(medians) % 10000)

