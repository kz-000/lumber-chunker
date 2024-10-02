SYSTEM_PROMPT = """
Instruction:
'ID XXXX: <text>' という形式の段落の文章を提供します。
文章の内容が大きく変わる段落を検出し、その１つ前の段落を出力してください。

Output：
内容の転換する段落のIDを次の形式で出力してください：'Answer: ID XXXX'。
転換する段落がない場合は、最終行を出力してください。

Additional Considerations:
非常に長い段落のグループは避けてください。内容の変化を特定しつつ、グループを適度な長さに保つことを目指してください。
"""

HUMAN_PROMPT = """
Context: 
{context}

Answer:
"""
