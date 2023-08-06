import numpy as np
from PEPit.function import Function


class LipschitzOperator(Function):
    """
    The :class:`LipschitzOperator` class overwrites the `add_class_constraints` method of :class:`Function`,
    implementing the interpolation constraints of the class of Lipschitz continuous operators.

    Note:
        Operator values can be requested through `gradient` and `function values` should not be used.

    Attributes:
        L (float) Lipschitz parameter

    Cocoercive operators are characterized by the parameter :math:`L`, hence can be instantiated as

    Example:
        >>> from PEPit import PEP
        >>> from PEPit.operators import LipschitzOperator
        >>> problem = PEP()
        >>> func = problem.declare_function(function_class=LipschitzOperator, L=1.)

    Notes:
        By setting L=1, we define a non expansive operator.

        By setting L<1, we define a contracting operator.

    References:

        [1] M. Kirszbraun (1934).
        Uber die zusammenziehende und Lipschitzsche transformationen.
        Fundamenta Mathematicae, 22 (1934).

        [2] F.A. Valentine (1943).
        On the extension of a vector function so as to preserve a Lipschitz condition.
        Bulletin of the American Mathematical Society, 49 (2).

        [3] F.A. Valentine (1945).
        A Lipschitz condition preserving extension for a vector function.
        American Journal of Mathematics, 67(1).

        Discussions and appropriate pointers for the interpolation problem can be found in:
        `[4] E. Ryu, A. Taylor, C. Bergeling, P. Giselsson (2020).
        Operator splitting performance estimation: Tight contraction factors and optimal parameter selection.
        SIAM Journal on Optimization, 30(3), 2251-2271.
        <https://arxiv.org/pdf/1812.00146.pdf>`_

    """

    def __init__(self,
                 L=1.,
                 is_leaf=True,
                 decomposition_dict=None,
                 reuse_gradient=True):
        """

        Args:
            L (float): Lipschitz continuity parameter.
            is_leaf (bool): True if self is defined from scratch.
                            False if self is defined as linear combination of leaf .
            decomposition_dict (dict): Decomposition of self as linear combination of leaf :class:`Function` objects.
                                       Keys are :class:`Function` objects and values are their associated coefficients.
            reuse_gradient (bool): If True, the same subgradient is returned
                                   when one requires it several times on the same :class:`Point`.
                                   If False, a new subgradient is computed each time one is required.

        Note:
            Lipschitz continuous operators are necessarily continuous, hence `reuse_gradient` is set to True.

        """
        super().__init__(is_leaf=is_leaf,
                         decomposition_dict=decomposition_dict,
                         reuse_gradient=True)
        # Store L
        self.L = L

        if self.L == np.inf:
            print("\033[96m(PEPit) The class of L-Lipschitz operators with L == np.inf implies no constraint: \n"
                  "it contains all multi-valued mappings. This might imply issues in your code.\033[0m")

    def add_class_constraints(self):
        """
        Formulates the list of interpolation constraints for self (Lipschitz operator),
        see [1, 2, 3] or e.g., [4, Fact 2].
        """

        for point_i in self.list_of_points:

            xi, gi, fi = point_i

            for point_j in self.list_of_points:

                xj, gj, fj = point_j

                if (xi != xj) | (gi != gj):
                    # Interpolation conditions of Lipschitz operator class
                    self.list_of_class_constraints.append((gi - gj) ** 2 - self.L ** 2 * (xi - xj) ** 2 <= 0)
