import shutil
import gradio as gr
import os
import webbrowser
import subprocess
import datetime
import json
import requests
import soundfile as sf
import numpy as np

import re
def cut_sent(para):
    para = re.sub('([。！;？\?])([^”’])', r"\1\n\2", para)  # 单字符断句符
    para = re.sub('(\.{6})([^”’])', r"\1\n\2", para)  # 英文省略号
    para = re.sub('(\…{2})([^”’])', r"\1\n\2", para)  # 中文省略号
    para = re.sub('([。！？\?][”’])([^，。！？\?])', r'\1\n\2', para)
    para = para.rstrip()  # 段尾如果有多余的\n就去掉它
    # 复制的
    return para.split("\n")

def cut_para(text):
    splitted_para = re.split('[\n]', text)#按段分
    splitted_para = [sentence.strip() for sentence in splitted_para if sentence.strip()]#删除空字符串
    return splitted_para


current_directory = os.path.dirname(os.path.abspath(__file__))
if not os.path.exists(f'{current_directory}/BACKUP'):
    os.mkdir(f'{current_directory}/BACKUP')
    
def refresh_backup_list():
    global list_backup
    list_backup = ['null']
    for item in os.listdir(f'{current_directory}/BACKUP'):
        item_path = os.path.join(f'{current_directory}/BACKUP', item)
        if os.path.isdir(item_path):
           list_backup.append(item)
    return (models.update(choices=list_backup),'已刷新下拉列表')

list_backup = ['null']
for item in os.listdir(f'{current_directory}/BACKUP'):
    item_path = os.path.join(f'{current_directory}/BACKUP', item)
    if os.path.isdir(item_path):
       list_backup.append(item)

def a1a_transcribe(size,lang):
     command = f'venv\python.exe short_audio_transcribe.py --languages {lang} --whisper_size {size}'
     print(command+'\n\n')
     subprocess.Popen(['start', 'cmd', '/k', command],cwd=current_directory,shell=True)
     return '新的命令行窗口已经打开，请关注输出信息。完成后无报错即可关闭进行下一步！'

def a1b_transcribe_genshin():
     command = r"venv\python.exe transcribe_genshin.py"
     print(command+'\n\n')
     subprocess.Popen(['start', 'cmd', '/k', command],cwd=current_directory,shell=True)
     return '新的命令行窗口已经打开，请关注输出信息。完成后无报错即可关闭进行下一步！'

def a2_preprocess_text():
     command = r"venv\python.exe preprocess_text.py"
     print(command+'\n\n')
     subprocess.Popen(['start', 'cmd', '/k', command],cwd=current_directory,shell=True)
     return '新的命令行窗口已经打开，请关注输出信息。完成后无报错即可关闭进行下一步！'

def a3_bert_gen():
     command = r"venv\python.exe bert_gen.py"
     print(command+'\n\n')
     subprocess.Popen(['start', 'cmd', '/k', command],cwd=current_directory,shell=True)
     return '新的命令行窗口已经打开，请关注输出信息。完成后无报错即可关闭进行下一步！'

def a35_json(bs,lr,interval):
    try:        
        config_path=f'{current_directory}/configs/config.json'
        config = json.load(open(config_path))
        config["train"]["batch_size"] = int(bs)
        config["train"]["learning_rate"] = lr
        config["train"]["log_interval"] = int(interval)
        config["train"]['eval_interval'] = int(interval)
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False) 
        return 'success'
    except Exception as error:
        return error 
    
        
def a4a_train():
     command = r"venv\python.exe train_ms.py"
     print(command+'\n\n')
     subprocess.Popen(['start', 'cmd', '/k', command],cwd=current_directory,shell=True)
     return '新的命令行窗口已经打开，请关注输出信息。关闭窗口或Ctrl+C终止训练'

def a4b_train_cont():
     command = r"venv\python.exe train_ms.py --cont"
     print(command+'\n\n')
     subprocess.Popen(['start', 'cmd', '/k', command],cwd=current_directory,shell=True)
     return '新的命令行窗口已经打开，请关注输出信息。关闭窗口或Ctrl+C终止训练'

def start_tb():
     command = r"venv\python.exe -m tensorboard.main --logdir=logs/OUTPUT_MODEL"
     print(command+'\n\n')
     subprocess.Popen(['start', 'cmd', '/k', command],cwd=current_directory,shell=True)
     return '新的命令行窗口已经打开，请关注输出信息。'

