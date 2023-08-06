"""
-----------------------------------------------------------------------------------------
Signal module
-----------------------------------------------------------------------------------------
Provides signal class.

### Author: 

Alejandro Alcaine Otín, Ph.D.
    lalcaine@usj.es"""

# DEPENDENCIES
from typing import Any, Callable

import numpy as np


class Signal:
    """Signal class as a container of np.ndarrays and attributes.
    
    Signal is inmutable."""

    # STATICS
    @staticmethod
    def __checker(data: np.ndarray | list = None) -> np.ndarray:
        """Private static method to manage input data.

        Args:
            data (np.ndarray | List, optional): Data to check.
            Defaults to None.

        Raises:
            TypeError: data is not list nor ndarray.

        Returns:
            np.ndarray: formated input data.
        """
        if data is None:
            return np.array([], ndmin=2)
        elif isinstance(data, list):
            if not (data and isinstance(data[0], list)):
                return np.array(data, ndmin=2).T
            else:
                conv = np.array(data)
                if conv.shape[0] < conv.shape[1]:
                    return conv.T
                return conv
        elif isinstance(data, np.ndarray):
            if len(data.shape) == 1:
                return data[:, np.newaxis]
            elif data.shape[0] < data.shape[1]:
                return data.T
            else:
                return data
        else:
            raise TypeError("data is not list nor ndarray.")

    # CONSTRUCTOR
    def __init__(self, data: np.ndarray | list = None, **kargs: dict[str, Any]) -> None:
        """Constructor.

        Args:
            data (np.ndarray | List, optional): Signal data (column form).
            Defaults to None.

            kargs (dict[str,Any], optional): Keyword arguments to become instance attributes.
        """
        self.__data = self.__checker(data)
        self.__dict__.update(kargs)

    # DUNDERS
    def __repr__(self) -> str:
        """Class representation.

        Returns:
            str: NumPy's data array representation.
        """
        return self.__data.__repr__()

    def __str__(self) -> str:
        """Class string parsing.

        Returns:
            str: Data array NumPy's string parsing.
        """
        return self.__data.__str__()

    def __iter__(self) -> Any:
        """Iterate over data.

        Returns:
            Any: Elements of the data ndarray.

        Yields:
            Iterator[Any]: Iterator to iterate.
        """
        for i in self.__data:
            yield i

    def __eq__(self, obj: "Signal") -> bool:
        """Equality testing.

        Args:
            obj (Signal): Signal object to compare.

        Returns:
            bool: Whether two Signal objects are equal or not.
        """
        common = set()
        for key in self.__dict__:
            if key in obj.__dict__:
                if isinstance(self.__dict__[key], np.ndarray) or isinstance(
                    obj.__dict__[key], np.ndarray
                ):
                    if np.array_equal(self.__dict__[key], obj.__dict__[key]):
                        common.add(key)
                else:
                    if self.__dict__[key] == obj.__dict__[key]:
                        common.add(key)

        return (
            len(set(self.__dict__.keys()).union(set(obj.__dict__.keys())) - common) == 0
            and self.__data == obj.signal
        )

    def __ne__(self, obj: "Signal") -> bool:
        """Inequality testing.

        Args:
            obj (Signal): Signal object to compare.

        Returns:
            bool: Whether two Signal objects are different or not.
        """
        return not self == obj

    def __getitem__(self, key: Any) -> np.ndarray:
        """Indexing and slicing.

        Args:
            key (Any): index or slice indexes.

        Returns:
            np.ndarray: _description_

        TO-DO: Allow channel-based slicing
        """

        return self.__data[key].copy()

    # PROPERTIES
    @property
    def size(self) -> int:
        """Property 'size'.

        Returns:
            int: Size of the data array.
        """
        return self.__data.size

    @property
    def shape(self) -> tuple:
        """Property 'shape'.

        Returns:
            tuple: Shape of the array (samples,signals).
        """
        return self.__data.shape

    @property
    def signal(self) -> np.ndarray:
        """Property 'signal'.

        Returns:
            np.ndarray: Copy of stored data array.
        """
        return self.__data.copy()
    
    @property
    def time_vector(self) -> np.ndarray:
        """Property 'time_vector'

        Returns:
            np.ndarray: Time vector of the signal.
        """
        try:
            return np.arange(0,self.num_samp)/self.sf
        except AttributeError:
            return np.arange(0,self.num_samp)

    @property
    def T(self) -> np.ndarray:
        """Transpose operator from NumPy.

        Returns:
            np.ndarray: Transposed copy of data array.
        """
        return self.__data.copy().T

    @property
    def num_signals(self) -> int:
        """Property 'num_signals'.

        Returns:
            int: Number of signals.
        """
        return self.__data.shape[1]

    @property
    def num_samp(self) -> int:
        """Property 'num_samp'.

        Returns:
            int: Number of samples of each signal.
        """
        return self.__data.shape[0]

    # METHODS
    def max(self, **kargs: Any) -> Any:
        """Maximum value of data.

        Args:
            kargs: Keyword arguments of NumPy's .max() method.

        Returns:
            Any: Minimum value of data according to NumPy's .max() method.
        """
        return self.__data.max(**kargs)

    def min(self, **kargs: Any) -> Any:
        """Minimum value of data.

        Args:
            kargs: Keyword arguments of NumPy's .min() method.

        Returns:
            Any: Minimum value of data according to NumPy's .min() method.
        """
        return self.__data.min(**kargs)

    def copy(self) -> "Signal":
        """Copy the object.

        Returns:
            Signal: Copy of the object.
        """
        attrs = {
            key: value for key, value in self.__dict__.items() if key != "_Signal__data"
        }
        return Signal(self.signal, **attrs)

    def process(self, func: Callable, *args: Any, **kargs: Any) -> "Signal":
        """Process a signal using a function.

        Args:
            func (Callable): Function to process the signal.

            *args (Any): Positional arguments of func.

            **kargs (Any): Keyword arguments of func.

        Returns:
            Signal: Processed signal object.
        """
        attrs = {
            key: value for key, value in self.__dict__.items() if key != "_Signal__data"
        }
        data = func(*args, **kargs)
        return Signal(data, **attrs)

    def set_signal(self, data: np.ndarray | list = None, **kargs: Any) -> None:
        """Setter method for modifying the stored data and attributes.

        Args:
            data (np.ndarray | List, optional): Signal data to modify (column form).
            Defaults to None.

            kargs (Any, optional): Attributes to be modified.
        """
        self.__data = self.__checker(data)
        self.__dict__.update(kargs)

    def get_signal_gain(self) -> np.ndarray:
        """Get a copy of the signal with gain (if not available, this is identical to
        the attribute 'signal')

        Returns:
            np.ndarray: Copy of the signal with gain.
        """
        try:
            return self.signal * self.gain
        except AttributeError:
            return self.signal