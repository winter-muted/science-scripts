# science-scripts 
A collection of scripts to help automate certain tasks common in HPC usage

## Installation
Clone the repo to a directory of your choice
```git clone https://www.github.com/winter-muted/science-links.git```

Run the install script
`./install.sh` or `python install.py`

Make the new commands available
`source ~/.bashrc`

To stay up to date:
`git pull --rebase origin master`
`python install.py`


## Descriptions

batch-benchmark -> time various job sizes to find the best bang for y(our) buck.

batch-del -> delete all jobs you are currently running when mistakes are made.

lab-stats -> query the database to see who is hogging the queue.

## Contribute
To improve a script or add a new one, make a pull request.
`pull code`

New scripts must have a help interface.
