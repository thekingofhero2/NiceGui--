from nicegui import ui
import random
import requests
import os
"""
50 yin
"""
base_resource_dir = r"D:\workspace\NiceGui--\READER_TOOL\resources\50"
def download_words(word):
    print(word)
    url = f"https://dict.youdao.com/dictvoice?le=jap&audio={word}&type=3"
    # 发送HTTP GET请求
    response = requests.get(url)

    # 检查响应状态码是否为200（成功）
    if response.status_code == 200:
        # 检查Content-Type是否为音频格式
        content_type = response.headers.get('Content-Type')

        if 'audio' in content_type:
            # 打开一个文件以二进制写模式保存内容
            with open(os.path.join(base_resource_dir,word+".mp3"), 'wb') as file:
                file.write(response.content)
            #print("文件已成功保存为 downloaded_media.mp3")
        else:
            print(f"下载的文件不是音频格式，Content-Type: {content_type}")
    else:
        print(f"请求失败，状态码: {response.status_code}")

def get_data():
    """
    :type 取值 all 全部/ping 平假名/pian 片假名/zhuo_pian 浊音片假名...
    """
    global global_setting
    global global_current_word
    true_keys = [x[0] for x in filter(lambda x:x[1] == True,global_setting["check_group"].items())]
    print(true_keys)
    dict_50 = {
        "ping":[{"label":"あ","roma":"a"},{"label":"い","roma":"i"},{"label":"う","roma":"u"},{"label":"え","roma":"e"},{"label":"お","roma":"o"},{"label":"か","roma":"ka"},{"label":"き","roma":"ki"},{"label":"く","roma":"ku"},{"label":"け","roma":"ke"},{"label":"こ","roma":"ko"},{"label":"さ","roma":"sa"},{"label":"し","roma":"shi"},{"label":"す","roma":"su"},{"label":"せ","roma":"se"},{"label":"そ","roma":"so"},{"label":"た","roma":"ta"},{"label":"ち","roma":"chi"},{"label":"つ","roma":"tsu"},{"label":"て","roma":"te"},{"label":"と","roma":"to"},{"label":"な","roma":"na"},{"label":"に","roma":"ni"},{"label":"ぬ","roma":"nu"},{"label":"ね","roma":"ne"},{"label":"の","roma":"no"},{"label":"は","roma":"ha"},{"label":"ひ","roma":"hi"},{"label":"ふ","roma":"fu"},{"label":"へ","roma":"he"},{"label":"ほ","roma":"ho"},{"label":"ま","roma":"ma"},{"label":"み","roma":"mi"},{"label":"む","roma":"mu"},{"label":"め","roma":"me"},{"label":"も","roma":"mo"},{"label":"や","roma":"ya"},{"label":"ゆ","roma":"yu"},{"label":"よ","roma":"yo"},{"label":"ら","roma":"ra"},{"label":"り","roma":"ri"},{"label":"る","roma":"ru"},{"label":"れ","roma":"re"},{"label":"ろ","roma":"ro"},{"label":"わ","roma":"wa"},{"label":"を","roma":"wo"},{"label":"ん","roma":"n"}]
        ,"pian":[{"label":"ア","roma":"a"},{"label":"イ","roma":"i"},{"label":"ウ","roma":"u"},{"label":"エ","roma":"e"},{"label":"オ","roma":"o"},{"label":"カ","roma":"ka"},{"label":"キ","roma":"ki"},{"label":"ク","roma":"ku"},{"label":"ケ","roma":"ke"},{"label":"コ","roma":"ko"},{"label":"サ","roma":"sa"},{"label":"シ","roma":"shi"},{"label":"ス","roma":"su"},{"label":"セ","roma":"se"},{"label":"ソ","roma":"so"},{"label":"タ","roma":"ta"},{"label":"チ","roma":"chi"},{"label":"ツ","roma":"tsu"},{"label":"テ","roma":"te"},{"label":"ト","roma":"to"},{"label":"ナ","roma":"na"},{"label":"ニ","roma":"ni"},{"label":"ヌ","roma":"nu"},{"label":"ネ","roma":"ne"},{"label":"ノ","roma":"no"},{"label":"ハ","roma":"ha"},{"label":"ヒ","roma":"hi"},{"label":"フ","roma":"fu"},{"label":"ヘ","roma":"he"},{"label":"ホ","roma":"ho"},{"label":"マ","roma":"ma"},{"label":"ミ","roma":"mi"},{"label":"ム","roma":"mu"},{"label":"メ","roma":"me"},{"label":"モ","roma":"mo"},{"label":"ヤ","roma":"ya"},{"label":"ユ","roma":"yu"},{"label":"ヨ","roma":"yo"},{"label":"ラ","roma":"ra"},{"label":"リ","roma":"ri"},{"label":"ル","roma":"ru"},{"label":"レ","roma":"re"},{"label":"ロ","roma":"ro"},{"label":"ワ","roma":"wa"},{"label":"ヲ","roma":"wo"},{"label":"ン","roma":"n"}]
        ,"zhuo_pian":[{"label":"ガ","roma":"ga"},{"label":"ギ","roma":"gi"},{"label":"グ","roma":"gu"},{"label":"ゲ","roma":"ge"},{"label":"ゴ","roma":"go"},{"label":"ザ","roma":"za"},{"label":"ジ","roma":"ji"},{"label":"ズ","roma":"zu"},{"label":"ゼ","roma":"ze"},{"label":"ゾ","roma":"zo"},{"label":"ダ","roma":"da"},{"label":"で","roma":"de"},{"label":"ド","roma":"do"},{"label":"ヂ(ji)","roma":"di"},{"label":"づ(zu)","roma":"du"},{"label":"バ","roma":"ba"},{"label":"ビ","roma":"bi"},{"label":"ブ","roma":"bu"},{"label":"ベ","roma":"be"},{"label":"ボ","roma":"bo"}]
        ,"zhuo_ping":[{"label":"が","roma":"ga"},{"label":"ぎ","roma":"gi"},{"label":"ぐ","roma":"gu"},{"label":"げ","roma":"ge"},{"label":"ご","roma":"go"},{"label":"ざ","roma":"za"},{"label":"じ","roma":"ji"},{"label":"ず","roma":"zu"},{"label":"ぜ","roma":"ze"},{"label":"ぞ","roma":"zo"},{"label":"だ","roma":"da"},{"label":"デ","roma":"de"},{"label":"ど","roma":"do"},{"label":"ぢ(ji)","roma":"di"},{"label":"ヅ(zu)","roma":"du"},{"label":"ば","roma":"ba"},{"label":"び","roma":"bi"},{"label":"ぶ","roma":"bu"},{"label":"べ","roma":"be"},{"label":"ぼ","roma":"bo"}]
        ,"banzhuo_ping":[{"label":"ぱ","roma":"pa"},{"label":"ぴ","roma":"pi"},{"label":"ぷ","roma":"pu"},{"label":"ぺ","roma":"pe"},{"label":"ぽ","roma":"po"}]
        ,"banzhuo_pian":[{"label":"パ","roma":"pa"},{"label":"ピ","roma":"pi"},{"label":"プ","roma":"pu"},{"label":"ペ","roma":"pe"},{"label":"ポ","roma":"po"}]
        ,"ao_ping":[{"label":"きゃ","roma":"kya"},{"label":"きゅ","roma":"kyu"},{"label":"きょ","roma":"kyo"},{"label":"しゃ","roma":"sha"},{"label":"しゅ","roma":"shu"},{"label":"しょ","roma":"sho"},{"label":"ちゃ","roma":"cha"},{"label":"ちゅ","roma":"chu"},{"label":"ちょ","roma":"cho"},{"label":"にゃ","roma":"nya"},{"label":"にゅ","roma":"nyu"},{"label":"にょ","roma":"nyo"},{"label":"みゃ","roma":"mya"},{"label":"みゅ","roma":"myu"},{"label":"みょ","roma":"myo"},{"label":"りゃ","roma":"rya"},{"label":"りゅ","roma":"ryu"},{"label":"りょ","roma":"ryo"},{"label":"ぎゃ","roma":"gya"},{"label":"ぎゅ","roma":"gyu"},{"label":"ぎょ","roma":"gyo"},{"label":"じゅ","roma":"ju"},{"label":"じょ","roma":"jo"},{"label":"びゃ","roma":"bya"},{"label":"びゅ","roma":"byu"},{"label":"びょ","roma":"byo"},{"label":"ぴゃ","roma":"pya"},{"label":"ぴゅ","roma":"pyu"},{"label":"ぴょ","roma":"pyo"}]
        ,"ao_pian":[{"label":"きゃ","roma":"kya"},{"label":"キュ","roma":"kyu"},{"label":"キョ","roma":"kyo"},{"label":"シャ","roma":"sha"},{"label":"シュ","roma":"shu"},{"label":"ショ","roma":"sho"}, {"label":"チャ ","roma":"cha"},{"label":"チュ","roma":"chu"},{"label":"チョ","roma":"cho"}, {"label":"ニャ","roma":"nya"},{"label":"ニュ","roma":"nyu"},{"label":"ニョ","roma":"nyo"},{"label":"ミャ","roma":"mya"},{"label":"ミュ","roma":"myu"},{"label":"ミョ","roma":"myo"},{"label":"リャ","roma":"rya"},{"label":"リュ","roma":"ryu"},{"label":"リョ","roma":"ryo"},{"label":"ギヤ","roma":"gya"},{"label":"ギユ","roma":"gyu"},{"label":"ギョ","roma":"gyo"},{"label":"ジュ","roma":"ju"},{"label":"ジョ","roma":"jo"},{"label":"ビャ","roma":"bya"},{"label":"ビュ","roma":"byu"},{"label":"ビョ","roma":"byo"},{"label":"ピャ","roma":"pya"},{"label":"ピュ","roma":"pyu"},{"label":"ピョ","roma":"pyo"}]
    }
    res = []
    for true_key in true_keys:
        res.extend(dict_50[true_key])
    print("本次练习：",res)
    random.shuffle(res)
    print("本次练习random：",res)
    global_typing_list['typing_list'] = res
    global_current_word = {"current_index":-1,"label":"","roma":"","right":False}
    get_next()

