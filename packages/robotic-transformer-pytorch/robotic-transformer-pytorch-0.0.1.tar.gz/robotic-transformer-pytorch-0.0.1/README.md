<img src="./rt1.png" width="450px"></img>

## Robotic Transformer - Pytorch (wip)

Implementation of <a href="https://ai.googleblog.com/2022/12/rt-1-robotics-transformer-for-real.html">RT1 (Robotic Transformer)</a>, from the Robotics at Google team, in Pytorch

## Install

```bash
$ pip install robotic-transformer-pytorch
```

## Usage

```python
import torch
from robotic_transformer_pytorch import MaxViT, RT1

vit = MaxViT(
    num_classes = 1000,
    dim_conv_stem = 64,
    dim = 96,
    dim_head = 32,
    depth = (2, 2, 5, 2),
    window_size = 7,
    mbconv_expansion_rate = 4,
    mbconv_shrinkage_rate = 0.25,
    dropout = 0.1
)

model = RT1(
    vit = vit,
    num_actions = 11,
    depth = 6,
    heads = 8,
    dim_head = 64,
)

video = torch.randn(1, 3, 6, 224, 224)

pred = model(video) # (1, 6, 11) # (batch, frames, action logits)
```

## Citations

```bibtex
@inproceedings{rt12022arxiv,
    title   = {RT-1: Robotics Transformer for Real-World Control at Scale},
    author={Anthony	Brohan and  Noah Brown and  Justice Carbajal and  Yevgen Chebotar and  Joseph Dabis and  Chelsea Finn and  Keerthana Gopalakrishnan and  Karol Hausman and  Alex Herzog and  Jasmine Hsu and  Julian Ibarz and  Brian Ichter and  Alex Irpan and  Tomas Jackson and  Sally Jesmonth and  Nikhil Joshi and  Ryan Julian and  Dmitry Kalashnikov and  Yuheng Kuang and  Isabel Leal and  Kuang-Huei Lee and  Sergey Levine and  Yao Lu and  Utsav Malla and  Deeksha Manjunath and  Igor Mordatch and  Ofir Nachum and  Carolina Parada and  Jodilyn Peralta and  Emily Perez and  Karl Pertsch and  Jornell Quiambao and  Kanishka Rao and  Michael Ryoo and  Grecia Salazar and  Pannag Sanketi and  Kevin Sayed and  Jaspiar Singh and  Sumedh Sontakke and  Austin Stone and  Clayton Tan and  Huong Tran and  Vincent Vanhoucke and Steve Vega and  Quan Vuong and  Fei Xia and  Ted Xiao and  Peng Xu and  Sichun Xu and  Tianhe Yu and  Brianna Zitkovich},
    booktitle = {arXiv preprint arXiv:2204.01691},
    year    = {2022}
}
```
