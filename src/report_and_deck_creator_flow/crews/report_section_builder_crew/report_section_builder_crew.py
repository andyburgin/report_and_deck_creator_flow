from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import EXASearchTool

import os

from report_and_deck_creator_flow.types import ReportSection


@CrewBase
class ReportSectionBuilderCrew():
    """ReportSectionBuilderCrew crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    @agent
    def researcher(self) -> Agent:
        search_tool = EXASearchTool(api_key=os.getenv("EXA_API_KEY"))

        return Agent(
            config=self.agents_config['researcher'],
            tools=[search_tool],
            verbose=True
        )

    @agent
    def writer(self) -> Agent:
        return Agent(
            config=self.agents_config['writer'],
            verbose=True
        )

    @task
    def research_report_section(self) -> Task:
        return Task(
            config=self.tasks_config['research_report_section'],
        )

    @task
    def write_report_section(self) -> Task:
        return Task(
            config=self.tasks_config['write_report_section'],
            output_pydantic=ReportSection
        )

    @crew
    def crew(self) -> Crew:
        """Creates the ReportSectionBuilderCrew crew"""

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
