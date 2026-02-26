"""
Roman numerals are represented by seven different symbols: I, V, X, L, C, D and M.

Symbol       Value
I             1
V             5
X             10
L             50
C             100
D             500
M             1000
For example, 2 is written as II in Roman numeral, just two ones added together. 12 is written as XII, which is simply X + II. The number 27 is written as XXVII, which is XX + V + II.

Roman numerals are usually written largest to smallest from left to right. However, the numeral for four is not IIII. Instead, the number four is written as IV. Because the one is before the five we subtract it making four. The same principle applies to the number nine, which is written as IX. There are six instances where subtraction is used:

I can be placed before V (5) and X (10) to make 4 and 9.
X can be placed before L (50) and C (100) to make 40 and 90.
C can be placed before D (500) and M (1000) to make 400 and 900.
Given a roman numeral, convert it to an integer.



Example 1:

Input: s = "III"
Output: 3
Explanation: III = 3.
Example 2:

Input: s = "LVIII"
Output: 58
Explanation: L = 50, V= 5, III = 3.
Example 3:

Input: s = "MCMXCIV"
Output: 1994
Explanation: M = 1000, CM = 900, XC = 90 and IV = 4.


"""


class romanConverter():

    def __init__(self, roman_num: str):
        self.mapping  = {
            'I' : 1,
        'V' : 5,
        'X' : 10,
        'L' : 50,
        'C' : 100,
        'D' : 500,
        'M' : 1000
        }
        self.roman_num = roman_num


    def roman_convert(self):
        numbers = []

        for each in self.roman_num:
            numbers.append(self.mapping[each])
        total = 0
        n = len(numbers)-1
        while n >= 0:
            if n > 0 and numbers[n - 1] < numbers[n]:
                total = total + numbers [n] - numbers[n -1]
                n = n - 2
                continue
            else:
                total = total + numbers[n]
                n = n - 1

        print(total)
        return total

    def roman_convert_opt(self):
        numbers = []
        total = 0
        for each in self.roman_num:
            numbers.append(self.mapping[each])

        for i in range(len(numbers)):
            if i + 1 < len(numbers) and numbers[i] < numbers[i+1]:
                total -= numbers[i]
            else:
                total += numbers[i]

        print(total)
        return total

roman_num = "MCMXCIV"

c = romanConverter(roman_num)
c.roman_convert()
c.roman_convert_opt()

