from ._dirichlet_multinomial_mixture import DirichletMultinomialMixture

import pkg_resources

__all__ = ["DirichletMultinomialMixture"]
__version__ = pkg_resources.get_distribution("pyDIMM").version