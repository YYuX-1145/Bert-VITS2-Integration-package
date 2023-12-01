import shutil
import gradio as gr
import os
import webbrowser
import subprocess
import json
import yaml
import argparse

#########################################################
py_dir=r"venv\python.exe" # SET PYTHON PATH HERE!
#########################################################


current_directory = os.path.dirname(os.path.abspath(__file__))
if not os.path.exists('./Data'):
    os.mkdir('./Data')
 
################### Load md
try:
   with open('docs/file_structure.md', mode="r", encoding="utf-8") as f:
       file_structure_md=f.read()
except Exception as e:
    file_structure_md='读取错误'+ str(e)
try:
   with open('docs/README.md', mode="r", encoding="utf-8") as f:
       readme_md=f.read()
except Exception as e:
    readme_md='读取错误'+ str(e)    
try:
   with open('docs/command_usage.md', mode="r", encoding="utf-8") as f:
       cmd_md=f.read()
except Exception as e:
    cmd_md='读取错误'+ str(e)       
try:
   with open('docs/update_info.md', mode="r", encoding="utf-8") as f:
       update_info=f.read()
except Exception as e:
    update_info='读取错误'+ str(e)       
try:
   with open('docs/errors.md', mode="r", encoding="utf-8") as f:
       errors=f.read()
except Exception as e:
    errors='读取错误'+ str(e)    
###################

current_page=1
class_info={}
emo_speaker_list=[]
emo_class_list=[]
emo_file_name_list=[]
emo_audio_list=[]
emo_tr_list=[]
emo_checkbox_list=[]
emo_current_proj_name=None
def load_emo_clu(proj_name):
    if proj_name=="" or proj_name=='null':
        return "请选择！",emo_speaker.update(choices=[],value=None)
    global emo_current_proj_name
    global class_info
    global emo_speaker_list
    emo_current_proj_name=proj_name
    
    try:
        class_info = yaml.load(open(os.path.join('Data',proj_name,'emo_clustering.yml')),Loader=yaml.FullLoader)
        emo_speaker_list=list(class_info.keys())
        return emo_status_text.update(value=f"当前的实验：{proj_name}"),emo_speaker.update(choices=emo_speaker_list,value=emo_speaker_list[0])#,*emo_change_speaker(emo_speaker_list[0])#,*load_page(emo_speaker_list[0],list(class_info[emo_speaker_list[0]].keys())[0])
    except Exception as e:
        class_info={}
        emo_speaker_list=[]
        return emo_status_text.update(value='加载错误'+str(e)),emo_speaker.update(choices=[],value=None)

def get_transcription(proj_name,spk,wav):#transciption and wav path
    y=yaml.load(open(os.path.join('Data',proj_name,'config.yml')),Loader=yaml.FullLoader)
    wav_path=os.path.normpath(os.path.join(y["dataset_path"],y["resample"]["out_dir"],spk,wav))
    list_path=os.path.join(y["dataset_path"],y["preprocess_text"]["cleaned_path"])
    with open(list_path, mode="r", encoding="utf-8", errors='ignore') as f:
        for lines in f:
            if os.path.normpath(lines.split("|")[0])==wav_path:
                return lines.split("|")[3],wav_path
        return "加载失败",""


def emo_change_speaker(speaker): 
    if speaker is None:
        return emo_chosen_class.update(choices=[],value=None)
    global current_page
    current_page=1
    lst=list(class_info[speaker].keys())
    return emo_chosen_class.update(choices=lst,value=lst[0]),*switch_page(speaker,lst[0])

def emo_change_class(speaker,class_):
    if (speaker is None) or (class_ is None):
        return emo_ret_none()
    global current_page
    current_page=1
    return switch_page(speaker,class_)

def emo_ret_none():
    global current_page
    wavname_list=[]
    transcription_list=[]
    audio_list=[]
    checkbox_list=[]
    for i in range(10):
        wavname_list.append(gr.Textbox().update(value=None,label='None',visible=False))
        audio_list.append(gr.Audio.update(label="情感参考音频",value=None,interactive=False,visible=False))
        transcription_list.append(gr.Textbox().update(value=None,visible=False))
        checkbox_list.append(gr.Checkbox().update(value=False,visible=False))
    wavname_list[0]=gr.Textbox().update(value='看起来列表似乎是空的',label='None',visible=True)
    list_all=wavname_list+transcription_list+audio_list+checkbox_list
    return *list_all,previous_btn.update(interactive=False),emo_page_index.update(value=current_page),next_btn.update(interactive=False)

