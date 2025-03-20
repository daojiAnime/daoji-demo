import logging

import structlog
from rich.console import Console
from rich.logging import RichHandler
from rich.style import Style
from rich.text import Text


class GradientLogRenderer:
    def __init__(self, colors=None, direction="diagonal"):
        """
        初始化渐变日志渲染器

        Args:
            colors: 渐变使用的颜色列表，例如["#0000FF", "#00FF00", "#FFFF00"]
            direction: 渐变方向，可选"diagonal"(斜向)、"horizontal"、"vertical"
        """
        self.console = Console()
        self.colors = colors or ["#0066ff", "#00ccff", "#00ffcc", "#00ff66"]  # 蓝到绿色渐变
        self.direction = direction

    def get_color_at_position(self, x, y, width, height):
        """根据位置计算颜色"""
        if self.direction == "horizontal":
            pos = x / width
        elif self.direction == "vertical":
            pos = y / height
        else:  # diagonal
            # 斜向渐变，根据位置在对角线上的投影计算
            pos = (x / width + y / height) / 2

        # 确保pos在0-1之间
        pos = max(0, min(1, pos))

        # 计算颜色索引
        color_sections = len(self.colors) - 1
        section_idx = min(int(pos * color_sections), color_sections - 1)
        section_pos = (pos * color_sections) - section_idx

        # 计算两个颜色间的插值
        color1 = self.colors[section_idx]
        color2 = self.colors[section_idx + 1]

        # 简单的RGB线性插值
        def interpolate_color(c1, c2, factor):
            # 从十六进制转换为RGB
            r1, g1, b1 = int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16)
            r2, g2, b2 = int(c2[1:3], 16), int(c2[3:5], 16), int(c2[5:7], 16)

            # 线性插值
            r = int(r1 + (r2 - r1) * factor)
            g = int(g1 + (g2 - g1) * factor)
            b = int(b1 + (b2 - b1) * factor)

            return f"#{r:02x}{g:02x}{b:02x}"

        return interpolate_color(color1, color2, section_pos)

    def __call__(self, _, __, event_dict):
        """structlog处理器调用接口"""
        # 获取消息文本
        message = event_dict.pop("event", "")
        log_level = event_dict.pop("level", "info").upper()

        # 创建带渐变的文本
        width = len(message)
        height = 1

        # 创建文本对象
        text = Text()

        # 为每个字符应用渐变色
        for i, char in enumerate(message):
            color = self.get_color_at_position(i, 0, width, height)
            text.append(char, Style(color=color))

        # 添加其他日志字段
        for key, value in event_dict.items():
            text.append(f" {key}={value}")

        # 输出到控制台
        self.console.print(text)

        # 返回空字符串，因为我们已经通过rich直接打印了
        return ""


# 配置Rich处理器
rich_handler = RichHandler(rich_tracebacks=True, markup=True, tracebacks_show_locals=True)

# 配置logging
logging.basicConfig(level=logging.INFO, format="%(message)s", datefmt="[%X]", handlers=[rich_handler])

# 配置structlog
structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        GradientLogRenderer(colors=["#0066ff", "#00ccff", "#00ffcc", "#00ff66", "#66ff00"], direction="diagonal"),
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

# 使用示例
logger = structlog.get_logger()

logger.info("这是一条带有斜向渐变色的日志信息")
logger.warning("警告信息也会有漂亮的渐变色效果")
logger.error("错误信息同样支持渐变色显示", extra_field="附加信息")

# 带有结构化数据的日志
logger.info("用户登录成功", user_id=123, ip="192.168.1.1", status="success")
