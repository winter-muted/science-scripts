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
python install.py
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

batch-benchmark -> time various job sizes to find the best bang for y(our) buck.

batch-del -> delete all jobs you are currently running when mistakes are made.

lab-stats -> query the database to see who is hogging the queue.

## Contribute
To improve a script or add a new one, make a pull request.
`pull code`

New scripts must have a help interface.
