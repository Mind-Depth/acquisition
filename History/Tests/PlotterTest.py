#!/usr/local/bin/python3

import unittest
import matplotlib.pyplot as plt
import numpy as np

class TestPlotting(unittest.TestCase):
        
    def test_plotting_fear(self):
        fearSpan = []
        prevLength = 0

        nextLength = len(plt.plot(fearSpan, 'r')[0].get_data()[1])
        self.assertEqual(nextLength, prevLength) #fearSpan is still empty so plotting should not do anything

        prevLength = nextLength
        fearSpan.extend([np.nan for i in range(10)])
        nextLength = len(plt.plot(fearSpan, 'r')[0].get_data()[1])
        self.assertGreater(nextLength, prevLength) #fearSpan now has more points to plot so plotted length should be greater than before

        prevLength = nextLength
        nextLength = len(plt.plot(fearSpan, 'r')[0].get_data()[1])
        self.assertEqual(nextLength, prevLength) #fearSpan has not been modified since previous plotting so the length should be the same