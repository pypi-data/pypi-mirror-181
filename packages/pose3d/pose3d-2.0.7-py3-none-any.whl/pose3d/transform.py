import numpy as np

from .te import TE
from .re import RE

from .pose import Pose

from .utils import valid_dim

class Transform:
    def __init__(self, name: str, orig: str = 'origin', dest: str = 'destination', te_dim: int = 3, re_dim: int = 3) -> None:
        # Set strings
        self.name = name
        self.origin = orig
        self.destination = dest

        # Init translation and rotation memebers
        if valid_dim(te_dim):
            self.translation = TE(dim = te_dim)

        if valid_dim(re_dim):
            self.rotation = RE(dim = re_dim)

    # Setter functions
    def between_poses(self, pose_1: Pose, pose_2: Pose) -> None:
        '''
        Compute transform between 2 3D poses. This instance of Transform
        will be modifed to compute the transform from pose_1 to pose_2.

        Parameters
        ----------
        - `pose_1` (`Pose`): Origin pose.
        - `pose_2` (`Pose`): Destination pose.
        '''
        if pose_1.dims() != pose_2.dims():
            raise AttributeError(f'Number of dimensions between both poses do not match: pose_1.dims() = {pose_1.dims()} and pose_2.dims = {pose_2.dims()}.')

        # Modify dimension of transformation depending on pose_1 and pose_2
        if pose_1.position.dim() != self.translation.dim():
            self.translation = TE(dim=pose_1.position.dim())

        if pose_1.orientation.dim() != self.rotation.dim():
            self.rotation = RE(dim=pose_1.orientation.dim())

        # Compute rotation from pose_1 to pose_2
        self.rotation.from_matrix(np.linalg.inv(pose_2.orientation.as_matrix()) * pose_1.orientation.as_matrix())
        self.translation.from_vector(pose_2.position.vector() - pose_1.position.vector())

    def identity(self) -> None:
        '''
        Set the transformation to zero and the rotation to identity.
        '''
        self.translation.zero()
        self.rotation.identity()
        
    def inv(self) -> None:
        '''
        Set the transformation it's inverse.
        '''
        self.rotation = self.rotation.inv()
        self.translation.from_vector(-self.rotation.apply(self.translation.vector()))

    def random(self) -> None:
        '''
        Set a random transformation.
        '''
        self.translation.random()
        self.rotation.random()
    
    # Getter functions
    def dims(self) -> tuple[int, int]:
        '''
        Returns the dimensions of the translation and rotation (in that order).

        Returns
        -------
        - `tuple[int, int]`: Dimension of translation and rotation (in that order)
        '''
        return self.translation.dim(), self.rotation.dim()

    def matrix(self, homogeneous: bool = True) -> np.ndarray:
        '''
        Return the transformation matrix.

        Returns
        -------
        - `np.ndarray`: Transformation matrix
        '''
        matrix = np.eye(max(self.dims()) + 1)
        
        if self.origin != self.destination:
            matrix[:self.rotation.dim(), :self.rotation.dim()] = self.rotation.as_matrix()
            matrix[:self.translation.dim(), -1] = self.translation.vector()

        if not homogeneous:
            return matrix[:-1, :]
        
        return matrix

    # Computation functions
    def apply(self, io: Pose|np.ndarray) -> Pose|np.ndarray:
        '''
        Apply transformation to `io`.

        Parameters
        ----------
        - `io` (`Pose | np.ndarray`): Element to apply transformation to

        Returns
        -------
        - `Pose|np.ndarray`: Output pose/vector
        '''

        # If io is a Pose
        if isinstance(io, Pose):
            io.orientation.from_matrix(np.matmul(self.rotation.as_matrix(), io.orientation.as_matrix()))
            io.position += self.translation

        # If io is a numpy vector
        if isinstance(io, np.ndarray):
            io = self.rotation.apply(io) + self.translation

        return io

    # Operator overloads
    def __repr__(self) -> str:
        return f'''Transform - {self.name}:
        Position:    {self.position.__repr__}
        Orientation: {self.orientation.__repr__}'''

    def __str__(self) -> str:
        return f'Translation: {self.position.__repr__}\nRotation:    {self.orientation.__repr__}'

    def __eq__(self, other: object) -> bool:
        return self.translation == other.translation and self.rotation == other.rotation

    def __ne__(self, other: object) -> bool:
        return self.translation != other.translation or self.rotation != other.rotation