bilibili@数列解析几何一生之敌
<div align="center">

# Bert-VITS2整合包
# 注意：本整合包是免费且无条件提供下载的！<br>整合包本体禁止商用，禁止二次分发。<br><br>继续使用代表你同意此条款
## 功能：整合包加入了标注功能。新加的WebUI可以让训练更加轻松。
<div align="left">

## 下载链接和教程
(1.0版教程)【【Bert-Vits2】带标注功能的整合包！轻松训练属于你的“神之嘴”！-哔哩哔哩】 https://b23.tv/Ir2OG5d   
2.0版简介和教程：https://www.bilibili.com/read/cv27647393/  
本仓库的代码是为了给自己部署不成功的，代码报错的人一些参考，或者是用于快速更新整合包。云端训练请自己结合原项目把相关文件和目录补齐。并且我不解答云训练相关问题。
## References|参考
+ [cronrpc/SubFix](https://github.com/cronrpc/SubFix)（界面和功能）
+ [fishaudio/Bert-VITS2](https://github.com/fishaudio/Bert-VITS2)（代码）
+ [Plachtaa/VITS-fast-fine-tuning](https://github.com/Plachtaa/VITS-fast-fine-tuning)（代码）
## 本整合包禁止二次分发和商用<br>
### 请留意:不要相信各类代训服务，不要购买任何模型。当然，如果你是富哥愿意送它们钱，我也没办法，反正损失的也不是我！

## 严禁将此项目用于一切违反《中华人民共和国宪法》，《中华人民共和国刑法》，《中华人民共和国治安管理处罚法》和《中华人民共和国民法典》之用途。由使用本整合包产生的问题和作者、原作者无关！！！

# Bert-VITS2整合包打标组件
# 简介
为本整合包或其他项目配套制作的快速易用的打标工具包。支持whisper、FunASR和原神数据集快速处理。支持进度恢复，意外终止进度不丢失。其中FunASR支持多进程。
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
# 以下为原项目的Readme：     

<div align="center">

<img alt="LOGO" src="https://cdn.jsdelivr.net/gh/fishaudio/fish-diffusion@main/images/logo_512x512.png" width="256" height="256" />

# Bert-VITS2

VITS2 Backbone with multilingual bert

For quick guide, please refer to `webui_preprocess.py`.

简易教程请参见 `webui_preprocess.py`。

## 请注意，本项目核心思路来源于[anyvoiceai/MassTTS](https://github.com/anyvoiceai/MassTTS) 一个非常好的tts项目
## MassTTS的演示demo为[ai版峰哥锐评峰哥本人,并找回了在金三角失落的腰子](https://www.bilibili.com/video/BV1w24y1c7z9)

[//]: # (## 本项目与[PlayVoice/vits_chinese]&#40;https://github.com/PlayVoice/vits_chinese&#41; 没有任何关系)

[//]: # ()
[//]: # (本仓库来源于之前朋友分享了ai峰哥的视频，本人被其中的效果惊艳，在自己尝试MassTTS以后发现fs在音质方面与vits有一定差距，并且training的pipeline比vits更复杂，因此按照其思路将bert)

## 成熟的旅行者/开拓者/舰长/博士/sensei/猎魔人/喵喵露/V应当参阅代码自己学习如何训练。

### 严禁将此项目用于一切违反《中华人民共和国宪法》，《中华人民共和国刑法》，《中华人民共和国治安管理处罚法》和《中华人民共和国民法典》之用途。
### 严禁用于任何政治相关用途。
#### Video:https://www.bilibili.com/video/BV1hp4y1K78E
#### Demo:https://www.bilibili.com/video/BV1TF411k78w
#### QQ Group：815818430
## References
+ [anyvoiceai/MassTTS](https://github.com/anyvoiceai/MassTTS)
+ [jaywalnut310/vits](https://github.com/jaywalnut310/vits)
+ [p0p4k/vits2_pytorch](https://github.com/p0p4k/vits2_pytorch)
+ [svc-develop-team/so-vits-svc](https://github.com/svc-develop-team/so-vits-svc)
+ [PaddlePaddle/PaddleSpeech](https://github.com/PaddlePaddle/PaddleSpeech)
+ [emotional-vits](https://github.com/innnky/emotional-vits)
+ [fish-speech](https://github.com/fishaudio/fish-speech)
+ [Bert-VITS2-UI](https://github.com/jiangyuxiaoxiao/Bert-VITS2-UI)
## 感谢所有贡献者作出的努力
<a href="https://github.com/fishaudio/Bert-VITS2/graphs/contributors" target="_blank">
  <img src="https://contrib.rocks/image?repo=fishaudio/Bert-VITS2"/>
</a>

[//]: # (# 本项目所有代码引用均已写明，bert部分代码思路来源于[AI峰哥]&#40;https://www.bilibili.com/video/BV1w24y1c7z9&#41;，与[vits_chinese]&#40;https://github.com/PlayVoice/vits_chinese&#41;无任何关系。欢迎各位查阅代码。同时，我们也对该开发者的[碰瓷，乃至开盒开发者的行为]&#40;https://www.bilibili.com/read/cv27101514/&#41;表示强烈谴责。)
