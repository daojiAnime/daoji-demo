import os

from gliner import GLiNER
from transformers import DebertaV2Tokenizer

os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"


class MultiNER:
    def __init__(
        self,
        labels: list = ["人名", "时间", "地名"],
        map_location: str = "cuda:0",
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
        if sentence_boundaries[-1] != len(tokens):
            sentence_boundaries.append(len(tokens))
        sentences = []
        last_index = 0
        for boundary in sentence_boundaries:
            if boundary - last_index + 1 <= max_length:
                sen = " ".join(tokens[last_index : boundary + 1])
            else:
                if sen:
                    sentences.append(sen)
                    last_index = boundary + 1
        if sen:
            sentences.append(sen)
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
