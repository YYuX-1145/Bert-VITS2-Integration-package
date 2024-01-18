import os
import json
current_directory = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(current_directory,"models","funasr"),exist_ok=True)
os.makedirs(os.path.join(current_directory,"models","whisper_model"),exist_ok=True)




class transcribe():
   def __init__(self,engine="whisper",languages="M",whisper_size="large",transcription_path=None,in_dir=None,out_dir=None,sr=44100,processes=0,use_global_cache=True) -> None:
      self.engine:str=engine
      self.languages:str=languages
      langdict={}
      if "C" in languages.upper():
        langdict["zh"]="ZH|"
      if "J" in languages.upper():
        langdict["ja"]="JP|"
      if "E" in languages.upper():
        langdict["en"]="EN|"
      if langdict=={}:
            langdict = {
            'zh': "ZH|",
            'ja': "JP|",
            "en": "EN|",
        }
      self.langdict:dict=langdict
      self.whisper_size:str=whisper_size
      self.transcription_path:str=transcription_path
      self.in_dir:str=in_dir
      self.out_dir:str=out_dir
      self.sr:int=sr
      self.processes:int=processes
      if not use_global_cache:
         os.environ["MODELSCOPE_CACHE"] = os.path.join(current_directory,"trancscript_models","funasr")
      if engine=="funasr":
        with open(os.path.join(current_directory,"init.json"), 'w', encoding='utf-8') as f:
            json.dump(self.langdict, f, indent=2, ensure_ascii=False)
         


   def run_transcribe(self):
      if self.engine=="funasr":
        from .funasr_transcribe import run
        print("[INFO]: Use Funasr to trancribe...")
      elif self.engine=="genshin":
        from .transcribe_genshin import run
        print("[INFO]: Processing genshin datasets ...")
      else:
        from .whisper_transcribe import run
        print("[INFO]: Use Whisper to trancribe...")
      run(self)


def get_lang(languages):
      if (languages == "C"or languages == "c"):
        lang='ZH'
        return lang,True 
      elif (languages == "J"or languages == "j"):
        lang='JP'
        return lang,True 
      elif (languages == "E"or languages == "e"):
        lang='EN'
        return lang,True
      elif (languages == "M"or languages == "m"):
        return "m",False
      else :
         return None,False 