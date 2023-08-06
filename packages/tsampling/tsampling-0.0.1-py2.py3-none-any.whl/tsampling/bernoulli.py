from numpy.random import binomial
from numpy import mean
import operator
from tsampling.root import RootThompsonSampling
from tsampling.priors import BetaPrior
from typing import List


class BernoulliExperiment(RootThompsonSampling):
    """ Class for Thompson Sampling with Bernoulli reward"""
    _default = {"a": 1, "b": 1}
    _posterior = "beta"

    def __init__(self, arms: int = None, priors: BetaPrior = None, labels: list = None):
        super().__init__(arms, priors, labels)

    def add_rewards(self, results: List[dict]):
        """Takes a list of dictionaries with the results and updates the Posterior
        distribution for the label.
        
        results = [{"label": "A", "reward": 1}, {"label":"B", "reward":0}]

        Parameters
        ----------
        results: List[dict] :
            
        """

        for result in results:
            self.posteriors[result["label"]]["a"] += result["reward"]
            self.posteriors[result["label"]]["b"] += 1 - result["reward"]
        return self

    def get_distribution(self, size) -> List[dict]:
        """Simulates the posterior predictive distribution for all available
        posterior distributions. 

        Parameters
        ----------
        size : int
            

        Returns
        -------
        Percentage of Success and Percentage of Failure.
        """
        distribution_stats = []
        for k, _ in self.posteriors.items():
            pred_result = [
                int(
                    binomial(
                        n=1,
                        p=self._avail_posteriors[self._posterior](
                            size=1, **self.posteriors[k]
                        ),
                        size=1,
                    )
                )
                for _ in range(size)
            ]
            summary_stats = {
                "Label": k,
                "Percentage - Success": sum(pred_result) / size,
                "Percentage - Fail": (len(pred_result) - sum(pred_result)) / size,
            }
            distribution_stats.append(summary_stats)
        return distribution_stats
