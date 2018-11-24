# Convert MOV and MP4 files to MP4 using python and ffmpeg

This script reads mov and mp4 files from input folder and get title and artist name from mysql database.
It converts each file into mp4 file with filename like 'artist name - title.mp4'.
When convering files, this script adds artist name and title into its metadata.
If filename what you want to convert doesn't exit in output folder, it starts converting.


## Dependency
Download [Python](https://www.python.org/downloads)


## Build Setup

```bash
# install peewee (ORM for python)
$ pip install peewee

# install ffmpy (ffmpeg wrapper)
$ pip install ffmpy

# install mysql connector
$ pip install PyMySQL

# run script
$ python convert.py
```


