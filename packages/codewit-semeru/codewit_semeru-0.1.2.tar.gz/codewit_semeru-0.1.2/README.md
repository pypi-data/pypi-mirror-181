# What-If-Code-Tool
## Visualization Tool for Code Generation Model Analysis

![demo-gif](Artifacts/codewit_demo.gif)
## Main Idea
[Google WIT](https://github.com/PAIR-code/what-if-tool) was the main inspiration for this project. Our goal is to create a similar tool purely for focusing on ML models revolving around software engineering design and principles, such as code completion and code generation. 

[BertViz](https://github.com/jessevig/bertviz) is a good first example for where our tool will go. We hope to support a full dashboard of several views that researchers would find helpful in order to analyze their models. This would probably include newly generated word count charts, probability distributions for new tokens, and attention views.

## Development
- Pip tool: user can install this tool from pip/conda and utilize with their NLP model
- Python Backend: user designates dataset and model as parameters for our tool. Our tool then runs the model and produces some vector dataset in its object.
- Jupyter-Dash Frontend: Jupyter-Dash allows for easy creation for data dashboard. Provides ability for easy callback methods with just Python.
<!-- - Ideas for Frontend
  - Dashboard: Several visuals at the same time. This would allow the user to interact with each of the visuals provided
  - One at a time: User designates which view they want to see from their view at any given point
  - Visuals would be available in python notebooks
- Some ideas: BertViz, Google WIT
- Plotly is a great tool to create large dashboard from python. Could be useful for a dashboard view
- Flask/Django can be used to implement the interactive component of the charts (connect listening events to python code) -->

## Development Plans
<!-- - [ ] Interview ML researchers (SEMERU) for what specific views would be useful for their exploration
- [x] Implement back-end to spit out some output to dynamic html
- [ ] Create new views, probability distribution
- [x] Allow for some interactive aspect with the charts -->
- [x] Code concept groupings view: categorize each of the tokens generated in output based on what type they are in code language (declaration, assignment, functions, etc.)
- [x] Display some statistics about the generated output with specific model (median, max, min, etc.)
- [x] Dynamics re-execution of pipeline when:
  - [ ] User edits # of tokens
  - [ ] User edits # of input sequences
  - [x] User changes model
  - [x] User selects new descriptive statistic
- [ ] Implement bertviz attention models inside app with Dash if possible

## Current Diagrams
### Components UML
![Components](Artifacts/component-diagram-updated.png)

### Sequence Diagram
![Sequence Diagram](Artifacts/sequence-diagram-updated.png)

## Supported Features
- [ ] 4 different views to visually classify code generation models (ind. token, token distrubtion, python token types, token type distribtuion)
- [ ] 4 pre-trained models for code generation from Hugging Face (GPT2, CodeGen, CodeParrot, GPT-Neo)
- [ ] Descriptive stats for datasets with many input sequences
- [ ] Dynamic re-execution on user inputs

## Installation
First prototype is currently available on PyPi. User will need to generate their own Hugging Face API token. 

```
%pip install codewit-semeru
%load_ext autoreload
%autoreload 2
```
```
from datasets.load import load_dataset
import pandas as pd

DATA_LEN = 1024
NUM_DATA = 20

dataset = load_dataset("code_x_glue_cc_code_completion_line", "python", split="train")

pruned_dataset = []
for i, input_seq in enumerate(dataset):
    temp = input_seq["input"]  # type: ignore
    if len(temp) <= DATA_LEN:
        pruned_dataset.append(temp)
    if len(pruned_dataset) >= NUM_DATA:
        break
pd.DataFrame(pruned_dataset).describe()
```
```
WITCode("codeparrot/codeparrot-small", pruned_dataset, "{api_key_goes_here}")
```
These lines can be run directly from your notebook. Python 3.8 is required. First chunk installs pip module, load auto-reload function. Second chunk loads up the CodeXGlue Code Completion dataset to be utilized with our tool. The last block is the actual implementaion in notebook to run our tool. User needs to supply their own api token to query HF models.

### Build and Run Docker Image
Start docker

Navigate to project folder and run ```docker-compose up -d --build``` to build image

Navigate to ```localhost:8888``` to run jupyter notebook. password is ```wit```

To stop docker container run ```docker-compose down```


### Build and Run Docker Image
Start docker

Navigate to project folder and run ```docker-compose up -d --build``` to build image

Navigate to ```localhost:8888``` to run jupyter notebook. password is ```wit```

To stop docker container run ```docker-compose down```

