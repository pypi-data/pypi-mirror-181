import json
from copy import deepcopy
from pathlib import Path

from pymultirole_plugins.v1.schema import Document, DocumentList

from pyprocessors_readinggrid.readinggrid import (
    ReadingGridProcessor,
    ReadingGridParameters,
)


def test_readinggrid():
    testdir = Path(__file__).parent / "data"
    json_file = testdir / "french.json"
    with json_file.open("r") as fin:
        doc = json.load(fin)
    doc = Document(**doc)
    nb_sents = len(doc.sentences)
    nb_annots = len(doc.annotations)
    parameters = ReadingGridParameters(separator="\u22ee")
    formatter = ReadingGridProcessor()
    docs = formatter.process([deepcopy(doc)], parameters)
    assert len(docs[0].sentences) < nb_sents
    assert len(docs[0].annotations) == nb_annots
    for sent in docs[0].sentences:
        stext = docs[0].text[sent.start : sent.end]
        assert "pas" not in stext
    sum_file = testdir / "french_grid.json"
    dl = DocumentList(__root__=docs)
    with sum_file.open("w") as fout:
        print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)

    parameters = ReadingGridParameters(
        separator="\u22ee", as_altText="Grille de lecture"
    )
    docs = formatter.process([deepcopy(doc)], parameters)
    assert len(docs[0].sentences) == nb_sents
    assert len(docs[0].annotations) == nb_annots
    assert len(docs[0].text) > len(docs[0].altTexts[0].text)
    assert "pas" not in docs[0].altTexts[0].text
    sum_file = testdir / "french_grid_alt.json"
    dl = DocumentList(__root__=docs)
    with sum_file.open("w") as fout:
        print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)
