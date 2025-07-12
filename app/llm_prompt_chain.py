
from langchain_ollama.llms import OllamaLLM
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama 


class Llm_prompt:
    def __init__(option,article,self):
        self.MODEL = "llama3.2"
        self.model = OllamaLLM(model= self.MODEL)
        self.embeddings=OllamaEmbeddings(model=self.MODEL)
        self.option = option
        self.article = article

    
    
    def create_chain(self):

        parser = StrOutputParser()

        template_summery =  """
                    Make a summery in 120 words based in context below. If you can't make the summery, reply "I can't"
                    Context: {self.article}
                    """
        prompt_summery = PromptTemplate.from_template(template_summery)
        
        template_simplifier =  """ Analyze the context below, and simplify it in such a way that a 5 year old child can understand. If you can't, reply "I can't"
                    Context: {self.article}
                    """
        prompt_simplifier = PromptTemplate.from_template(template_simplifier)



        chain_summery = prompt_summery | self.model | parser



        chain_simplifer = prompt_simplifier | self.model | parser


        if (self.option == "Summerize"|"Summery"|"Shorten"):
            Summery = chain_summery.invoke({"article":self.article})
            return Summery
        elif(self.option == "Simplify"|"Explain"):
            Simplify = chain_simplifer.invoke({"article":self.article})
            return Simplify
    def run(self):
        self.create_chain()
if __name__ == "__main__":
    app = Llm_prompt()
    app.run()
