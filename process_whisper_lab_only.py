import os
import argparse
from config import config

global speaker_annos
speaker_annos = []


def process_text(item):
    spkdir, wav_name, args = item
    speaker = spkdir.replace("\\", "/").split("/")[-1]
    wav_path = os.path.join(args.in_dir, speaker, wav_name)
    global speaker_annos
    tr_name = wav_name.replace('.wav', '')
    try:
        with open(args.out_dir+'/'+speaker+'/'+tr_name+'.lab', "r", encoding="utf-8") as file:
             text = file.read()
        #text = f'{lang}|{text}\n' #
        speaker_annos.append(args.out_dir+'/'+speaker+'/'+wav_name+ "|" + speaker + "|" + text)
    except:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--in_dir", type=str, default=config.resample_config.in_dir, help="path to source dir")   
    parser.add_argument("--out_dir", type=str, default=config.resample_config.out_dir, help="path to target dir")    
    parent_dir=config.resample_config.in_dir
    print("请注意，这个处理程序只能够处理2.1版整合包whisper打标的音频，不能处理原神数据集。文件内容格式为: <语言>|<文本>\n")
    speaker_names = list(os.walk(parent_dir))[0][1]   
    args = parser.parse_args()     
    for speaker in os.listdir(args.in_dir):
        spk_dir = os.path.join(args.in_dir, speaker)
        if os.path.isdir(spk_dir):
            print(spk_dir)
            for i in os.listdir(spk_dir):
               if i.endswith("wav"):
                  pro=(spk_dir, i, args)
                  process_text(pro)
    if len(speaker_annos) == 0:
        print("transcribe error. len(speaker_annos) == 0")
    else:
      with open(config.preprocess_text_config.transcription_path, 'w', encoding='utf-8') as f:
        for line in speaker_annos:
            f.write(line)
      print("finished.")