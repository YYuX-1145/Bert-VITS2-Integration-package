# Bert-VITS2整合包

VITS2 Backbone with bert
## 整合包已经完成制作，修改好的代码已经发布了。代码发布于此处。我结合VITS-Fast-Fine-Tuning修正了原项目的代码使其能在Windows上正常运行，并加入了标注功能，但仍有未解决的问题。

## 下载链接和教程
【【Bert-Vits2】带标注功能的整合包！轻松训练属于你的“神之嘴”！-哔哩哔哩】 https://b23.tv/Ir2OG5d   
本仓库的代码是为了给自己部署不成功的，代码报错的人一些参考，或者是用于快速更新整合包。云端训练请自己结合原项目把相关文件和目录补齐。

## 严禁将此项目用于一切违反《中华人民共和国宪法》，《中华人民共和国刑法》，《中华人民共和国治安管理处罚法》和《中华人民共和国民法典》之用途。由使用本整合包产生的问题和作者、原作者无关！！！

## 说一下整合包内大家遇到的2个问题
1.自动标注提示没有短音频：如果确定数据集存放位置正确，安装ffmpeg即可，已经有人自己解决了这个问题。我自己2遍调试下来ffmpeg的安装在我自己的电脑上是没有问题的（从环境变量里删除就会报错！安装后恢复正常！） 但是要注意安装完可能要重启电脑，另外要检查环境变量里的ffmpeg是不是从其他来源安装了，版本不对有可能产生错误。如果按照说明安装后仍未解决问题，尝试手动安装（教程自己搜）--补充：现在又来了个路径有中文导致该错误的例子（？） 以及，手动安装可以尝试把它加入系统的Path   
2.ZeroDivisionError: integer division or modulo by zero 零除错误：关键代码和9.3原项目同步更新，新整合包已经解决了此问题。  
3.whisper下载问题：把whisper_model文件夹下的文件复制到 C:\Users\\<电脑的用户名>\\.cache\whisper 里面即可  
4.如果不使用自带的标注，自行重采样数据集至44100Hz单声道。  

## V1.1.1更新
前往另一个分支。

# 以下为原项目的Readme

## 请注意，本项目核心思路来源于[anyvoiceai/MassTTS](https://github.com/anyvoiceai/MassTTS) 一个非常好的tts项目
## MassTTS的演示demo为[ai版峰哥锐评峰哥本人,并找回了在金三角失落的腰子](https://www.bilibili.com/video/BV1w24y1c7z9)
## 本项目与[PlayVoice/vits_chinese](https://github.com/PlayVoice/vits_chinese) 没有任何关系

本仓库来源于之前朋友分享了ai峰哥的视频，本人被其中的效果惊艳，在自己尝试MassTTS以后发现fs在音质方面与vits有一定差距，并且training的pipeline比vits更复杂，因此按照其思路将bert
与vits结合起来以获得更好的韵律。本身我们是出于兴趣玩开源项目，用爱发电，我们本无意与任何人起冲突，然而[MaxMax2016](https://github.com/MaxMax2016)
以及其organization[PlayVoice](https://github.com/PlayVoice)几次三番前来碰瓷，说本项目抄袭了他们的代码，甚至上法院云云，因此在Readme中特别声明，本项目与
[PlayVoice/vits_chinese](https://github.com/PlayVoice/vits_chinese)没有任何关系，结合bert的思路方面也是完全来源于MassTTS



附：对面认为本项目抄袭了他代码的证据，诸位可以自行查看并做出判断，[bert_vits2引用的MassTTS的实际代码](https://github.com/PlayVoice/vits_chinese/tree/4781241520c6b9fdcf090fca289148719272e89f#bert_vits2%E5%BC%95%E7%94%A8%E7%9A%84masstts%E7%9A%84%E5%AE%9E%E9%99%85%E4%BB%A3%E7%A0%81)

## 成熟的旅行者/开拓者/舰长/博士/sensei/猎魔人/喵喵露/V应当参阅代码自己学习如何训练。
### 严禁将此项目用于一切违反《中华人民共和国宪法》，《中华人民共和国刑法》，《中华人民共和国治安管理处罚法》和《中华人民共和国民法典》之用途。
### 严禁用于任何政治相关用途。
#### Video:https://www.bilibili.com/video/BV1hp4y1K78E
#### Demo:https://www.bilibili.com/video/BV1TF411k78w
## References
+ [anyvoiceai/MassTTS](https://github.com/anyvoiceai/MassTTS)
+ [jaywalnut310/vits](https://github.com/jaywalnut310/vits)
+ [p0p4k/vits2_pytorch](https://github.com/p0p4k/vits2_pytorch)
+ [svc-develop-team/so-vits-svc](https://github.com/svc-develop-team/so-vits-svc)
+ [PaddlePaddle/PaddleSpeech](https://github.com/PaddlePaddle/PaddleSpeech)
+ [emotional-vits](https://github.com/innnky/emotional-vits)
## 感谢所有贡献者作出的努力
<a href="https://github.com/fishaudio/Bert-VITS2/graphs/contributors" target="_blank">
  <img src="https://contrib.rocks/image?repo=fishaudio/Bert-VITS2"/>
</a>

# 本项目所有代码引用均已写明，bert部分代码思路来源于[AI峰哥](https://www.bilibili.com/video/BV1w24y1c7z9)，与[vits_chinese](https://github.com/PlayVoice/vits_chinese)无任何关系。欢迎各位查阅代码。同时，我们也对该开发者的[碰瓷，乃至开盒开发者的行为](https://www.bilibili.com/read/cv27101514/)表示强烈谴责。
