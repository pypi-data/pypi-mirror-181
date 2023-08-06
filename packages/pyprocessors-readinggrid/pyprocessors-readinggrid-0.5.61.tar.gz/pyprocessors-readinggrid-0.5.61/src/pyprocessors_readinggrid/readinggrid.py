from typing import Type, List, cast
from collections_extended import RangeMap
from pydantic import BaseModel, Field
from pymultirole_plugins.v1.processor import ProcessorBase, ProcessorParameters
from pymultirole_plugins.v1.schema import Document, Sentence, AltText


class ReadingGridParameters(ProcessorParameters):
    separator: str = Field(
        "", description="Separator to append to the remaining sentences"
    )
    min_annotations: int = Field(
        1,
        description="The minimum number of annotations required to keep the sentence.",
    )
    as_altText: str = Field(
        None,
        description="""If defined generate the summary as an alternative text of the input document,
    if not replace the text of the input document.""",
    )


class ReadingGridProcessor(ProcessorBase):
    """ "A processor that generate a reduced/focussed version of the document keeping only the sentences
    that actually contain annotations.
    """

    def process(
        self, documents: List[Document], parameters: ProcessorParameters
    ) -> List[Document]:
        params: ReadingGridParameters = cast(ReadingGridParameters, parameters)
        for document in documents:
            sentences = []
            annotations = []
            start = 0
            text = ""
            separator = params.separator
            use_altText = params.as_altText is not None and len(params.as_altText) > 0
            if not separator.startswith("\n"):
                separator = "\n" + separator
            if not separator.endswith("\n"):
                separator = separator + "\n"
            if document.sentences is not None and document.annotations is not None:
                sentence_map = RangeMap()
                for s in document.sentences:
                    if s.end > s.start:
                        sentence_map[s.start : s.end] = []
                for a in document.annotations:
                    sentence_map[a.start].append(a)
                for sent in sentence_map.ranges():
                    ann_list = sent.value
                    if ann_list and len(ann_list) >= params.min_annotations:
                        sstart = start
                        send = sstart + (sent.stop - sent.start)
                        sentences.append(Sentence(start=sstart, end=send))
                        text += document.text[sent.start : sent.stop] + separator
                        if not use_altText:
                            for a in ann_list:
                                astart = a.start - sent.start
                                aend = a.end - sent.start
                                a.start = sstart + astart
                                a.end = sstart + aend
                                annotations.append(a)
                        start = len(text)
            if text.endswith(separator):
                text = text[: -len(separator)]
            if use_altText:
                document.altTexts = document.altTexts or []
                altTexts = [
                    alt for alt in document.altTexts if alt.name != params.as_altText
                ]
                altTexts.append(AltText(name=params.as_altText, text=text))
                document.altTexts = altTexts
            else:
                document.sentences = sentences
                document.annotations = annotations
                document.text = text
        return documents

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return ReadingGridParameters
