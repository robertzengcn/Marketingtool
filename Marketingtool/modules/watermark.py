# -*- coding: utf-8 -*-
import os
import subprocess
import tempfile
import re
import get_watermark
class RunCommandError(Exception):
    pass
class Watermark():
    def __init__(self):
        pass
    def remove_watermark(self,video_path:str,output_path:str,max_frames:int=50):
        """
        remove watermark from video
        """
        if os.path.exists(video_path)!=True:
            raise FileNotFoundError("File not found")        
        tmpdir =self.getframe(video_path,max_frames)
        getWaterMark=get_watermark()
        image_path=getWaterMark.get_watermarks(tmpdir)
        if image_path==None:
            raise Exception("watermark not generate success")
        # start to remove watermark
        removecmd="ffmpeg -hide_banner -loglevel warning -y -stats -i "+video_path+" -acodec copy -vf \"removelogo="+image_path+"/mask.png\" "+output_path+""
        self.cmd(removecmd)
    def getframe(self,video_path:str,max_frames:int=50)->str:    
        """
        get frame from video
        """
        getframe="ffprobe -hide_banner -loglevel warning -select_streams v -skip_frame nokey -show_frames -show_entries frame=pkt_dts_time "+video_path+" | grep \"pkt_dts_time=\" | xargs shuf -n "+str(max_frames)+" -e | awk -F  \"=\" '{print $2}'"
        keyframes_time=self.cmd(getframe)
        tmpdir = tempfile.mkdtemp()
        print("Extracting frames (up to: "+str(max_frames)+")... to the tmp path:"+tmpdir)
        counter=0
        for i in keyframes_time: 
            if not re.match("^[0-9]+([.][0-9]+)?$", i): 
                print("Skipping unrecognize timing: " + i)
                continue
        generateframe="ffmpeg -y -hide_banner -loglevel error -ss "+i+" -i "+video_path+" -vframes 1 "+tmpdir+"/output_"+counter+".png\""
        self.cmd(generateframe)
        # print("$counter ")
        counter=counter+1
        if counter < 2:
            raise Exception("frames extracted, need at least 2, aborting.")
        return tmpdir
    def cmd(command):
        subp = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding="utf-8")

        if subp.poll() == 0:
            return subp.communicate()[1]
        else:
            raise RunCommandError("run command error for:"+subp.communicate()[1])