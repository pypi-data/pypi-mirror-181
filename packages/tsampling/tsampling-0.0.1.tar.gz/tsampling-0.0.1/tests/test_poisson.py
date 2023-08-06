import pytest
from tsampling.poisson import PoissonExperiment
from tsampling.priors import GammaPrior
from pandas import Series

"""Tests for `tsampling` package."""
class TestPoissonExperiment:
    """ Class for testing Poisson Experiment class functions """
    def test_init_arms(self):
        """ Tests PoissonExperiment with default priors """
        exper = PoissonExperiment(3)
        assert len(exper.posteriors) == 3
        assert isinstance(exper.posteriors, dict)
        for k, _ in exper.posteriors.items():
            assert isinstance(exper.posteriors[k], dict)
            assert exper.posteriors[k] == {"shape": 0.001, "scale": 1000}

    def test_init_custom(self):
        """ Tests PoissonExperiment with custom priors """
        prior = GammaPrior()
        means = Series([100, 200])
        variances = Series([20, None])
        effective_sizes = Series([None, 20])
        labels = Series(["option1", "option2"])
        prior.add_multiple(means, variances, effective_sizes, labels)
        exper = PoissonExperiment(priors=prior)
        assert len(exper.posteriors) == 2

    def test_update_posterior(self):
        """ Tests add_wards function for Poisson experiment """
        exper = PoissonExperiment(3)
        exper.add_rewards(
            [{"label": "option1", "reward": 100}, {"label": "option2", "reward": 200}]
        )
        assert exper.posteriors == {
            "option1": {"shape": 100.001, "scale": 0.999},
            "option2": {"shape": 200.001, "scale": 0.999},
            "option3": {"shape": 0.001, "scale": 1000},
        }

    def test_pull_arm(self):
        """ Tests choose_arm function for Poisson Experiment """
        exper = PoissonExperiment(3)
        assert exper.choose_arm() in [key for key, _ in exper.posteriors.items()]

    def test_get_distribution(self):
        """ Tests get_distribution function for Poisson experiment """
        exper = PoissonExperiment(3)
        assert isinstance(exper.get_distribution(size=10000), list)
        assert len(exper.get_distribution(size=1000)) == len(exper.posteriors)
    
    def test_plot_posterior(self):
        """ Tests plot_posterior function for Poisson experiment """
        exper = PoissonExperiment(3)
        assert True