def b1_move_in(model_name):
   if model_name=="":
       time = datetime.datetime.now().strftime('%Y_%m_%d-%H_%M_%S')#获取时间     
       path=f'{current_directory}/BACKUP/{time}'
   else:
       path=f'{current_directory}/BACKUP/{model_name}' 
   try:    
     os.mkdir(path)
     os.mkdir(f'{path}/logs')
     os.mkdir(f'{path}/custom_character_voice')
     os.mkdir(f'{path}/genshin_dataset')
     os.mkdir(f'{path}/filelists')
     
     items = os.listdir(f'{current_directory}/logs')
     if items!=[]:
      for item in items:
        source_item_path = os.path.join(f'{current_directory}/logs', item)
        destination_item_path = os.path.join(f'{path}/logs', item)
        shutil.move(source_item_path, destination_item_path)
     #shutil.move(source_folder, destination_folder)
     items = os.listdir(f'{current_directory}/custom_character_voice')
     if items!=[]:
      for item in items:
        source_item_path = os.path.join(f'{current_directory}/custom_character_voice', item)
        destination_item_path = os.path.join(f'{path}/custom_character_voice', item)
        shutil.move(source_item_path, destination_item_path)
     items = os.listdir(f'{current_directory}/genshin_dataset')
     if items!=[]:
      for item in items:
        source_item_path = os.path.join(f'{current_directory}/genshin_dataset', item)
        destination_item_path = os.path.join(f'{path}/genshin_dataset', item)
        shutil.move(source_item_path, destination_item_path)
     items = os.listdir(f'{current_directory}/filelists')
     if items!=[]:
      for item in items:
        source_item_path = os.path.join(f'{current_directory}/filelists', item)
        destination_item_path = os.path.join(f'{path}/filelists', item)
        shutil.move(source_item_path, destination_item_path)
        
     shutil.copy(f'{current_directory}/configs/config.json',f'{path}/config.json')
     return'success'
   except Exception as error:
     return error 
   
def b2_move_out(parent_path):
    if parent_path =='null':
        return "请选择文件夹！"
    parent_path=f'{current_directory}/BACKUP/{parent_path}'
    
    if not os.path.exists(parent_path):
        return "找不到目录"
    try:
       items0= os.listdir(f'{current_directory}/genshin_dataset')
       items1= os.listdir(f'{current_directory}/custom_character_voice')
       if (items0!=[])or(items1!=[]):
          b1_move_in("")
          
       shutil.rmtree(f'{current_directory}/logs')
       shutil.rmtree(f'{current_directory}/custom_character_voice')
       shutil.rmtree(f'{current_directory}/genshin_dataset')
       shutil.rmtree(f'{current_directory}/filelists')
       shutil.copy(f'{parent_path}/config.json',f'{current_directory}/configs/config.json')
       shutil.move(f'{parent_path}/logs',f'{current_directory}')
       shutil.move(f'{parent_path}/custom_character_voice',f'{current_directory}')
       shutil.move(f'{parent_path}/genshin_dataset',f'{current_directory}')
       shutil.move(f'{parent_path}/filelists',f'{current_directory}')
       shutil.rmtree(parent_path)
       return "SUCCESS"
    except Exception as error:
       return error 


ckpt_list = ['null']
try:
   file_list = os.listdir(f'{current_directory}/logs/OUTPUT_MODEL')
   for ck in file_list:
      if os.path.splitext(ck)[-1] == ".pth"and ck[:2] != "D_" and ck[:4] !="DUR_":
         ckpt_list.append(ck)
except Exception as error:
    print("Attention. An error occurred in reading {./logs/OUTPUT_MODEL}.Check if the directory exists.")
    print(error)

def refresh_models_in_logs():
   try:
      file_list = os.listdir(f'{current_directory}/logs/OUTPUT_MODEL')
      global ckpt_list
      ckpt_list = ['null']
      for ck in file_list:
         if os.path.splitext(ck)[-1] == ".pth"and ck[:2] == "G_":
            ckpt_list.append(ck)
      return (models_logs.update(choices=ckpt_list),"已刷新下拉列表")
   except Exception as error:
      return(models_logs.update(choices=['null']),f"读取失败 {error}")

