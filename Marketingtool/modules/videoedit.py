from moviepy.editor import VideoFileClip, concatenate_videoclips,TextClip,CompositeVideoClip
import os.path
class Videoedit():
    def __init__(self)-> None:
        pass 
    
    def insertVideo(self, origin, inVideo, outputpath):
        """
        insert an video into another video
        """
        if os.path.exists(origin)!=True:
            raise FileNotFoundError("origin video File not found")
        if os.path.exists(inVideo)!=True:
            raise FileNotFoundError("insert video File not found")
        splist=self.splitVideo(origin,2)
        clip1=splist[0].resize((1280, 720))
        clip2=splist[1].resize((1280, 720))
        clip3=VideoFileClip(inVideo).resize((1280, 720))
        final_clip = concatenate_videoclips([clip1,clip3,clip2])
        final_clip.write_videofile(outputpath)
        pass
    def splitVideo(self,videopath:str,parts:int)->list:
        
        clip = VideoFileClip(videopath)
        duration = clip.duration
        clip_list = []
        for i in range(parts):
            clip_list.append(clip.subclip(i*duration/parts,(i+1)*duration/parts))
        return clip_list
    def InsertText(self,videopath:str, outputpath:str,text:str,step:int,insertNum:int,fronsize:int,frontcolor:str,duration:int)->str:
        """
        Insert text into video
        """
        outputfilename=os.path.basename(outputpath)
        if outputfilename.lower=='fly':
            raise Exception("output path should not use fly") 
        
        clip = VideoFileClip(videopath) 
        t = 0
        # duration = duration
        textlist=[]
        for x in range(0,insertNum):
            textlist.append(text)
        txt_clips=[]
        for intext,i in zip(textlist,range(0,insertNum)):
            txt_clip = TextClip(intext, fontsize = fronsize, color = frontcolor)
            txt_clip = txt_clip.set_start(t)
            txt_clip = txt_clip.set_pos('top').set_duration(duration) 
            txt_clips.append(txt_clip)
            t=t+step
        finalVideo=[clip]
        for item in txt_clips:
            finalVideo.append(item)
        video = CompositeVideoClip(finalVideo) 
        video.write_videofile(outputpath)   
        return outputpath
        