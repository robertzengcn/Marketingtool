# -*- coding: utf-8 -*-
import codecs
from deep_translator import GoogleTranslator,BaiduTranslator

GOOGLE_TRANSLATION_LIMIT = 5000
class Translator():
    def __init__(self)-> None:
        pass 

    @staticmethod
    def read_file_as_list(file_name):
        fr = codecs.open(file_name, "r", encoding='utf-8-sig')
        lines = fr.read()
        fr.close()
         # some SRTs such as created by whisper doesn't have \r\n but some other have it
        if "\r\n" in lines:
            return lines.split("\r\n\r\n")
        if "\n\n" in lines:
            return lines.split("\n\n")
    # add /n to the end of text    
    def handletxtend(self, translated_sub:str)-> list[str]:
        if "\r\n" in translated_sub:
            temp_translated = translated_sub.split("\n\r")
            return temp_translated
        elif "\n" in translated_sub:
            temp_translated = translated_sub.split("\n")
            temp_translated[-1] = temp_translated[-1] + "\n"
            return temp_translated
        else:
            return [translated_sub+"\n"]              

    def subtitle_translator(self, file_name, target_language,source_language='auto',translator_tool='google')->str:
        """
        this function translate a subtitle file from original language to desired  language
        
        line may be the order number of the subtitle or just for real line 
        such as answer to age given "33" or there is no order number but "-->"   
        must be present to in the middle of the start and end time of subtitle
        to be shown. There must a empty line between two ordered subtitle.
        Expected / standart subtitle should be like this:    
            1
            00:00:27,987 --> 00:00:29,374
            - Babe.
            - Mmm.
            
            2
            00:00:30,210 --> 00:00:31,634
            - Lizzie.
            - Mmm.
            
            3
        """
        fw = self.write_file(self, file_name, target_language, source_language)
        content_list = self.read_file_as_list(file_name)
        durations = []
        contents = []
        translate_limit = 3000
        # text_translatable = ''
        if translator_tool=='google':
            translate_limit = 5000
            if(target_language=='zh'):
                target_language = 'zh-CN'
            if(source_language=='zh'):
                source_language = 'zh-CN'    
            translator =GoogleTranslator(source=source_language, target=target_language)
        elif translator_tool=='baidu':
            translator =BaiduTranslator(source=source_language, target=target_language)
        else:
            raise Exception("Translator not supported")
        number_of_translatable_content = len(content_list)
        # time_info = ''
        text_info = ''        
        for c in range(number_of_translatable_content):
            lines = []
            # some SRTs such as created by whisper doesn't have \r\n but some other have it
            if "\r\n" in content_list[c]:
                lines = content_list[c].split("\r\n")
            if "\n" in content_list[c]:
                lines = content_list[c].split("\n")


           
            for i in range(len(lines)):
                time_info=''
                if lines[i].rstrip().isdigit() and "-->" in lines[i + 1]:
                    time_info += lines[i] + "\r\n"+lines[i + 1] + "\r\n"
                    durations.append(time_info)
                    continue
                elif "-->" in lines[i]:
                    continue
                else:
                    text_info += lines[i] + "\n" 
        
        if len(text_info) <= 0:
            raise Exception("Subtitle file is not valid")
        elif len(text_info) > translate_limit: 
            # if the text for translation is more than limit characters 
            textlist=text_info.split("\n")     
            prepared_text = ''
            for i in range(len(textlist)):
                prepared_text+=textlist[i]
                # Prepare segmented translation
                if len(prepared_text) > translate_limit-100:
                   translated_sub =translator.translate(prepared_text) 
                   cres=self.handletxtend(translated_sub)
                   contents += cres 
                   prepared_text=''
                else:
                   translated_sub =translator.translate(prepared_text) 
                   cres=self.handletxtend(translated_sub)
                   contents += cres 
        else:
            translated_sub =translator.translate(text_info)  
            cres=self.handletxtend(translated_sub)
            contents += cres  
            # list doesn't have the value at number_of_translatable_content index
            # if ((len(text_translatable) + len(text_info) > (translate_limit-100))and len(text_translatable.strip())>0 )or c == number_of_translatable_content-1:
            #     try:  
            #         print(len(text_translatable))
            #         print(len(text_info))
            #         translated_sub = translator.translate(text_translatable)
            #         print(text_translatable)
            #         print(translated_sub)
            #         # translated_sub = self.yandex_translator(text_translatable, source_language, target_language)
            #         if "\r\n" in translated_sub:
            #             temp_translated = translated_sub.split("\n\r")
            #         elif "\n" in translated_sub:
            #             temp_translated = translated_sub.split("\n")
            #         temp_translated[-1] = temp_translated[-1] + "\n"
            #         contents += temp_translated
            #         #contents.append(temp_translated)
            #     except TypeError as err:
            #         translated_sub = 'err'
            #         print(err)
                    
            #     text_translatable = text_info
            # else:
            #     # print(time_info)
            #     durations.append(time_info)
            #     text_translatable += text_info + "\n\r"
    
        # print(len(contents))
        # print(len(durations))
        # for ic in range(len(contents)):
        #     print(contents[ic])   
        # print(len(contents)) 
        # print(len(durations))   
        for d, c in zip(durations, contents):     
            print(d)
            fw.write(d)
            print(c)
            fw.write(c)
            # print(d + c)
        return self.format_file_name(file_name, target_language, source_language)
        # Print information about the subtitle
        # info = "Translated by subtitle_translator via %s translator \nwritten by Mesut Gunes: https://github.com/gunesmes/subtitle_translator\n" % translator_tool
        # fw.write(info)
        # print(info)
        # print("New file name: ", self.format_file_name(file_name, target_language, source_language))
    @staticmethod
    def write_file(self, file_name, target_language, source_language):
        fn = self.format_file_name(file_name, target_language, source_language)
        fw = open(fn, 'w')

        return fw  
    @staticmethod
    def format_file_name(file_name, target_language, source_language):
        name_sep = "_" + source_language + "_to_" + target_language

        # index number of last dot
        last_dot = file_name.rfind('.')

        # means that there is no dot in the file name, 
        # and file name has no file type extension 
        if last_dot == -1:
            new_file_name = file_name + str(name_sep) + '.srt'

        else:
            baseName = file_name[0: last_dot]
            ext = file_name[last_dot: len(file_name)]
            new_file_name = baseName + str(name_sep) + ext
        return new_file_name  