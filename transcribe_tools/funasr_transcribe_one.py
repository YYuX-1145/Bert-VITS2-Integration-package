import os
import sys
import json


current_directory = os.path.dirname(os.path.abspath(__file__))
cfg_path=os.path.join(current_directory,"init.json")
init_cfg = json.load(open(cfg_path, encoding="utf-8"))
#os.remove(cfg_path)
lang_asr_map={}
if "zh" in init_cfg:
     from .asr_zh import transcribe_zh 
     lang_asr_map["ZH"]=transcribe_zh
if "ja" in init_cfg:
     from .asr_jp import transcribe_jp 
     lang_asr_map["JP"]=transcribe_jp
if "en" in init_cfg:
     from .asr_en import transcribe_en 
     lang_asr_map["EN"]=transcribe_en
if lang_asr_map=={}:
      print("ERROR : lang_dict is EMPTY !!!")
        
def get_text(save_path,lang):
        global lang_asr_map           
        return lang_asr_map[lang](save_path)