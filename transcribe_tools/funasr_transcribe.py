import os

import torchaudio
from tqdm import tqdm
from multiprocessing import Pool
from . import funasr_transcribe_one
from .funasr_transcribe_one import get_text



#from modelscope.pipelines import pipeline
#from modelscope.utils.constant import Tasks


current_directory = os.path.dirname(os.path.abspath(__file__))
os.environ["MODELSCOPE_CACHE"] = os.path.join(current_directory,"trancscript_models","funasr")



def transcribe_one(item):
    parent_dir,sav_dir,speaker,wavfile,target_sr=item
    if not wavfile.startswith("processed_"):
        try:
            assert os.path.splitext(wavfile)[-1]==".wav"
            save_path = sav_dir+"/"+ speaker + "/" + f"processed_{wavfile}"
            lab_path = sav_dir+"/"+ speaker + "/" + f"processed_{os.path.splitext(wavfile)[0]}.lab"
            wav_path =parent_dir + "/" + speaker + "/" + wavfile
            if not os.path.exists(save_path):                
                processed=True
                wav, sr = torchaudio.load(wav_path, frame_offset=0, num_frames=-1, normalize=True,channels_first=True)
                wav = wav.mean(dim=0).unsqueeze(0)
                if sr != target_sr:
                        wav = torchaudio.transforms.Resample(orig_freq=sr, new_freq=target_sr)(wav)
                if wav.shape[1] / sr > 20:
                        print(f"warning: {wavfile} too long\n")
                torchaudio.save(save_path, wav, target_sr, channels_first=True)
            else:
                   processed=False

                
            try:
                with open((lab_path), "r", encoding="utf-8") as f:
                    text=f.read()
                assert text[0:3] =="ZH|"
                print("[进度恢复]： "+lab_path+"已找到并已经成功读取") 
            except:# transcribe text
                if not processed:
                    print("[进度恢复]： "+lab_path+"未找到、读取错误或不是目标语言")            
                text = get_text(save_path) 
                assert text !=""  
                print(text)      
                text = "ZH|" + text + "\n"
                with open((lab_path), "w", encoding="utf-8") as f:
                    f.write(text)        
            return "./"+save_path.replace('\\','/') + "|" + speaker + "|" + text 
        except Exception as e:
            print(e)  

def run_transcription(speaker,processs):
    global parent_dir,sav_dir,target_sr
    global speaker_annos
    tasks = [(parent_dir,sav_dir,speaker,wavfile,target_sr) for wavfile in os.listdir(os.path.join(parent_dir,speaker))]
    with Pool(processes=processs) as p:                
        speaker_annos += list(tqdm(p.imap(transcribe_one,tasks),total=len(tasks)))
        

def run(args):
    global parent_dir,sav_dir,target_sr
    global speaker_annos
    parent_dir=args.in_dir
    sav_dir=args.out_dir
    speaker_names = list(os.walk(parent_dir))[0][1]
    speaker_annos = []
    target_sr = args.sr
    processs=args.processes
    if processs<=0:
            processs=1
    print(f"使用进程数量：{processs}")
    for speaker in speaker_names:
        print(f'Speaker: {speaker}')
        os.makedirs(sav_dir+"/"+ speaker,exist_ok=True)
        run_transcription(speaker,processs)

    #end
    #print(speaker_annos)
    if len(speaker_annos) == 0:
        print("Warning: length of speaker_annos == 0")
        print("this IS NOT expected. Please check your file structure and make sure your audio language is supported.")
    else:
        with open(args.transcription_path, 'w', encoding='utf-8') as f:
            for line in speaker_annos:
                if line is None:
                     continue
                f.write(line)
        print("finished")