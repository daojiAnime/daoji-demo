#!/usr/bin/env python
"""
词云生成器命令行工具
用法: python generate_wordcloud.py --input your_text.txt --output wordcloud.png
"""

import argparse
import sys
import unicodedata
from pathlib import Path
from string import ascii_lowercase

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from wordcloud import STOPWORDS, ImageColorGenerator
from wordcloud import WordCloud as WC

GOOD_CHARS = ascii_lowercase + " '-.:/\\"


def text_filter(text):
    """过滤文本，只保留有效字符"""
    text = unicodedata.normalize("NFKD", text).lower()
    words = ["".join(c for c in word if c in GOOD_CHARS).strip() for word in text.split()]
    return " ".join(word for word in words if len(word) > 1)


def generate_wordcloud(text, mask_path=None, output_path=None, scale=1, bg_color="#36393F"):
    """生成词云图像"""
    # 处理蒙版图像
    if mask_path and Path(mask_path).exists():
        mask = np.asarray(Image.open(mask_path))
        color_gen = ImageColorGenerator(mask)
    else:
        # 创建简单的圆形蒙版
        x, y = np.ogrid[:300, :300]
        mask = (x - 150) ** 2 + (y - 150) ** 2 > 130**2
        mask = 255 * mask.astype(int)
        mask = np.stack([mask, mask, mask], axis=2)
        color_gen = lambda *args, **kwargs: "white"  # 默认颜色

    # 过滤文本
    filtered_text = text_filter(text)

    # 生成词云
    wc = WC(
        prefer_horizontal=0.95,
        color_func=color_gen,
        background_color=bg_color,
        mask=mask if "mask" in locals() else None,
        scale=scale,
        stopwords=STOPWORDS | set("nope really idk nothing dont cant none".split()),
        max_words=200,
        random_state=42,
    ).generate(filtered_text)

    # 获取PIL图像对象
    wordcloud_image = wc.to_image()

    # 保存结果
    if output_path:
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        # 直接保存PIL图像，避免matplotlib的额外处理
        wordcloud_image.save(output_file)
        print(f"词云已保存至: {output_file}")

    return wordcloud_image


def main():
    """主函数，解析命令行参数并生成词云"""
    parser = argparse.ArgumentParser(description="生成词云图像")
    parser.add_argument("--input", "-i", required=True, help="输入文本文件路径")
    parser.add_argument("--output", "-o", default="wordcloud.png", help="输出图像路径")
    parser.add_argument("--mask", "-m", help="蒙版图像路径")
    parser.add_argument("--scale", "-s", type=float, default=2.0, help="缩放比例")
    parser.add_argument("--bg-color", default="#36393F", help="背景颜色")
    parser.add_argument("--show", action="store_true", help="显示生成的图像")

    args = parser.parse_args()

    # 检查输入文件
    if not Path(args.input).exists():
        print(f"错误: 输入文件 '{args.input}' 不存在")
        return 1

    try:
        # 读取文本文件
        with open(args.input, encoding="utf-8") as f:
            text = f.read()

        # 生成词云
        wordcloud_image = generate_wordcloud(
            text=text, mask_path=args.mask, output_path=args.output, scale=args.scale, bg_color=args.bg_color
        )

        # 如果需要，显示图像
        if args.show:
            plt.figure(figsize=(10, 8))
            plt.imshow(np.array(wordcloud_image))
            plt.axis("off")
            plt.show()

        return 0

    except Exception as e:
        print(f"生成词云时发生错误: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
