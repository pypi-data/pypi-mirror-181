from .te import TE
from .re import RE

from .utils import valid_dim

class Pose:
    def __init__(self, name: str = '', te_dim: int = 3, re_dim: int = 3) -> None:
        '''
        The `__init__` function is called when a new instance of the `Pose` class is created.
        It initializes all of the variables in the class and sets them to their default values.
        
        Parameters
        ----------
        - `name` (`str`): Set the name of the object (default: '')
        - `te_dim` (`int`): Set the dimension of the position member (default: 3)
        - `re_dim` (`int`): Set the dimension of the orientation member (default: 3)
        '''
        self.name = name

        if valid_dim(te_dim):
            self.position = TE(dim=te_dim)

        if valid_dim(re_dim):
            self.orientation = RE(dim=re_dim)

    # Setter functions
    def random(self) -> None:
        '''
        Sets the position and orientation to random values.
        '''
        self.orientation.random()
        self.position.random()

    def zero(self) -> None:
        '''
        Sets the position vector to zero and orientation to identity.
        '''
        self.orientation.identity()
        self.position.zero()

    # Getter functions
    def dims(self) -> tuple[int, int]:
        '''
        Returns the dimensions of the position and orientation (in that order).

        Returns
        -------
        - `tuple[int, int]`: Dimension of position and orientation (in that order)
        '''
        return self.position.dim(), self.orientation.dim()

    # Operator overloads
    def __str__(self) -> str:
        return f'''Pose ({self.__dim}D) - {self.name}:
        Position:    {self.position.__repr__}
        Orientation: {self.orientation.__repr__}'''

    def __repr__(self) -> str:
        return f'Position:    {self.position.__repr__}\nOrientation: {self.orientation.__repr__}'

    def __eq__(self, other) -> bool:
        if isinstance(other, Pose) and other.__dim == self.__dim:
            return self.orientation == other.orientation and self.position == other.position
        else:
            return False

    def __ne__(self, other) -> bool:
        if isinstance(other, Pose) and other.__dim == self.__dim:
            return self.orientation != other.orientation or self.position != other.position
        else:
            return False