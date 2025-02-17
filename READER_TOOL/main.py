#!/usr/bin/env python3
from local_file_picker import local_file_picker

from nicegui import ui
import pysubs2
import time

dict_m = {'video_file':"","subtitle_file":"","end_long":999999999,"global_index":0,"current_cn":"","current_other":""}

async def pick_file(type="v") -> None:
    """
    :type :"v" or "s" ，v代表选取video，s代表选取字幕文件
    """
    global dict_m
    result = await local_file_picker('~', multiple=False)
    print(result)
    if type == 'v':
        dict_m['video_file'] = result[0]
    elif type == 's':
        dict_m['subtitle_file'] = result[0]
    show_video.refresh()
    #ui.notify(f'You chose {result}')

def part_play():
    if len(dict_m['subtitle_file']) > 0:
        subs = pysubs2.load(dict_m['subtitle_file'], encoding="utf-8")
        #subs.shift(s=2.5)
        res_all = {}
        for index_i,line in enumerate(subs):
            #print(line)
            s = line.text.split("\\N")
            #a = "123"
            #print(a[a.find("2"):])
            cn,other = (s[0][s[0].find("}")+1:],s[1][s[1].find("}")+1:]) if len(s) > 1 else (s[0][s[0].find("}")+1:],"")
            #print(cn,other)
            #print(line.start/1000,line.end/1000,cn,other)
            res_all[index_i] = (line.start/1000,line.end/1000 - line.start/1000,cn,other)
        return res_all
@ui.refreshable
def show_video():
    if len(dict_m['video_file']) != 0 :
        with ui.row().classes("w-full"):
            v = ui.video(dict_m['video_file'],loop=True)
            def check_time(e):
               "根据播放时长要求停止"
               if time.time() > dict_m['end_long']:
                   v.pause()
               #print(e)
            v.on("timeupdate",handler=check_time)
        with ui.row().classes("w-full"):
            ui.label("abc")
            p = part_play()
            def play_next(p):
                start ,long_s = p[dict_m['global_index']][0],p[dict_m['global_index']][1]
                cur = time.time()
                v.seek(start)
                dict_m['current_cn'] = p[dict_m['global_index']][2]
                dict_m['current_other'] = p[dict_m['global_index']][3]
                dict_m['global_index'] += 1
                dict_m['end_long'] = cur + long_s
                
                v.play()
            def play_re(p):
                if dict_m['global_index'] > 1:
                    dict_m['global_index'] -= 1
                play_next(p)
        with ui.row().classes("w-full"):
            ui.button('重复', on_click=lambda: play_re(p) )
            ui.button('下一条', on_click=lambda: play_next(p))
        with ui.column().classes("w-full"):
            show_sub_title()

def show_sub_title():
    ui.label("").bind_text_from(dict_m,"current_cn")
    ui.label("").bind_text_from(dict_m,"current_other")
@ui.page('/')
def index():
    with ui.row():
        ui.button('选择视频文件', on_click=lambda x:pick_file("v"), icon='folder')
        ui.button('选择字幕文件', on_click=lambda x:pick_file("s"), icon='folder')
    show_video()

ui.run(native=True,reload=True,window_size=(320, 720))
