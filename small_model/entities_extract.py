import os

from gliner import GLiNER
from transformers import DebertaV2Tokenizer

os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"


class MultiNER:
    def __init__(
        self,
        labels: list = ["人名", "时间", "地名"],
        map_location: str = "cpu",
        model_name: str = "urchade/gliner_multi-v2.1",
        tokenizer_model: str = "microsoft/mdeberta-v3-base",
    ):
        # Initialize GLiNER with the base model
        self.tokenizer: DebertaV2Tokenizer = DebertaV2Tokenizer.from_pretrained(tokenizer_model)
        self.model = GLiNER.from_pretrained(model_name, map_location=map_location)
        self.labels = labels

    def __call__(self, text: str, labels: list = None, threshold: float = 0.5):
        return self.predict(text, labels, threshold)

    def to_batch(self, text: str, max_length: int = 380, batch_size: int = 16) -> list:
        tokens = self.tokenizer.tokenize(text)
        # 以['。', '.', '\n']切分句子
        sentence_boundaries = [i for i, token in enumerate(tokens) if token in ["。", ".", "\n"]]
        if not sentence_boundaries or sentence_boundaries[-1] != len(tokens) - 1:
            sentence_boundaries.append(len(tokens) - 1)

        sentences = []
        last_index = 0
        for boundary in sentence_boundaries:
            if boundary - last_index + 1 <= max_length:
                sen = " ".join(tokens[last_index : boundary + 1])
                sentences.append(sen)
            else:
                # 如果句子太长，则分割
                current = last_index
                while current <= boundary:
                    end = min(current + max_length - 1, boundary)
                    sen = " ".join(tokens[current : end + 1])
                    sentences.append(sen)
                    current = end + 1
            last_index = boundary + 1

        # 将句子分批
        final_batches = []
        for i in range(0, len(sentences), batch_size):
            final_batches.append(sentences[i : i + batch_size])

        return final_batches

    def predict(
        self, text: str, labels: list = None, threshold: float = 0.5, batch_size: int = 16, max_length: int = 380
    ) -> list:
        if labels:
            self.labels = labels
        bcts = self.to_batch(text=text, max_length=max_length, batch_size=batch_size)
        entities_l = []
        for bct in bcts:
            bct_entities = self.model.batch_predict_entities(bct, self.labels, threshold=threshold)
            for sentence in bct_entities:
                for ent in sentence:
                    ent["text"] = ent["text"].replace(" ", "")
                    if ent["text"] not in self.labels:
                        entities_l.append(ent)
        return entities_l


ner = MultiNER(map_location="cpu")

# 示例使用
if __name__ == "__main__":
    # 模拟数据
    sample_text = """
    张三于2023年5月1日前往北京参加会议。
    会上，李四提到他们计划在上海建立新的研发中心。
    王五则表示，他将于下周一前往广州考察市场。
    """

    # 提取命名实体
    results = ner(sample_text)

    # 打印结果
    print("提取的实体：")
    for entity in results:
        print(f"类型: {entity['label']}, 文本: {entity['text']}, 置信度: {entity['score']:.4f}")
