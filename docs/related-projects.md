<h1 align='center'>
    Related Projects
</h1>

This documentation provides the project workflow of the relevant bridge projects.

## Decision Tree Project
The workflow for the decision tree project consists of data acquisition, data cleaning and transformation, modeling, and prediction. Figure 1 describes the five-step process of this project.

![methodology for the project](../images/decision-tree-process.png)
<p align='center'> <b> Fig. 1 Data process for the Actuarial Life Table </b> </p>


### Data acquisition
To acquire the NBI dataset this sections provides in detail [instructions](../../index.md).
 
### Data cleaning and transformation
The NBI dataset is a temporal dataset containing data from across all states in the united states from 1992 - 2022. To build a model to predict future maintenance of the model or deterioration. We have employed several transformation techniques that take into account the format of the data.

The data generation is a separate script from the data acquisition script, and it is often customized according to the application. The generation of data also considers basic cleaning and transformation of the dataset. For each application, we have highlighted the transformation taken to reproduce the dataset.

This format takes into account the ground truth.
- [Maintenance](maintenance-decision-tree.md) 
- [Deterioration](deterioration-decision-tree.md) 