def load_page(page_start,page_end,spk,class_name):#load lines of content
    global emo_current_proj_name
    wavname_list=[]
    transcription_list=[]
    audio_list=[]
    checkbox_list=[]
    #page_start,page_end,_,_=calculate_page(spk,class_name)
    for i in range(page_start, page_end+1):
        wav_name=class_info[spk][class_name][i]
        tr,wavpath=get_transcription(emo_current_proj_name,spk,wav_name)
        if wavpath=="":
           audio_list.append(gr.Audio.update(label="情感参考音频",value=None,interactive=False,visible=True)) 
        else:
           audio_list.append(gr.Audio.update(label="情感参考音频",value=wavpath,interactive=False,visible=True)) 
        wavname_list.append(gr.Textbox().update(value=wav_name,label=i,visible=True))        
        transcription_list.append(gr.Textbox().update(value=tr,visible=True))
        checkbox_list.append(gr.Checkbox().update(value=False,visible=True))
    length=page_end-page_start
    if length<10:
        for i in range(9-length):
            wavname_list.append(gr.Textbox().update(value=None,label='None',visible=False))
            audio_list.append(gr.Audio.update(label="情感参考音频",value=None,interactive=False,visible=False))
            transcription_list.append(gr.Textbox().update(value=None,visible=False))
            checkbox_list.append(gr.Checkbox().update(value=False,visible=False))
    list_all=wavname_list+transcription_list+audio_list+checkbox_list
    return list_all

def calculate_page(length):#calculate the index and return
    global current_page
    if length<=10 and current_page==1:
        return 0,length-1,False,False#range,left,right
    else:
        end=10*current_page-1
        if end > length-1:#num<10
           end=length-1
           return 10*(current_page-1),end,True,False
        else:#full
           if current_page==1:
              return 10*(current_page-1),end,False,True 
           return 10*(current_page-1),end,True,True

def switch_page(speaker,class_name):#switch to the specified page or adjust page index , then load page.
    global current_page
    global class_info
    if current_page<1:
        current_page=1
    length=len(class_info[speaker][class_name])
    if length==0:
        return emo_ret_none()
    if current_page>1 and (current_page-1)*10>=length:#e.g [0-9],page==2-> [10] -> out of range
        current_page-=1
    #print(length)
    page_start,page_end,left,right=calculate_page(length)
    #print(page_start,page_end)
    return *load_page(page_start,page_end,speaker,class_name),previous_btn.update(interactive=left),emo_page_index.update(value=current_page),next_btn.update(interactive=right)

def reverse_selection(*checkbox_list):
    rt_list = [not i if i is True else True for i in checkbox_list]
    return rt_list

def del_wav_in_class(speaker,class_name,*checkbox_list):
    length=len(class_info[speaker][class_name])
    page_start,page_end,_,_=calculate_page(length)
    id=0
    checkbox_list=list(checkbox_list)
    for i in range(page_start, page_end+1):
        if checkbox_list[id]:
            class_info[speaker][class_name][id]=None
        id+=1
    while None in class_info[speaker][class_name]:
        class_info[speaker][class_name].remove(None)
    return switch_page(speaker,class_name)

def del_rename_class(speaker,class_,new_name=None):
    global class_info
    global current_page
    if new_name is not None:
        if new_name in class_info[speaker]:
            return emo_chosen_class.update(value=new_name,choices=list(class_info[speaker].keys())),gr.Textbox().update(placeholder='重名了！',value=None)
        class_info[speaker][new_name]=class_info[speaker][class_]
        del class_info[speaker][class_]
        return emo_chosen_class.update(value=new_name,choices=list(class_info[speaker].keys())),gr.Textbox().update(placeholder='输入重命名',value=None)
    else:
        del class_info[speaker][class_]
        lst=list(class_info[speaker].keys())
        current_page=0
        return emo_chosen_class.update(choices=lst,value=lst[0])      



current_yml=None
def get_status():
    global current_yml
    try:
        cfg = yaml.load(open('config.yml'),Loader=yaml.FullLoader)
        current_yml='当前的训练： '+os.path.basename(cfg["dataset_path"])+"\n\n以下是配置文件内容：\n\n"
        with open('config.yml', mode="r", encoding="utf-8", errors='ignore') as f:
            current_y=f.read()
            current_yml+=current_y
    except Exception as error:
        current_yml=error

get_status()

def p0_write_yml(name,val_per_spk,max_val_total,bert_num_processes,emo_num_processes,num_workers,keep_ckpts):
    if name=='null'or name=='':
        return '请选择！'
    config_path=os.path.join('Data',name,'config.yml')
    config_yml = yaml.load(open(config_path),Loader=yaml.FullLoader)
    config_yml["preprocess_text"]["val_per_spk"] = int(val_per_spk)
    config_yml["preprocess_text"]["max_val_total"] = int(max_val_total)
    config_yml["bert_gen"]["num_processes"] = int(bert_num_processes)
    config_yml["emo_gen"]["num_processes"] = int(emo_num_processes)
    config_yml["train_ms"]["num_workers"]=int(num_workers)
    config_yml["train_ms"]["keep_ckpts"]=int(keep_ckpts)
    with open(config_path, 'w', encoding='utf-8') as f:
          yaml.dump(config_yml, f) 
    return 'Success'