# @ui.refreshable
# def show_change():
#     pass
global_setting = {"audio":""
                  ,"check_group":{"ping":True,
                                "pian":True,
                                "zhuo_pian":True,
                                "zhuo_ping":True,
                                "banzhuo_ping":True,
                                "banzhuo_pian":True,
                                "ao_ping":True,
                                "ao_pian":True}
}
global_typing_list = {"typing_list":[]}
global_current_word = {"current_index":-1,"label":"","roma":"","right":False}
def get_next():
    global global_current_word
    global global_typing_list
    typing_list = global_typing_list['typing_list']
    curr_index = global_current_word["current_index"]
    # for i,item in enumerate(typing_list):
    #     if item['label'] == global_current_word['label']:
    #         curr_index = i 
    #         break 
    curr_index +=1
    if curr_index < 0 :
        curr_index = 0
    if curr_index == len(typing_list):
        ui.notify("本次练习结束！")
        return 
    if len(typing_list)>0:
        label = typing_list[curr_index]["label"]
        roma  = typing_list[curr_index]['roma']
        global_current_word = {"current_index":curr_index,"label":label,"roma":roma,"right":False}
    show_page.refresh()

def check_input(e,ui_audio):
    if e.value == global_current_word['roma']:
        word = global_current_word['label']
        mp3_file = os.path.join(os.path.join(base_resource_dir,word+".mp3"))
        if not os.path.exists(mp3_file):
            download_words(word)
        ui_audio.set_source(mp3_file)
        ui_audio.play()
        get_next()
        
        print(global_current_word)
    else:
        global_current_word['right'] = True
    print(e)


