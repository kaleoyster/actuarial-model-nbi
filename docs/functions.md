# 🗂  Functions 

The following the documentation for are the function used in the model.

| Functions| Description | Argument type | Return type |
| -------- | ------------| ------------- | ----------- |
| create_dummy_data | Returns a NBI dummy data | None | data - List |
| compute_hazard_rate | Returns a hazard dictionary | list_count, list_age | hazard_dictionary - dictionary |
| identify_window | creates segmentation for data | from_year, to_year | data - List |
| leaves | Returns the number of bridges that leave the study at age x|list_count, list_age | leaves_dict - dictionary |
| exposures | Returns the number of bridges in the study at age x | list_count, list_age | exposures_dict - dictionary |
| compute_probabilities | Returns compute probability of survival | hazard_dictionary | probabilities_dict - dictionary |

## 🦾 Usage and examples

### 1. create_dummy_data:
Return a NBI dummy data

#### Arguments 
None

#### Return 
Data - list

#### Example

```python
data = create_dummy_data()
```
### 2. identify_window:
Returns windows and segments the data accordingly

#### Arguments
from_year (int)

```python
    from_year = 1992
```
to_year (int)

```python
    to_year = 1994
```

#### Return
- *new_data: list*

#### Example

```python
data = identify_window()
```
### 3. compute_hazard_rate:
Returns computation of the harzard rate using leaves and exposure.

#### Arguments
- *list_count: list* 
- *list_age: list*

#### Return
*hazard_dictionary: dictionary*

#### Example
```python
hazard_dictionary = computed_hazard_rate(list_count, list_age)
```
```zsh
defaultdict(None, {2: -12, 3: -21, 4: -12, 5: 12, 6: 3, 7: 2, 8: 6, 9: -13, 10: 13})
```

### 4. exposures:
Returns the number of bridges in the study at age x.

#### Arguments
- *list_count: list*
- *list_age: list*

#### Returns
- *exposures_dict: dictionary*

#### Example
``` python
age = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
count = [100, 88, 67, 55, 67, 70, 72, 78, 65, 78]
print(exposures(count, age))
```
```zsh
defaultdict(None, {2: -12, 3: -21, 4: -12, 5: 12, 6: 3, 7: 2, 8: 6, 9: -13, 10: 13})
```
### 5. leaves:
Returns the number of bridges left in the study at age x.

#### Arguments
- list_count: list
- list_age: list

#### Returns
- leaves_dict: dictionary

#### Example
``` python
age = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
count = [100, 88, 67, 55, 67, 70, 72, 78, 65, 78]
print(exposures(count, age))
```
```zsh
defaultdict(None, {1: 100, 2: 88, 3: 67, 4: 55, 5: 67, 6: 70, 7: 72, 8: 78, 9: 65, 10: 78})
```
### 6. compute_probabilities:
Returns the compute probabilities of survival given hazard rates

#### Arguments
- *hazard_dictionary: defaultdict*

#### Returns
- *probabilities_dict: dictionary*

#### Example
``` python
# Define hazard 
hazard = defaultdict(None,
                {2: 0.7613636363636364,
                 3: 0.8208955223880597,
                 4: 1.2181818181818183,
                 5: 1.044776119402985,
                 6: 1.0285714285714285,
                 7: 1.0833333333333333,
                 8: 0.8333333333333334,
                 9: 1.2})

# Print and compute probabilities 
print(compute_probabilities(hazard))
```

```zsh
defaultdict(None, {2: 0.23863636363636365, 
                   3: 0.17910447761194026, 
                   4: -0.21818181818181825, 
                   5: -0.04477611940298498, 
                   6: -0.02857142857142847, 
                   7: -0.08333333333333326, 
                   8: 0.16666666666666663, 
                   9: -0.19999999999999996})

```