list_project = []  
def refresh_project_list():
    global list_project
    list_project = []  
    for item in os.listdir('Data'):
       item_path = os.path.join('Data', item)
       if os.path.isdir(item_path):
          list_project.append(item)
    return (project_name.update(choices=list_project),project_name2.update(choices=list_project),project_name3.update(choices=list_project),project_name4.update(choices=list_project),'已刷新下拉列表')

for item in os.listdir('Data'):
    item_path = os.path.join('Data', item)
    if os.path.isdir(item_path):
        list_project.append(item)



def p0_mkdir(name):
    if name!='':
       try:   
         path='Data'
         path=os.path.join('Data',name)  
         os.mkdir(path)#path=data/xxx/
         os.mkdir(os.path.join(path,'custom_character_voice'))
         os.mkdir(os.path.join(path,'filelists'))
         os.mkdir(os.path.join(path,'models'))       
         shutil.copy("./configs/config.json",os.path.join(path,"config.json"))
         try:
            with open('./configs/default_config.yml', mode="r", encoding="utf-8") as f:
                cfg_yml=yaml.load(f,Loader=yaml.FullLoader)
         except:
            with open('default_config.yml', mode="r", encoding="utf-8") as f:
                cfg_yml=yaml.load(f,Loader=yaml.FullLoader)
         cfg_yml["dataset_path"]=path
         cfg_yml["resample"]["in_dir"]="custom_character_voice"
         cfg_yml["resample"]["out_dir"]="custom_character_voice"
         cfg_yml["preprocess_text"]["cleaned_path"]='filelists/cleaned.list'
         cfg_yml["preprocess_text"]["transcription_path"]='filelists/short_character_anno.list'
         cfg_yml["preprocess_text"]["train_path"]='filelists/train.list'
         cfg_yml["preprocess_text"]["val_path"]='filelists/val.list'
         cfg_yml["preprocess_text"]["config_path"]='config.json'
         cfg_yml["bert_gen"]["config_path"]='config.json'
         cfg_yml["emo_gen"]["config_path"]='config.json'
         cfg_yml["train_ms"]["config_path"]='config.json'
         with open(os.path.join(path,"config.yml"), 'w', encoding='utf-8') as f:
            yaml.dump(cfg_yml, f) 
         os.startfile(path)
         refresh_project_list()
         return project_name.update(choices=list_project,value=name),'Success. 已经自动打开了创建好的文件夹。请将音频按说话人分文件夹放入custom_character_voice内。然后进行下一步操作。'
       except Exception as error:
         return error   
    else:
       return '请输入名称！'    

def p0_load_cfg(projectname):
    if projectname=='null'or projectname=='':
        return p0_status.update(value=current_yml),'请选择！'
    try:
        shutil.copy(os.path.join('Data',projectname,'config.yml'),'config.yml')
        get_status()
        return p0_status.update(value=current_yml) ,'Success'
    except Exception as error:
        return p0_status.update(value=current_yml),error

        


def a1a_transcribe(size,lang):
     command = f'{py_dir} short_audio_transcribe.py --languages {lang} --whisper_size {size}'
     print(command+'\n\n')
     subprocess.Popen(['start', 'cmd', '/k', command],cwd=current_directory,shell=True)
     return '新的命令行窗口已经打开，请关注输出信息。完成后无报错即可关闭进行下一步！'

def a1b_transcribe_genshin():
     command = f"{py_dir} transcribe_genshin.py"
     print(command+'\n\n')
     subprocess.Popen(['start', 'cmd', '/k', command],cwd=current_directory,shell=True)
     return '新的命令行窗口已经打开，请关注输出信息。完成后无报错即可关闭进行下一步！'

def a2_preprocess_text():
     command = f"{py_dir} preprocess_text.py"
     print(command+'\n\n')
     subprocess.Popen(['start', 'cmd', '/k', command],cwd=current_directory,shell=True)
     return '新的命令行窗口已经打开，请关注输出信息。完成后无报错即可关闭进行下一步！'

def a3_bert_gen():
     command = f"{py_dir} bert_gen.py"
     print(command+'\n\n')
     subprocess.Popen(['start', 'cmd', '/k', command],cwd=current_directory,shell=True)
     return '新的命令行窗口已经打开，请关注输出信息。完成后无报错即可关闭进行下一步！'

