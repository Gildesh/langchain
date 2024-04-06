from dotenv import load_dotenv
from langchain.agents import AgentType, initialize_agent
from langchain_experimental.agents import create_csv_agent
from langchain_experimental.agents.agent_toolkits import create_python_agent
from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool
from langchain_experimental.tools import PythonREPLTool
import qrcode, os
load_dotenv()

def main():
    print("Start...")
    python_agent_executor = create_python_agent(
        llm=ChatOpenAI(temperature=0, model="gpt-4"),
        tool=PythonREPLTool(),
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

   # python_agent_executor.run(
   #     """generate and save in current working directory 15 QRcodes
   #                             that point to www.udemy.com/course/langchain, you have qrcode package installed already, you have the os module imported already"""
    #)
    csv_agent = create_csv_agent(
        llm=ChatOpenAI(temperature=0, model="gpt-4"),
        path="episode_info.csv",
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    )

    #csv_agent.run("how many columns are there in file episode_info.csv")
    #csv_agent.run("print seasons ascending order of the number of episodes they have")    
    grand_agent = initialize_agent(
        tools=[
            Tool(
                name="PythonAgent",
                func=python_agent_executor.run,
                description="""useful when you need to transform natural language and write from it python and execute the python code,
                              returning the results of the code execution,
                            DO NOT SEND PYTHON CODE TO THIS TOOL""",
            ),
            Tool(
                name="CSVAgent",
                func=csv_agent.run,
                description="""useful when you need to answer question over episode_info.csv file,
                             takes an input the entire question and returns the answer after running pandas calculations""",
            ),
        ],
        llm=ChatOpenAI(temperature=0, model="gpt-4"),
        agent_type=AgentType.OPENAI_FUNCTIONS,
        verbose=True,
    )

    #grand_agent.run("""generate and save in current working directory 15 QRcodes that point to www.udemy.com/course/langchain, you have qrcode package installed already and you have the os module imported already. if the qrcode images are already there, delete them and save again.""")

    grand_agent.run("print seasons ascending order of the number of episodes they have")

if __name__ == "__main__":
    main()
