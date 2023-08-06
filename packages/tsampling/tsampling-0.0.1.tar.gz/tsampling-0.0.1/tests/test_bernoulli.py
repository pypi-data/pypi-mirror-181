import pytest
from tsampling.bernoulli import BernoulliExperiment
from tsampling.priors import BetaPrior
from pandas import Series

"""Tests for `tsampling` package."""

class TestBernoulliExperiment:
    """ Class for testing Bernoulli Experiment class functions"""
    def test_init_arms(self):
        """ Tests BernoulliExperiment with default priors"""
        exper = BernoulliExperiment(3)
        assert len(exper.posteriors) == 3
        assert isinstance(exper.posteriors, dict)
        for k, _ in exper.posteriors.items():
            assert isinstance(exper.posteriors[k], dict)
            assert exper.posteriors[k] == {"a": 1, "b": 1}

    def test_init_custom(self):
        """Tests BernoulliExperiment with custom priors """
        prior = BetaPrior()
        means = Series([0.2, 0.5])
        variances = Series([0.02, 0.2])
        effective_sizes = Series([10, 10])
        labels = Series(["option1", "option2"])
        prior.add_multiple(means, variances, effective_sizes, labels)
        exper = BernoulliExperiment(priors=prior)
        assert len(exper.posteriors) == 2

    def test_update_posterior(self):
        """ Tests add_wards function for Bernoulli experiment """
        exper = BernoulliExperiment(3)
        exper.add_rewards(
            [{"label": "option1", "reward": 1}, {"label": "option2", "reward": 0}]
        )
        assert exper.posteriors == {
            "option1": {"a": 2, "b": 1},
            "option2": {"a": 1, "b": 2},
            "option3": {"a": 1, "b": 1},
        }

    def test_pull_arm(self):
        """ Tests choose_arm function for Bernoulli Experiment """
        exper = BernoulliExperiment(3)
        assert exper.choose_arm() in [key for key, _ in exper.posteriors.items()]

    def test_get_distribution(self):
        """ Tests get_distribution function for Bernoulli experiment """
        exper = BernoulliExperiment(3)
        assert isinstance(exper.get_distribution(size=10000), list)
        assert len(exper.get_distribution(size=1000)) == len(exper.posteriors)
    
    def test_plot_posterior(self):
        """ Tests plot_posterior function for Bernoulli experiment """
        exper = BernoulliExperiment(3)
        assert True
        
    
    