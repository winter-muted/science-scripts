# science-scripts 
A collection of scripts to help automate certain tasks common in HPC usage

## Installation
_Clone the repo to a directory of your choice:_
```
git clone https://www.github.com/winter-muted/science-scripts.git
```

_Run either install script:_
```
./install.sh
_or_
python install.py ( not yet implemented 2/11 )
```

_Make the new commands available:_
```
source ~/.bashrc
```

_To stay up to date:_
```
git pull --rebase origin master
python install.py
```


## Descriptions

qsub-bench -> time various job sizes to find the best bang for (y)our buck. (BETA!!)

qsub-batch -> batch submission of pbs files. (BETA!!)

del-batch -> delete jobs you are currently running when mistakes are made. (not implemented yet)

lab-stats -> query the database to see who is hogging the queue. (not implemented yet)

## Contribute
To improve a script or add a new one, make a pull request. It is recommended that you use a devel branch.

New scripts must have a help interface.
