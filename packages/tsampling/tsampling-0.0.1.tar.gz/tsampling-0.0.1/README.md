# tsampling
Thompson Sampling Multi-Armed Bandit for Python

A package that implements the Thompson Sampling approach for a Multi-Armed Bandit.
The purpose of this project is to help people simply create and maintain Thompson Sampling experiments that have Bernoulli and Poisson distributions.

## Usage

### Setting up the experiment:

The following method will instantiate the experiment with the default priors.
```python
from tsampling.bernoulli import BernoulliExperiment

experiment = BernoulliExperiment(arms=2)
```

You can also set your custom priors by using the Priors module:
```python

from tsampling.bernoulli import BernoulliExperiment
from tsampling.priors import BetaPrior

pr = BetaPrior()
pr.add_one(mean=0.5, variance=0.2, effective_size=10, label="option1")
pr.add_one(mean=0.6, variance=0.3, effective_size=30, label="option2")
experiment = BernoulliExperiment(priors=pr)
```

### Performing an action:
You can randomly choos which arm to "pull" in the multi-armed bandit:
```python
experiment.choose_arm()
```

### Updating reward:
You can update the different arms information by adding reward information:

```python
rewards = [{"label":"option1", "reward":1}, {"label":"option2", "reward":0}]
experiment.add_rewards(rewards)
```

### Plotting Posterior Distribution:
You can plot the posterior distribution 

```python
experiment.plot_posterior()
```

## Installation

### Pip 
```
pip install tsampling
```

## License
 Free software: MIT license

## Credits

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

_Cookiecutter: https://github.com/audreyr/cookiecutter
`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
