from PEPit import PEP
from PEPit.functions.convex_function import ConvexFunction


def wc_accelerated_gradient_flow_convex(t, verbose=1):
    """
    Consider the convex minimization problem

    .. math:: f_\\star \\triangleq \\min_x f(x),

    where :math:`f` is convex.

    This code computes a worst-case guarantee for an **accelerated gradient** flow.
    That is, it verifies the inequality

    .. math:: \\frac{d}{dt}\\mathcal{V}(X_t, t) \\leqslant 0 ,

    is valid, where :math:`\\mathcal{V}(X_t, t) = t^2(f(X_t) - f(x_\\star)) + 2 \\|(X_t - x_\star) + \\frac{t}{2}\\frac{d}{dt}X_t \\|^2`,
    :math:`X_t` is the output of an **accelerated gradient** flow, and where :math:`x_\\star` is the minimizer of :math:`f`.
    
    In short, for given values of :math:`t`, it verifies :math:`\\frac{d}{dt}\\mathcal{V}(X_t, t) \\leqslant 0`.

    **Algorithm**:
    For :math:`t \\geqslant 0`,

                .. math:: \\frac{d^2}{dt^2}X_t + \\frac{3}{t}\\frac{d}{dt}X_t + \\nabla f(X_t) = 0,

    with some initialization :math:`X_{0}\\triangleq x_0`.

    **Theoretical guarantee**:

        The following **tight** guarantee can be verified in [1, Section 2]:

        .. math:: \\frac{d}{dt}\\mathcal{V}(X_t, t) \\leqslant 0.

        After integrating between :math:`0` and :math:`T`,

        .. math:: f(X_T) - f_\\star \\leqslant \\frac{2}{T^2}\\|x_0 - x_\\star\\|^2.

        The detailed approach using PEPs is available in [2, Theorem 2.6].

    **References**:

    `[1] W. Su, S. Boyd, E. J. Candès (2016).
    A differential equation for modeling Nesterov's accelerated gradient method: Theory and insights. In the Journal of
    Machine Learning Research (JMLR).
    <https://jmlr.org/papers/volume17/15-084/15-084.pdf>`_

    `[2] C. Moucer, A. Taylor, F. Bach (2022).
    A systematic approach to Lyapunov analyses of continuous-time models in convex optimization.
    <https://arxiv.org/pdf/2205.12772.pdf>`_

    Args:
        t (float): time step
        verbose (int): Level of information details to print.

                        - -1: No verbose at all.
                        - 0: This example's output.
                        - 1: This example's output + PEPit information.
                        - 2: This example's output + PEPit information + CVXPY details.

    Returns:
        pepit_tau (float): worst-case value
        theoretical_tau (float): theoretical value

    Example:
        >>> pepit_tau, theoretical_tau = wc_accelerated_gradient_flow_convex(t=3.4, verbose=1)
        (PEPit) Setting up the problem: size of the main PSD matrix: 4x4
        (PEPit) Setting up the problem: performance measure is minimum of 1 element(s)
        (PEPit) Setting up the problem: Adding initial conditions and general constraints ...
        (PEPit) Setting up the problem: initial conditions and general constraints (0 constraint(s) added)
        (PEPit) Setting up the problem: interpolation conditions for 1 function(s)
                         function 1 : Adding 2 scalar constraint(s) ...
                         function 1 : 2 scalar constraint(s) added
        (PEPit) Compiling SDP
        (PEPit) Calling SDP solver
        (PEPit) Solver status: optimal (solver: SCS); optimal value: -1.2008648627755779e-18
        *** Example file: worst-case performance of an accelerated gradient flow ***
                PEPit guarantee:         d/dt V(X_t,t) <= -1.20086e-18
                Theoretical guarantee:   d/dt V(X_t) <= 0.0

    """

    # Instantiate PEP
    problem = PEP()

    # Declare a convex smooth function
    func = problem.declare_function(ConvexFunction)

    # Start by defining its unique optimal point xs = x_* and corresponding function value fs = f_*
    xs = func.stationary_point()
    fs = func.value(xs)

    # Then define the starting point xt (considering the derivative of the Lyapunov function) and a derivative
    xt = problem.set_initial_point()
    gt, ft = func.oracle(xt)
    xt_dot = problem.set_initial_point()

    # Run the gradient flow (and define the derivative of the starting point)
    xt_dot_dot = - 3 / t * xt_dot - gt

    # Chose the Lyapunov function and compute its derivative
    lyap = t ** 2 * (ft - fs) + 2 * ((xt - xs) + t / 2 * xt_dot) ** 2
    lyap_dot = 2 * t * (ft - fs) + t ** 2 * xt_dot * gt + 4 * ((xt - xs) + t / 2 * xt_dot) * (3 / 2 * xt_dot + t / 2 * xt_dot_dot)

    # Set the performance metric to the function value accuracy
    problem.set_performance_metric(lyap_dot)

    # Solve the PEP
    pepit_verbose = max(verbose, 0)
    pepit_tau = problem.solve(verbose=pepit_verbose)

    # Compute theoretical guarantee (for comparison)
    theoretical_tau = 0.

    # Print conclusion if required
    if verbose != -1:
        print('*** Example file: worst-case performance of an accelerated gradient flow ***')
        print('\tPEPit guarantee:\t d/dt V(X_t,t) <= {:.6}'.format(pepit_tau))
        print('\tTheoretical guarantee:\t d/dt V(X_t) <= {:.6}'.format(theoretical_tau))

    # Return the worst-case guarantee of the evaluated method (and the reference theoretical value)
    return pepit_tau, theoretical_tau


if __name__ == "__main__":
    pepit_tau, theoretical_tau = wc_accelerated_gradient_flow_convex(t=3.4, verbose=1)
