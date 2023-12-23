# 整合包版本V2.3 
bilibili@数列解析几何一生之敌
# 训练和命令行使用说明
## 注意：管理器里的每个按钮都对应了命令或训练相关操作。你需要自己学习训练流程。<br>（如果使用webui，则不需要手动复制任何文件。）
## 关于命令行
启动命令行时 `%PYTHON%`
指代了包内的python环境，即`venv\python.exe`，使用时代替`python` 。  
如果要使用自己的环境，~~需要更改管理器代码。修改是极其简单的。~~ 启动管理器附加参数`-d` 指定python路径。
## 环境维护和升级（示例）：

 ```
 %PYTHON% -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
 ```
 一般情况下无需执行此命令。  
 看不懂的也不要执行这条命令。

## ~~0.安装ffmpeg：~~
```
%PYTHON% setup_ffmpeg.py
```
~~执行一次即可。安装是把当前文件夹下ffmpeg加入环境变量，因此执行完不要移动或删除。否则需要手动更改环境变量。安装完可能需要重启才能生效。部分设备可能要手动加入系统的path,请自行寻找教程。~~ 现在路径已经写死，正常情况下无需执行此命令

## 注意：首先需要创建或更改全局设置。作用见default_config.yml。将config.yml放在根目录下即可生效。并需要创建对应存放数据的文件夹。
* ### 对应的管理器操作：第一栏创建文件夹，放入你的数据集（要求见“数据集重采样和标注”），再修改全局训练设置并保存(可选)，然后点击加载(必需)。
## 参数解释
* `num_workers` : 简单地说是训练集加载线程数。这个值越高，内存开销越大，内存16G的情况下不建议设置太大。如果过低则会影响训练速度。

# 关于数据集制备、预处理流程和开始训练
## 管理器训练菜单内每一个按钮都对应了如下步骤

# 1.数据集重采样和标注：
* 训练需要没有噪声和背景音乐且说话清晰的单语言音频。
* 如果已有list文件，自行按训练流程处理对应文件，并将音频自行重采样至*44100Hz单声道*。请注意：某些软件导出的音频可能导致训练错误。
* 这一步会重采样音频并生成符合格式的.list数据集标注文件，包含路径，语言，说话人和转录文本。  
## 请将音频 `按说话人` 分文件夹放入 `raw` 内。 

## a.whisper通用标注（会自动重采样）：音频建议在2-10s之间。根据显存和实际需求选择配置，large效果最好但显存开销大，推荐10-12G显存。
```
%PYTHON% short_audio_transcribe.py --languages "CJE" --whisper_size large
```
```
%PYTHON% short_audio_transcribe.py --languages "CJE" --whisper_size medium
```
```
%PYTHON% short_audio_transcribe.py --languages "CJE" --whisper_size small
```
会同时生成`.lab`后缀含语言和文本的小标注文件，方便进度恢复，内容为：`<语言>|<转录文本>`     
* 原始数据音频不要以`processed_`开头  
* whisper模型下载太慢或者失败，现在可以将whisper模型放在whisper_model下。

## b.处理下载的已标注的原神数据集（也会自动重采样）：
```
%PYTHON% transcribe_genshin.py
```
* 适合处理红血球佬的原神数据集，会重采样并依据.lab标注生成list
* 处理的lab文件内容是`<转录文本>`  
* 请按提示输入对应字母来选择语言。

## 2.文本预处理：
```
%PYTHON% preprocess_text.py
```
* 在开始之前，建议打开list更正标注，推荐的工具：Subfix ，转到辅助功能页面启动。
* 目的是将转录文本处理为注音以供训练，并划分训练集和验证集。  
* 旧版本生成的cleaned文件请删除重新生成。

# 3.生成bert特征文件
```
%PYTHON% bert_gen.py
```

**旧版本生成的文件请删除重新生成。**

# 4.训练：
## 请先修改训练配置（位于Data/<实验名>/configs.json）
## 参数解释
`batch_size`: 批大小，一次训练所抓取的数据样本数量。增加此数值在一定范围内有助于提高效果，也可能加快总体训练速度。但也会增加显存开销。  
`learning_rate`: 学习率。可视情况调整，不宜过小或过大。   
`log_interval`: 输出训练情况的间隔。  
`eval_interval`: 评估和保存间隔。  
`bf16_run`: 一定程度上降低资源开销，但对模型性能影响未知。
## 首次训练：
你需要先将底模复制进模型输出目录中  
  
然后执行
```
%PYTHON% train_ms.py 
```
## 继续训练：
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
* 可选择HiyoriUI或者Gradio WebUI
* 修改全局配置，然后执行命令
```
%PYTHON% server_fastapi.py  ::HiyoriUI
```
```
%PYTHON% webui.py  ::GradioUI
```
参数：--y 可选，指定全局配置文件路径
