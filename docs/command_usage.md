# 版本V2.1
# 训练和命令行使用说明
## 注意：管理器里的每个按钮都对应了命令或训练相关操作。你需要自己学习训练流程。（如果使用webui，则不需要手动复制任何文件。）
```
%PYTHON% 
```
指代了包内的python环境，使用时代替
```
python
```
如果要使用自己的环境，需要更改管理器代码。修改是极其简单的。
## 环境维护和升级（示例）：

 ```
 %PYTHON% -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
 ```
 一般情况下无需执行此命令。  
 看不懂的也不要执行这条命令。

## 0.安装ffmpeg：
```
%PYTHON% setup_ffmpeg.py
```
执行一次即可。安装是把当前文件夹下ffmpeg加入环境变量，因此执行完不要移动或删除。否则需要手动更改环境变量。***安装完可能需要重启才能生效。部分设备可能要手动加入系统的path,请自行寻找教程。***

# 注意：首先需要创建或更改全局设置。作用见default_config.yml。将config.yml放在根目录下即可生效。
## 参数解释
* `num_workers` : 简单地说是训练集加载线程数。这个值越高，内存开销越大，内存16G的情况下不建议设置太大。如果过低则会影响训练速度。


# 1.数据集重采样和标注：
* 训练需要没有噪声和背景音乐且说话清晰的单语言音频。
* 如果已有list文件，自行按训练流程处理对应文件，并将音频自行重采样至44100Hz单声道。请注意：某些软件导出的音频可能导致训练错误。
* 这一步会生成符合格式的.list数据集标注文件，包含路径，语言，说话人和转录文本  
### 请将音频`按说话人分文件夹`放入`custom_character_voice`内。 
## a.whisper通用标注（会自动重采样）：音频在2-10s。根据显存选择配置，large需要12G显存。
```
%PYTHON% short_audio_transcribe.py --languages "CJE" --whisper_size large
```
```
%PYTHON% short_audio_transcribe.py --languages "CJE" --whisper_size medium
```
```
%PYTHON% short_audio_transcribe.py --languages "CJE" --whisper_size small
```
可选参数：`--lab_gen False`禁用生成标注  
默认同时生成`.lab`后缀标注文件，内容为：`<语言>|<转录文本>`  
方便后续直接使用此数据集（使用方法见下）   
 
**下载太慢或者失败，现在可以将whisper模型放在whisper_model下。**

## b.处理下载的已标注的原神数据集（也会自动重采样）：
```
%PYTHON% transcribe_genshin.py
```
处理的lab文件内容是`<转录文本>`  
请按提示输入对应字母来选择语言。
### 如果希望处理whisper已经标注好的数据集  
执行
```
%PYTHON% process_whisper_lab_only.py
```
（不会也无需重采样）
## 2.文本预处理：
```
%PYTHON% preprocess_text.py
```
* 目的是将转录文本处理为注音以供训练。  

* 旧版本生成的cleaned文件请删除重新生成。

# 3.bert_gen & emo_gen
```
%PYTHON% bert_gen.py
```
```
%PYTHON% emo_gen.py
```
* 生成bert文件和emo文件  

**旧版本生成的文件请删除重新生成。**
# 4.训练：
**请先修改训练配置（位于Data/<实验名>/configs.json）**
## 参数解释
`batch_size`: 批大小，一次训练所抓取的数据样本数量。增加此数值在一定范围内有助于提高效果，也可能加快总体训练速度。但也会增加显存开销。
`learning_rate`: 学习率。推荐0.0002在batch_size=16下，可视情况调整，不宜过小或过大。   
`log_interval`: 输出训练情况的间隔。  
`eval_interval`: 评估和保存间隔。
## 首次训练：
你需要先将底模复制进models（模型输出目录）中  
  
然后执行
```
%PYTHON% train_ms.py 
```
## 继续训练
把`config.json`里的`skip_optimizer`改为`false`  
  
  然后执行  
```
%PYTHON% train_ms.py 
```  

# 启动TensorBoard：
```
%PYTHON% -m tensorboard.main --logdir=Data/<实验名>/models
```
看不懂不要管它

# 5.推理：
```
%PYTHON% webui.py -m Data\XXX\models\G_100.pth
```
参数：--c 可选，指定配置文件路径  --m为模型指定路径
