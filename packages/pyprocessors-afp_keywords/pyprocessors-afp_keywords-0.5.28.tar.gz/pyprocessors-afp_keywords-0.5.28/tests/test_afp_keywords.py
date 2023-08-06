import json
import os
from pathlib import Path
from typing import List

os.environ["MODELS_DIR"] = os.path.join(os.path.dirname(__file__), "../models")
from pyprocessors_afp_keywords.afp_keywords import (
    AFPKeywordsParameters,
    AFPKeywordsProcessor,
)
from pymultirole_plugins.v1.schema import DocumentList, Document


def test_afp_keywords_fr():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/afp_doc_fr.json")
    source = Path(
        "/media/olivier/DATA/corpora/AFP/POC/CORPUS/Compléments/fr/batch8593.json"
    )
    parameters = AFPKeywordsParameters()
    annotator = AFPKeywordsProcessor()
    with source.open("r") as fin:
        jdocs = json.load(fin)
        docs: List[Document] = annotator.process(
            [Document(**jdoc) for jdoc in jdocs], parameters
        )
        for doc in docs:
            if "slug" in doc.metadata and doc.metadata["slug"]:
                print(f"{doc.metadata['slug']}\t{doc.altTexts[0].text}")
        result = Path(testdir, "data/afp_doc_fr_slug.json")
        dl = DocumentList(__root__=docs)
        with result.open("w") as fout:
            print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)


def test_afp_keywords_en():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/afp_doc_en.json")
    parameters = AFPKeywordsParameters(lang="en")
    annotator = AFPKeywordsProcessor()
    with source.open("r") as fin:
        jdocs = json.load(fin)
        docs: List[Document] = annotator.process(
            [Document(**jdoc) for jdoc in jdocs], parameters
        )
        result = Path(testdir, "data/afp_doc_en_slug.json")
        dl = DocumentList(__root__=docs)
        with result.open("w") as fout:
            print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)
