# sh-miR API #
[![GNU License](http://img.shields.io/badge/license-GNU-blue.svg)](http://www.gnu.org/licenses/gpl.html)
[![Documentation Status](https://readthedocs.org/projects/shmir-api/badge/?version=latest)](https://readthedocs.org/projects/shmir-api/?badge=latest)

## Requirements ##

* [docker](https://www.docker.com)
* [docker-compose](https://docs.docker.com/compose/)

That's all you need, how cool is that? :)

If you use SELinux, please allow to create volumes in directory where sh-miR
designer is cloned. Assuming you're in this directory, please execute:

```
    $ sudo chcon -Rvt svirt_sandbox_file_t .
```

## Quick Start ##

To start server:
```
    $ docker-compose up
```
You may need to run this command by root.

After this commands server builds all its dependencies and start sh-miR RESTful API.


## Usage ##

### There are three services: ###
* mfold
* creating sh-miR(s) from siRNA
* creating sh-miR(s) from transcript


Each of them have three URLs:
* task creator URL - */service/DATA?optional_arg1=1&optional_arg2=2
* status URL - */service/status/TASK_ID
* result URL - */service/result/TASK_ID


Where:
* service - one of services
* DATA - data which is needed to do task
* TASK_ID - id of created task


## Services ##
* mfold
    * creator - returns TASK_ID <br> URL: `*/mfold/DATA`
    * status - returns STATUS (ok, error, fail) <br> URL: `*/mfold/status/TASK_ID`
    * result - returns zipped results of folding <br> URL: `*/mfold/result/TASK_ID`

Where DATA is a sequence which we would like to fold.

Examples:
```
    $ curl -i http://127.0.0.1:8080/mfold/UUUGUAUUCGCCCUAGCGC
    $ curl -i -X GET http://127.0.0.1:8080/mfold/status/f3591b31-49d9-47da-ae78-898792db26a5
    $ curl -i -X GET http://127.0.0.1:8080/mfold/result/f3591b31-49d9-47da-ae78-898792db26a5
```
<br>
* from_sirna
    * creator - returns TASK_ID <br> URL: `*/from_sirna/DATA`
    * status - returns STATUS (ok, error, fail) <br> URL: `*/from_sirna/status/TASK_ID`
    * result - returns list of tuples (score sh-miR, backbone name, pdf) <br> URL: `*/from_sirna/result/TASK_ID`

Where DATA is a one siRNA strand (active) or two siRNA strands separated by space (in url "%20"). First strand is active, both are in 5-3 orientation.
Pdf is a task ID of mfold. To get this file use mfold service.

Examples:
```
    $ curl -i http://127.0.0.1:8080/from_sirna/UUUGUAUUCGCCCUAGCGC%20CGCUAUGGCGAAUACAAACA
    $ curl -i -X GET http://127.0.0.1:8080/from_sirna/status/f3591b31-49d9-47da-ae78-898792db26a5
    $ curl -i -X GET http://127.0.0.1:8080/from_sirna/result/f3591b31-49d9-47da-ae78-898792db26a5
```
Then we download folded sh-miR: <br>
`$ curl -i -X GET http://127.0.0.1:8080/mfold/result/4bbee83a-0337-4efa-a018-13517390ebd1`

<br>
* from_transcript
    * creator - returns TASK_ID <br> URL: `*/from_transcript/DATA?optional`
        * min_gc - minimal GC content (default 40)
        * max_gc - maximal GC content (default 60)
        * max_offtarget - maximal offtarget (default 10)
        * mirna_name - name of backbone (default 'all')
        * stymulators - immunostimulatory sequences `['yes', 'no', 'no_difference']` (default 'no_difference')
    * status - returns STATUS (ok, error, fail) <br> URL: `*/from_transcript/status/TASK_ID`
    * result - returns list of dicts with keys: sh_mir, score, pdf, sequence and bacbone <br> URL: `*/from_transcript/result/TASK_ID`

Where DATA is transcript name from NCBI
Pdf is task ID of mfold. To get this file use mfold service.

Examples:
```
    $ curl -i http://127.0.0.1:8080/from_transcript/NM_001164782.1
    $ curl -i -X GET http://127.0.0.1:8080/from_transcript/status/f3591b31-49d9-47da-ae78-898792db26a5
    $ curl -i -X GET http://127.0.0.1:8080/from_transcript/result/f3591b31-49d9-47da-ae78-898792db26a5
```
Then we download folded sh-miR:<br>
    `$ curl -i -X GET http://127.0.0.1:8080/mfold/result/4bbee83a-0337-4efa-a018-13517390ebd1`


## Development ##

### Debuging
Put somewhere in the code:
`import rpdb; rpdb.set_trace()`
Connecting to rpdb:
`$ ./scripts/rpdb_docker`

### Downloading own blast database
`$ ./scripts/blast_docker`

### Clearing caches
`$ ./scripts/flush`

### Watching celery tasks (flower):
Go to: <i>$DOCKER_IP</i>:5555/
