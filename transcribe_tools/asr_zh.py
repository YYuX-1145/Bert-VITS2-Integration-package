from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
inference_pipeline = pipeline(
                task=Tasks.auto_speech_recognition,
                model='damo/speech_paraformer-large-vad-punc_asr_nat-zh-cn-16k-common-vocab8404-pytorch',
                model_revision="v1.2.4",
                vad_model='damo/speech_fsmn_vad_zh-cn-16k-common-pytorch',
                punc_model='damo/punc_ct-transformer_zh-cn-common-vocab272727-pytorch',)
def transcribe_zh(save_path):
    return inference_pipeline(audio_in=save_path)["text"]