def a3_emo_gen():
    command = f"{py_dir} emo_gen.py"
    print(command+'\n\n')
    subprocess.Popen(['start', 'cmd', '/k', command],cwd=current_directory,shell=True)
    return '新的命令行窗口已经打开，请关注输出信息。完成后无报错即可关闭进行下一步！'

def a35_json(bs,lr,interval):
    try:
        with open('config.yml', mode="r", encoding="utf-8") as f:
            cfg_yml=yaml.load(f,Loader=yaml.FullLoader)
        config_path=os.path.join(cfg_yml["dataset_path"],'config.json')
        configjson = json.load(open(config_path, encoding="utf-8"))
        configjson["train"]["batch_size"] = int(bs)
        configjson["train"]["learning_rate"] = lr
        configjson["train"]["log_interval"] = int(interval)
        configjson["train"]['eval_interval'] = int(interval)
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(configjson, f, indent=2, ensure_ascii=False) 
        return 'success'
    except Exception as error:
        return error 
    
        
def a4a_train():
     command = f"{py_dir} train_ms.py"
     with open('config.yml', mode="r", encoding="utf-8") as f:
          configyml=yaml.load(f,Loader=yaml.FullLoader)
     cfg_path=os.path.join(configyml["dataset_path"],'config.json')        
     configjson = json.load(open(cfg_path, encoding="utf-8"))
     if not configjson["train"]["skip_optimizer"]:
         configjson["train"]["skip_optimizer"]=True
         with open(cfg_path, 'w', encoding='utf-8') as f:
             json.dump(configjson, f, indent=2, ensure_ascii=False)
         print("已经修改配置文件！\n")
     shutil.copy('./pretrained_models/D_0.pth',os.path.join(os.path.join(configyml["dataset_path"],configyml["train_ms"]["model"]),'D_0.pth'))
     shutil.copy('./pretrained_models/G_0.pth',os.path.join(os.path.join(configyml["dataset_path"],configyml["train_ms"]["model"]),'G_0.pth'))
     shutil.copy('./pretrained_models/DUR_0.pth',os.path.join(os.path.join(configyml["dataset_path"],configyml["train_ms"]["model"]),'DUR_0.pth'))
     print("已经复制了底模\n")
     subprocess.Popen(['start', 'cmd', '/k', command],cwd=current_directory,shell=True)
     print(command+'\n\n')
     return '新的命令行窗口已经打开，请关注输出信息。关闭窗口或Ctrl+C终止训练'

def a4b_train_cont():
     command = f"{py_dir} train_ms.py"
     with open('config.yml', mode="r", encoding="utf-8") as f:
            configyml=yaml.load(f,Loader=yaml.FullLoader)
     cfg_path=os.path.join(configyml["dataset_path"],'config.json')   
     configjson = json.load(open(cfg_path, encoding="utf-8"))
     if configjson["train"]["skip_optimizer"]:
         configjson["train"]["skip_optimizer"]=False
         with open(cfg_path, 'w', encoding='utf-8') as f:
             json.dump(configjson, f, indent=2, ensure_ascii=False)
         print("已经修改配置文件！\n")
     subprocess.Popen(['start', 'cmd', '/k', command],cwd=current_directory,shell=True)
     print(command+'\n\n')
     return '新的命令行窗口已经打开，请关注输出信息。关闭窗口或Ctrl+C终止训练'

def start_tb():
     with open('config.yml', mode="r", encoding="utf-8") as f:
            configyml=yaml.load(f,Loader=yaml.FullLoader)
     command = f"{py_dir} -m tensorboard.main --logdir="+os.path.join(configyml["dataset_path"],configyml["train_ms"]["model"])
     print(command+'\n\n')
     subprocess.Popen(['start', 'cmd', '/k', command],cwd=current_directory,shell=True)
     return '新的命令行窗口已经打开，请关注输出信息。'

ckpt_list = ['null']

def c2_refresh_sub_opt(name):  
   try:
       global ckpt_list
       ckpt_list=['null']
       file_list = os.listdir(os.path.join("Data",name,"models"))
       for ck in file_list:
         if os.path.splitext(ck)[-1] == ".pth"and ck[:2] != "D_" and ck[:4] !="DUR_":
            ckpt_list.append(ck)
       return models_in_project.update(choices=ckpt_list,value=ckpt_list[-1])
   except :
       return models_in_project.update(choices=['null'],value='null')

def c2_infer(proj_name,model_name):
    if proj_name=='null' or model_name=='null':
        return '请选择模型！'
   
    path=f'./Data/{proj_name}'
    command = f'{py_dir} webui.py -c {path}/config.json -m {path}/models/{model_name}'
    print(command+'\n\n')
    subprocess.Popen(['start', 'cmd', '/k', command],cwd=current_directory,shell=True)
    return '新的命令行窗口已经打开，请关注输出信息。关闭窗口结束推理服务。'

