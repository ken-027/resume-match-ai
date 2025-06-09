from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class ResumeMatchAi():
    """ResumeMatchAi crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def resume_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['resume_analyst'], # type: ignore[index]
            verbose=True
        )

    @agent
    def job_scraper(self) -> Agent:
        return Agent(
            config=self.agents_config['job_scraper'], # type: ignore[index]
            verbose=True
        )

    @agent
    def matchmaker(self) -> Agent:
        return Agent(
            config=self.agents_config['matchmaker'], # type: ignore[index]
            verbose=True
        )

    @agent
    def advisor(self) -> Agent:
        return Agent(
            config=self.agents_config['advisor'], # type: ignore[index]
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def resume_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['resume_analysis_task'], # type: ignore[index]
            output_file='output/analyst_report.md'
        )

    @task
    def job_scraping_task(self) -> Task:
        return Task(
            config=self.tasks_config['job_scraping_task'], # type: ignore[index]
            output_file='output/job_scraping_report.md'
        )

    @task
    def job_matching_task(self) -> Task:
        return Task(
            config=self.tasks_config['job_matching_task'], # type: ignore[index]
            output_file='output/job_matching_report.md'
        )

    @task
    def resume_advising_task(self) -> Task:
        return Task(
            config=self.tasks_config['resume_advising_task'], # type: ignore[index]
            output_file='output/resume_advising_report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the ResumeMatchAi crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
