from os import listdir
from os.path import isfile, join
import ffmpy
import subprocess
import json
from peewee import *
import os

db = MySQLDatabase('convert', user='', password='', host='localhost', port=3306)


class BaseModel(Model):
    class Meta:
        database = db


class Track(BaseModel):
    title = CharField(null=True)
    artist = CharField(null=True)
    class Meta:
        table_name = 'tracks'


class File(BaseModel):
    trackid = IntegerField()
    filename = CharField(null=True)
    class Meta:
        table_name = 'files'


class Artist(BaseModel):
    id = BigIntegerField()
    name = CharField(null=True)
    class Meta:
        table_name = 'artists'

db.connect()


def validate(val):
    return val.encode('utf-8').decode('utf-8')


mypath = '<input path here>'
outpath = '<output path here>'


onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

def get_output_files():
    if os.path.isdir(outpath):
        return [f for f in listdir(outpath) if isfile(join(outpath, f))]
    else:
        print ("@@@ Output folder doesn't exists @@@\n")


for file in onlyfiles:
    if '.mov' in file or '.mp4' in file:
        tup_resp = ffmpy.FFprobe(
            inputs={file: None},
            global_options=[
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_format', '-show_streams']
        ).run(stdout=subprocess.PIPE)

        meta = json.loads(tup_resp[0].decode('utf-8'))

        filename = ''

        query = (File.select(File.filename, Track.title, Artist.name)
            .join(Track, on=(Track.id==File.trackid))
            .join(Artist, on=(Artist.id==Track.artist))
            .where(File.filename==file))
        
        for cursor in query:
            if cursor.track.artist.name:
                filename = validate(cursor.track.artist.name) + ' - '

            if cursor.track.title:
                filename = filename + validate(cursor.track.title)

            if filename is not '':
                filename = filename + '.mp4'

                out_filename = outpath + '/' + filename
                input_filename = mypath + '/' + file

                output_list = get_output_files()

                if filename not in output_list:
                    # convert file
                    ff = ffmpy.FFmpeg(
                        inputs={
                            input_filename: None
                        },
                        outputs={
                            out_filename: [
                                '-metadata', 'title='+cursor.track.title,
                                '-metadata', 'artist='+cursor.track.artist.name
                            ]
                        }
                    )

                    ff.run()