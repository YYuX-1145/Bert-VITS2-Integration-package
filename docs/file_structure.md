## Data文件夹下文件结构如下，每个实验可以有多个说话人：
```
Data
├─Project1(实验名)
│  │  config.json(模型配置)
│  │  config.yml（全局配置）
│  │
│  ├─raw（放音频的文件夹，处理前的音频文件放到这，按说话人分文件夹，支持多说话人）
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
│  ├─wavs(处理完的音频自动放到这)
│  │  └─Speaker1
│  │  │       processed_xxx.wav
│  │  │       processed_yyy.wav
│  │  │       processed_zzz.wav
│  │  │            ......
│  │  │
│  │  └─Speaker2
│  │          processed_xxx.wav
│  │          processed_yyy.wav
│  │          processed_zzz.wav
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

```
## filelists/short_character_anno.list原始标注文件内容展示
```
{路径(相对根目录)}|{说话人}|{语言}|{文本}
```
### 例如：
```
Data\HuTao\wavs/胡桃/vo_card_hutao_invite_easy_02.wav|胡桃|ZH|本堂主略施小计，你就败下阵来了，嘿嘿嘿。
```
如不需要走自动打标流程，请按照如上格式自行准备好相关文件。