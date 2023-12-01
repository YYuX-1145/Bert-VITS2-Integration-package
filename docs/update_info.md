# 整合包更新内容(V2.1)
## Bert-VITS2更新可参阅：
+ [fishaudio/Bert-VITS2](https://github.com/fishaudio/Bert-VITS2/releases)
* 代码版本：11.30日master分支代码
# WebUI管理器和整合包更新
* 1.增加对whisper-large-V3支持，打标准确的有些许提升
* 2.whisper打标默认会同时生成.lab标注文本文件，下一次处理数据集就更简单了。
* 3.提前一个版本加入情绪快速分类功能（见辅助功能），支持编辑和预览分类配置文件，推理时可以快速调用参考音频。
* 4.支持启动HiyoriUI推理（截止制作时，对应版本还未发布，有需要可以自己去下载，并自己更新server_fastapi.py）
* 5.管理器支持启动参数`-p`指定端口，默认6660。
* 6.比原来更好的界面（？）
## 还未更新的内容
* 1.模型混合和onnx导出
* 2.以上内容比较冷门，暂不打算在webui中加入此功能。你可以参阅对应代码执行操作。  
注意：由于emo-vq效果不佳，因此2.1算作一个过渡版本。  
问题或建议反馈：（https://githb.com/YYuX-1145/Bert-VITS2-Integration-package/issues）
# 推荐的工具/软件
## Hiyori UI for BertVits2
[jiangyuxiaoxiao/Bert-VITS2-UI](https://github.com/jiangyuxiaoxiao/Bert-VITS2-UI)  
* 官方的全新推理UI,支持动态加载、卸载模型，更换模型无需重启。
* 在2.0.2版本旧整合包中已经集成了Hiyori UI，但截止本整合包发布时，还没有推出适配的版本。有需要可以自己去下载，并自己更新server_fastapi.py。
## SubFix  
[cronrpc/SubFix](https://github.com/cronrpc/SubFix)  
[B站链接]https://www.bilibili.com/video/BV1My4y1P7WX/

SubFix是一个数据集辅助制作工具，一个用于轻松地编辑修改音频字幕的网页工具。能够实时地看到改动，方便地对音频进行合并、分割、删除、编辑字幕，同时能够马上知道改动后的效果。
## Audio-Slicer(slicer-gui)

音频切分工具，建议在whisper打标前使用。音频过长或长度变化大会导致显存开过山车影响训练效率。

## UVR5
分离背景音乐/噪声和人声的AI软件。不多赘述。