import re
text = 'Keep this <think>delete this</think> and this'
cleaned = re.sub(r'<think>.*?</think>', '', text)
# Result: 'Keep this  and this'
print(cleaned)