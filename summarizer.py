
import re
import logging
from typing import List

import torch
from transformers import pipeline


# --------------------------------------------------
# LOGGING CONFIGURATION
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# --------------------------------------------------
# AI TEXT SUMMARIZER
# --------------------------------------------------

class TextSummarizer:

    def __init__(self):

        self.model_name = "sshleifer/distilbart-cnn-12-6"

        # Maximum safe input tokens per chunk
        self.max_input_tokens = 850

        # Overlap between chunks when splitting long sentences
        self.chunk_overlap = 40

        # Select available device
        self.device = 0 if torch.cuda.is_available() else -1

        logger.info("Loading AI Summarization Model...")

        try:

            self.summarizer = pipeline(
                task="summarization",
                model=self.model_name,
                device=self.device
            )

            self.tokenizer = self.summarizer.tokenizer

            logger.info("AI Model Loaded Successfully!")

            logger.info(
                "Running on: %s",
                "GPU" if self.device >= 0 else "CPU"
            )

        except Exception as error:

            logger.exception("Failed to load AI model.")

            raise RuntimeError(
                f"Unable to load summarization model: {error}"
            ) from error

    # --------------------------------------------------
    # TOKEN COUNT
    # --------------------------------------------------

    def count_tokens(self, text: str) -> int:

        return len(
            self.tokenizer.encode(
                text,
                add_special_tokens=True
            )
        )

    # --------------------------------------------------
    # CLEAN INPUT TEXT
    # --------------------------------------------------

    def clean_text(self, text: str) -> str:

        if not isinstance(text, str):
            raise TypeError("Input must be a string.")

        # Normalize whitespace
        text = re.sub(r"\s+", " ", text)

        return text.strip()

    # --------------------------------------------------
    # SPLIT LONG SENTENCES
    # --------------------------------------------------

    def split_long_sentence(
        self,
        sentence: str,
        max_tokens: int = None
    ) -> List[str]:

        max_tokens = max_tokens or self.max_input_tokens

        token_ids = self.tokenizer.encode(
            sentence,
            add_special_tokens=False
        )

        chunks = []

        start = 0

        while start < len(token_ids):

            end = min(
                start + max_tokens - 2,
                len(token_ids)
            )

            chunk_ids = token_ids[start:end]

            chunk = self.tokenizer.decode(
                chunk_ids,
                skip_special_tokens=True,
                clean_up_tokenization_spaces=True
            )

            if chunk.strip():
                chunks.append(chunk.strip())

            if end >= len(token_ids):
                break

            start = max(
                start + 1,
                end - self.chunk_overlap
            )

        return chunks

    # --------------------------------------------------
    # SPLIT TEXT INTO MANAGEABLE CHUNKS
    # --------------------------------------------------

    def split_text(
        self,
        text: str,
        max_tokens: int = None
    ) -> List[str]:

        max_tokens = max_tokens or self.max_input_tokens

        text = self.clean_text(text)

        if not text:
            return []

        # Split while preserving sentence punctuation
        sentences = re.split(
            r'(?<=[.!?])\s+',
            text
        )

        chunks = []

        current_chunk = ""

        for sentence in sentences:

            sentence = sentence.strip()

            if not sentence:
                continue

            # Handle sentences exceeding token limit
            if self.count_tokens(sentence) > max_tokens:

                if current_chunk:
                    chunks.append(current_chunk)
                    current_chunk = ""

                long_sentence_chunks = self.split_long_sentence(
                    sentence,
                    max_tokens
                )

                chunks.extend(long_sentence_chunks)

                continue

            candidate = (
                f"{current_chunk} {sentence}"
                if current_chunk
                else sentence
            )

            if self.count_tokens(candidate) <= max_tokens:

                current_chunk = candidate

            else:

                if current_chunk:
                    chunks.append(current_chunk)

                current_chunk = sentence

        if current_chunk:
            chunks.append(current_chunk)

        logger.info(
            "Text divided into %d chunks.",
            len(chunks)
        )

        return chunks

    # --------------------------------------------------
    # SUMMARY LENGTH CONFIGURATION
    # --------------------------------------------------

    def get_length_settings(
        self,
        summary_length: str
    ) -> dict:

        settings = {

            "short": {
                "max": 60,
                "min": 15
            },

            "medium": {
                "max": 110,
                "min": 25
            },

            "long": {
                "max": 180,
                "min": 40
            }

        }

        return settings.get(
            summary_length.lower(),
            settings["medium"]
        )

    # --------------------------------------------------
    # SUMMARIZE INDIVIDUAL CHUNK
    # --------------------------------------------------

    def summarize_chunk(
        self,
        text: str,
        summary_length: str = "medium"
    ) -> str:

        text = text.strip()

        if not text:
            return ""

        input_tokens = self.count_tokens(text)

        # Skip model generation for very small inputs
        if input_tokens < 15:
            return text

        settings = self.get_length_settings(
            summary_length
        )

        # Keep generated output proportional to input
        max_length = min(
            settings["max"],
            max(15, int(input_tokens * 0.75))
        )

        min_length = min(
            settings["min"],
            max(5, int(max_length * 0.35))
        )

        if min_length >= max_length:
            min_length = max(1, max_length // 2)

        try:

            result = self.summarizer(
                text,
                max_length=max_length,
                min_length=min_length,
                do_sample=False,
                truncation=True,
                num_beams=4,
                early_stopping=True
            )

            summary = result[0]["summary_text"]

            return summary.strip()

        except Exception as error:

            logger.exception("Chunk summarization failed.")

            raise RuntimeError(
                f"Unable to summarize text chunk: {error}"
            ) from error

    # --------------------------------------------------
    # COMPLETE TEXT SUMMARIZATION
    # --------------------------------------------------

    def summarize(
        self,
        text: str,
        summary_length: str = "medium"
    ) -> str:

        # Validate input
        if not text or not text.strip():
            return "Please enter some text to summarize."

        text = self.clean_text(text)

        summary_length = summary_length.lower()

        if summary_length not in ["short", "medium", "long"]:
            summary_length = "medium"

        logger.info(
            "Starting summarization. Length: %s",
            summary_length
        )

        try:

            # Step 1: Split original content
            chunks = self.split_text(text)

            if not chunks:
                return "No meaningful text found."

            # Step 2: Summarize each chunk
            summaries = []

            for index, chunk in enumerate(chunks, start=1):

                logger.info(
                    "Processing chunk %d of %d",
                    index,
                    len(chunks)
                )

                summary = self.summarize_chunk(
                    chunk,
                    summary_length
                )

                if summary:
                    summaries.append(summary)

            if not summaries:
                return "Unable to generate a summary."

            # Step 3: Combine chunk summaries
            final_summary = " ".join(summaries)

            # Step 4: Reduce large combined summaries
            # without exceeding the model's input limit

            max_iterations = 5
            iteration = 0

            while (
                self.count_tokens(final_summary) > self.max_input_tokens
                and iteration < max_iterations
            ):

                logger.info(
                    "Reducing combined summary. Pass %d",
                    iteration + 1
                )

                summary_chunks = self.split_text(
                    final_summary
                )

                reduced_summaries = []

                for chunk in summary_chunks:

                    reduced = self.summarize_chunk(
                        chunk,
                        summary_length
                    )

                    if reduced:
                        reduced_summaries.append(reduced)

                new_summary = " ".join(reduced_summaries)

                # Prevent infinite reduction loops
                if new_summary == final_summary:
                    break

                final_summary = new_summary

                iteration += 1

            logger.info("Summarization completed successfully.")

            return final_summary.strip()

        except Exception as error:

            logger.exception("Summarization process failed.")

            raise RuntimeError(
                f"Summarization failed: {error}"
            ) from error
    