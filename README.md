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
git lfs clone https://github.com/sainyam/DataPrism
cd DataPrism
```

### Step 2: Install dependencies

```
sudo apt-get virtualenv
virtualenv venv
source ./venv/bin/activate 

pip install -r requirements.txt
```

### Step 3: Generate all plots

```
bash reproduce.sh
```
