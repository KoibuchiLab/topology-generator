# topology-generator
This repo generates a customized topology for given number of node and network degree.

## Prerequisite
* pandas
* networkx

In case of installation by pip, the following is recommended (for ubuntu).
```shell
$ sudo apt-get install python-pip
$ sudo pip install pandas networkx
```

## Run
```shell
$ python nwGen.py -f <inputfile> -n <nodes> -d <degree>
```
Or you can edit your configuration in [trafficPattern.py](trafficPattern.py) and simply run
```shell
$ python nwGen.py
```

## Source Files
### [nwGen.py](nwGen.py)
* This is the main program.
### [algorithm.py](algorithm.py)
* This includes various required algorithms in the main program.
### [trafficPattern.py](trafficPattern.py)
* This helps to produce classical traffic patterns.

## Output
The topology information is stored in the output/ folder. Each line follows the format as follows.
```
src_sw src_port dst_sw dst_port
```
Switches are numbered from 0, and ports are numbered from 1.
Note that, port 0 is retained for the local host.