def c2_infer_2(proj_name,model_name):
    y=yaml.load(open('config.yml'),Loader=yaml.FullLoader)
    if proj_name=='null' or model_name=='null':
        y["server"]["models"]=[]
    else:
        y["server"]["models"]=[]
        y["server"]["models"].append({"config":os.path.join('Data',proj_name,'config.json'),"device":'cuda',"language": 'ZH',"model":os.path.join('Data',proj_name,'models',model_name),"speakers":[]})
    with open("config.yml", 'w', encoding='utf-8') as f:
        yaml.dump(y, f) 
    subprocess.Popen(['start', 'cmd', '/k',f'{py_dir} server_fastapi.py'],cwd=current_directory,shell=True)
    return '已经修改了全局配置文件。新的命令行窗口已经打开，请关注输出信息。关闭窗口结束推理服务。'

def write_version(name,version,cont):
    if name=='null':
        return opt_continue.update(value=False),'请选择！'
    path=os.path.join('Data',name,'config.json')
    try:
       configjson = json.load(open(path))
       if "version" in configjson:
          if not cont:
            return opt_continue.update(value=False),'版本信息已经存在，是不是手滑了？'
          configjson["version"] = version
       else:
           configjson["version"] = version
       with open(path, 'w', encoding='utf-8') as f:
            json.dump(configjson, f, indent=2, ensure_ascii=False) 
       return opt_continue.update(value=False),f'Success. {version}'
    except Exception as e:
       return opt_continue.update(value=False),e

def switch_previous_page(speaker,class_name):
    global current_page
    current_page-=1
    return switch_page(speaker,class_name)
def switch_next_page(speaker,class_name):
    global current_page
    current_page+=1
    return switch_page(speaker,class_name)

def emo_write(proj_name):
    global class_info
    try:
        with open(os.path.join('Data',proj_name,'emo_clustering.yml'), 'w', encoding='utf-8') as f:
            yaml.dump(class_info, f) 
        return 'Success'
    except Exception as e:
        return '写入出错'+str(e)

