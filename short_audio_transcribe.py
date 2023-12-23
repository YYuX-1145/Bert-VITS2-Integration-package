import whisper
import os
import json
import torchaudio
import argparse
import torch
from config import config
current_directory = os.path.dirname(os.path.abspath(__file__))
os.environ['PATH']=os.path.join(current_directory,"ffmpeg","bin")
lang2token = {
            'zh': "ZH|",
            'ja': "JP|",
            "en": "EN|",
        }
def transcribe_one(audio_path):
    # load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(audio_path)
    audio = whisper.pad_or_trim(audio)

    # make log-Mel spectrogram and move to the same device as the model
    try:
        mel = whisper.log_mel_spectrogram(audio).to(model.device)
        _, probs = model.detect_language(mel)
    except:
        mel = whisper.log_mel_spectrogram(audio=audio, n_mels=128).to(model.device)
        _, probs = model.detect_language(mel)

    # detect the spoken language
    
    print(f"Detected language: {max(probs, key=probs.get)}")
    lang = max(probs, key=probs.get)
    # decode the audio
    options = whisper.DecodingOptions(beam_size=5)
    result = whisper.decode(model, mel, options)

    # print the recognized text
    print(result.text)
    return lang, result.text
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--languages", default="CJ")
    parser.add_argument("--whisper_size", default="medium")
    args = parser.parse_args()
    if args.languages == "CJE":
        lang2token = {
            'zh': "ZH|",
            'ja': "JP|",
            "en": "EN|",
        }
    elif args.languages == "CJ":
        lang2token = {
            'zh': "ZH|",
            'ja': "JP|",
        }
    elif args.languages == "C":
        lang2token = {
            'zh': "ZH|",
        }
    assert (torch.cuda.is_available()), "Please enable GPU in order to run Whisper!"
    #model = whisper.load_model(args.whisper_size)
    model = whisper.load_model(args.whisper_size, download_root = ".\\whisper_model")
    #parent_dir = "./custom_character_voice/"
    parent_dir=config.resample_config.in_dir
    sav_dir=config.resample_config.out_dir
    speaker_names = list(os.walk(parent_dir))[0][1]
    speaker_annos = []
    total_files = sum([len(files) for r, d, files in os.walk(parent_dir)])
    with open(config.train_ms_config.config_path,'r', encoding='utf-8') as f:
        hps = json.load(f)
    target_sr = hps['data']['sampling_rate']
    processed_files = 0
    for speaker in speaker_names:
        print(f'Speaker: {speaker}')
        os.makedirs(sav_dir+"/"+ speaker,exist_ok=True)
        for i, wavfile in enumerate(list(os.walk(os.path.join(parent_dir,speaker)))[0][2]):
            # try to load file as audio
            if wavfile.startswith("processed_"):
                continue
            try:
                save_path = sav_dir+"/"+ speaker + "/" + f"processed_{wavfile}"
                lab_path = sav_dir+"/"+ speaker + "/" + f"processed_{os.path.splitext(wavfile)[0]}.lab"
                wav_path =parent_dir + "/" + speaker + "/" + wavfile
                if not os.path.exists(save_path):                
                    processed=True
                    wav, sr = torchaudio.load(wav_path, frame_offset=0, num_frames=-1, normalize=True,
                                          channels_first=True)
                    wav = wav.mean(dim=0).unsqueeze(0)
                    if sr != target_sr:
                        wav = torchaudio.transforms.Resample(orig_freq=sr, new_freq=target_sr)(wav)
                    if wav.shape[1] / sr > 20:
                        print(f"warning: {wavfile} too long\n")
                    torchaudio.save(save_path, wav, target_sr, channels_first=True)
                else:
                   processed=False

                # transcribe text
                try:
                    with open((lab_path), "r", encoding="utf-8") as f:
                        text=f.read()
                    assert text[0:3] in lang2token.values()
                    print("[进度恢复]： "+lab_path+"已找到并已经成功读取") 
                except:
                    if not processed:
                        print("[进度恢复]： "+lab_path+"未找到、读取错误或不是目标语言")
                    lang, text = transcribe_one(save_path)
                    if lang not in list(lang2token.keys()):
                        print(f"{lang} not supported, ignoring\n")
                        continue
                #text = "ZH|" + text + "\n"                
                    text = lang2token[lang] + text + "\n"
                    with open((lab_path), "w", encoding="utf-8") as f:
                        f.write(text)
                speaker_annos.append("./"+save_path.replace('\\','/') + "|" + speaker + "|" + text)
                processed_files += 1
                print(f"Processed: {processed_files}/{total_files}")
            except Exception as e:
                print(e)
                continue
    #end
    if len(speaker_annos) == 0:
        print("Warning: length of speaker_annos == 0")
        print("this IS NOT expected. Please check your file structure , make sure your audio language is supported or check ffmpeg path.")
    else:
        with open(config.preprocess_text_config.transcription_path, 'w', encoding='utf-8') as f:
            for line in speaker_annos:
                f.write(line)
        print("finished")