speakers_list=[]

def get_speaker_list(config_path):
    global speakers_list
    try:
        config = json.load(open(config_path))
        speaker_ids = config["data"]["spk2id"]
        speakers_list = list(speaker_ids.keys())
    except Exception as e:
        print(e)
        speakers_list=[]

def c1_infer(file_name):
    if file_name=='null':
        return "请选择模型！"    
    command = f'venv\python.exe webui.py -c ./logs/OUTPUT_MODEL/config.json -m ./logs/OUTPUT_MODEL/{file_name}'
    print(command+'\n\n')
    subprocess.Popen(['start', 'cmd', '/k', command],cwd=current_directory,shell=True)
    get_speaker_list(f'{current_directory}/logs/OUTPUT_MODEL/config.json')
    return (speaker.update(choices=speakers_list),'新的命令行窗口已经打开，请关注输出信息。关闭窗口结束推理服务。')

def c2_refresh_models_backup():
    refresh_backup_list()
    return (backup_name.update(choices=list_backup),'已刷新下拉列表')

backup_ckpt_list=['null']

def c2_refresh_sub_opt(parent_path):  
   try:
       global backup_ckpt_list
       backup_ckpt_list=['null']
       file_list = os.listdir(f'{current_directory}/BACKUP/{parent_path}/logs/OUTPUT_MODEL')
       for ck in file_list:
         if os.path.splitext(ck)[-1] == ".pth"and ck[:2] != "D_" and ck[:4] !="DUR_":
            backup_ckpt_list.append(ck)
       return models_in_backup.update(choices=backup_ckpt_list)
   except :
       return models_in_backup.update(choices=['null'])

def c2_infer(bkup_name,model_name):
    if bkup_name=='null' or model_name=='null':
        return '请选择模型！'
   
    path=f'./BACKUP/{bkup_name}/logs/OUTPUT_MODEL'
    command = f'venv\python.exe webui.py -c {path}/config.json -m {path}/{model_name}'
    print(command+'\n\n')
    subprocess.Popen(['start', 'cmd', '/k', command],cwd=current_directory,shell=True)
    get_speaker_list(f'{current_directory}/BACKUP/{bkup_name}/logs/OUTPUT_MODEL/config.json')
    return (speaker.update(choices=speakers_list),'新的命令行窗口已经打开，请关注输出信息。关闭窗口结束推理服务。')

def inference_api(text,spk,sdp,ns,nsw,ls,lang,url):
        try:
            # API地址
            API_URL = 'http://127.0.0.1:7860/run/predict/'#
            if url!=''and url!='default':
                API_URL = f'{url}/run/predict/'
            data_json = {
                "fn_index":0,
                "data":[
                    '"' + text + '"',#text
                   spk,#spk                 
                   sdp,	# int | float (numeric value between 0 and 1) in 'SDP Ratio' Slider component
				   ns,	# int | float (numeric value between 0.1 and 2) in 'Noise Scale' Slider component
				   nsw,	# int | float (numeric value between 0.1 and 2) in 'Noise Scale W' Slider component
				   ls,	# int | float (numeric value between 0.1 and 2) in 'Length Scale' Slider component
                   lang #language
                ],
            }
            response = requests.post(url=API_URL, json=data_json)
            response.raise_for_status() 
            result = response.content
            ret = json.loads(result)
            path = ret['data'][1]['name']
            return path
        except :
            return 'error'

def d1_long_text_infer(text,speaker,sdp_ratio,noise_scale,noise_scale_w,length_scale,language,interval_between_sent,interval_between_para,cut_by_sent,url):
    if speaker=='null':
        return ('请选择说话人！',None)
    while(text.find("\n\n")!=-1):
        text=text.replace("\n\n","\n")
    #print(text,speaker,sdp_ratio,noise_scale,noise_scale_w,length_scale,language,interval_between_sent,interval_between_para,cut_by_sent,url)
    para_list=cut_para(text)
    audio_list = []
    #print(para_list)
    if not cut_by_sent:
        for p in para_list:
            path=inference_api(p,speaker,sdp_ratio,noise_scale,noise_scale_w,length_scale,language,url)
            au,sr = sf.read(path)
            audio_list.append(au)
            silence = np.zeros((int)(44100*interval_between_para)) 
            audio_list.append(silence) 
    else:
        for p in para_list:
            sent_list=cut_sent(p)
            for s in sent_list:
               path=inference_api(s,speaker,sdp_ratio,noise_scale,noise_scale_w,length_scale,language,url)
               au,sr = sf.read(path)
               audio_list.append(au)
               silence = np.zeros((int)(44100*interval_between_sent)) 
               audio_list.append(silence)
            if (interval_between_para-interval_between_sent)>0:
               silence = np.zeros((int)(44100*(interval_between_para-interval_between_sent))) 
               audio_list.append(silence)
    audio_concat = np.concatenate(audio_list)
    return ("Success", (44100, audio_concat))

