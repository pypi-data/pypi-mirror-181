import numpy as np
from scipy.spatial.transform import Rotation
from .utils import RE_TOLERANCE, valid_dim

class ER:
    def __init__(self, name: str = '', dim: int = 3) -> None:
        '''
        The `__init__` function is called when a new instance of the `RE` class is created.
        It initializes all of the variables in the class and sets them to their default values.

        By default, the `self.__rotation` member value is set to an identity value.

        Parameters
        ----------
        - `name` (`str`): Set the name of the object (default: '')
        - `dim` (`int`): Set the dimension of the vector (default: 3)
        '''
        self.name = name
        self.__rotation = Rotation(quat=[0, 0, 0, 1])
        self.identity()

        if valid_dim(dim):
            self.__dim = dim

    # Setter functions
    def identity(self) -> None:
        '''
        The `identity` function sets the `self.__rotation` member to
        the equivalent of an identity matrix.
        '''
        self.__rotation = Rotation.identity()

    def inv(self) -> None:
        '''
        The `inv` function sets the `self.__rotation` member to its inverse.
        '''
        self.__rotation = self.__rotation.inv()

    def random(self) -> None:
        '''
        The `random` function sets the `self.__rotation` member to a random value.
        '''
        self.__rotation = Rotation.random()

    def from_quat(self, quat: np.ndarray|list) -> None:
        '''
        The `from_quat` function set the `self.__rotation` member from the value of
        the input `quat`.

        Note: This function will not work for `RE` objects that are defined in 2D space.

        Parameters
        ----------
        - `quat` (`np.ndarray|list`): Input quaternion
        '''
        if self.__dim == 2:
            raise AttributeError(f'Unable to set 2D rotation from quaternion input.')

        if len(quat) != 4:
            raise ValueError(f'Input vector shape must be equal to 4 (input shape: {len(quat)}).')

        self.__rotation = Rotation.from_quat(np.array(quat))

    def from_matrix(self, matrix: np.ndarray) -> None:
        '''
        The `from_matrix` function set the `self.__rotation` member from the value of
        the input `matrix`. The function will first check whether the input matrix dimensions
        are suitable for the number of dimensions set for the `RE` object.

        Parameters
        ----------
        - `matrix` (`np.ndarray`): Input matrix
        '''
        if matrix.shape != (self.__dim, self.__dim):
            raise ValueError(f'Input matrix shape must be ({self.__dim}, {self.__dim}) when rotation dimension is {self.__dim}. Current input matrix shape: {matrix.shape}.')

        if self.__dim == 2:
            matrix = np.hstack(np.array(matrix), np.zeros(2))
            matrix = np.vstack(np.array(matrix), [0, 0, 1])

        self.__rotation = Rotation.from_matrix(matrix)

    def from_angle_axis(self, angle_axis: np.ndarray) -> None:
        '''
        The `from_angle_axis` function set the `self.__rotation` member from the value of
        the input `angle_axis`.

        Note: This function will not work for `RE` objects that are defined in 2D space.

        Parameters
        ----------
        - `angle_axis` (`np.ndarray`): Input angle-axis vector
        '''
        if self.__dim == 2:
            raise AttributeError(f'Unable to set 2D rotation from angle-axis input.')

        if len(angle_axis) != 3:
            raise ValueError(f'Input vector shape must be equal to 3 (input shape: {len(angle_axis)}).')

        self.__rotation = Rotation.from_rotvec(np.array(angle_axis))

    def from_euler(self, sequence: str = None, angles: np.ndarray|list = None, degrees: bool = True) -> None:
        '''
        The `from_euler` function set the `self.__rotation` member from the value(s) of
        the inputs `sequence` and `angles`. The angle will be converted from degrees to
        radians if `degrees` is `True`.

        Parameters
        ----------
        - `sequence` (`str`): Sequence of euler angles (e.g. 'xyz', 'xy', 'zyx')
        - `angles` (`np.ndarray|list`): List of euler angles
        - `degrees` (`bool`): Set to true if input angles are in degrees (default: `True`)
        '''
        if angles is None:
            raise ValueError(f'Input angles cannot be None.')

        if self.__dim == 3:
            if sequence is None:
                raise ValueError(f'Input sequence cannot be None.')

            self.__rotation = Rotation.from_euler(sequence, np.array(angles), degrees)

        elif self.__dim == 2:
            self.__rotation = Rotation.from_euler('z', np.array(angles), degrees)

    # Getter functions
    def dim(self) -> int:
        '''
        Return the number of dimensions.

        Returns
        -------
        - `int`: Value of `self.__dim` member
        '''
        return self.__dim

    def as_quat(self) -> np.ndarray:
        '''
        Return the stored `self.__rotation` member in quaternion form.

        Returns
        -------
        - `np.ndarray`: Quaternion vector
        '''
        return self.__rotation.as_quat()

    def as_matrix(self) -> np.ndarray:
        '''
        Return the stored `self.__rotation` member in matrix form.

        Returns
        -------
        - `np.ndarray`: Rotation matrix
        '''
        return self.__rotation.as_matrix()[:self.__dim, :self.__dim]

    def as_angle_axis(self) -> np.ndarray:
        '''
        Return the stored `self.__rotation` member in angle-axis form.

        Returns
        -------
        - `np.ndarray`: Angle-axis vector
        '''
        return self.__rotation.as_rotvec()

    def as_euler(self, sequence: str = None, degrees: bool = True) -> np.ndarray|float:
        '''
        Return the stored `self.__rotation` member in euler angles.

        Parameters
        ----------
        - `sequence` (`str`): Sequence in which the euler angle will be returned
        - `degrees` (`bool`): Option to return euler angles in degrees or not

        Returns
        -------
        - `np.ndarray|float`: Euler angle(s) (if `RE` is in 2D then only a float will be returned)
        '''
        if self.__dim == 3:
            if sequence is None:
                raise ValueError(f'Input sequence cannot be None.')

            return self.__rotation.as_euler(sequence, degrees)

        elif self.__dim == 2:
            return self.__rotation.as_euler('z', degrees)[0]

    def yaw(self, degrees: bool = True) -> float:
        '''
        Return rotation angle around the z axis.

        Note: This function will not work for 2D rotations. It is recommended to use `as_euler()` instead.

        Parameters
        ----------
        - `degrees` (`bool`): Option to return value in degrees or radians (default: `True`)

        Returns
        -------
        - `float`: Yaw angle (in specified units)
        '''
        if self.__dim == 2:
            raise AttributeError(f'Unable to return yaw angle of 2D rotation (Call as_euler() instead).')

        return self.__rotation.as_euler('xyz', degrees)[2]

    def pitch(self, degrees: bool = True) -> float:
        '''
        Return rotation angle around the y axis.

        Note: This function will not work for 2D rotations. It is recommended to use `as_euler()` instead.

        Parameters
        ----------
        - `degrees` (`bool`): Option to return value in degrees or radians (default: `True`)

        Returns
        -------
        - `float`: Pitch angle (in specified units)
        '''
        if self.__dim == 2:
            raise AttributeError(f'Unable to return pitch angle of 2D rotation (Call as_euler() instead).')

        return self.__rotation.as_euler('xyz', degrees)[1]

    def roll(self, degrees: bool = True) -> float:
        '''
        Return rotation angle around the x axis.

        Note: This function will not work for 2D rotations. It is recommended to use `as_euler()` instead.

        Parameters
        ----------
        - `degrees` (`bool`): Option to return value in degrees or radians (default: `True`)

        Returns
        -------
        - `float`: Roll angle (in specified units)
        '''
        if self.__dim == 2:
            raise AttributeError(f'Unable to return roll angle of 2D rotation (Call as_euler() instead).')

        return self.__rotation.as_euler('xyz', degrees)[0]

    # Computation functions
    def apply(self, input: np.ndarray|list) -> np.ndarray:
        '''
        The `apply` function applies this rotation to `input` vector.

        Note: The dimension of the input vector must match the set dimension of the `RE` object.

        Parameters
        ----------
        - `input` (`np.ndarray|list`): Input vector to be rotated

        Returns
        -------
        - `np.ndarray`: Rotated vector
        '''
        input = np.array(input)

        # Check shape of input
        if input.shape[0] != self.__dim:
            raise ValueError(f'Input shape mismatch: self.__dim ({self.__dim}) != input.shape ({input.shape[0]})')

        return self.__rotation.apply(input)

    # Operator overloading
    def __str__(self) -> str:
        return f'RE - {self.name}: {self.__repr__()} degrees'

    def __repr__(self) -> str:
        if self.__dim == 3:
            sequence = 'xyz'
        if self.__dim == 2:
            sequence = 'z'

        return f'{self.as_euler(sequence, degrees=True)} degrees'

    def __eq__(self, other):
        if isinstance(other, ER):
            return np.allclose(self.as_quat(),
                               other.as_quat(),
                               rtol=RE_TOLERANCE,
                               atol=RE_TOLERANCE)
        else:
            raise TypeError(f'Input parameter is {type(other)}, not RE as expected.')

    def __ne__(self, other):
        if isinstance(other, ER):
            return not np.allclose(self.as_quat(),
                                   other.as_quat(),
                                   rtol=RE_TOLERANCE,
                                   atol=RE_TOLERANCE)
        else:
            raise TypeError(f'Input parameter is {type(other)}, not RE as expected.')
