import logging,sys

logging.basicConfig(stream=sys.stderr,format="%(message)s")
logging.root.setLevel(logging.INFO)

# if -q setlevel warn
# if -debug basicconfig() i meant thange the format of messages

import argparse
from .video import delete_video,info_video


def exercise_cmd():
    raise NotImplemented()


parser = argparse.ArgumentParser(prog='nf')

parser.add_argument('--output-as',choices=['json','yaml','short'],default='short')
subparsers = parser.add_subparsers(help='сущности')

video_parser = subparsers.add_parser('video', help='Default')

video_commands=video_parser.add_subparsers(help='video comands')
del_video=video_commands.add_parser('delete')
del_video.add_argument('id',type=int)
del_video.set_defaults(invoke=delete_video)

info_video_parser=video_commands.add_parser('info')
info_video_parser.add_argument('id',type=int)
info_video_parser.set_defaults(invoke=info_video)


cam_parser = subparsers.add_parser('exercise', help='parse this instead of default')
cam_parser.set_defaults(which=exercise_cmd)

def write_to_stdout(data):
    sys.stdout.write(data)

def invoke_subparser_job(args): # invoking function binded to subparser
    return args.invoke(args)



import yaml,json
def main():
    argument = parser.parse_args()

    output_data=invoke_subparser_job(argument) #invoking a function for particular parser
    if argument.output_as=='short':
        output=str(output_data)
    elif argument.output_as=='yaml':
        output=yaml.dump(output_data.raw_data)
    elif argument.output_as=='json':
        output=json.dumps(output_data.raw_data,indent=4)
    else:
        raise Exception('Wrong parameter in --output-as')

    write_to_stdout(output)