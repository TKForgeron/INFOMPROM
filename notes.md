## To do:
- Create BPMN models of the processes described in quick reference.

## Ideas:
- transform logs into images, then use CNNs for prediction, pattern/feature engineering, problem classification
- use transfer learning
- GRU for prediction

L* gives 3 possible avenues for results:

1. DETECT problems in execution
2. PREDICT execution of current cases
3. RECOMMEND changes in execution

As our goal for this project we pick <1/2/3>, since <argumentation>.

## Questions:
What is actually changed and how is it changed?
What is the throughput time for every activity?
What does the spike in events represent?
How much time does it take after a change to go back to a steady state?
For every major business change, what does the descriptive statistics look like?
How can we detect drifts from steady state A to B?


### Meeting May 16
How do the average steps to resolution change over time (for all sub categories)?
What are the average business hours lost (per category, per impact value)?
How can we build a regression model that given some predictor variables predicts {how long a case will take/whether a case will be reopened}?
How can we predict time left using LTSs?
How many incidents took place for SCs?
What are the different versions of the incident management process (and stats about them)?