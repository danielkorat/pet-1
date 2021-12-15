# DLSA Using PET


## Install

```
pip install -r requirements.txt
```

## Train

See variables in `run_train.sh` for setting dataset and hyperparametrs.

Run:
```
./run_train.sh
```

Run in background:
```
./bg.sh
```

Average accuracy and elapsed training time over all seeds is saved to `output_{timestamp}/final_result.txt`.