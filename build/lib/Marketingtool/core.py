from Marketingtool.commandline import get_command_line
import os
import logging
from Marketingtool.config import get_config
from Marketingtool.audioprocess import Audioprocess



logger = logging.getLogger(__name__)


class WrongConfigurationError(Exception):
    pass



def main(return_results=False, parse_cmd_line=True, config_from_dict=None,external_config_file_path=None):
    if parse_cmd_line:
        cmd_line_args = get_command_line()
        if cmd_line_args.get('config_file', None):
            external_config_file_path = os.path.abspath(
                cmd_line_args.get('config_file'))
            logger.info("external config file is {}".format(
                external_config_file_path))
    config = get_config(cmd_line_args, external_config_file_path, config_from_dict)    
    action = config.get('action', None)
    
    if action == 'transcribe':
        audiofile = config.get('audio-file', None)
        if audiofile == None:
            raise WrongConfigurationError("audio file is not specified")
        audioprocess = Audioprocess()
        
        audioprocess.transcribeSpeech() 

    
    

