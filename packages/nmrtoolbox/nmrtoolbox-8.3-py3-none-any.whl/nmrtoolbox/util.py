from dataclasses import dataclass
from collections import defaultdict
import numpy as np

class PeakOutsideOfMaskError(Exception):
    # use this when the position of a Peak is outside of the ppm ranges covered by a Mask
    pass


class ParsePeakTableError(Exception):
    pass


@dataclass
class Range:
    """
    Store a min and max value to define a range
    """
    min: float
    max: float

    def contains(self, val):
        """
        Check if value is in range
        :param val: value to check (float or int)
        :return: bool
        """
        if not isinstance(val, (float, int)):
            raise TypeError('must enter a float or int')
        return self.min <= val <= self.max


class Data:
    def __init__(self, name, value, unit):
        # NOT using @dataclass because it requires explicit typing; want to allow value to be int, float, str, etc.
        self.name = name
        self.value = value
        self.unit = unit

    def get(self, field):
        try:
            return self.__getattribute__(field)
        except AttributeError:
            raise AttributeError(f'invalid field: {field}')

    def print(self):
        print(f"{self.name} = {str(self.value)} [{self.unit}]")


class TableData:
    def __init__(self):
        self.data = {}

    def set(self, name, value, unit=None):
        self.data[name] = Data(name=name, value=value, unit=unit)

    def get(self, name):
        try:
            return self.data[name]
        except KeyError as e:
            raise KeyError(e)

    def print(self):
        [d.print() for d in self.data.values()]


class AxisData:
    def __init__(self):
        """dictionary of axis names where the values are dictionaries of Data objects"""
        self.data = defaultdict(dict)

    def axis_list(self):
        return list(self.data.keys())

    def set(self, axis, name, value, unit=None):
        axis = axis.upper()
        self.data[axis][name] = Data(name=name, value=value, unit=unit)

    def set_data(self, data):
        if not isinstance(data, AxisData):
            raise TypeError('input must be of type AxisData')
        for ax in data.axis_list():
            self.data[ax] = {**self.data[ax], **data.data[ax]}

    def get(self, name, axis=None):
        """
        Return an AxisData object that only contains data for the desired "name" and "axis"
        name: property name
        axis: name of axis (str) or list of axis names
        """
        if axis is None:
            ax_list = self.axis_list()
        else:
            if not isinstance(axis, list):
                axis = [axis]
            try:
                ax_list = [ax.upper() for ax in axis]
            except AttributeError:
                raise AttributeError(f"axis should probably be 'X', 'Y', 'Z' or similar. unable to use: {str(axis)}")

        out = AxisData()
        try:
            for ax in ax_list:
                out.data[ax][name] = self.data[ax][name]
        except KeyError as e:
            raise KeyError(e)
        return out

    def get_field(self, name, axis=None, field='value'):
        # get the AxisData object containing just the desired "name"
        # extract out just the .value data and return that as a list
        data_out = self.get(axis=axis, name=name)
        return [data_out.data[ax][name].get(field) for ax in data_out.axis_list()]

    def print(self):
        for axis in self.axis_list():
            print(f"axis = {axis}")
            [d.print() for d in self.data[axis].values()]


class ROI:
    def __init__(self, axis_list, range_list):
        """
        Define a region of interest (ROI) by giving the min/max values along each axis
        :param axis_list: axis names (e.g. use 'X', 'Y', 'Z' as used by PeakTable)
        :param range_list: list or tuple containing a min/max list or tuple for each axis
        """
        # if there is only one axis, then convert singleton inputs into lists
        if not isinstance(axis_list, (list, tuple)):
            axis_list = [axis_list]
        if not isinstance(range_list[0], (list, tuple)):
            range_list = [range_list]
        if not all(len(r) == 2 for r in range_list):
            raise ValueError('must enter a min/max ppm value for each axis as a list of lists')

        if len(axis_list) != len(range_list):
            raise ValueError('must enter a min/max ppm value for each axis')

        # dictionary to contain range values for each axis
        # it is best to access this data through self.range() which can allow no inputs (i.e. get the entire _range
        # dict) or take an input to specify a single axis (i.e. get the Range object for that axis)
        self._range = dict()
        for axis, vals in zip(axis_list, range_list):
            if not isinstance(vals, (list, tuple)):
                raise TypeError(f'must provide the min/max values as a list or tuple for axis: {axis}')
            if len(vals) != 2:
                raise ValueError(f'must provide min and max as a tuple or list of 2 values for axis: {axis}')
            try:
                # make sure the "min" field gets the minimum value and "max" field gets maximum value
                # (regardless of order given).   NMR people are strange in how they orient these values
                self._range[axis] = Range(
                    min=float(min(vals)),
                    max=float(max(vals)),
                )
            except ValueError:
                raise ValueError(f'could not convert ROI range values into floats: {range_list}')

    def axis_list(self):
        return self._range.keys()

    def range(self, axis=None):
        if axis is None:
            # default => return entire _range dictionary
            return self._range
        else:
            try:
                return self._range[axis]
            except KeyError:
                raise KeyError(f'axis not found: {axis}')
            except TypeError:
                raise TypeError('axis should be a string')


def weightedL2(a, b, w):
    """weighted norm of vectors a and b using weighting coefficients from w"""
    q = a - b
    return np.sqrt((w * q * q).sum())


def pairwise_weighted_norm(A, B, w=None):
    """
    A and B are matrices where each row is a vector of n dimensions.
    w is a vector of length n containing weighting factors for an L2 norm
    """
    if not (isinstance(A, np.ndarray) and isinstance(B, np.ndarray)):
        raise TypeError('must provide inputs as numpy.array')
    rowA, colA = A.shape
    rowB, colB = B.shape
    if colA != colB:
        raise ValueError('A and B must have same number dimensions in each column vector')

    if w is not None:
        try:
            w = np.asarray(w)
        except:
            raise TypeError('weights must be provided as data type that can be converted to numpy.array')
    else:
        w = np.ones(colA)
    numW = len(w)

    if numW != colA:
        raise ValueError('w must have the same number of weighting factors as A and B have dimensions')

    N = np.zeros((rowA, rowB))
    for indexA, a in enumerate(A):
        for indexB, b in enumerate(B):
            N[indexA][indexB] = weightedL2(a, b, w)
    return N


def pairwise_weighted_norm2(A, B, w=None):
    """
    A and B are matrices where each row is a vector of n dimensions.
    w is a vector of length n containing weighting factors for an L2 norm
    """
    if not (isinstance(A, np.ndarray) and isinstance(B, np.ndarray)):
        raise TypeError('must provide inputs as numpy.array')
    rowA, colA = A.shape
    rowB, colB = B.shape
    if colA != colB:
        raise ValueError('A and B must have same number dimensions in each column vector')

    if w is not None:
        try:
            w = np.asarray(w)
        except:
            raise TypeError('weights must be provided as data type that can be converted to numpy.array')
    else:
        w = np.ones(colA)
    numW = len(w)

    if numW != colA:
        raise ValueError('w must have the same number of weighting factors as A and B have dimensions')

    N = np.zeros((rowA, rowB))
    for indexA, a in enumerate(A):

        Q = B - a
        N[indexA] = np.sqrt((w * np.matmul(Q, Q.T)).sum())

    return N