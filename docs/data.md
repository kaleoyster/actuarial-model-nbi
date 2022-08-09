<h1 align='center'>
        Data 
</h1>
This page only describes the seleciton of attributes, data cleaning, and data transformation of the NBI data used for this project. For any information regarding data acquistion, please follow the these [instructions](google.com) . Also, for a brief steps follow the [quickstart](quickstart.md) page.

## Background
The NBI dataset is a temporal dataset containing data from across all states in the united states from 1992 - 2022. To build a model to predict future maintenance of the model or
deterioration. We have employed several transformation techniques that take into account the format of the data. The data generation is a separate script from the data acquisition script, and it is often customized according to the application. The generation of data also considers basic cleaning and transformation of the dataset. For this application, we have highlighted the transformation taken to reproduce the dataset.

### Assumptions
There are several considerations regarding the bridge inspection dataset used in this project:
1. When a maintenance event occurs on a bridge and that event is recorded, the bridge is permanently removed from the study. 
2. There are other options on how to handle a bridge once a maintenance event occurs, each with its own consequences. These include:
    - Allow the bridge to re-enter the study at the same age.
    - Allow the bridge to re-enter the study at a younger age, given the type of maintenance which occurred.
3. The data generation scripts takes into account all the aspects of the assumptions.
