from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from langchain_openai import ChatOpenAI

from report_and_deck_creator_flow.types import Slide, DeckSection

@CrewBase
class SlideDeckSectionBuilderCrew():
    """SlideDeckSectionBuilderCrew crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    llm = ChatOpenAI(model="gpt-4o-mini")

    @agent
    def deck_section_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['deck_section_writer'],
            llm=self.llm,
            verbose=True
        )

    @task
    def section_writer_task(self) -> Task:
        return Task(
            config=self.tasks_config['deck_section_writer_task'],
            output_pydantic=DeckSection
        )

    @crew
    def crew(self) -> Crew:
        """Creates the SlideDeckSectionBuilderCrew crew"""

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