def d2_file_infer(file,speaker,sdp_ratio,noise_scale,noise_scale_w,length_scale,language,interval_between_sent,interval_between_para,cut_by_sent,url):
    try:
      with open(file.name, "r", encoding="utf-8") as file:
         text = file.read()
         return d1_long_text_infer(text,speaker,sdp_ratio,noise_scale,noise_scale_w,length_scale,language,interval_between_sent,interval_between_para,cut_by_sent,url)
    except Exception as error:
        return (error,None)
if __name__ == "__main__":
    with gr.Blocks(title="Bert-VITS-2-Manager-WebUI") as app:
        gr.Markdown(value="""
        Bert-VITS2训练管理器
                    
        严禁将此项目用于一切违反《中华人民共和国宪法》，《中华人民共和国刑法》，《中华人民共和国治安管理处罚法》和《中华人民共和国民法典》之用途。由使用本整合包产生的问题和作者、原作者无关！！！
        
        作者：bilibili@数列解析几何一生之敌
        
        适用于整合包版本V1.1.1
                    
        WebUI更新日期：2023.10.12  
        """)
        with gr.Tabs():
           with gr.TabItem("训练"):
               with gr.Row():              
                    with gr.Column():
                       a1a_btn = gr.Button(value="1.a.数据集重采样和标注(使用whisper)", variant="primary")
               whisper_size = gr.Radio(label="选择whisper大小，large需要12G显存", choices=['large','medium','small'], value="medium")
               language = gr.Radio(label="选择语言(其他语言会跳过)", choices=['C','CJ'], value="CJ")
               with gr.Column():
                       a1b_btn = gr.Button(value="1.b.处理下载的已标注的原神数据集", variant="primary")
               with gr.Column():
                       a1_textbox_output_text = gr.Textbox(label="输出信息", placeholder="点击处理按钮，二选一",interactive=False)
               gr.Markdown(value='\n')        
               with gr.Row():              
                    with gr.Column():
                       a2_btn = gr.Button(value="2.文本预处理", variant="primary")
               with gr.Column():
                       a2_textbox_output_text = gr.Textbox(label="输出信息", placeholder="点击处理按钮",interactive=False)
               gr.Markdown(value='\n')         
               with gr.Row():              
                    with gr.Column():
                       a3_btn = gr.Button(value="3.生成bert文件", variant="primary")
               with gr.Column():
                       a3_textbox_output_text = gr.Textbox(label="输出信息", placeholder="点击处理按钮",interactive=False)
               gr.Markdown(value='\n')
               with gr.Row():
                    with gr.Row():
                        a35_textbox_bs = gr.Number(label="批大小", value="8",interactive=True)
                        a35_textbox_lr = gr.Number(label="学习率", value="0.0001",interactive=True)
                        a35_textbox_save = gr.Number(label="保存间隔", value="100",interactive=True)
               with gr.Column():
                   a35_btn = gr.Button(value="写入配置文件", variant="primary")
                   a35_textbox_output_text = gr.Textbox(label="输出信息", placeholder="点击处理按钮",interactive=False)
               gr.Markdown(value='\n')    
               with gr.Row():              
                    with gr.Column():
                       a4a_btn = gr.Button(value="4a.首次训练", variant="primary")
                    with gr.Column():
                       a4b_btn = gr.Button(value="4b.继续训练", variant="primary")                       
               with gr.Column():
                       a4_textbox_output_text = gr.Textbox(label="输出信息", placeholder="点击处理按钮",interactive=False)
               gr.Markdown(value='\n')         
               with gr.Row():              
                    with gr.Column():
                       tb_btn = gr.Button(value="启动TensorBoard", variant="primary")            
                       tb_textbox_output_text = gr.Textbox(label="输出信息", placeholder="点击处理按钮",interactive=False)
           #            
           with gr.TabItem("模型管理"):
               with gr.Row():              
                    with gr.Column():
                       textbox_backup_name = gr.Textbox(
                       label="这将移走所有训练文件，以供启动新的训练，请输入实验名称,最好不要包含中文、特殊字符和保留字符，不输入则以时间命名。",
                       placeholder="请输入实验名称,最好不要包含中文、特殊字符和保留字符。",
                       value="",
                       lines=1,
                       interactive=True)
                       b1_btn = gr.Button(value="备份当前训练", variant="primary")
               with gr.Column():
                       b1_textbox_output_text = gr.Textbox(label="输出信息", placeholder="点击处理按钮",interactive=False) 
               gr.Markdown(value='\n')
               with gr.Row(): 
                   with gr.Column():
                       models = gr.Dropdown(label="选择备份的训练(如果当前存在数据集，将自动备份并按时间命名)", choices=list_backup, value='null'if not list_backup else list_backup[0],interactive=True)
                       b2_btn_load = gr.Button(value="加载选中的训练", variant="primary") 
                       b2_btn_refresh= gr.Button(value="刷新选项", variant="secondary") 
                   with gr.Column():
                       b2_textbox_output_text = gr.Textbox(label="输出信息", placeholder="点击处理按钮",interactive=False)  

            #                       
           with gr.TabItem("启动推理"):
                gr.Markdown(value='工作区模型推理(logs文件夹)') 
                with gr.Row(): 
                    models_logs = gr.Dropdown(label="选择logs文件夹内的模型", choices=ckpt_list, value='null'if not ckpt_list else ckpt_list[-1],interactive=True)              
                    with gr.Column():
                       c1_btn = gr.Button(value="工作区推理", variant="primary")
                       c1_btn_refresh=gr.Button(value="刷新选项", variant="secondary")
                with gr.Column():
                       c1_textbox_output_text = gr.Textbox(label="输出信息", placeholder="点击处理按钮",interactive=False) 
                       
                gr.Markdown(value='\n备份区模型推理(BACKUP文件夹)') 
                with gr.Row():
                    backup_name = gr.Dropdown(label="选择备份的训练(实验名)", choices=list_backup, value='null',interactive=True)
                    models_in_backup = gr.Dropdown(label="选择模型", choices=backup_ckpt_list, value='null'if not backup_ckpt_list else backup_ckpt_list[0],interactive=True)
                    with gr.Column():
                       c2_btn = gr.Button(value="备份区推理", variant="primary")
                       c2_btn_refresh=gr.Button(value="刷新选项", variant="secondary")
                with gr.Column():
                       c2_textbox_output_text = gr.Textbox(label="输出信息", placeholder="点击处理按钮",interactive=False) 
                backup_name.change(c2_refresh_sub_opt,[backup_name],[models_in_backup])  
                '''
                gr.Markdown(value='\n自行填写绝对路径') 
                with gr.Row():
                    c3_input1 = gr.Textbox(placeholder="填写模型路径",interactive=True)
                    c3_input2 = gr.Textbox(placeholder="填写配置文件路径，不填默认和模型同路径",interactive=True)
                with gr.Column():
                    c3_btn = gr.Button(value="推理", variant="primary")
                '''    
           with gr.TabItem("辅助功能"):
               gr.Markdown(value='API长句合成(请先启动推理WebUI后使用)') 
               with gr.Row():
                   d1_textbox_intput_text = gr.TextArea(label="输入长文本", value="生活就像海洋.只有意志坚强的人。\n才能到达彼岸。",interactive=True) 
               with gr.Row():            
                   with gr.Column():
                       gr.Markdown(value='参数')
                       speaker = gr.Dropdown(choices=speakers_list,value='null'if not speakers_list else speakers_list[0], label="Speaker")
                       sdp_ratio = gr.Slider(minimum=0, maximum=1, value=0.2, step=0.1, label="SDP Ratio")
                       noise_scale = gr.Slider(minimum=0.1, maximum=2, value=0.6, step=0.1, label="Noise Scale")
                       noise_scale_w = gr.Slider(minimum=0.1, maximum=2, value=0.8, step=0.1, label="Noise Scale W")
                       length_scale = gr.Slider(minimum=0.1, maximum=2, value=1, step=0.1, label="Length Scale")
                       language = gr.Dropdown(choices=['ZH','JP'], value='ZH', label="Language")
                   with gr.Column():   
                       gr.Markdown(value='选项')
                       interval_between_sent= gr.Slider(minimum=0, maximum=5, value=0.2, step=0.1, label="句间停顿(秒)，勾选按句切分才生效")
                       interval_between_para= gr.Slider(minimum=0, maximum=10, value=1, step=0.1, label="段间停顿(秒)，需要大于句间停顿才有效")
                       opt_cut_by_sent = gr.Checkbox(label = "按句切分    在按段落切分的基础上再按句子切分文本")
                       url_wui=gr.Textbox(label="WebUI地址 #正常情况下不用填", placeholder="default",lines=2,interactive=True)
                       input_file = gr.Files(label="上传txt纯文本文件",file_types=['text'],file_count='single')
                   with gr.Column():
                       d1_btn = gr.Button("从文本框生成", variant="primary")
                       d2_btn = gr.Button("从文件生成", variant="primary")
                       d1_textbox_output_text=gr.Textbox(label="输出信息", placeholder="点击处理按钮",interactive=False)
                       d1_audio_output = gr.Audio(label="Output Audio")
        a1a_btn.click(
            a1a_transcribe,
            inputs=[whisper_size,language],
            outputs=[
                a1_textbox_output_text,
            ],
        )
 
        a1b_btn.click(
            a1b_transcribe_genshin,
            outputs=[
                a1_textbox_output_text,
            ],
        )
        
        a2_btn.click(
            a2_preprocess_text,
            outputs=[
                a2_textbox_output_text,
            ],
        )
        
        a3_btn.click(
            a3_bert_gen,
            outputs=[
                a3_textbox_output_text,
            ],
        )
        a35_btn.click(
            a35_json,
            inputs=[a35_textbox_bs,a35_textbox_lr,a35_textbox_save],
            outputs=[
                a35_textbox_output_text,
            ],
        )
        a4a_btn.click(
            a4a_train,
            outputs=[
                a4_textbox_output_text,
            ],
        )
        a4b_btn.click(
            a4b_train_cont,
            outputs=[
                a4_textbox_output_text,
            ],
        ) 
        tb_btn.click(
            start_tb,
            outputs=[
                tb_textbox_output_text,
            ],
        )
        b1_btn.click(
            b1_move_in,
            inputs=[textbox_backup_name],
            outputs=[
                b1_textbox_output_text,
            ],
        )            
        b2_btn_load.click(
            b2_move_out,
            inputs=[models],
            outputs=[
                b2_textbox_output_text,
            ],
        )        
        b2_btn_refresh.click(refresh_backup_list,[],[models,b2_textbox_output_text])
        
        c1_btn.click(
            c1_infer,
            inputs=[models_logs],
            outputs=[speaker,
                c1_textbox_output_text
            ],
        )
        c1_btn_refresh.click(refresh_models_in_logs,[],[models_logs,c1_textbox_output_text])
        c2_btn.click(
            c2_infer,
            inputs=[backup_name,models_in_backup],
            outputs=[speaker,
                c2_textbox_output_text,
            ],
        )          
        c2_btn_refresh.click(c2_refresh_models_backup,[],[backup_name,c2_textbox_output_text])
        d1_btn.click(
            d1_long_text_infer,
            inputs=[
                d1_textbox_intput_text,#text
                speaker,
                sdp_ratio,
                noise_scale,
                noise_scale_w,
                length_scale,
                language,
                interval_between_sent,
                interval_between_para,
                opt_cut_by_sent,
                url_wui
            ],
            outputs=[d1_textbox_output_text, d1_audio_output],
        )
        d2_btn.click(
            d2_file_infer,
            inputs=[
                input_file,#text
                speaker,
                sdp_ratio,
                noise_scale,
                noise_scale_w,
                length_scale,
                language,
                interval_between_sent,
                interval_between_para,
                opt_cut_by_sent,
                url_wui
            ],
            outputs=[d1_textbox_output_text, d1_audio_output],
        )
webbrowser.open("http://127.0.0.1:6660")
app.launch(server_port=6660)
