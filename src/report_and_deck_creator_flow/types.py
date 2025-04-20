from typing import List

from pydantic import BaseModel

class ReportSectionOutline(BaseModel):
    title: str = ''
    description: str = ''

class ReportOutline(BaseModel):
    sections: List[ReportSectionOutline] = []

class ReportSection(BaseModel):
    title: str = ""
    content: str = ""

class Slide(BaseModel):
    title: str
    type: str
    content: str
    presenter_notes: str

class DeckSection(BaseModel):
    section_title: str
    section_presenter_notes: str
    slides: List[Slide]

class Deck(BaseModel):
    introduction_title: str
    introduction_subtitle: str
    introduction_presenter_notes: str
    agenda_presenter_notes: str
    conclusion_title: str
    conclusion_subtitle: str
    conclusion_presenter_notes: str