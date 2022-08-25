<h1 align='center'>
      Actuarial lifetable version 2
</h1>

# TODO:
- [ ] Find the research papers for the study window.
- [ ] Organize the methodology of the actuarial life table.

## Data 
* **Source:** National Bridge Inventory
* **Timeline:** 1992 to 2022
* **Scope:** All U.S. states 🇺🇸
* 👉 [**Data acqusition and transformation**](https://github.com/kaleoyster/nbi/tree/b5fb41950ee0a44c1d8967a1a672c0e3ea47b07f)

### Determine study window
- Over lapping study windows.
- We have data from 1992 to 2022.
- There are random variation over the study windows.
- The following is the new approach:
For each window, create a life table for each study window.
    - Study window 1: 1992 - 1998
    - Study window 2: 1998 - 2004
    - Study window 3: 2004 - 2008
    - Study window 4: 2008 - 2012
    - Study window 5: 2012 - 2016
    - Study window 6: 2016 - 2020
    - and so and so forth.

- Within the new propoposed process for the actuarial life table, we have seven steps to be computed for each study window:

### Determine the study window

- The rational behind the study window of 3 years to 4 years is the standard practice in actuary. However, within in the bridge life-cycle, bridges often get maintained in 20 years. Therefore, we need to observe a long period of time.

### Compute population and death rate

- For each age from 0 to 100, compute the number of bridges per age, and number of bridges maintained for each age.

### Compute death rate

- Death rate is denoted as $m_x$
- The meaning of the death with respect to bridges is not same. As bridges get repaired or maintained, we consider this as the death of the bridge.
- The definition of death with respect to bridges.
- Using the mortality rate / survival rate as the baseline may prove complementary to the BDS score
- Baseline difference score accounts for performance of the bridge health.
- The baseline based on mortality may account for maintenance.
- However, the maintenance based baseline may not be useful in computing a score.

### Compute conditional probability of death rate
- Compute death rate probability of maintenance ($q_x$):
- Formulation:

  $$q_x = {D_x \over (P_x + (0.5 * D_x))}$$
 
### Compute conditional probability of survival rate
- Conditional probability of survival without maintenance (survival) is denoted by $(p_x)$:

$$ p_x = {1 - q_x}$$

### Compute lived at age x
- These computations are depended on previous computations
- To compute number of bridges surviving to age $l_x$ to age $x$
- Compute lived at age x Compute bridge years lived at age $x$
$$ L_x = {\sum_{i=0}^{n}l_x}$$

### Compute tatal years lived at age x
- Compute total years lived at age $x$ $(T_x)$

$$ T_x = {\sum_{i=0}^{n}L_x}$$

### Compute life expectancy
- Compute life expectancy compute life expectancy $e_x$

$$ e_x = {T_{xi} \over l_{xi}}$$

### Compute the conditional probability of survival, based on the study window, we can compute $_tP_x$
- Compute conditional probability of survival Based on the study window, we can compute the $_tP_x$ for each age.

## Assumptions
* What is the average time-span before there is a maintenance activity? - Glen Washer
- When a maintenance event occurs on a bridge and that maintenance event is recorded, the bridge is permanently removed from the study. 
- There are other options on how to handle a bridge once a maintenance event occurs, each with its own consequences. These include:
    - Allow the bridge to re-enter the study at the same age.
    - Allow the bridge to re-enter the study at a younger age, given the type of maintenance which occurred.


## 📝 There are few consideration regarding the computation of the actuarial model
- When using the mortality rates as baseline:
    - Does computing with a denominator of 0 useful / valid as concluding 0 for life-table.
    - Zero in the denominator suggest that there are no available records for that age. That doesn't necessarily translate to no deaths.

- It would be much more wiser to have an instantaneous rate of failure for several study windows. These study windows are four years apart.
- The study windows represent bridges built during these time windows and then surviving for the next windows.

2. The hazard rate computes instantaneous rate of failure.
3. **Focus:** The study needs to focus on one single component of the bridge such as `deck`.
4. **Definition:** We need to define repair and reconstruction. This could be defined using the `Bridge Intervention Matrix`.
    - Instead of calling the death of the bridge, we can introduce a term `deterioration until maintenance`. Do we need to compute the total number of deterioration until maintenance?

5. **Correct span for the study window:** By referring to older literature, we can identify the study windows. 
    → **Research question: How to find the appropriate span for the study window using data driven methods?**

6. **Application:** This methodology can guide in answering the questions regarding the `average daily traffic` effect on the `deck` repair and maintenances.


1. We need to find the appropriate length of the study window.
    - Determining the appropriate length of the study window using historical evidence.
        - For all the bridges built in the year from 1992 to 2010. Determine the average time for first major intervention.
        - Out of 17,536 bridges, only 2 % of the bridges are built in 1992.
        * And, a total of 4,479 bridges (~35%) bridges were built in between 1992 to 2020.
        * For 333 bridges built in 1992, only 77 (23%) of the bridges have any intervention, moreover, the average length is 4.79 years before intervention, max(26), min(1), and median is 2.
        * Mean and median time before intervention in these bridges.
    - Do we need to have variable study window, as the the mortality rate of observing one intervention changes over a period of time?
    * There are revised considerations for each of the study window:
        - Overall, the idea of study window of last four-years or last-three years, would guide in calculating lifetable. Each of the study window will provide an understanding of changing life expectancy of the bridges.
    *  In an attempt to find the most appropriate study window:
        - Can we bridge the all bridges around this four year time together, and treat them as bridges built in within a study window.

2. There are challenges in understanding the true mortality of the bridges as not all bridges are tracked every year over the their life cycle.
    - However, due to the inconsistent year built data, where year built of the bridges change over a period of time. One might observe that number of records available may be higher than expected.
    - For instance in 2022, a bridge built in 2014, may have a total of 29 records as opposed to 9 records.

3. Identifying the interventions from the NBI inspections records have been a major challenge Bridge Intervention Matrix (BMI):
    - Since bridge assessment is subjective, there can be various inspection variance, on top of repair and reconstruction. 
4. Computing the $_tP_x$ for all
5. In computing the life table statistics, there is a very narrow range ages, that we can compute the statistics. 

#### Validation
We validate the use of our functions by applying to publicly available data to match the resultant results. We implemented on bridges to understand the life expectancy of the population used in the following reference [3].

### Pipeline
We validated our data pipeline to ensure all data processing and compuation operations are conducted as expected. As a result, we require our validation process to have consistency. We created a dummy data, such that the results of the lifetable are expected.

#### Bridge life cycle:
- The lifetable will mimic the life cycle of an average bridge:
- **Starting year:** 1992
- **Ending year:** 2021
- **Starting condition rating:** 9
- **Average time it takes for maintenances:** 5 yrs


