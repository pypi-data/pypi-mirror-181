from numpy.random import beta, gamma, binomial
from functools import partial
from pandas import Series, DataFrame
import operator
import seaborn as sns
import matplotlib.pyplot as plt
from typing import List
from itertools import combinations


class RootPrior:
    """Class to add one or more priors to experiment """
    def __init__(self):
        self.priors = {}

    def _param_calculator(self, *args):
        """
        Hidden method that creates the prior's given specifications

        """
        return self

    def add_one(
        self, mean: float, variance: float, effective_size: int, label: str
    ) -> dict:
        """Allow for individual priors to be specified and added to the priors list

        Parameters
        ----------
        mean: float 
            
        variance: float 
            
        effective_size: int 
            
        label: str 
            

        """

        new_prior = {label: self._param_calculator(mean, variance, effective_size)}
        self.priors.update(new_prior)
        return self

    def add_multiple(
        self, means: Series, variances: Series, effective_sizes: Series, labels: Series
    ) -> List[dict]:
        """Allow for a group of priors to be specified at once
        information: DataFrame

        Parameters
        ----------
        means: Series 
            
        variances: Series 
            
        effective_sizes: Series 
            
        labels: Series 
            

        """
        params = [means, variances, effective_sizes, labels]
        if any([len(a) != len(b) for a, b in list(combinations(params, 2))]):
            message = (
                f"Lengths of given series do not match. Lengths - "
                f"mean:{len(means)}, "
                f"variance:{len(variances)}, "
                f"effective_size:{len(effective_sizes)}, "
                f"labels:{len(labels)}"
            )
            raise ValueError(message)
        for i, _ in enumerate(labels):
            new_prior = {
                labels[i]: self._param_calculator(
                    means[i], variances[i], effective_sizes[i]
                )
            }
            self.priors.update(new_prior)
        return self


class RootThompsonSampling:
    """ Parent Class for Thompson Sampling """
    _default = {}
    _posterior = ""

    def __init__(self, arms: int = None, priors: RootPrior = None, labels: list = None):
        self._avail_posteriors = {"beta": partial(beta), "gamma": partial(gamma)}
        if arms is None and priors is None:
            raise ValueError("Must have either arms or priors specified")
        if priors:
            self.posteriors = priors.priors
        elif arms:
            self.posteriors = {
                (f"{labels[i]}" if labels else f"option{i+1}"): self._default.copy()
                for i in range(arms)
            }

    def _sample_posterior(self, size: int = None, key: str = None):
        """

        Parameters
        ----------
        size: int :
             (Default value = None)
        key: str :
             (Default value = None)

        Returns
        -------

        """
        return self._avail_posteriors[self._posterior](
            size=size, **self.posteriors[key]
        )

    def choose_arm(self):
        """Choose which arm to pull.
        
        This function will sample from the posterior distributions
        posterior and determine the maximum theta from all of the options

        Returns
        -------
        the largest theta
        """

        theta_est = {}  
        for key, _ in self.posteriors.items():
            theta_est[key] = self._sample_posterior(1, key)
        return max(theta_est.items(), key=operator.itemgetter(1))[0]

    def plot_posterior(self):
        """ See the posteriors' distribution"""
        plot_values = {
            key: self._sample_posterior(10000, key)
            for key, _ in self.posteriors.items()
        }

        for key, sim_array in plot_values.items():
            sns.distplot(sim_array, hist=False, label=key)
        plt.title("Posterior Distributions")
        plt.legend()
        plt.xlabel("Parameter Value")

        