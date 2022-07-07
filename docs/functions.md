# 🗂  Functions 

The following the documentation for are the function used in the model.

| Functions| Description | Argument type | Return type |
| -------- | ------------| ------------- | ----------- |
| create_dummy_data | Returns a NBI dummy data | None | data - List |
| compute_hazard_score | Returns a computed dummy hazard score | None | data - List |
| identify_window | creates segmentation for data | from_year, to_year | data - List |
| leaves | returns the number of bridges that leave the study at age x|list_count, list_age | leaves_dict - dictionary |
| exposures | returns the number of bridges in the study at age x | list_count, list_age | exposures_dict - dictionary |

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
new_data - list

#### Example

```python
data = identify_window()
```
### 3. compute_hazard_scored:
Returns computation of the harzard function

#### Arguments

```python
```
```python
```

#### Return
computed_hazard_scored

#### Example

```python
data = computed_hazard_scored()
```

### 4. exposures:
Returns the number of bridges in the study at age x.

#### Arguments
- list_count: list
- list_age: list

#### Returns
- exposures_dict: dictionary

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

## 💡 Conceptual overview of the essential actuarial functions.  

| Item         | Description |
| ------------ | ----------- |
| leave(x)     | The number of bridges that leave the study at age x.|
| exposures(x) |  The number of bridges in the study at age x|
| h(x) | Hazard rate age x. See equation 1 |
| S(x) | Survival rate age x. See equation 2 |
| F(x) | The mortality rate (or cumulative probability of failure) of bridges exposed at age 1 before reaching age x |
| y_P_1 | Probability of survival at age y for the next year. See Equation 5 |
