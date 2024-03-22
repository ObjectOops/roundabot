"""
Low-pass filter and color conversion utility.

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

def rgb2hsv(r: float, g: float, b: float) -> tuple[float, float, float]:
    v = ma = max(r, g, b)
    mi = min(r, g, b)
    s = (ma - mi) / ma
    t = 0
    if ma == r:
        t = 0 + (g - b) / (ma - mi)
    elif ma == g:
        t = 2 + (b - r) / (ma - mi)
    elif ma == b:
        t = 4 + (r - g) / (ma - mi)
    h = 60 * t
    if h < 0:
        h += 360
    return (h, s, v)
