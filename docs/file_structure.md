### Data文件夹下文件结构如下，每个实验可以有多个说话人：
```
Data
├─Project1(实验名)
│  │  config.json(模型配置)
│  │  config.yml（全局配置）
│  │
│  ├─custom_character_voice（放音频的文件夹，按说话人分文件夹，支持多说话人）
│  │  └─Speaker1（说话人名称）
│  │  │       xxx.wav
│  │  │       yyy.wav
│  │  │       zzz.wav
│  │  │            ......
│  │  │
│  │  └─Speaker2
│  │          xxx.wav
│  │          yyy.wav
│  │          zzz.wav
│  │                 ......
│  │
│  ├─filelists(放标注的，一开始为空)
│  │      cleaned.list
│  │      short_character_anno.list
│  │      train.list
│  │      val.list
│  │
│  └─models（模型保存到这，一开始为空）
│      │  DUR_0.pth
│      │  DUR_100.pth
│      │  D_0.pth
│      │  D_100.pth
│      │  G_0.pth
│      │  G_100.pth
│      │  train.log
│      └─eval
│              events.out.xxxx
│
......
└─Project n
    │  config.json
    │  config.yml
    │
    ├─custom_character_voice
    │  └─Speaker1
    │          AAA.wav
    │          BBB.wav
    │          CCC.wav
    │
    ├─filelists
    │      cleaned.list
    │      short_character_anno.list
    │      train.list
    │      val.list
    │
    └─models
        │  DUR_0.pth
        │  DUR_100.pth
        │  DUR_200.pth
            ......
```