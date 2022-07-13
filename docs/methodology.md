<h1 align='center'>
Methodology 🧭
</h1>
There are considerations regarding the dataset and algorithms

## 📝 Points
1. The hazard rate computes instantaneous rate of failure.
- It would be much more wiser to have an instantaneous rate of failure for several study windows.
   * **Study window 1:** 1992 - 1998
   * **Study window 2:** 1998 - 2004
   * **Study window 3:** 2004 - 2008 
   * **Study window 4:** 2008 - 2012
   * **Study window 5:** 2012 - 2016
   * and so and so forth.

- The study windows represent bridges built durning these time windows and then surviving for the next windows.

2. **Focus:** The study needs to focus on one single component of the bridge such as `deck`.
3. **Definition:** We need to define repair and reconstruction. This could be defined using the `Bridge Intervention Matrix`.
- Instead of calling the death of the bridge, we can introduce a term `surviving untill maintenance`.

4. **Correct span for the study window:** By referring to older literature, we can identify the study windows.
5. **Application:** This methodology can guide in answer the questions regarding the `average daily traffic` effect on the `deck` repiar and maintenances.
![Bridge Intervention Matrix](/Users/kale/vimwiki/assets/intervention-matrix.png)

## Assumptions
* Some assumptions were made about the bridges. When a maintenance event occurs on a bridge and that event is recorded, the bridge is permanently removed from the study. 
* There are other options on how to handle a bridge once a maintenance event occurs, each with its own consequences. These include:
    - Allow the bridge to re-enter the study at the same age.
    - Allow the bridge to re-enter the study at a younger age, given the type of maintenance which occurred.

## Data 
* **Source:** National Bridge Inventory
* **Timeline:** 1992 to 2021
* **State:** All U.S. states 🇺🇸
* 👉 [**Data acqusition and transformation**](https://github.com/kaleoyster/nbi/tree/b5fb41950ee0a44c1d8967a1a672c0e3ea47b07f)

## ⚙️  Algorithm 
The algorithm is divied into four steps:
1. Select study window
2. Compute exposure 
3. Compute hazard rate 
4. Compute mortality

#### 💡 Conceptual overview of the essential actuarial functions
| Item           | Description                                                                                                    |
| -------------- | -------------------------------------------------------------------------------------------------------------- |
| $leave(x)$     | The number of bridges that leave the study at age $x$                                                          |
| $exposures(x)$ | The number of bridges in the study at age $x$                                                                  |
| $h(x)$         | Hazard rate age $x$. See equation 1                                                                            |
| $S(x)$         | Survival rate age $x$. See equation 2                                                                          |
| $F(x)$         | The mortality rate (or cumulative probability of failure) of bridges exposed at age 1 before reaching age $x$  |
| $_yP_1$        | Probability of survival at age $y$ for the next year. See Equation 5                                           |

#### 🪟  Select study window
- The general concept of this approach is to establish a study period and observe the behavior of the bridges as they pass through this window.
- For this study, the chosen window was five years: 2013 to 2017, inclusively. 
- This selection was based on the length of our available time series data; yet in general, a different window can be chosen for longer or shorter time series data.

#### ☢ Exposures
- Exposures represent how many bridges of each age are available to “fail" (require maintenance in the bridge case). 
- For example, if there are 100 bridges aged 35, and 50 bridges aged 40 in the study, then the exposure for ages 35 and 40 are 100 and 50, respectively.
- To compute the exposures, we need to know the age of each bridge in the study.
- The counts for each age are incremented regardless of when in the five years in the study window a bridge reaches that age. For example, if a bridge is 45 years old in 2013 and another bridge is also 45 years old in 2016, both bridges are counted as exposures for age 45.

#### ☣️  Hazard rate
- Hazard function is also referred to as the force of mortality, or also thought as the instantaneous rate of failure.
    * For a very small change in time $x$, the probability that a life who has attained age $x$, fails before attaining age $x + dx$.
    * However, computing this instantaneous rate of failure requires that a bridge be part of the study for the entire year for it to contribute to the exposures for that year.
    * This requirement reduces the number of observations in the dataset (Richards 2011). 

- In contrast, we use a simpler maximum likelihood estimator that can accommodate partial year exposures to capture maintenance patterns.
- Hence, if $leave(x)$ is the number of bridges that leave the study at age $x$ and $exposures(x)$ is the number of exposures at age $x$ 

The hazard rate is defined as the following:
$$ h(x) = { exposures(x + 1) \over exposures(x)} $$

The survival rate $S(x)$ can be computed as show in the equation 2:
$$ {S(x) = 1 - h(x)}$$

#### ☁️  Probabilities

A period life table is baed on the mortality expeirence of a population during a relative short period of time. 
#### New understanding of the methodology
- $f(x):$ Starting at the start time, the probability distribution of when you will die.
- $F(x):$ Just the cumulative distribution, at time $T$, what % of the population will be dead?
- $S(x):$ $1-F(x)$, at time $T$, what % of the population will be alive?
- $h(x):$  Hazard function, at a given time $T$, of the people still alive, this can be used to estimate how many people will die in the next time interval, or if interval → 0, `instantaneous` death rate.
    - Hazard rate: It measures the total amount of risk that has been accumulated up to time t.
    - Count data interpration: `It gives the number of times we would expect to observe failures over a given period, if only the failure events were repeatable`
- $H(x):$ Cumulative hazard function.

#### Previous understanding of the methodology

- Instead of the absolute number of surviving bridges at age $x$ life tables commonly compute a probability of survival. 
- The probability of survival for bridges exposed from age 1 to age $x$ is:  $_1P_x$, or simply $P_x$. 
- It is computed from the hazard rate as shown in Equation 3:
- The mortality rate (or cumulative probability of failure), $F(x)$ of bridges exposed at age 1
before reaching age $x$ is then calculated from the probability of survival, as shown in Equation 4:
$$F(x) = 1 − _t(P(x))$$
- Note that $F(x)$ can also be expressed as $_1Q_x$ or simply $Q_x$. $_1Q_1$ is the cumulative probability of failure within the next year. $_1Q_1$ is computed from the probabilities of surviving within the next year $_1P_1$ and subtracting that from 1. Similarly, the probability of failure for years two, three, four, and five are computed. These are $_2Q_1$, $_3Q_1$, $_4Q_1$, $_5Q_1$ respectively.
- $_4Q_1$ and $_5Q_1$ respectively. These relationships are shown in Equation 5.
    $$ _1Q_1 = 1 - _1P_1 $$
    $$ _2Q_1 = 1 - _2P_1 $$
    $$ _3Q_1 = 1 - _3P_1 $$
    $$ _4Q_1 = 1 - _4P_1 $$
    $$ _5Q_1 = 1 - _5P_1 $$

## References

1. [Intuition for cumulative hazard function -- survival analysis](https://stats.stackexchange.com/questions/60238/intuition-for-cumulative-hazard-function-survival-analysis)



