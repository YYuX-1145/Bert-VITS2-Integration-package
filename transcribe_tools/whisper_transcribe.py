import whisper
import os

import torchaudio

import torch

current_directory = os.path.dirname(os.path.abspath(__file__))


def transcribe_one(audio_path):
    global model
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
    if lang=="zh":
        options = whisper.DecodingOptions(beam_size=5,prompt="在这三大欲望当中，因为食欲是满足人类生存需求的欲望。所以，满足食欲的行为，在这三者中，优先性是第一位的。")
    else:
        options = whisper.DecodingOptions(beam_size=5)
    result = whisper.decode(model, mel, options)

    # print the recognized text
    print(result.text)
    return lang, result.text
def run(args):
    global model
    print(args.langdict)
    assert (torch.cuda.is_available()), "Please enable GPU in order to run Whisper!"
    if not args.use_global_cache:
        model = whisper.load_model(args.whisper_size, download_root = os.path.join(current_directory,"trancscript_models","whisper_model"))
    else:
        model = whisper.load_model(args.whisper_size)
    #parent_dir = "./custom_character_voice/"
    parent_dir=args.in_dir
    sav_dir=args.out_dir
    speaker_names = list(os.walk(parent_dir))[0][1]
    speaker_annos = []
    total_files = sum([len(files) for r, d, files in os.walk(parent_dir)])

    processed_files = 0
    for speaker in speaker_names:
        print(f'Speaker: {speaker}')
        os.makedirs(sav_dir+"/"+ speaker,exist_ok=True)
        for i, wavfile in enumerate(list(os.walk(os.path.join(parent_dir,speaker)))[0][2]):
            # try to load file as audio
            if wavfile.startswith("processed_") or os.path.splitext(wavfile)[-1]!=".wav":
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
                    if sr != args.sr:
                        wav = torchaudio.transforms.Resample(orig_freq=sr, new_freq=args.sr)(wav)
                    if wav.shape[1] / sr > 20:
                        print(f"warning: {wavfile} too long\n")
                    torchaudio.save(save_path, wav, args.sr, channels_first=True)
                else:
                   processed=False

                # transcribe text
                try:
                    with open((lab_path), "r", encoding="utf-8") as f:
                        text=f.read()
                    assert text[0:3] in args.langdict.values()
                    print("[进度恢复]： "+lab_path+"已找到并已经成功读取") 
                except:
                    if not processed:
                        print("[进度恢复]： "+lab_path+"未找到、读取错误或不是目标语言")
                    lang, text = transcribe_one(save_path)
                    if lang not in list(args.langdict.keys()):
                        print(f"{lang} not supported, ignoring\n")
                        continue
                #text = "ZH|" + text + "\n"                
                    text = args.langdict[lang] + text + "\n"
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
        with open(args.transcription_path, 'w', encoding='utf-8') as f:
            for line in speaker_annos:
                f.write(line)
        print("finished")
