from itertools import combinations
from sympy import Matrix, sqrt


def is_vector(m: Matrix) -> bool:
    '''Checks that a matrix is a vector.'''
    return m.rows == 1 or m.cols == 1


def norm(vector: Matrix):
    '''Calculates the length/norm of a vector'''
    if not is_vector(vector):
        raise ValueError("Input must be a vector.")

    return sqrt(sum(v**2 for v in vector))


def dist(v: Matrix, u: Matrix):
    '''Calculates the euclidean distance between two vectors.'''
    if not is_vector(v) and not is_vector(u):
        raise ValueError("input are not vectors.")

    return sqrt(sum((vi - ui)**2 for vi, ui in zip(v, u)))


def is_orthogonal(vectors: list[Matrix]):
    """Takes a list of vectors and checks if they form an orthogonal set."""
    for v, u in combinations(vectors, 2):
        if v.dot(u) != 0:
            return False

    return True


def is_orthonormal(vectors: list[Matrix]):
    '''Takes a list of vectors and checks if they form an orthonormal set.'''
    for v in vectors:
        if v.dot(v) != 1:
            return False

    return is_orthogonal(vectors)


def orthonormalize(vectors: list[Matrix]):
    '''Checks that a list of vectors form an orthogonal set and normalizes it
to create an orthonormal set.'''
    if not is_orthogonal(vectors):
        raise ValueError("Input does not constitute an orthogonal set.")

    for v in vectors:
        yield v / norm(v)


def moore_penrose(A: Matrix, b: Matrix):
    '''Calculates the Moore-Penrose Pseudo-inverse.'''
    if not is_vector(b):
        raise ValueError("Input: 'b' is not a vector.")

    A_T = A.transpose()
    return (A_T * A).inv() * A_T * b


def least_squares_error(A: Matrix, b: Matrix, x_hat: Matrix = None):
    '''Calculates the Least-Squares Error (LSE).'''
    if x_hat is None:
        x_hat = moore_penrose(A, b)

    return norm(b - A*x_hat)


def least_squares_fit(xs: list[float], ys: list[float], degree: int = 1):
    '''Performs (polynomial) least-squares fitting.'''
    def _design_matrix(xs: list[float], degree: int = 1):
        '''Constructs a design matrix, X, of nth-degree'''
        return [[1] + [x**d for d in range(1, degree+1)] for x in xs]

    y = Matrix(ys)

    X = Matrix(_design_matrix(xs, degree))
    X_T = X.transpose()

    A_aug = (X_T * X).row_join(X_T*y)

    result, _ = A_aug.rref()

    beta = result.col(-1)

    def _f(x: float) -> float:
        return sum((b*x**i for i, b in enumerate(beta)))

    return _f, beta
