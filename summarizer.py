
import torch
from transformers import pipeline


class TextSummarizer:

    def __init__(self):
        self.model_name = "sshleifer/distilbart-cnn-12-6"

        # Select CPU or GPU automatically
        self.device = 0 if torch.cuda.is_available() else -1

        print("Loading AI Summarization Model...")

        self.summarizer = pipeline(
            "summarization",
            model=self.model_name,
            device=self.device
        )

        print("AI Model Loaded Successfully!")

    def summarize(self, text, summary_length="medium"):

        if not text or not text.strip():
            return "Please enter some text to summarize."

        # Configure summary length
        length_settings = {
            "short": {"max_length": 60, "min_length": 20},
            "medium": {"max_length": 120, "min_length": 40},
            "long": {"max_length": 180, "min_length": 70}
        }

        settings = length_settings.get(
            summary_length.lower(),
            length_settings["medium"]
        )

        # Model input limit
        input_text = text.strip()

        # Generate summary
        result = self.summarizer(
            input_text,
            max_length=settings["max_length"],
            min_length=settings["min_length"],
            do_sample=False,
            truncation=True
        )

        return result[0]["summary_text"]
