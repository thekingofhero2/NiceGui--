#!/usr/bin/env python3
from local_file_picker import local_file_picker

from nicegui import ui
import pysubs2
import time
import re 
from nicegui.events import KeyEventArguments,KeyboardModifiers,GenericEventArguments
from settings import *
import os 

class MainTool:
    def __init__(self):
        self.dict_m =  {'video_file':""#r"C:\Users\lenovo\Videos\bilibili\output\IT商务日语-面试-【短评】面接的重点.mp4"
          ,"subtitle_file":""#r"C:\Users\lenovo\Videos\bilibili\output\IT商务日语-面试-【短评】面接的重点.srt"
          ,"subtitle_file_z":""#r"C:\Users\lenovo\Videos\bilibili\output\IT商务日语-面试-【短评】面接的重点.ja.srt"
          ,"end_long":999999999
          ,"global_index":0
          ,"current_cn":""
          ,"current_other":""
          ,"show_current":False
          ,"last_directory":"~"}

    async def pick_file(self,type="v") -> None:
        """
        :type :"v" or "s" ，v代表选取video，s代表选取字幕文件
        """
        print(self.dict_m['last_directory'])
        result = await local_file_picker(self.dict_m['last_directory'], multiple=False)
        if result is not None:
            self.dict_m['last_directory'] = os.path.dirname(result[0])
            if type == 'v':
                self.dict_m['video_file'] = result[0]
            elif type == 's':
                self.dict_m['subtitle_file'] = result[0]
            elif type == 's_z':
                self.dict_m['subtitle_file_z'] = result[0]
            self.show_video.refresh()
        #ui.notify(f'You chose {result}')

    
    @ui.refreshable
    def show_video(self,):
        
        if len(self.dict_m['video_file']) != 0 :
            with ui.row().classes("w-full"):
                self.v = ui.video(self.dict_m['video_file'],loop=True)
                def check_time(e):
                    "根据播放时长要求停止"
                    if time.time() > self.dict_m['end_long']:
                        self.v.pause()
                #print(e)
                self.v.on("timeupdate",handler=check_time)
            with ui.row().classes("w-full"):
                #ui.label("abc")
                self.p = self.part_play()
                
                    
            with ui.row().classes("w-full"):
                ui.button('上一条', on_click=lambda: self.play_before())
                ui.button('重复', on_click=lambda: self.play_re() )
                ui.button('下一条', on_click=lambda: self.play_next())
            
            with ui.row().classes("w-full"):
                ui_input = ui.input().on("keyup.ctrl",handler=lambda  e: self.handle_key(e)).props("autofocus").classes("w-full")


            with ui.column().classes("w-full"):
                self.show_sub_title()

    def handle_key(self,e:GenericEventArguments):
        print(e.args['code'])

        #ctrl+r 重复当前
        #ctrl+b 回上一句
        #ctrl+n 下一句
        if e.args['code'] == 'KeyR':
            self.play_re()
        if e.args['code'] == 'KeyB':
            self.play_before()
        if e.args['code'] == 'KeyN' :
            self.play_next()
        if e.args['code'] == 'Enter' :
            self.play_re()
            
            self.dict_m["show_current"] = True
            
        # if e.key in ('r','R') and KeyboardModifiers.ctrl :
        #     self.play_re()
        # if e.key in ('b','B') and KeyboardModifiers.ctrl :
        #     self.play_before()
        # if e.key in ('n','N') and KeyboardModifiers.ctrl :
        #     self.play_next()
    def show_sub_title(self,):
        with ui.column().classes("w-full"):
            ui.label("中文相关说明：")
            ui.input().classes("w-full h-[60px]").bind_value_from(self.dict_m,"current_cn")#.bind_visibility_from(self.dict_m,"show_current")
            ui.label("外文原文：")
            ui.input().classes("w-full h-[60px]").bind_value_from(self.dict_m,"current_other").bind_visibility_from(self.dict_m,"show_current")
            
        
    def play_next(self):
        "播放下一曲"
        start ,long_s = self.p[self.dict_m['global_index']][0],self.p[self.dict_m['global_index']][1]
        cur = time.time()
        self.v.seek(start)
        self.dict_m['current_cn'] = self.p[self.dict_m['global_index']][2]
        self.dict_m['current_other'] = self.p[self.dict_m['global_index']][3]
        self.dict_m['global_index'] += 1
        self.dict_m['end_long'] = cur + long_s
        self.dict_m["show_current"] = False
        self.v.play()
    def play_re(self,):
        "播放重复"
        if self.dict_m['global_index'] > 0:
            self.dict_m['global_index'] -= 1
        self.play_next()
    def play_before(self,):
        "播放上一曲"
        if self.dict_m['global_index'] > 0:
            self.dict_m['global_index'] -= 1
        #再退一步
        if self.dict_m['global_index'] > 0:
            self.dict_m['global_index'] -= 1
        self.play_next()
    def part_play(self,):
        if len(self.dict_m['subtitle_file']) > 0 and len(self.dict_m['subtitle_file_z']) > 0 :
            subs_org = pysubs2.load(self.dict_m['subtitle_file'], encoding="utf-8")
            subs_z = pysubs2.load(self.dict_m['subtitle_file_z'], encoding="utf-8")
            if len(subs_org) != len(subs_z):
                ui.notify("字幕文件不对！")
                return
            else:
                res_all = {}
                for index_i,line in enumerate(subs_org):
                    cn,other = (subs_z[index_i].text,line.text)
                    if line.start not in res_all.keys():
                        res_all[line.start] = (line.start/1000,line.end/1000 - line.start/1000,cn,other)
                
               
            res_all2 = {}
            for index_i ,item in enumerate(res_all.items()):
                print(item[1])
                res_all2[index_i]=item[1]
            return res_all2
        # if len(self.dict_m['subtitle_file']) > 0:
        #     subs = pysubs2.load(self.dict_m['subtitle_file'], encoding="utf-8")
        #     def lang_type(txt):
        #         jap = re.compile(r'[\u3040-\u309F\u30A0-\u30FF\uAC00-\uD7A3]')  # \uAC00-\uD7A3为匹配韩文的，其余为日文
        #         if jap.search(txt):
        #             return 'jap'
        #         return 'cn'
        #     res_all = {}
        #     for index_i,line in enumerate(subs):
        #         cn,other = (None,None)
        #         s = line.text.split("\\N")
        #         if len(s) > 1:
        #             #说明 中文、外文都在一条字幕上显示（无论是这个时代 还是人心 \\N 時代も 人の心も）
        #             cn,other = (s[0][s[0].find("}")+1:],s[1][s[1].find("}")+1:])
        #         else:
        #             #说明 中文、外文都不一条字幕上显示，需要将两个starttime相同的字幕关联起来。
        #             s = s[0]
        #             if lang_type(s) == 'cn':
        #                 cn = s
        #             else:
        #                 other = s
        #         if line.start not in res_all.keys():
        #             res_all[line.start] = (line.start/1000,line.end/1000 - line.start/1000,cn,other)
        #         else:
        #             if cn is None:
        #                 res_all[line.start] = (line.start/1000,line.end/1000 - line.start/1000,res_all[line.start][2],other)
        #             elif other is None:
        #                 res_all[line.start] = (line.start/1000,line.end/1000 - line.start/1000,cn,res_all[line.start][3])
               
        #     res_all2 = {}
        #     for index_i ,item in enumerate(res_all.items()):
        #         res_all2[index_i]=item[1]

        #     return res_all2
@ui.page('/')
def index():
    maintool = MainTool()
    with ui.row():
        ui.button('选择视频文件', on_click=lambda x:maintool.pick_file("v"), icon='folder')
        ui.button('选择外文字幕文件', on_click=lambda x:maintool.pick_file("s"), icon='folder')
        ui.button('选择中文字幕文件', on_click=lambda x:maintool.pick_file("s_z"), icon='folder')
    
   
        
    
    #keyboard = ui.keyboard(on_key=maintool.handle_key)
    maintool.show_video()

#ui.run(host='0.0.0.0',native=True,reload=True,window_size=(320, 720))
ui.run(native=True,reload=True,window_size=(640, 800))
