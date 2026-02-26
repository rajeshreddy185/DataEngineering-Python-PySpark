from typing import List

"""
Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.

Example 1:

Input: nums = [2,7,11,15], target = 18
h={}

for k,v in ((0,2),(1,7),(2,11),(3,15)):
    d = 18 - 2
    if 16 in keys?
       yes: 
          return [h[d], v]
       no:
         h[d], k
         .
         .
         .
    h={2:0,7:1, 11:2, 15:3 }
    d = 18 - 7
    if 11 in keys?
       yes: 
          return [h[d], v]
       no:
         h[d], k
return[]
   
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].
Example 2:

Input: nums = [3,2,4], target = 6
Output: [1,2]
Example 3:

Input: nums = [3,3], target = 6
Output: [0,1]
 

Constraints:

2 <= nums.length <= 104
-109 <= nums[i] <= 109
-109 <= target <= 109
"""
#brute force method

class Solution:

    def two_sum(self, nums: List[int], target: int) -> List[int]:
        l = len(nums)
        for i in range(l):
            for j in range(i + 1 ,l):
                if nums[i] + nums[j] == target:
                    print("Two sum index", [i,i])
                    return [i, j]
        print("No Two sum index")
        return []

    def two_sum_optimised(self, nums: List[int], target: int) -> List[int]:
        prev_val = {}
        for k,v in enumerate(nums):
            diff = target - v
            if diff in prev_val.keys():
                print("Two sum index",[prev_val[diff], k])
                return [prev_val[diff], k]
            prev_val[v] = k
        print("No Two sum index")
        return []

    def two_sum_optm(self, nums: List[int], target: int) -> List[int]:
        hmap = {}
        for i in range(len(nums)):
            hmap[nums[i]] = i
        for i in range(len(nums)):
            diff = target - nums[i]
            if diff in hmap and hmap[diff] != i:
                print("Two sum index",[i, hmap[diff]])
                return [i, hmap[diff]]
        print("No Two sum index")
        return []


s = Solution()
s.two_sum([1,2,3,4,43], 5)
s.two_sum_optimised([1,2,3,4,43], 5)
s.two_sum_optm([1,2,3,4,43], 5)



