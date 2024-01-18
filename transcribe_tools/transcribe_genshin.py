import os
import librosa
import numpy as np
from multiprocessing import Pool, cpu_count
from . import get_lang
import soundfile
#from scipy.io import wavfile
from tqdm import tqdm



def process(item):  
    spkdir, wav_name, args = item
    speaker = spkdir.replace("\\", "/").split("/")[-1]
    wav_path = os.path.join(args.in_dir, speaker, wav_name)
    if os.path.exists(wav_path) and '.wav' in wav_path:
        os.makedirs(os.path.join(args.out_dir, speaker), exist_ok=True)
        wav, sr = librosa.load(wav_path, sr=args.sr)
        soundfile.write(
            os.path.join(args.out_dir, speaker, wav_name),
            wav,
            sr
        )

def process_text(item):
    spkdir, wav_name, args,lang = item
    speaker = os.path.split(spkdir)[-1]
    #wav_path = os.path.join(args.in_dir, speaker, wav_name)
    global speaker_annos
    tr_name = wav_name[:-4]
    with open(args.in_dir+'/'+speaker+'/'+tr_name+'.lab', "r", encoding="utf-8") as file:
             text = file.read()
    text = text.replace("{NICKNAME}",'旅行者')
    text = text.replace("{M#他}{F#她}",'他')
    text = text.replace("{M#她}{F#他}",'他')
    text = text.replace("|",'')
    if "{M#妹妹}{F#哥哥}" in text:
        if tr_name.endswith("a"):
           text = text.replace("{M#妹妹}{F#哥哥}",'妹妹')
        if tr_name.endswith("b"):
           text = text.replace("{M#妹妹}{F#哥哥}",'哥哥')
    text = text.replace("#",'')   
    text = f'{lang}|{text}\n' #
    speaker_annos.append(args.out_dir+'/'+speaker+'/'+wav_name+ "|" + speaker + "|" + text)

  

def run(args):
    global speaker_annos
    speaker_annos = []
    lang = None
    if len (args.languages)==1:
       languages=args.languages
       lang,entered=get_lang(languages)
    while lang is None:
      print("Enter a letter to choose language.\n")
      print("C = Chinese ; J = Japanese ;E = English;M = Chose language for each speaker later.\n e.g: C \n")
      languages=input("Enter language: ")
      lang,entered=get_lang(languages)
      if lang is not None:
         break
      else:
        print("Illegal Arguments! Please try again.\n")

    processs = args.processes
    if processs<=0:
      print("processes=AUTO")
      processs = cpu_count()-2 if cpu_count() >4 else 1
    print(f"使用进程数：{processs}")
    pool = Pool(processes=processs)
    print(f'Using Language:{lang}')
    for speaker in os.listdir(args.in_dir):
        spk_dir = os.path.join(args.in_dir, speaker)
        if os.path.isdir(spk_dir):
          if not entered:
            lang=None
            while lang is None or lang=="m":
                lang,_ = get_lang(input(f"Enter a letter to choose language for Speaker: {spk_dir} :"))
            print(f"{spk_dir}:{lang}")
            for _ in tqdm(pool.imap_unordered(process, [(spk_dir, i, args) for i in os.listdir(spk_dir) if i.endswith("wav")])):
                pass
            for i in os.listdir(spk_dir):
               if i.endswith("wav"):
                  pro=(spk_dir, i, args, lang)
                  process_text(pro)
    if len(speaker_annos) == 0:
        print("transcribe error. len(speaker_annos) == 0")
    else:
      with open(args.transcription_path, 'w', encoding='utf-8') as f:
        for line in speaker_annos:
            f.write(line)
      print("finished.")
