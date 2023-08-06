RE_TOLERANCE = 1e-10
TE_TOLERANCE = 1e-10

def valid_dim(input_dim: int) -> bool:
    valid_dims = [1, 2, 3]

    if input_dim not in valid_dims:
        raise ValueError(f'Input value for dim argument ({input_dim}) is not valid. Use one of the following: {valid_dims}.')
        
    else:
        return True

VALID_ROTATION_TYPES = ['euler', 'quaternion', 'angle-axis', 'matrix', 'rodrigues']