@ui.refreshable
def show_page(ui_audio):
    with ui.column().classes("w-full"):
        ui.label().classes("text-h2").bind_text_from(global_current_word,"label")
        ui.label().bind_text_from(global_current_word,"roma").bind_visibility(global_current_word,"right")   
        ui.input( ).props('autofocus').on_value_change(lambda e:check_input(e,ui_audio))
@ui.page("/")
def page_50():
    with ui.row().classes("w-full"):
        ui.checkbox("平",value=True,on_change=get_data).bind_value(global_setting['check_group'],"ping")
        ui.checkbox("片",value=True,on_change=get_data).bind_value(global_setting['check_group'],"pian")
        ui.checkbox("浊平",value=True,on_change=get_data).bind_value(global_setting['check_group'],"zhuo_ping")
        ui.checkbox("浊片",value=True,on_change=get_data).bind_value(global_setting['check_group'],"zhuo_pian")
        ui.checkbox("半浊平",value=True,on_change=get_data).bind_value(global_setting['check_group'],"banzhuo_ping")
        ui.checkbox("半浊片",value=True,on_change=get_data).bind_value(global_setting['check_group'],"banzhuo_pian")
        ui.checkbox("拗平",value=True,on_change=get_data).bind_value(global_setting['check_group'],"ao_ping")
        ui.checkbox("拗片",value=True,on_change=get_data).bind_value(global_setting['check_group'],"ao_pian")

    ui_audio = ui.audio(src="")
    
    get_data()
    
    #print(len(global_typing_list['typing_list']),len(list(set([i['label'] for i in global_typing_list['typing_list']]))))
    
    show_page(ui_audio)

#page_50()
ui.run(native=True,reload=True,window_size=(360, 720))
