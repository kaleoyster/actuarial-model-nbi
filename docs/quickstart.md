<h1 align='center'>
            ⚡️ Quickstart 
</h1>

## Table of Content

The following are the steps required to get the this project up and running:
1. Data acquistion
2. Installation of required packages and software
3. Process datasets
4. Generate application datasets
5. Configure and generate results 

### Installation of required packages and software
The implementation of this project is based on python and mongoDB. This project uses document style database to collect and store the cleaned inspection records from 1992 to 2022 for all states. 

#### Install MongoDB
The following are the installation instructions for community edition of [Linux](https://www.mongodb.com/docs/manual/administration/install-on-linux/), [Windows](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-windows/), and [MacOS](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-os-x/).

#### Install Python
The following are the instructions for installing python for [Linux](https://www.python.org/downloads/source/), [Windows](https://www.python.org/downloads/release/python-3106/), and [MacOS](https://www.python.org/downloads/macos/).

#### Install Git
The following are the instructions for installing Git for [Linux](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git), [Windows](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git), and [MacOs](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

### Data acquisition 
There are two main ways to acquire the NBI datasets:
1. Manual 
2. Automated

#### Manual acquisition
[InfoBridge](https://infobridge.fhwa.dot.gov/Data) and [FHWA](https://www.fhwa.dot.gov/bridge/nbi/ascii.cfm) host NBI dataset for all states and from year 1992 to 2022. InfoBridges has accompanying interface that also allows for selection of specific attributes.

#### Automated acquisition

This sections provide in detail the instructions.

####  Download NBI files
```zsh
python Downloadv1.py
```


### Generate application datasets

#### Generate dataset

```zsh
python generate_dataset.py
```


### Configure and generate results

#### Configuration

To configure the actuarial model to produce results for specific fields or study window, Edit `main` function in the `actuarial.py` python script.

The following is an example of the a configuration.
```python
def main():
    
    # Owner
    field = 'owner'
    yNames = ['1', '2', '3', '4']

    # Study window years
    studywindow = [[1992, 2002], # Study window 1
                   [2002, 2004]] # Study window 2
    heatmaps = []
    for category in yNames:
        rates = compute_categorical_lifetable(data,
                                          study_window_years,
                                          field,
                                          category)
        heatmaps.append(rates[0])

```

#### Execution

```zsh
python actuarial.py
```

