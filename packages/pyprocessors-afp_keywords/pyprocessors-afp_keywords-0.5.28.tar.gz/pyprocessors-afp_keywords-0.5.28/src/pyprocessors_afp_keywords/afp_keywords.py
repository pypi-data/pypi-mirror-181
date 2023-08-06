import os
from enum import Enum
from functools import lru_cache
from functools import partial
from pathlib import Path
from typing import List
from typing import Type, cast
from cytoolz import functoolz
from fasttext.FastText import _FastText, load_model
from pydantic import Field, BaseModel
from pymultirole_plugins.v1.processor import ProcessorBase, ProcessorParameters
from pymultirole_plugins.v1.schema import Document, Category, AltText
from textacy import preprocessing

_home = os.path.expanduser("~")
xdg_cache_home = os.environ.get("XDG_CACHE_HOME") or os.path.join(_home, ".cache")
MODELS_DIR = os.environ.get("MODELS_DIR", "models")


class AFPLang(str, Enum):
    fr = "fr"
    en = "en"
    de = "de"
    ar = "ar"


class AFPKeywordsParameters(ProcessorParameters):
    lang: AFPLang = Field(
        AFPLang.fr,
        description="""Which [afp_keywords](
                            https://github.com/thunlp/afp_keywords)  model to use.""",
    )
    number: int = Field(8, description="""Number of keywords to return.""")
    as_altText: str = Field(
        "slug",
        description="If defined, generate the slug as an alternative text of the input document.",
    )


class AFPKeywordsProcessor(ProcessorBase):
    """AFP keywords extractor."""

    def process(
        self, documents: List[Document], parameters: ProcessorParameters
    ) -> List[Document]:
        params: AFPKeywordsParameters = cast(AFPKeywordsParameters, parameters)

        m: _FastText = get_model(params.lang)
        preproc = get_preprocessor()
        for document in documents:
            document.categories = []
            text = preproc(document.text)
            labels, probs = m.predict(text, k=params.number)
            labels = [
                label[len("__label__"):]
                for label in labels
                if label.startswith("__label__")
            ]
            for label, prob in zip(labels, probs):
                document.categories.append(Category(label=label, score=prob))
                slug = "-".join(labels)
            if params.as_altText is not None and len(params.as_altText):
                document.altTexts = document.altTexts or []
                altTexts = [
                    alt for alt in document.altTexts if alt.name != params.as_altText
                ]
                altTexts.append(AltText(name=params.as_altText, text=slug))
                document.altTexts = altTexts
        return documents

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return AFPKeywordsParameters


@lru_cache(maxsize=None)
def get_model(lang):
    modeldir = Path(MODELS_DIR) / "fasttext" / lang.value
    model_file = modeldir / "slug.ftz"
    if model_file.exists():
        model = load_model(str(model_file))
    return model


@lru_cache(maxsize=None)
def get_preprocessor():
    LINEBREAK2SPACE = str.maketrans({"\n": " ", "\r": " "})
    preproc = functoolz.compose_left(
        preprocessing.normalize.normalize_unicode,
        lambda x: x.lower(),
        preprocessing.remove.remove_punctuation,
        preprocessing.normalize.normalize_whitespace,
        lambda x: x.translate(LINEBREAK2SPACE),
        partial(preprocessing.normalize.normalize_repeating_chars, chars=" "),
    )
    return preproc
