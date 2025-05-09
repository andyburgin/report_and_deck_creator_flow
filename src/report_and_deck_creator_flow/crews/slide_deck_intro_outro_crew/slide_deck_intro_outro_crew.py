from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from report_and_deck_creator_flow.types import Deck

@CrewBase
class SlideDeckIntroOutroCrew():
    """SlideDeckIntroOutroCrew crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def slide_deck_intro_outro_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['slide_deck_intro_outro_writer'],
            verbose=True
        )

    @task
    def slide_deck_intro_outro_writer_task(self) -> Task:
        return Task(
            config=self.tasks_config['slide_deck_intro_outro_writer_task'],
            output_pydantic=Deck
        )

    @crew
    def crew(self) -> Crew:
        """Creates the SlideDeckIntroOutroCrew crew"""

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
