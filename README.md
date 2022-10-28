# DataPrism
Suggested Python: 3.9.13

## Reproducibility Steps

### Step 0: Download and Install git lfs

Follow the instructions here: https://git-lfs.github.com/

Once downloaded and installed, set up Git LFS for your user account by running: 

```
git lfs install
```

You only need to run this once per user account.

### Step 1: Download this repo and cd to it

```
git clone https://github.com/sainyam/DataPrism
cd DataPrism
```

### Step 2: Download datasets.zip
```
https://drive.google.com/file/d/1syQhwIRwdWJBqqT0mJQWfN9LGsZOylnV/view?usp=sharing
```

### Step 3: Install dependencies

```
sudo apt-get install -y virtualenv
virtualenv venv
source ./venv/bin/activate 

pip install -r requirements.txt
```

In case you want to use a custom location for python, please use virtualenv -p <PYTHON_PATH> venv instead
### Step 3: Generate all plots

```
bash reproduce.sh
```

One of the baselines (Anchors) take several hours to run for all experiments. To avoid running only this baselline, please run any script with flag `-a off`. Example:

```
bash reproduce.sh -a off
```  

Plots will be present in freshRuns/ folder
