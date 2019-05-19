"""
    This script contains classes for antenna arrays

    This script requires that `numpy` be installed within the Python
    environment you are running this script in.

    This file can be imported as a module and contains the following
    class:

    * Linear_Array

    ----------
    Antarray - Antenna Array Analysis Module
    Copyright (C) 2018 - 2019  Zhengyu Peng
    E-mail: zpeng.me@gmail.com
    Website: https://zpeng.me

    `                      `
    -:.                  -#:
    -//:.              -###:
    -////:.          -#####:
    -/:.://:.      -###++##:
    ..   `://:-  -###+. :##:
           `:/+####+.   :##:
    .::::::::/+###.     :##:
    .////-----+##:    `:###:
     `-//:.   :##:  `:###/.
       `-//:. :##:`:###/.
         `-//:+######/.
           `-/+####/.
             `+##+.
              :##:
              :##:
              :##:
              :##:
              :##:
               .+:

"""

import numpy as np
from antarray import Antenna
from antarray import Antenna_Array


class Linear_Array(Antenna_Array):
    def __init__(self, size, spacing):
        self.size = size
        self.spacing = spacing
        antenna_list = []
        for idx in range(0, self.size):
            antenna_list.append(Antenna(x=idx*self.spacing, y=0))
        Antenna_Array.__init__(self, antenna_list)

    def get_pattern(self, theta, beam_loc=0, window=1):
        # window_type = linear_array_config['window_type_idx']
        # window_sll = linear_array_config['window_sll']
        # window_nbar = linear_array_config['window_nbar']

        weight = np.exp(-1j * 2 * np.pi * self.x * np.sin(
            beam_loc / 180 * np.pi))
        # * window_dict[
        # window_type](array_size, window_sll,
        #            window_nbar)

        weight = weight / np.sum(np.abs(weight))

        theta_grid, array_geometry_grid = np.meshgrid(
            theta, self.x)
        A = np.exp(1j * 2 * np.pi * array_geometry_grid * np.sin(
            theta_grid / 180 * np.pi))

        AF = 20 * np.log10(np.abs(np.matmul(weight, A)) + 0.00001)

        return AF

    def update_parameters(self, **kwargs):
        keys = ['size', 'spacing']
        self.__dict__.update((k, v) for k, v in kwargs.items() if k in keys)
        self.__init__(self.size, self.spacing)