import os
import sys

from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks


current_directory = os.path.dirname(os.path.abspath(__file__))
os.environ["MODELSCOPE_CACHE"] = os.path.join(current_directory,"models","funasr")
inference_pipeline = pipeline(
                task=Tasks.auto_speech_recognition,
                model='damo/speech_paraformer-large-vad-punc_asr_nat-zh-cn-16k-common-vocab8404-pytorch',
                model_revision="v1.2.4")   

def get_text(save_path):
    global inference_pipeline
    return inference_pipeline(audio_in=save_path)["text"] 