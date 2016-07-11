# RinaSystems test taks

### Simple distriubute computing app including linear, multiprocessing and celery processing

## How to use
1. Clone package:
   `git clone https://github.com/yaroslavprogrammer/rinasystems-test`
2. Go to cloned dir and run `source bootstrap.sh` or `. bootstrap.sh` than all setup will be automated
3. Then download DB or move from another dir to `taskcelery/db/`, you will have something like this `taskcelery/db/edrmv2txt-v2/...subdirs`
4. To run tasks just `cd taskcelery` and `python runner celery 4000` (4000 is number of files will be scanned) then open another console in same dir then activate env by `source env.sh` and run `celery -A words.tasks worker` with any args as you want. There are `linear and multiprocessing` workers available in runner.
5. For gui task open `taskgui/index.html` (will be updated soon)

### All taks was runned in Core i7 6500U. Gained perfomance 35s per 10000 files using 4 parallel workers. Finded bottleneck is nltk function
