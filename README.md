# Setup
```bash
> git clone repository
> cd lumber_chunker
> pip install -e .
```


# How to use
```python
import sys
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from lumber_chunker import LumberChunker

AZURE_OPENAI_API_KEY = ""
AZURE_OPENAI_ENDPOINT = ""


text = """
日本の春は、美しい桜の花が咲き乱れる季節です。毎年3月から4月にかけて、全国各地で桜が満開になり、多くの人々が花見を楽しみに訪れます。公園や川沿い、神社の境内など、桜の名所にはシートを敷いてお弁当を広げる家族連れや、カメラを持った観光客の姿が見られます。
特に東京の上野公園や京都の哲学の道、福岡の舞鶴公園などは、桜の名所として有名です。これらの場所では、夜になるとライトアップされた桜が幻想的な雰囲気を醸し出し、昼間とはまた違った美しさを楽しむことができます。
しかし、桜の花は非常に短命で、満開の時期はわずか1週間ほど。その儚さが、桜の美しさを一層引き立てているのかもしれません。散り始めた桜の花びらが風に舞う様子は、まるで雪が降っているかのようで、多くの人々の心に深い感動を与えます。
このように、桜は日本の文化や風景に深く根付いており、春の訪れを告げる大切なシンボルとなっています。桜の季節が過ぎると、新緑の美しい夏がやってきますが、また来年も美しい桜の花を見られることを楽しみに、多くの人々が春の訪れを待ち望んでいます。
"""


llm = AzureChatOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    openai_api_key=AZURE_OPENAI_API_KEY,
    openai_api_version="2023-09-01-preview",
    deployment_name="gpt-4o-mini",
    model_name="gpt-4o-mini",
)

chunker = LumberChunker(llm, max_tokens=1500)
texts = chunker.split_text(text)

for text in texts:
    print(text + "\n")
```