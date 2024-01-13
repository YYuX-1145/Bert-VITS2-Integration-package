from config import config
import json
import argparse
import time

if __name__ == "__main__":
    with open(config.train_ms_config.config_path,'r', encoding='utf-8') as f:
        hps = json.load(f)
    target_sr = hps['data']['sampling_rate']
    parser = argparse.ArgumentParser()
    parser.add_argument("--engine", default="whisper",type=str)
    parser.add_argument("--languages", default="CJE",type=str)
    parser.add_argument("--whisper_size", default="medium",type=str)
    parser.add_argument("--transcription_path", default=config.preprocess_text_config.transcription_path,type=str)
    parser.add_argument("--in_dir", type=str, default=config.resample_config.in_dir, help="path to source dir")
    parser.add_argument("--out_dir", type=str, default=config.resample_config.out_dir, help="path to target dir")
    parser.add_argument("--sr", default=target_sr,type=int)
    parser.add_argument("--processes", default=1,type=int)    
    args = parser.parse_args()

    if args.engine=="funasr":
        from transcribe_tools.funasr_transcribe import run
        print("[INFO]: Use Funasr to trancribe...")
    elif args.engine=="genshin":
        from transcribe_tools.transcribe_genshin import run
        print("[INFO]: Processing genshin datasets ...")
    else:
        from transcribe_tools.whisper_transcribe import run
        print("[INFO]: Use Whisper to trancribe...")
        
    t1 = time.time()
    run(args)
    t2 = time.time()
    m, s = divmod(t2-t1, 60)
    use_time="%02d:%02d"%(m, s)
    print(f'所用时间:{use_time}')