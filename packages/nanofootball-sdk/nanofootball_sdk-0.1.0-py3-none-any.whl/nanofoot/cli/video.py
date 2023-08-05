from .. import VideoService
import yaml
import logging
import sys
logger=logging.getLogger('cli.video_commands')
logger.setLevel(level=logging.DEBUG)

def delete_video(args):
    v=VideoService()
    try:
        video=v.get(args.id)
        if video: #if video exists
            v.delete(args.id)
            logger.info(f'Deleted video {video}.')
            return True
        else:
            logger.warn(f'Delete: Video {str(args.id)} not exist')
        #for some reasons twice deleting videos returns sucess from api
    except Exception as e:
        logger.error(f'Cant delete video {str(args.id)}: {e}')

def info_video(args):
    v=VideoService()
    video_info=v.get(args.id)
    if video_info:
        return video_info
    else:
        logger.error(f'Video {args.id} not exists')
    
