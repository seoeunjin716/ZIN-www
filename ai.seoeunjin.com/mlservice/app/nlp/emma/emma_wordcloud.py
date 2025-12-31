from __future__ import annotations

import pathlib
from typing import Iterable, List, Optional

import nltk
from nltk import FreqDist
from nltk.tag import pos_tag
from nltk.tokenize import RegexpTokenizer
from wordcloud import WordCloud


class EmmaWordCloud:
    """
    Generate a word cloud from the Gutenberg "Emma" corpus.

    The class downloads required NLTK resources on first use and
    produces a word cloud image file based on proper nouns frequency.
    """

    def __init__(
        self,
        font_path: Optional[str] = None,
        stopwords: Optional[Iterable[str]] = None,
    ) -> None:
        self.font_path = font_path
        default_stopwords = {"Mr.", "Mrs.", "Miss", "Mr", "Mrs", "Dear"}
        self.stopwords = set(stopwords) if stopwords is not None else default_stopwords
        self._tokenizer = RegexpTokenizer(r"[\w]+")

    def _ensure_resources(self) -> None:
        """Download required NLTK resources if missing."""
        nltk.download("gutenberg", quiet=True)
        nltk.download("punkt", quiet=True)
        # Newer NLTK uses averaged_perceptron_tagger_eng; keep legacy name as fallback.
        nltk.download("averaged_perceptron_tagger", quiet=True)
        nltk.download("averaged_perceptron_tagger_eng", quiet=True)

    def _load_raw_text(self) -> str:
        from nltk.corpus import gutenberg

        return gutenberg.raw("austen-emma.txt")

    def _extract_proper_nouns(self, text: str) -> List[str]:
        tokens = self._tokenizer.tokenize(text)
        tagged = pos_tag(tokens)
        return [
            token
            for token, tag in tagged
            if tag == "NNP" and token not in self.stopwords
        ]

    def _freq_dist(self, tokens: List[str]) -> FreqDist:
        return FreqDist(tokens)

    def generate(
        self,
        output_path: str,
        width: int = 1000,
        height: int = 600,
        background_color: str = "white",
        random_state: int = 0,
    ) -> pathlib.Path:
        """
        Generate a word cloud image and save it to output_path.

        Returns the saved pathlib.Path.
        """
        self._ensure_resources()
        raw_text = self._load_raw_text()
        proper_nouns = self._extract_proper_nouns(raw_text)
        freq = self._freq_dist(proper_nouns)

        wc = WordCloud(
            width=width,
            height=height,
            background_color=background_color,
            random_state=random_state,
            font_path=self.font_path,
        ).generate_from_frequencies(freq)

        output = pathlib.Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        wc.to_file(str(output))
        return output


if __name__ == "__main__":
    generator = EmmaWordCloud(font_path=None)
    saved_path = generator.generate("emma_wordcloud.png")
    print(f"Word cloud saved to: {saved_path.resolve()}")
