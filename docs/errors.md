# 常见错误和解决办法
错误反馈：(https://github.com/YYuX-1145/Bert-VITS2-Integration-package/issues)
# whisper转写文本时的错误
```
Warning: no short audios found
```
* ffmpeg没有被正确安装(会伴随一连串“找不到文件”)。
* 文件结构摆放错误。
# 训练时的报错 
## 数据集问题
```
ERROR:models:emb_g.weight is not in the checkpoint
```
加载底膜时，是正常的。无需担心
```
RuntimeError: expand(torch.FloatTensor{[2, 1025, 278]}, size=[2, 1025]):
 the number of sizes provided (2) must be 
 greater or equal to the number of dimensions in the tensor (3)
```
* 原因：音频为双声道，没有重采样。

```
RuntimeError: The expanded size of the tensor (32)
 must match the existing size (0) at non-singleton dimension 1. 
Target sizes: [192, 32]. Tensor sizes: [192, 0]
```
* 可能的原因：每条音频过短

```
UserWarning: Detected call of `lr_scheduler.step()` before `optimizer.step()`. 
In PyTorch 1.1.0 and later, you should call them in the opposite order:
 `optimizer.step()` before `lr_scheduler.step()`.  
Failure to do this will result in PyTorch skipping the first value of the learning rate schedule. 
See more details at https://pytorch.org/docs/stable/optim.html#how-to-adjust-learning-rate
  warnings.warn("Detected call of `lr_scheduler.step()` before `optimizer.step()`.
0it [00:00, ?it/s]
INFO:OUTPUT_MODEL:====> Epoch: 2
0it [00:00, ?it/s]
INFO:OUTPUT_MODEL:====> Epoch: 3
0it [00:00, ?it/s]
INFO:OUTPUT_MODEL:====> Epoch: 4
0it [00:00, ?it/s]
```
* 可能原因：空跑了，可能是音频过少或者其他原因导致没法正常分配训练音频。
## 硬件和软件问题(CUDA,CUDNN ERROR)
```
CUDNN_XXX_ERROR
```
* 原因：显卡硬件或驱动故障，或者爆显存
* 解决方法：不要超频，更新（或回滚到稳定的版本）驱动。
* 爆显存解决方法：降低批大小。
```
OSError: [WinError 1455] 页面文件太小，无法完成操作。
```
* 原因：（虚拟）内存不足
* 解决方法：确保硬盘空间充足（通常是C盘），并让Windows自动分配虚拟内存，并降低训练全局配置里的num_workers。
```
RuntimeError: PytorchStreamReader failed reading zip archive: 
invalid header or archive is corrupted
```
* 在极个别情况下出现过，可能在下载时数据损坏。
* 重新下载相关文件。

## 其他奇怪的问题
```
pyopenjtalk报奇怪的错误
```
* 整合包路径中不要含有中文或特殊字符。