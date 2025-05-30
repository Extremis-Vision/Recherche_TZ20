import sys, os 

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Recherche.DeepSearch import DeepSearch
from Recherche.Keywords import question_expertsearch
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from typing import List, Optional

class ExpertSearch(DeepSearch):
    def get_research_question(self, question: str, context: str, NB_Question : int = 3 , language : str = "French"):
        parser = PydanticOutputParser(pydantic_object=question_expertsearch(NB_Question))

        system_prompt = f"""
            You are an intelligent AI research assistant. Your job is to help users clarify and deepen their research by generating three highly relevant, distinct research questions based on their initial query.

            **Instructions:**
            - Carefully analyze the user's question to understand their intent and the context.
            - Generate exactly three research questions that cover different possible research directions or levels of depth. For example: 
                - a broad overview,
                - a focused exploration of a specific aspect,
                - a deep dive into underlying mechanisms or implications.
            - Each question should be clear, concise, and directly related to the user's original query.
            - Do not ask for clarification or additional information; instead, anticipate what the user might want to know next.
            - Adapt the questions to the user's intent (e.g., general information, detailed analysis, practical application, comparison, etc.).
            - Respond only with the list of three questions, without any introduction or explanation.
            - Respond in {language}.
            - The context is {context}
            """

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", "{input}\n{format_instructions}")
        ])

        chain = prompt | self._get_model() | parser


        try:
            response = chain.invoke({
                "input": question,
                "format_instructions": parser.get_format_instructions(),
                "context" : context
            })
            return response
        
        except Exception as e:
            print(f"Erreur de parsing : {e}")
            return None

# Exemple utilisation 
#expert = ExpertSearch()
#resultat = expert.get_research_question("Qu'est ce que l'ia","Veut avoir des informations sur l'ia")
#print(resultat)
