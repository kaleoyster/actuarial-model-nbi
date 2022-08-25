<h1 align='center'>
    Methodology 
</h1>

There are several different version of compute life tables for identifying and studying bridge maintenance patterns:

1. [Life table by O'Brien Chin (v1)](life-table-v1.md)
2. [New proposed method (v2)](life-table.v2.md)

## Data 
* **Source:** National Bridge Inventory
* **Timeline:** 1992 to 2021
* **Scope:** All U.S. states 🇺🇸
* 👉 [**Data acqusition and transformation**](https://github.com/kaleoyster/nbi/tree/b5fb41950ee0a44c1d8967a1a672c0e3ea47b07f)


## 💡 A brief comparison of methods

| Item           | Description                                                                                                    | Version 1 (O'Brien Chin) | Version 2 |
| -------------- | -------------------------------------------------------------------------------------------------------------- | -------------------| ----|
| Study window   | To observe the behavior of the bridges as they pass through this window | Established as five year study window 2013 - 2017 | Established as five year multiple study windows from 1992 to 2020, with an option of overlapping study windows |
| $leave(x)$     | The number of bridges that leave the study at age $x$                                                          | Computed similar to the described definition, similar to mortality rate | New approach use the concept of conditional probability of dying instead of mortality rate, change in notation used as $D_x$| 
| $exposures(x)$ | The number of bridges in the study at age $x$                                                                  | Assumes that a bridge be a part of the study for the entire year for it to contribute ot the exposure for that year | Exposures are computed similar to the previous method |
| Hazard rate $h(x)$         | Hazard rate age $x$. See equation 1                                                                            | Computed as $leaves(x) \over exposure(x)$ | $D_x \over P_x + (0.5 * D_x)$ |
| $S(x)$         | Survival rate age $x$. See equation 2 | Computed as $S(x) = 1 - h(x)$| Computed as $P_x = 1 - Q_x$ |
| $F(x)$         | The mortality rate (or cumulative probability of failure) of bridges exposed at age 1 before reaching age $x$  | $1 - P_x$ |Conditional probability of death $q_x = (D_x / (P_x + (0.5 * D_x)))$ |
| $_yP_1$        | Probability of survival at age $y$ for the next year. See Equation 5 | This version can compute the probability of survival for next 5 years.| Although, this method is so far not implemented, the version can implement next 5 years of probability | 

## References

1. [Intuition for cumulative hazard function -- survival analysis](https://stats.stackexchange.com/questions/60238/intuition-for-cumulative-hazard-function-survival-analysis)
2. [Methodology to calculating national life tables](https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/healthandlifeexpectancies/methodologies/guidetocalculatingnationallifetables)
3. [Computing Life Tables](https://www.measureevaluation.org/resources/training/online-courses-and-resources/non-certificate-courses-and-mini-tutorials/multiple-decrement-life-tables/lesson-3.html)
4. [Validation by simulation bridge life cycles]()
