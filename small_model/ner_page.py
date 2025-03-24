import os
import re

os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
import streamlit as st

from small_model.entities_extract import ner

st.set_page_config(page_title="Named Entity Recognition", page_icon="👀", layout="wide")


def main():
    st.title("命名实体识别（NER）")

    # 输入
    entity_text = st.text_input("请输入想要识别的实体类型(以英文逗号或者中文逗号分隔)")
    text = st.text_area("请输入要进行命名实体识别的文本", "在2024年6月的晚上，约翰·史密斯在纽约的中央公园散步。")
    threshold = st.sidebar.slider("阈值", 0.0, 1.0, 0.5, 0.01)

    if st.button("识别实体"):
        if not entity_text or not text:
            st.warning("请输入实体类型和文本")
        else:
            with st.spinner("Running..."):
                entity_type = re.split(r"[,，]", entity_text)
                # ner = MultiNER()
                entities = ner(text=text, labels=entity_type, threshold=threshold)

                if entities:
                    unique_texts = set()
                    unique_labels = set()
                    col1, col2 = st.columns(2)
                    with col1:
                        st.subheader("实体")
                    with col2:
                        st.subheader("实体类别")
                    for entity in entities:
                        entity_t = entity["text"]
                        entity_label = entity["label"]
                        if entity_t not in unique_texts:
                            # Add entity text to unique set
                            unique_texts.add(entity_t)
                            unique_labels.add(entity_label)
                            with col1:
                                st.write(entity_t)
                            with col2:
                                st.write(entity_label)
                    st.success(f"识别到的实体类型为： {unique_labels}")
                else:
                    st.warning(f"未识别到类型: {entity_type} 的实体。")


if __name__ == "__main__":
    main()
