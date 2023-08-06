![logo](docs/images/logo-full.png)

A Python package for wagering related functions and statistical analysis. 

### Main Features
- Implied Probabilities
- Expected Values
- Ranking Probabilities
- Staking Methods

### Links
- [Documentation](https://jemjemwalsh.github.io/betqstat)
- [Examples](docs/examples)
- [Contact](https://jemjemwalsh.github.io/betqstat/contact)


## Installation
Install with pip:
```bash
pip install betqstat
```
Or pip3:
```bash
pip3 install betqstat
```
Python 3.8+ is required.


## Roadmap
This is an early development version. The following are to be completed or are ideas to be considered:

- [ ] Examples
- [ ] Automated tests
- [ ] Implied Probabilities (impliedprob)
  - [x] Functions to remove over-round from odds, different methods
  - [ ] Create an argument target margin, so for example could get the implied probs for a place market.
  - [ ] ML method to calculate implied prob from bookie odds?
- [ ] Expected Values (ev)
  - [ ] Estimate's for ev where calculation not possible
- [ ] Ranking probabilities (rank)
  - [ ] Alternative methods to Harville for ordering probabilities
  - [ ] Calculate market derivatives from ordering probabilities, prob place 2nd, 3rd, 4th etc.
  - [ ] Same race multi style odds/sim
- [ ] Staking (stake)
  - [x] Round up to smallest increment 
- [ ] Odds (odds)
  - [x] Betfair actual odds negative commission 
  - [ ] Covert decimal to fraction and vice versa
  - [ ] Convert ratings to probability/price
- [ ] Bookie
  - [ ] Functions to introduce bookie's margin to probabilities, reverse implied probs functions.
- [ ] Analysis
  - [ ] Stats: BTM, Edge, time from jump brackets, odds brackets, weighted average price
- [ ] Other Ideas
  - [ ] betfair tool to get harness code
  - [ ] mapping tool to map meetings/races/runners


## Contributing to betqstat
The betqstat package was created to share wagering tools and ideas, all contributions are welcome. 
[Get in touch](https://jemjemwalsh.github.io/bookie-tools/contact) or submit a pull request.


## Contributors
Thanks to the following people who have contributed to this project:
* [@jemjemwalsh](https://github.com/jemjemwalsh/) 🤔💻📖💡🔣🐛
* [@Bryley](https://github.com/Bryley) 🚇
