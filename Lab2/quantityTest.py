# This is a performance test file.
# C:\Users\tay\Desktop\LAB2.cpp
import cProfile
from codeForPerformanceTest import getResult

if __name__ == '__main__':
    cProfile.run('getResult(1)')
    cProfile.run('getResult(2)')
    cProfile.run('getResult(3)')
    cProfile.run('getResult(4)')
