import numpy as np
import os, io, random, pygame
from PIL import Image, ImageFont, ImageDraw


def text_to_img(text=u"这是一段测试文本", font_size=24, position="left", **args):
    pygame.init()

    im = Image.new("RGB", args["text_window"], args["bg_color"])
    font = pygame.font.SysFont("notosanscjktc", font_size, bold=True, italic=False)

    rtext = font.render(text, True, args["font_color"], args["bg_color"])

    sio = io.BytesIO()
    pygame.image.save(rtext, sio)
    sio.seek(0)

    line = Image.open(sio)
    if position == "left":
        im.paste(line, (10, 10))
    elif position == "center":
        gap = (args["text_window"][0] - line.size[0]) // 2
        im.paste(line, (gap, 10))
    return im


def draw_text(input_json, **args):
    img_list = []
    for key, value in input_json.items():
        if value == "通过":
            img_list.append(text_to_img(text=f"==> 测试内容：{key}， 测试结果：{value}.", font_color=args["normal_color"], **args))
        else:
            result, reason = value.split(":")
            img_list.append(
                text_to_img(text=f"==> 测试内容：{key}， 测试结果：{result}.", font_color=args["abnormal_color"], **args))
            img_list.append(text_to_img(text=f"          失败原因：{reason}", font_color=args["abnormal_color"], **args))

    report = Image.new("RGB", (args["text_window"][0], args["text_window"][1] * len(img_list)), args["bg_color"])
    for i, img in enumerate(img_list):
        report.paste(img, (10, 10 + i * args["text_window"][1]))

    return report


def draw_view(input_view, **args):
    gap = max((args["text_window"][0] - 2 * args["view_window"][0]) // 4, 10)
    report = Image.new("RGB", (args["text_window"][0], (args["view_window"][1] + gap) * len(input_view) // 2),
                       args["bg_color"])
    for i in range(len(input_view) // 2):
        left = input_view[2 * i].resize(args["view_window"])
        right = input_view[2 * i + 1].resize(args["view_window"])
        report.paste(left, (gap, i * gap + i * args["view_window"][1]))
        report.paste(right, (args["view_window"][0] + 3 * gap, i * gap + i * args["view_window"][1]))

    return report


def concate_image(image_list, **args):
    W_list = [i.size[0] for i in image_list]
    W = max(W_list)
    H_list = [i.size[1] for i in image_list]
    pdf = Image.new("RGB", (W, sum(H_list)), args["bg_color"])
    for i in range(len(image_list)):
        gap = (W - W_list[i]) // 2
        pdf.paste(image_list[i], (gap, sum(H_list[0:i])))
    return pdf


def draw_pdf(test_result, view_result, **args):
    im_list = []
    im_list.append(text_to_img(text=f"数据集验证报告", font_size=40, position="center", font_color=(20, 20, 200), **args))  # title
    im_list.append(text_to_img(text=f"1.解析器验证结果：", font_size=26, position="left", font_color=(20, 20, 200), **args))
    im_list.append(draw_text(test_result, **args))
    if view_result:
        im_list.append(
            text_to_img(text=f"2.部分样本可视化结果：", font_size=26, position="left", font_color=(20, 20, 200), **args))
        im_list.append(draw_view(view_result, **args))

    pdf = concate_image(im_list, **args)
    pdf.save(args["out_path"])


if __name__ == "__main__":
    draw_configs = {
        "data_set_name": "VOC 2007",
        "text_window": (1200, 60),
        "normal_color": (20, 200, 20),
        "abnormal_color": (200, 20, 20),
        "bg_color": (220, 220, 220),
        "view_window": (500, 400),
        "out_path": "1.pdf"
    }

    text = ["通过", "未通过:Struct名称定义不规范, 不能包含非法字符"]
    parse_result = {
        f"测试项{i}": text[random.randint(0, 1)]
        for i in range(20)
    }

    view_result = [Image.open("example.png", "r") for i in range(4)]
    #     view_result = []
    draw_pdf(parse_result, view_result, **draw_configs)