def run_ec_gen(proj_name,num_clusters,num_wav):
     if proj_name=="":
        command = f"{py_dir} emotion_clustering.py -n {int(num_clusters)} -r {int(num_wav)}"
     else:
        command = f"{py_dir} emotion_clustering.py -y {os.path.join('Data',proj_name,'config.yml')} -n {int(num_clusters)} -r {int(num_wav)}" 
     print(command+'\n\n')
     subprocess.Popen(['start', 'cmd', '/k', command],cwd=current_directory,shell=True)
     return '新的命令行窗口已经打开，请关注输出信息。'

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p", "--server_port", default=6660,type=int,help="server_port"
    )
    args = parser.parse_args()
    with gr.Blocks(title="Bert-VITS-2-Manager-WebUI-210") as app:
        gr.Markdown(value="""
        Bert-VITS2训练管理器
                    
        严禁将此项目用于一切违反《中华人民共和国宪法》，《中华人民共和国刑法》，《中华人民共和国治安管理处罚法》和《中华人民共和国民法典》之用途。由使用本整合包产生的问题和作者、原作者无关！！！
        
        作者：bilibili@数列解析几何一生之敌
        
        适用于整合包版本V2.1,不兼容之前的版本。
                    
        WebUI更新日期：2023.11.30
        """) 
        with gr.Tabs():
           with gr.TabItem("1.创建实验文件夹和加载全局配置"):
               with gr.Row(): 
                   with gr.Column():
                       p0_mkdir_name=gr.Textbox(label="这将创建实验文件夹，请输入实验名称,不要包含中文、特殊字符和保留字符。",
                       placeholder="请输入实验名称,最好不要包含中文、特殊字符和保留字符。",
                       value="",
                       lines=1,
                       interactive=True)                       
                       p0_mkdir_output_text = gr.Textbox(label="输出信息", placeholder="点击处理按钮",interactive=False)
                       p0_mkdir_btn=gr.Button(value="创建！", variant="primary")

                       gr.Markdown(value="<br>")
                                                     
                       project_name = gr.Dropdown(label="实验文件夹", choices=list_project, value='null'if not list_project else list_project[-1],interactive=True) 
                       with gr.Row():
                            p0_val_ps = gr.Number(label="每个说话人的验证集数", value="4",interactive=True)
                            p0_val_tt = gr.Number(label="总的验证集数", value="8",interactive=True)
                            p0_bg_t = gr.Number(label="bert_gen线程数", value="2",interactive=True)
                            p0_emo_t = gr.Number(label="emo_gen线程数", value="2",interactive=True)
                            p0_dataloader = gr.Number(label="num_workers", value="4",interactive=True)
                            p0_keep_ckpt = gr.Number(label="模型留存个数", value="10",interactive=True)
                       p0_load_cfg_output_text = gr.Textbox(label="输出信息", placeholder="点击处理按钮",interactive=False)
                       with gr.Row():
                          p0_write_cfg_btn=gr.Button(value="保存更改(但不会自动加载)", variant="primary")
                          p0_load_cfg_btn = gr.Button(value="加载训练配置", variant="primary")
                          p0_load_cfg_refresh_btn=gr.Button(value="刷新选项", variant="secondary")


                   with gr.Column():
                       #p0_current_proj=gr.Textbox(label="当前生效的训练",value="",interactive=False)
                       p0_status=gr.TextArea(label="训练前请确认当前的全局配置信息", value=current_yml,interactive=False)

           with gr.TabItem("2.训练"):
               with gr.Column():                                 
                   whisper_size = gr.Radio(label="选择whisper大小，large需要12G显存", choices=['large','medium','small'], value="medium")
                   language = gr.Radio(label="选择语言(默认中日英，其他不支持的语言会被跳过)", choices=['C','CJ','CJE'], value="CJE") 
               with gr.Column():
                    with gr.Row():
                        a1a_btn = gr.Button(value="1.a.数据集重采样和标注(使用whisper)", variant="primary")
                        a1b_btn = gr.Button(value="1.b.处理下载的已标注的原神数据集", variant="primary") 
                    a1_textbox_output_text = gr.Textbox(label="输出信息", placeholder="点击处理按钮，二选一",interactive=False)                
               #gr.Markdown(value="<br>")      
               with gr.Row():
                    a2_btn = gr.Button(value="2.文本预处理", variant="primary")
                    a2_textbox_output_text = gr.Textbox(label="输出信息", placeholder="点击处理按钮",interactive=False)
               #gr.Markdown(value="<br>") 
               with gr.Row():
                  a3_btn = gr.Button(value="3-1.生成bert文件", variant="primary")
                  a3_btn_2 = gr.Button(value="3-2.生成emo文件", variant="primary")
                  a3_textbox_output_text = gr.Textbox(label="输出信息", placeholder="点击处理按钮",interactive=False)                                  
              # gr.Markdown(value="<br>") 
               with gr.Row():
                    #with gr.Column():
                    a35_btn = gr.Button(value="写入配置文件", variant="primary")
                    with gr.Column():
                        with gr.Row():
                            a35_textbox_bs = gr.Number(label="批大小", value="8",interactive=True)
                            a35_textbox_lr = gr.Number(label="学习率", value="0.0001",interactive=True)
                            a35_textbox_save = gr.Number(label="保存间隔", value="100",interactive=True)
                        a35_textbox_output_text = gr.Textbox(label="输出信息", placeholder="点击处理按钮",interactive=False) 
               #gr.Markdown(value="<br>") 
               with gr.Row():              
                    with gr.Row():
                       a4a_btn = gr.Button(value="4a.首次训练", variant="primary")
                       a4b_btn = gr.Button(value="4b.继续训练", variant="primary")                       
                    with gr.Column():
                       a4_textbox_output_text = gr.Textbox(label="输出信息", placeholder="点击处理按钮",interactive=False)
        
               with gr.Row():              
                       tb_btn = gr.Button(value="启动TensorBoard", variant="primary")            
                       tb_textbox_output_text = gr.Textbox(label="输出信息", placeholder="点击处理按钮",interactive=False)                   
           with gr.TabItem("3.启动推理"):
                gr.Markdown(value='工作区模型推理(Data内各实验目录下的模型)') 
                with gr.Row():
                    project_name2 = gr.Dropdown(label="选择实验名", choices=list_project, value='null',interactive=True)
                    models_in_project = gr.Dropdown(label="选择模型", choices=ckpt_list, value='null'if not ckpt_list else ckpt_list[0],interactive=True)
                    with gr.Column():
                       c2_btn = gr.Button(value="启动推理(Gr WebUI)", variant="primary")
                       c2_btn2 = gr.Button(value="启动推理(Hiyori UI)", variant="primary")
                       c2_btn_refresh=gr.Button(value="刷新选项", variant="secondary")
                with gr.Column():
                       c2_textbox_output_text = gr.Textbox(label="输出信息", placeholder="点击处理按钮",interactive=False) 
                project_name2.change(c2_refresh_sub_opt,[project_name2],[models_in_project]) 
           with gr.TabItem("辅助功能"):
                with gr.TabItem("情感分类编辑"):
                    with gr.Row():
                        project_name4=gr.Dropdown(label="选择实验名", choices=list_project,value=''if not list_project else list_project[0],interactive=True)
                        emo_proj_load_btn=gr.Button(value="加载配置", variant="primary")
                        emo_proj_refresh=gr.Button(value="刷新选项", variant="secondary")
                    emo_status_text=gr.Textbox(label="状态", placeholder="点击处理按钮",interactive=False)
                #   
                    with gr.Column():
                        with gr.Row():
                            emo_speaker=gr.Dropdown(label='选择说话人',choices=emo_speaker_list,interactive=True)
                            emo_chosen_class=gr.Dropdown(label='选择类别',choices=emo_class_list,interactive=True)
                            emo_write_btn=gr.Button(value="写入(保存更改)", variant="primary")
                        with gr.Accordion("生成配置"):
                            with gr.Row():
                                ec_gen_btn=gr.Button(value="生成配置",variant="primary")
                                ec_gen_n_clu=gr.Number(label="类别数量",value=5)
                                ec_gen_range=gr.Number(label="每类的音频数",value=5)                    
                        with gr.Accordion("编辑区域"):
                            with gr.Row():                                
                                emo_enter_rename=gr.Textbox(label="重命名",placeholder="在此输入重命名，然后点击重命名按钮",scale=2)
                                emo_enter_rename_btn=gr.Button(value="重命名类别", variant="primary",scale=1)
                                emo_del_class_btn=gr.Button(value="删除此类别", variant="primary",scale=1)
                                emo_del_wav_btn=gr.Button(value="删除所选", variant="primary",scale=1)
                                emo_reverse_selection_btn=gr.Button(value="反向选择", variant="primary",scale=1)
                        with gr.Row():
                                emo_file_name=gr.Textbox(label="文件名",value='空列表',interactive=False,scale=4)
                                emo_tr=gr.Textbox(label="文本",value=None,interactive=False,scale=5,visible=False)
                                emo_wav=gr.Audio(label="情感参考音频",value=None,interactive=False,visible=False,scale=5)
                                emo_checkbox=gr.Checkbox(label='选择',value=False,scale=1,visible=False)
                                emo_tr_list.append(emo_tr)
                                emo_file_name_list.append(emo_file_name)
                                emo_audio_list.append(emo_wav)
                                emo_checkbox_list.append(emo_checkbox)
                        for i in range(9):
                            with gr.Row():
                                emo_file_name=gr.Textbox(label="文件名",value=None,interactive=False,scale=4,visible=False)
                                emo_tr=gr.Textbox(label="文本",value=None,interactive=False,scale=5,visible=False)
                                emo_wav=gr.Audio(label="情感参考音频",value=None,interactive=False,visible=False,scale=5)
                                emo_checkbox=gr.Checkbox(label='选择',value=False,scale=1,visible=False)
                                emo_tr_list.append(emo_tr)
                                emo_file_name_list.append(emo_file_name)
                                emo_audio_list.append(emo_wav)
                                emo_checkbox_list.append(emo_checkbox)
                        with gr.Row():
                            previous_btn=gr.Button(value="<-上一页", variant="secondary",interactive=False,scale=5)
                            emo_page_index=gr.Number(label='页码',value=current_page,interactive=False,scale=1)
                            next_btn=gr.Button(value="下一页->", variant="primary",interactive=False,scale=5)
                        emo_speaker.change(emo_change_speaker,[emo_speaker],[emo_chosen_class,*emo_file_name_list,*emo_tr_list,*emo_audio_list,*emo_checkbox_list,previous_btn,emo_page_index,next_btn])
                        emo_chosen_class.change(emo_change_class,[emo_speaker,emo_chosen_class],[*emo_file_name_list,*emo_tr_list,*emo_audio_list,*emo_checkbox_list,previous_btn,emo_page_index,next_btn])
                with gr.TabItem("配置文件添加版本号"):
                    gr.Markdown(value='旧版本模型的配置文件添加版本号后方可在2.0版本下使用兼容推理')
                    gr.Markdown(value='按文件结构把配置文件和模型放到对应位置，然后开始操作。')
                    gr.Markdown(value='使用1.1和1.1.1版兼容推理需要安装上一个版本使用的日语bert。')
                    gr.Markdown(value='可选版本为1.0.1,1.1,1.1.1和2.0。旧整合包版本为1.0.1或1.1.1或2.0。')
                    project_name3 = gr.Dropdown(label="选择实验名", choices=list_project, value='null'if not list_project else list_project[0],interactive=True)
                    with gr.Row():
                      with gr.Column():
                          choose_version=gr.Dropdown(label="选择版本", choices=['1.0.1','1.1','1.1.1','2.0','2.1'], value='1.0.1',interactive=True)
                          opt_continue = gr.Checkbox(label="我没手滑")
                          write_ver_btn=gr.Button(value="写入",variant="primary")
                          write_ver_refresh_btn=gr.Button(value="刷新",variant="secondary")
                      with gr.Column():
                          write_ver_textbox=gr.Textbox(label="输出信息", placeholder="点击处理按钮",interactive=False)
           with gr.TabItem("关于&帮助"):
                with gr.TabItem("项目简介"):
                    with gr.Row():            
                        gr.Markdown(value=readme_md)
                        gr.Markdown(value=update_info)
                with gr.TabItem("训练流程和命令行使用"): 
                    with gr.Row():                  
                        gr.Markdown(value=cmd_md)                      
                        gr.Markdown(value=file_structure_md)
                with gr.TabItem("常见错误"):
                    with gr.Row():
                        gr.Markdown(value=errors)

        p0_write_cfg_btn.click(p0_write_yml,
                           inputs=[project_name,p0_val_ps,p0_val_tt,p0_bg_t,p0_emo_t,p0_dataloader,p0_keep_ckpt],
                           outputs=[
                p0_load_cfg_output_text,
            ],)                
        p0_mkdir_btn.click(p0_mkdir,
                           inputs=[p0_mkdir_name],
                           outputs=[
                               project_name,
                p0_mkdir_output_text,
            ],)
        p0_load_cfg_btn.click(p0_load_cfg,
                           inputs=[project_name],
                           outputs=[p0_status,
                p0_load_cfg_output_text,
            ],)
        p0_load_cfg_refresh_btn.click(refresh_project_list,
                           inputs=[],
                           outputs=[project_name,
                                    project_name2,
                                    project_name3,
                                    project_name4,
                p0_load_cfg_output_text,
            ],)
        emo_proj_refresh.click(refresh_project_list,
                           inputs=[],
                           outputs=[project_name,
                                    project_name2,
                                    project_name3,
                                    project_name4,
                emo_status_text,
            ],)        
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
        a3_btn_2.click(
            a3_emo_gen,
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
        c2_btn.click(
            c2_infer,
            inputs=[project_name2,models_in_project],
            outputs=[
                c2_textbox_output_text,
            ],
        )
        c2_btn2.click(
            c2_infer_2,
            inputs=[project_name2,models_in_project],
            outputs=[
                c2_textbox_output_text,
            ],
        )            
        c2_btn_refresh.click(refresh_project_list,[],[project_name,project_name2,project_name3,project_name4,c2_textbox_output_text])
        write_ver_refresh_btn.click(refresh_project_list,[],[project_name,project_name2,project_name3,project_name4,write_ver_textbox])
        write_ver_btn.click(
            write_version,
            inputs=[project_name3,choose_version,opt_continue],
            outputs=[opt_continue,
                write_ver_textbox,
            ],
        ) 
        emo_proj_load_btn.click(load_emo_clu,inputs=[project_name4],outputs=[emo_status_text,emo_speaker])
        #emo_del_class_btn.click()
        emo_del_wav_btn.click(
            del_wav_in_class,
            inputs=[emo_speaker,emo_chosen_class,*emo_checkbox_list],
            outputs=[*emo_file_name_list,*emo_tr_list,*emo_audio_list,*emo_checkbox_list,previous_btn,emo_page_index,next_btn]
        )
        emo_reverse_selection_btn.click(
            reverse_selection,
            inputs=[*emo_checkbox_list],
            outputs=[*emo_checkbox_list]
        )
        emo_del_class_btn.click(
            del_rename_class,
            inputs=[emo_speaker,emo_chosen_class],
            outputs=[emo_chosen_class]
        )
        emo_enter_rename_btn.click(
            del_rename_class,
            inputs=[emo_speaker,emo_chosen_class,emo_enter_rename],
            outputs=[emo_chosen_class,emo_enter_rename]
        )        
        next_btn.click(
            switch_next_page,
            inputs=[emo_speaker,emo_chosen_class],
            outputs=[*emo_file_name_list,*emo_tr_list,*emo_audio_list,*emo_checkbox_list,previous_btn,emo_page_index,next_btn]
            )
        previous_btn.click(
            switch_previous_page,
            inputs=[emo_speaker,emo_chosen_class],
            outputs=[*emo_file_name_list,*emo_tr_list,*emo_audio_list,*emo_checkbox_list,previous_btn,emo_page_index,next_btn]
            ) 
        emo_write_btn.click(
            emo_write,
            inputs=[project_name4],
            outputs=[emo_status_text]
        ) 
        ec_gen_btn.click(
            run_ec_gen,
            inputs=[project_name4,ec_gen_n_clu,ec_gen_range],
            outputs=[emo_status_text]
        )      
webbrowser.open(f"http://127.0.0.1:{args.server_port}")
app.launch(share=False,server_port=args.server_port)
