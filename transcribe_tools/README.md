# Bert-VITS2整合包打标组件
# 简介
为本整合包或其他项目配套制作的快速易用的打标工具包。支持whisper、FunASR和原神数据集快速处理。其中FunASR支持多进程。
## 安装依赖
```
pip install -r transcribe_tools/requirements.txt
```
确保你的电脑里已安装C++工具包，否则某些依赖可能无法正常安装。
## 快速使用
和Bert-VITS2项目数据结构一致，按说话人分文件夹。音频必须为wav格式。
```
python auto_transcribe.py
```
可指定参数见代码。  
请将auto_transcribe.py放入项目根目录内。  
要使用本工具为GPT-SoVITS制作数据集，请将输出list的语言字母改为小写，用记事本打开按ctrl+f使用查找和替换。  
* 例如：`|ZH|`改为`|zh|`
* 此外，`JP`需要改为`ja`
## 调用参考（见auto_transcribe.py）：
```
    import transcribe_tools

    transcribe_tools.transcribe(
    engine= "whisper", 
    languages= "M",
    whisper_size= "large",
    transcription_path = None,
    in_dir= None,
    out_dir= None,
    sr= 44100,
    processes= 0,
    use_global_cache= True,
    use_path_ffmpeg= True
    ).run_transcribe()
```
`engine`:字符串，指定打标方式。可选：funasr、whisper、genshin（原始人重采样）  
`languages`：字符串。通过包含字母C、J、E的字符串指定语言。例如：CJE、CJ、C。M表示多语言。具体效果和打标方式有关：  
whisper：过滤未选择的语言。  
funasr：会加载选中语言的模型。每个说话人只支持同一种语言。如果没有多语言多说话人的需求请只指定一种语言，否则加载用不到的模型会浪费显存。当指定多语言时，处理时会要求你输入每个说话人的语言。
genshin：同funasr。  
`whisper_size`：字符串。whisper模型大小。large、medium、small。只在选择使用whisper时生效。  
`transcription_path`:字符串。指定输出的list文件路径。  
`in_dir`&`out_dir`：字符串。音频输入/输出路径。请注意：**要按说话人分文件夹**！  
`sr`:整数。设置重采样的采样率  
`processes`:整数。funasr和genshin进程数量，增加这个值在一定范围内提高处理速度。当为0时，funasr默认进程数为1，genshin为逻辑处理器数量-4，且不低于1。whisper不支持多进程。  
`use_global_cache`:默认启用。开启时，whisper和funasr缓存使用系统默认目录。否则会缓存在模块文件夹内。  
`use_path_ffmpeg`:默认启用。开启时，whisper需要的ffmpeg从系统的环境变量读取，否则使用整合包模块目录内的ffmpeg。