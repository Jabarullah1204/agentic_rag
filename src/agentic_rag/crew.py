from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource


@CrewBase
class AgenticRag():
    """Agentic RAG crew"""

    # Local Ollama LLM
    llm = LLM(
        model="ollama/qwen2.5:3b",
        base_url="http://localhost:11434"
    )

    # PDF Knowledge Base
    knowledge_source = PDFKnowledgeSource(
        file_paths=[
            "refund_policy.pdf",
            "shipping_policy.pdf",
            "warranty_policy.pdf"
        ]
    )

    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def query_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['query_analyzer'],
            llm=self.llm,
            verbose=True
        )

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            llm=self.llm,
            verbose=True
        )

    @agent
    def fact_checker(self) -> Agent:
        return Agent(
            config=self.agents_config['fact_checker'],
            llm=self.llm,
            verbose=True
        )

    @agent
    def answer_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['answer_generator'],
            llm=self.llm,
            verbose=True
        )

    @task
    def query_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['query_analysis_task'],
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],
        )

    @task
    def fact_check_task(self) -> Task:
        return Task(
            config=self.tasks_config['fact_check_task'],
        )

    @task
    def answer_generation_task(self) -> Task:
        return Task(
            config=self.tasks_config['answer_generation_task'],
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Agentic RAG crew"""

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,

            knowledge_sources=[
                self.knowledge_source
            ],

            embedder={
                "provider": "sentence-transformer",
                "config": {
                    "model_name": "all-MiniLM-L6-v2",
                    "device": "cpu",
                    "normalize_embeddings": False
                }
            },

            verbose=True,
        )