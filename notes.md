## To do:

- Create BPMN models of the processes described in quick reference.

### Ideas:

- transform logs into images, then use CNNs for prediction, pattern/feature engineering, problem classification
- use transfer learning
- GRU for prediction

L\* gives 3 possible avenues for results:

1. DETECT problems in execution
2. PREDICT execution of current cases
3. RECOMMEND changes in execution

As our goal for this project we pick <1/2/3>, since <argumentation>.

### Questions:

- What is actually changed and how is it changed?
- What is the throughput time for every activity?
- What does the spike in events represent?
- How much time does it take after a change to go back to a steady state?
- For every major business change, what does the descriptive statistics look like?
- How can we detect drifts from steady state A to B?

### Meeting May 16

- How do the average steps to resolution change over time (for all sub categories)?
- What are the average business hours lost (per category, per impact value)?
- How can we build a regression model that given some predictor variables predicts {how long a case will take/whether a case will be reopened}?
- How can we predict time left using LTSs?
- How many incidents took place for SCs?
- What are the different versions of the incident management process (and stats about them)?

Analyze handovers between teams

### Meeting May 18

Chosen business questions:

- How can we predict time left using LTSs?
- What are the average business hours lost (per category, per impact value)?
- choose 1:
  1.  How does time affect the process? (are there patterns in time, e.g., faster processing in weekends)
  2.  What are the bottlenecks in the process?

### Lecture May 25

- ATS approach doesn't take in long term dependencies. So if, e.g., there is a correlation between {time it took to get from activity A to B} and {time remaining if you have just executed D}, this is not captured in the model/taken advantage of in the prediction. <-- could be stated in limitations section, or attempts could be done to tackle this.

### Meeting May 26 Joel&Tim

- UC1: add/update data while live/online
- UC2: run prediction models
- preprocessing:
  - timestamps to unix-timestamps
  - categorical to one-hot encoded
- add features to ATS data
  - amount of pingpongs
  - remaining time

### Meeting June 8 (All)

- **Goal of the project:**

  - Time Prediction
    - BQ1: creating transparency (side effect: user/client satisfaction [client time management])
    - BQ2: manage resources

- Introduction
  - Rabobank's problem, what part we are going to tackle
- Problem Description
  - Reader's Guide
  1.  Explain Rabo's ITIL process
  2.  Business problem
  3.  Our approach (what do we tackle, and how)
  4.  Why this approach (expected benefits)
- Data
  - Reader's Guide
  1.  High-level data description
      - Percentages of priority categories
  2.  Data Preparation
      - Describe filters:
        - As we would lack a definition of 'complete' when using all cases, we only use cases that start with 'open' and end with 'close'.
        - we do take in weekends (explain why)
        - we do take in infrequent traces (explain why)
  3.  Limitations and Assumptions
  4.  BQ1
      - Request for info (case category) stats, use for arguing importance of transparency (without our model its guestimating, with our model its more factual)
      - MSE/MAE using Average Duration Prediction (without leveraging states)
      - General boxplots of mean activities (per case) and mean duration (per case)
      - Boxplots per prio/casetype
  5.  BQ2
      - Graph of cases over time, with possible interpretations
      - Heatmap of number of incidents during week per hour (x: day of week, y: hour of day, color: number of incidents)
      - Team descriptions
        - #incidents per team
        - particularities about team: case category, priority
        - performance per team
- Prediction
  - Reader's Guide
  1.  Related Work
  2.  Methodology
  3.  Implementation (if we get extention
  4.  Results
- Conclusion
- Discussion
  - Reader's Guide
  1.  Limitations
  2.  Future Work

### Meeting June 10 (Joel, Tim)

Use cases:

1. traverse ATS to determine bucket to use for predicting new event
2. transform list of dicts to dataframe inside of each bucket
3. lay foundations for implementing ML models at each Bucket (avg, max, min, median, sample mean, linear regression, RF, li)

### Future Work (Tim)
- add feature: minimum bucket size (tunable)
