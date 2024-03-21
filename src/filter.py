"""
Low-pass filter.

Reference: https://github.com/ObjectOops/mollusc-personal/blob/fcfb2dfadf87f6d9b333f3e1be489a0d6c2b803f/utility/Filter.java
"""

class LowPassFilter:

    def __init__(self, initial_value: float, gain: float):
        self.previous_estimate = initial_value
        self.gain = gain

    def out(self, current_value: float) -> float:
        ret = gain * self.previous_estimate + (1 - gain) * current_value
        previous_estimate = ret
        return ret
