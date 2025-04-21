#!/usr/bin/env python
from random import randint

from pydantic import BaseModel

from crewai.flow import Flow, listen, start

from typing import List
from .types import ReportOutline, ReportSection, ReportSectionOutline, DeckSection, Slide, Deck

from .crews.outline_report_crew.outline_report_crew import OutlineReportCrew
from .crews.slide_deck_builder_crew.slide_deck_builder_crew import SlideDeckBuilderCrew
from .crews.slide_deck_section_builder_crew.slide_deck_section_builder_crew import SlideDeckSectionBuilderCrew
from .crews.write_report_section_crew.write_report_section_crew import WriteReportSectionCrew

from  .slides_lib import slides

import subprocess

class ReportDeckState(BaseModel):

    title: str = (
        "The application of mermaid diagrams"
    )
    topic: str = (
        "using mermaid diagrams to enhance software documentation"
    )
    goal: str = """
        The goal of this report is to provide a comprehensive overview of using mermaid diagrams to communicate charts, flows and state trasitions in software documentation.
    """
    section_count : str = "4"
    section_length: str = "1000"
    report: List[ReportSection] = []
    report_outline: ReportOutline = []
    deck_sections: List[DeckSection] = []
    deck : Deck = None



class ReportDeckFlow(Flow[ReportDeckState]):

    @start()
    def generate_report_outline(self):
        print("# Flow: generate_report_outline")
        output = (
            OutlineReportCrew()
            .crew()
            .kickoff(inputs={
                "topic": self.state.topic, 
                "goal": self.state.goal,
                "section_count": self.state.section_count,
                "section_length": self.state.section_length
            })
        )

        self.state.report_outline = output["sections"]

        print("# Flow: generate_report_outline DONE")


    @listen(generate_report_outline)
    def write_sections(self):
        print("# Flow: Writing Report Sections")

        #section_outline = self.state.report_outline[1]
        for section_outline in self.state.report_outline:
            print("# Flow: Writing Report Section '" + section_outline.title + "'")

            output = (
                WriteReportSectionCrew()
                .crew()
                .kickoff(
                    inputs={
                        "goal": self.state.goal,
                        "topic": self.state.topic,
                        "section_length": self.state.section_length,
                        "section_title": section_outline.title,
                        "section_description": section_outline.description,
                        "report_outline": [
                            section_outline.model_dump_json()
                            for section_outline in self.state.report_outline
                        ],
                    }
                )
            )

            section = ReportSection(title=output["title"], content=output["content"])
            self.state.report.append(section)

            print("# Flow: Writing Report Section DONE '" + section_outline.title + "'")


    @listen(write_sections)
    def compile_report(self):
        print("# Flow: Compiling Report Sections")

        # compile sections
        report_content = ""
        for section in self.state.report:
            # Add the section title as an # heading
            report_content += f"# {section.title}\n\n"
            # Add the section content
            report_content += f"{section.content}\n\n"
    
        # generate file_name .md 
        filename = f"./{self.state.title.replace(' ', '_')}.md"
    
        # Save the combined content into the file
        with open(filename, "w", encoding="utf-8") as file:
            file.write(report_content)
    
        print(f"# Flow: Report saved as {filename}")


    @listen(write_sections)
    def build_slide_deck(self):
        print("# Flow: build_slide_deck")

        output = (
            SlideDeckBuilderCrew()
            .crew()
            .kickoff(
                inputs={
                    "topic": self.state.topic,
                    "presentation_outline": [
                        section_outline.model_dump_json()
                        for section_outline in self.state.report_outline
                    ],
                }
            )
        )

        self.state.deck = Deck(
            introduction_title=output["introduction_title"], 
            introduction_subtitle=output["introduction_subtitle"], 
            introduction_presenter_notes=output["introduction_presenter_notes"], 
            agenda_presenter_notes=output["agenda_presenter_notes"], 
            conclusion_title=output["conclusion_title"], 
            conclusion_subtitle=output["conclusion_subtitle"], 
            conclusion_presenter_notes=output["conclusion_presenter_notes"]
        )

        print("# Flow: build_slide_deck DONE")


    @listen(build_slide_deck)
    def build_slide_deck_sections(self):
        print("# Flow: build_slide_deck_sections")

        for section in self.state.report:

            output = (
                SlideDeckSectionBuilderCrew()
                .crew()
                .kickoff(
                    inputs={
                        "goal": self.state.goal,
                        "topic": self.state.topic,
                        "section_title": section.title,
                        "section_text": section.content,
                        "presentation_outline": [
                            section_outline.model_dump_json()
                            for section_outline in self.state.report_outline
                        ],
                    }
                )
            )

            section = DeckSection(section_title=output["section_title"], section_presenter_notes=output["section_presenter_notes"], slides=output["slides"])
            self.state.deck_sections.append(section)
            
            print("# Flow: build_slide_deck_sections DONE")


    @listen(build_slide_deck)
    def output_slide_deck(self):
        print("# Flow: output_slide_deck")

        print("> TITLE title='"+ self.state.deck.introduction_title+"', subtitle'"+ self.state.deck.introduction_subtitle+"', notes='"+ self.state.deck.introduction_presenter_notes + "'")
        slides.add_title(self.state.deck.introduction_title, self.state.deck.introduction_subtitle, self.state.deck.introduction_presenter_notes)

        agenda_list = ""
        for section in self.state.deck_sections:
            agenda_list = agenda_list + section.section_title + "\n"
        print("> AGENDA title='"+ self.state.deck.introduction_title + "', notes='"+ self.state.deck.agenda_presenter_notes)
        slides.add_agenda(self.state.deck.introduction_title,agenda_list, self.state.deck.agenda_presenter_notes)

        for section in self.state.deck_sections:
            print("> SECTION title='"+ section.section_title + "', notes='"+ section.section_presenter_notes)
            slides.add_section(section.section_title,section.section_presenter_notes)

            for slide in section.slides:
                print(">> SLIDE title='" + slide.title + "', type='" + slide.type + "',content='" + slide.content + "', notes='" + slide.presenter_notes + "'")
                if slide.type == "bullets" and slide.content.count('\n') > 0:    # TODO and the \n > 0 
                    slides.add_bullets(slide.title, slide.content, slide.presenter_notes)
                elif slide.type == "diagram":
                    inputfile = open("input.mmd", "w")
                    inputfile.write(slide.content)
                    inputfile.close()
                    try:
                        p = subprocess.run('mmdc -i input.mmd -o output.png -t dark -b transparent -p ./puppeteer-config.json -s 5', shell=True, check=True, capture_output=True, encoding='utf-8')
                        slides.add_picture(slide.title, "output.png", slide.presenter_notes)
                    except Exception as e:
                        slides.add_text(slide.title, "ERROR PARSING:\n\n" + str(e) + "\n\n" + slide.content, slide.presenter_notes)
                else:
                    slides.add_text(slide.title, slide.content, slide.presenter_notes)

        print("> CLOSE title='"+ self.state.deck.conclusion_title + "', subtitle'"+ self.state.deck.conclusion_subtitle + "', notes='"+ self.state.deck.conclusion_presenter_notes + "'")
        slides.add_closing(self.state.deck.conclusion_title, self.state.deck.conclusion_subtitle, self.state.deck.conclusion_presenter_notes)
        
        # generate file_name .pptx 
        filename = f"./{self.state.title.replace(' ', '_')}.pptx"
        slides.save(filename)
        
        print("# Flow: output_slide_deck DONE")

def kickoff():
    report_deck_flow = ReportDeckFlow()
    report_deck_flow.kickoff()


def plot():
    report_deck_flow = ReportDeckFlow()
    report_deck_flow.plot()


if __name__ == "__main__":
    kickoff()
