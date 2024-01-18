from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
inference_pipeline = pipeline(
                task=Tasks.auto_speech_recognition,
                model="damo/speech_UniASR_asr_2pass-ja-16k-common-vocab93-tensorflow1-offline",
            )
def transcribe_jp(save_path):
    text = inference_pipeline(audio_in=save_path)["text"].strip()
    text = text.replace(" ", "")
    return text