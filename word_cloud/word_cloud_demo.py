import os
import unicodedata
from pathlib import Path
from string import ascii_lowercase

import numpy as np
import pandas as pd
from PIL import Image
from wordcloud import STOPWORDS, ImageColorGenerator
from wordcloud import WordCloud as WC

GOOD_CHARS = ascii_lowercase + " '-.:/\\"


def text_filter(text):
    text = unicodedata.normalize("NFKD", text).lower()
    words = ["".join(c for c in word if c in GOOD_CHARS).strip() for word in text.split()]
    return " ".join(word for word in words if len(word) > 1)


def generate(image_path: Path, text_series: pd.Series, scale=1):
    mask = np.asarray(Image.open(image_path))
    color_gen = ImageColorGenerator(mask)

    text: str = text_filter(text_series.str.cat(sep=" "))

    wc = WC(
        prefer_horizontal=0.95,
        color_func=color_gen,
        background_color="#36393F",
        mask=mask,
        scale=scale,
        stopwords=STOPWORDS | set("nope really idk nothing dont cant none".split()),
    ).generate(text)

    return wc.to_image()


if __name__ == "__main__":
    # 创建模拟数据 - 一个关于Python编程语言的调查
    data = {
        "What do you like about Python Discord? What keeps you involved in the server?": [
            "I love how helpful the community is.",
            "The code reviews and learning resources are amazing.",
            "Python coding challenges help me improve my skills.",
            "The community projects are a great way to learn.",
            "I enjoy helping others solve Python problems.",
            "The discussions about new Python features are interesting.",
            "Great place to share Python libraries and tools.",
            "The mentoring aspect of the community is valuable.",
            "Python Discord offers a friendly environment for beginners.",
            "The async programming discussions have been very helpful.",
        ]
    }

    # 创建DataFrame
    survey_data = pd.DataFrame(data)

    # 确保images目录存在
    os.makedirs("word_cloud/images", exist_ok=True)

    # 使用简单的圆形蒙版（如果没有logo图像）
    image_path = Path("/Users/datagrand/Downloads/颜 文字 君.jpeg")
    if not image_path.exists():
        # 创建圆形蒙版
        x, y = np.ogrid[:300, :300]
        mask = (x - 150) ** 2 + (y - 150) ** 2 > 130**2
        mask = 255 * mask.astype(int)
        mask = np.stack([mask, mask, mask], axis=2)

        # 保存蒙版图像
        mask_image = Image.fromarray(mask.astype(np.uint8))
        image_path.parent.mkdir(parents=True, exist_ok=True)
        mask_image.save(image_path)
        print(f"创建了默认蒙版图像: {image_path}")

    # 生成词云
    wordcloud_image = generate(
        image_path,
        survey_data["What do you like about Python Discord? What keeps you involved in the server?"],
        scale=2.0,  # 增加缩放比例以提高清晰度
    )

    # 直接使用PIL保存图像，提高清晰度
    output_path = Path("word_cloud/images/python_discord_wordcloud.png")
    wordcloud_image.save(output_path)
    print(f"词云已保存至: {output_path}")

    # 展示保存的图像路径
    print(f"可以通过以下命令查看图像: open {output_path}")
