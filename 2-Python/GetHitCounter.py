
"""
Problem Description
Design a hit counter which counts the number of hits received in the past 5 minutes (i.e., the last 300 seconds).

Your system should accept a timestamp parameter (in seconds granularity), and you may assume that calls are being made 
to the system in chronological order (i.e., timestamp is monotonically increasing). You may also assume that the earliest
timestamp starts at 1.


Option 1: The Queue Approach (Best for Low Volume)
This is the most intuitive. We store hits in a list and pop them from the front once they are older than 300 seconds.

Very simple to implement.
If you have 1 million hits in one second, the queue grows to 1 million elements. getHits becomes slow because it
has to potentially pop millions of items.

Option 2: The Circular Array
"""

from collections import deque


class hitCounter():
    
    def __init__(self):
        self.hits = deque()
        
    def hit(self, timestamp: int) -> None:
        self.hits.append(timestamp)
        
    def getHits(self, timestamp: int) -> int:
        while self.hits and timestamp - self.hits[0] >= 300:
            self.hits.popleft()
        return len(self.hits)



class HitCounter:
    def __init__(self):
        self.buckets = [[0, 0] for _ in range(300)]

    def hit(self, timestamp: int) -> None:
        idx = timestamp % 300
        time_at_idx, count_at_idx = self.buckets[idx]
        if time_at_idx == timestamp:
            self.buckets[idx][1] += 1
        else:
            self.buckets[idx][0] = timestamp
            self.buckets[idx][1] = 1

    def getHits(self, timestamp: int) -> int:
        total_hits = 0
        for i in range(300):
            time_at_idx, count_at_idx = self.buckets[i]
            if timestamp - time_at_idx < 300:
                total_hits += count_at_idx
        return total_hits
