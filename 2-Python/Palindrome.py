"""
121

convert this to list
if its 1 digit just a number

if its 2 digit num if 1st == 2nd ?

if len of list is odd
  loop through 1st, last
               1st +1 , last -1
               till len/2 -1
               if all are same then
            return palindrome
if len of list is even
    loop through 1st, last
               1st +1 , last -1
               till len/2
               if all are same then
            return palindrome


math-based approach

initial State
x = 12221
original = 12221
reversed_num = 0

Iteration 1:
- Get last digit: x % 10 → 12221 % 10 = 1
- Build reversed: (0 * 10) + 1 = 1
- Peel off digit: x //= 10 → 12221 // 10 = 1222
- State: x = 1222, reversed_num = 1

Iteration 2:
- Get last digit: 1222 % 10 = 2
- Build reversed: (1 * 10) + 2 = 12
- Peel off digit: 1222 // 10 = 122
- State: x = 122, reversed_num = 12

Iteration 3:
- Get last digit: 122 % 10 = 2
- Build reversed: (12 * 10) + 2 = 122
- Peel off digit: 122 // 10 = 12
- State: x = 12, reversed_num = 122

Iteration 4:
- Get last digit: 12 % 10 = 2
- Build reversed: (122 * 10) + 2 = 1222
- Peel off digit: 12 // 10 = 1
- State: x = 1, reversed_num = 1222

Iteration 5:
- Get last digit: 1 % 10 = 1
- Build reversed: (1222 * 10) + 1 = 12221
- Peel off digit: 1 // 10 = 0
- State: x = 0, reversed_num = 12221

Final Check:
- The loop terminates because x is no longer > 0
- Comparison: original (12221) == reversed_num (12221)
- Result: True


"""

class Solution:
    def isPalindromeStr(self, x: str) -> bool:
        if x[::] == x[::-1]:
            print("Yes! a palindrome isPalindromeStr")
            return True
        else:
            print("Not a palindrome isPalindromeStr")
            return False

    def isPalindrome(self, s: str) -> bool:
        x, y = 0, len(s)-1
        while x < y:
            if s[x] != s[y]:
                print("Not a palindrome isPalindrome")
                return False
            x = x + 1
            y = y - 1
        print("Yes! a palindrome isPalindrome")
        return True



    def isPalindrome_opt(self, x: int) -> bool:
        original = x
        reversed_num = 0
        while x > 0:
            reversed_num = (reversed_num * 10)+(x%10)
            print("rev num", reversed_num)
            print("x", x)
            x = x//10
            print("X", x)
        if reversed_num == original:
            print("Yes! a palindrome isPalindrome_opt")
            return True
        else:
            print("Not a palindrome isPalindrome_opt")
            return False



s = Solution()

s.isPalindrome('12221')
s.isPalindromeStr('12221')
s.isPalindrome_opt(112211)