import pywebio
import PIL.Image
from io import BytesIO

import torch
import torchvision.transforms

from model.myModel_import import *


@pywebio.config(title="卷积神经网络Demo", description="基于CiFar10数据集图像分类")
def page1():
    train_set_classes = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']

    def show_info():
        pywebio.output.put_markdown("# 基于CiFar10数据集的图像分类")
        pywebio.output.put_html("<br>")
        pywebio.output.put_table([
            [pywebio.output.span('数据集', row=1), pywebio.output.span('支持类别', col=4)],
            ['CiFar10', train_set_classes]
        ])
        pywebio.output.put_html("<br>")

    graph_img = PIL.Image.open("./images/net_graph.png")

    show_net = [pywebio.output.put_text('net'),
                pywebio.output.put_image(graph_img)]

    def popup_window(title, content):
        pywebio.output.popup(title=title, content=content)

    show_info()

    pywebio.output.put_buttons(['查看网络结果'], [lambda: popup_window('网络结构', show_net)])

    pywebio.input.actions("", [{'label': "上传图片", 'value': "", 'color': 'success', }])
    inpic = pywebio.input.file_upload(label="上传图片 please upload a image")

    pywebio.output.popup("加载中", [
        pywebio.output.put_loading(),
    ])

    img = PIL.Image.open(BytesIO(inpic['content']))
    img = img.convert("RGB")
    transform01 = torchvision.transforms.Compose([
        torchvision.transforms.Resize((32, 32)),
        torchvision.transforms.ToTensor()
    ])
    img = transform01(img)
    img = torch.reshape(img, (1, 3, 32, 32))
    model = torch.load("./model/myModel_46.pth", map_location=torch.device('cpu'))

    with torch.no_grad():
        output = model(img)
    print(output)

    pywebio.output.popup(
        title='识别结果',
        content=[
            pywebio.output.put_markdown("分类结果：\n # " + train_set_classes[output.argmax(1).item()]),
            pywebio.output.put_image(None if not inpic else inpic['content'])
        ]
    )
    del model, inpic, img


if __name__ == '__main__':
    pywebio.start_server(
        applications=[page1, ],
        debug=True,
        cdn=False,
        auto_open_webbrowser=False,
        remote_access=False,
        prot=8899
    )
