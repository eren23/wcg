![WCG Logo](assets/logo.png)


# WCG (Web Code Generator)
WCG is a llm based html code generator. It is a tool that currently supports javascript to be used in chrome extensions and python selenium scripts. The tool is being designed to use as a tool in larger agent based systems to navigate in websites using high level commands and tasks to be executed in the browser. With the data obtained through this interactions the goal is to finetune new smaller models to be used in the agent based system.

This project was inspired by another OS project [LaVague](https://github.com/lavague-ai/LaVague), and at the beginning based on that fundamentally but has many changes to align with the goals of this project.

Though the code generation is working ok based on the tests, the project has still yet to have a working demo with the agent based system on an extension or a selenium script. 

TODO:

- [ ] Create a working demo on a chrome extension
- [ ] Create a working demo on a selenium script
- [ ] Support more inference providers for larger availability of models
- [ ] Make the module a pip package
- [ ] Make the code better and more readable
- [ ] Support small language models trained on the data obtained from the agent based system
- [ ] Integrate in a larger agent based system

## Installation

```bash
git clone https://github.com/eren23/wcg
python setup.py install
```

## Usage

Currently no extension is supported so I suggest using the backend directly or use the way I use it in the backend. 

```bash
uvicorn app:app --reload
```

```bash
cd examples
python test_client.py
```