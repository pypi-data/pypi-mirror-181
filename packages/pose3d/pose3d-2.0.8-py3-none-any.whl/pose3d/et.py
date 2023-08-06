import numpy as np

from .utils import valid_dim

class ET:
    def __init__(self, name: str = '', dim: int = 3, vector: np.ndarray|list = None) -> None:
        '''
        The `__init__` function is called when a new instance of the `TE` class is created.
        It initializes all of the variables in the class and sets them to their default values.

        By default, the `self.__vector` member value is set to zero.
        
        Parameters
        ----------
        - `name` (`str`): Set the name of the object (default: '')
        - `dim` (`int`): Set the dimension of the vector (default: 3)
        - `vector` (`np.ndarray|list`): Set value of vector at `__init__` (default: `None`)
        '''
        self.name = name

        if valid_dim(dim):
            self.__dim = dim

        if vector is None:
            self.__vector = np.zeros(self.__dim)
        else:
            if valid_dim(len(vector)):
                self.__dim = len(vector)
                self.__vector = np.array(vector)

    # Setter functions
    def random(self) -> None:
        '''
        The `random` function sets the `self.__vector` member to a random state.
        '''
        self.from_vector(np.random.rand(self.__dim))

    def from_vector(self, vector: np.ndarray|list) -> None:
        '''
        The `from_vector` function sets the `self.__vector` to the input vector.

        The function also checks whether the input dimension matches the class dimension.

        Parameters
        ----------
        - `vector` (`np.ndarray|list`): Input vector
        '''
        vector = np.array(vector)
        if vector.shape != self.__vector.shape:
            raise ValueError(f'Input vector dimension ({vector.shape[0]}) does not match the set dimension ({self.__vector.shape[0]}).')
        
        self.__vector = vector

    def zero(self) -> None:
        '''
        The `zero` function sets the `self.__vector` to zero.
        '''
        self.from_vector(np.zeros(self.__dim))

    def inv(self) -> None:
        '''
        The `inv` function sets the `self.__vector` member to its inverse (negative value).
        '''
        self.from_vector(-self.vector())

    # Getter functions
    def dim(self) -> int:
        '''
        Return the number of dimensions.

        Returns
        -------
        - `int`: Value of `self.__dim` member
        '''
        return self.__dim

    def vector(self) -> np.ndarray:
        '''
        Return the value of the `self.__vector` member.

        Returns
        -------
        - `np.ndarray`: Value of `self.__vector` member
        '''
        return self.__vector

    def x(self) -> float:
        '''
        Return the first element of the `self.__vector` member.

        Returns
        -------
        - `float`: First element of the `self.__vector` member
        '''
        return float(self.vector()[0])

    def y(self) -> float:
        '''
        Return the second element of the `self.__vector` member.

        Returns
        -------
        - `float`: Second element of the `self.__vector` member
        '''
        return float(self.vector()[1])

    def z(self) -> float:
        '''
        Return the third element of the `self.__vector` member.

        Note: This function will only work for `TE` classes set to 3 dimensions.

        Returns
        -------
        - `float`: Third element of the `self.__vector` member
        '''
        return float(self.vector()[2])

    # Operator overloads
    def __str__(self) -> str:
        return f'TE{self.__dim} - {self.name}: {self.vector()}'

    def __repr__(self) -> str:
        return f'{self.vector()}'

    def __add__(self, other):
        if isinstance(other, ET):
            if other.vector().shape == self.vector().shape:
                return ET(name=f'Sum of {self.name} and {other.name}',
                          vector=self.vector() + other.vector())

        elif isinstance(other, np.ndarray):
            if other.shape == self.vector().shape:
                return ET(name=self.name,
                           vector=self.vector() + other)

        else:
            raise TypeError(f'Input parameter is {type(other)}, not TE or np.ndarray as expected.')

    def __sub__(self, other):
        if isinstance(other, ET):
            if other.vector().shape == self.vector().shape:
                return ET(name=f'Sum of {self.name} and {other.name}',
                          vector=self.vector() - other.vector())

        elif isinstance(other, np.ndarray):
            if other.shape == self.vector().shape:
                return ET(name=self.name,
                           vector=self.vector() - other)

        else:
            raise TypeError(f'Input parameter is {type(other)}, not TE or np.ndarray as expected.')

    def __iadd__(self, other):
        if isinstance(other, ET):
            if other.vector().shape == self.vector().shape:
                self.from_vector(self.vector() + other.vector())

        elif isinstance(other, np.ndarray):
            if other.shape == self.vector().shape:
                self.from_vector(self.vector() + other)

        else:
            raise TypeError(f'Input parameter is {type(other)}, not TE or np.ndarray as expected.')

    def __isub__(self, other):
        if isinstance(other, ET):
            if other.vector().shape == self.vector().shape:
                self.from_vector(self.vector() - other.vector())

        elif isinstance(other, np.ndarray):
            if other.shape == self.vector().shape:
                self.from_vector(self.vector() - other)

        else:
            raise TypeError(f'Input parameter is {type(other)}, not TE or np.ndarray as expected.')

    def __eq__(self, other):
        if isinstance(other, ET):
            return np.array_equal(self.vector(), other.vector())
            
        elif isinstance(other, np.ndarray):
            return np.array_equal(self.vector(), other)

        else:
            raise TypeError(f'Input parameter is {type(other)}, not TE or np.ndarray as expected.')

    def __ne__(self, other):
        if isinstance(other, ET):
            return not np.array_equal(self.vector(), other.vector())
            
        elif isinstance(other, np.ndarray):
            return not np.array_equal(self.vector(), other)

        else:
            raise TypeError(f'Input parameter is {type(other)}, not TE or np.ndarray as expected.')

    def __neg__(self):
        self.from_vector(-self.vector())

    def __abs__(self):
        self.from_vector(abs(self.vector()))