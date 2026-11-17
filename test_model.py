
from summarizer import TextSummarizer

# Initialize AI model
ai = TextSummarizer()

sample_text = """
Artificial Intelligence is transforming the modern world.
It is used in healthcare, education, transportation,
finance, and many other industries.

Machine learning is a subset of artificial intelligencer
that allows computers to learn patterns from data
without being explicitly programmed for every task.

Deep learning uses neural networks with multiple layers
to solve complex problems such as image recognition,
speech processing, and natural language understanding.

Generative AI is another important development that
can create new content such as text, images, audio,
and computer code.
"""

print("\nOriginal Text:\n")
print(sample_text)

print("\nGenerated Summary:\n")

summary = ai.summarize(sample_text, "medium")

print(summary)
