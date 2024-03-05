from dotenv import load_dotenv
import os
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from third_parties.linkedin import scrape_linkedin_profile
from agents import linkedin_lookup_agent, twitter_lookup_agent
import requests
from third_parties.twitter import scrape_user_tweets
from output_parsers import person_intel_parser, PersonIntel

#name = 'Abhay Saini'

def ice_break(name:str)->Tuple[PersonIntel,str]:
    ################## Dumbest Way ##################
    information = """Elon Reeve Musk (/ˈiːlɒn/; EE-lon; born June 28, 1971) is a businessman and investor. He is the founder, chairman, CEO, and CTO of SpaceX; angel investor, CEO, product architect and former chairman of Tesla, Inc.; owner, chairman and CTO of X Corp.; founder of the Boring Company and xAI; co-founder of Neuralink and OpenAI; and president of the Musk Foundation. He is the wealthiest person in the world, with an estimated net worth of US$232 billion as of December 2023, according to the Bloomberg Billionaires Index, and $254 billion according to Forbes, primarily from his ownership stakes in Tesla and SpaceX.[5][6]
    A member of the wealthy South African Musk family, Elon was born in Pretoria and briefly attended the University of Pretoria before immigrating to Canada at age 18, acquiring citizenship through his Canadian-born mother. Two years later, he matriculated at Queen's University at Kingston in Canada. Musk later transferred to the University of Pennsylvania, and received bachelor's degrees in economics and physics. He moved to California in 1995 to attend Stanford University. However, Musk dropped out after two days and, with his brother Kimbal, co-founded online city guide software company Zip2. The startup was acquired by Compaq for $307 million in 1999, and, that same year Musk co-founded X.com, a direct bank. X.com merged with Confinity in 2000 to form PayPal.
    In October 2002, eBay acquired PayPal for $1.5 billion, and that same year, with $100 million of the money he made, Musk founded SpaceX, a spaceflight services company. In 2004, he became an early investor in electric vehicle manufacturer Tesla Motors, Inc. (now Tesla, Inc.). He became its chairman and product architect, assuming the position of CEO in 2008. In 2006, Musk helped create SolarCity, a solar-energy company that was acquired by Tesla in 2016 and became Tesla Energy. In 2013, he proposed a hyperloop high-speed vactrain transportation system. In 2015, he co-founded OpenAI, a nonprofit artificial intelligence research company. The following year, Musk co-founded Neuralink—a neurotechnology company developing brain–computer interfaces—and the Boring Company, a tunnel construction company. In 2022, he acquired Twitter for $44 billion. He subsequently merged the company into newly created X Corp. and rebranded the service as X the following year. In March 2023, he founded xAI, an artificial intelligence company."""
    ################# Get linkedin url from SERPAPI ###########
    linkedin_profile_url = linkedin_lookup_agent.lookup(name=name)
    print(linkedin_profile_url)
    twitter_username = twitter_lookup_agent.lookup(name=name)
    print(twitter_username)
    ################## Expensive Way ##################
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_profile_url)
    tweets = scrape_user_tweets(username=twitter_username, num_tweets=5)
    ################## Best Way ########################
    gist_response = requests.get("https://gist.githubusercontent.com/Gildesh/0c70c783dcc1744b73cc39e756bc23f0/raw/897f2b4adba199c657916c52ac3e117ec11172a0/abhay.json")
    ################## Rest of the Code ################
    summary_template = """
        given the information about a person I want you to create:
        1. A short summary
        2. two interesting facts about them
        """
    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template)

    summary_template_mix = """
        given the linkedin information {linked_information} and twitter information (twitter_information) about a person I want you to create:
        1. A short summary
        2. two interesting facts about them
        3. A creative icebreaker to open a conversation with them
        4. a topic that may interest them
        \n{format_instructions)

        """
    summary_prompt_template_mix = PromptTemplate(
        input_variables=["linkedin_information", "twitter_information"], template=summary_template_mix, partial_variables={"format_instructions":peson_intel_parser.get_format_instructions})

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    #chain = LLMChain(llm=llm, prompt=summary_prompt_template)
    chain_mix = LLMChain(llm=llm, prompt=summary_prompt_template_mix)
    #print(chain.invoke(input={"information": gist_response.json()}))
    #print(chain.run(information=gist_response.json()))
    #print(chain_mix.run(linkedin_information = gist_response.json(), twitter_information=tweets))
    #print(chain_mix.invoke(input={"linkedin_information":gist_response.json(), "twitter_information":tweets}))
    #print(chain.run(information=linkedin_data))
    result = chain_mix.invoke(input={"linkedin_information":gist_response.json(), "twitter_information":tweets})
    return person_intel_parser.parse(result), linked_data.get("profile_pic_url")
if __name__ == "__main__":
    load_dotenv()
    name = 'Elon Musk'
    print("Hello world")
    ice_break(name)
