import datasets
from llama_index.core.schema import Document
import colorama
from llama_index.core.tools import FunctionTool
from llama_index.retrievers.bm25 import BM25Retriever


class Retriever():
    def __init__(self, confirm_load=False):
        '''
            Ingests the Guestbook for the Gala and supports the exporting of the FunctionalTool for an AgentWorkFlow to leverage
            
            This class handles the detailed logic.
        
            Details:
                leverages the BM25Retriever due to it's ability search without pre-embedding Documents
        '''
        self.confirm_load = confirm_load
        self.guest_book = self.load_guest_dataset(confirm_load)
        self.bm25_retriever = BM25Retriever.from_defaults(nodes=self.guest_book)
        # returns this as an accessible tool for AgentWorkFlows
        self.guest_info_tool = FunctionTool.from_defaults(self.get_guest_info)
    
    
    def load_guest_dataset(self, confirm_load=False) -> list[Document]:
        '''
            loads the guest dataset for the gala and returns the guestbook as a list of Document
            
            Args:
                confirm_load (bool): boolean value that controls the printed output of each appended guest
            
            Returns:
                docs (list[Document]): returns the Document object for each guest invited to the gala
        '''
        guest_dataset = datasets.load_dataset("agents-course/unit3-invitees", split="train")
        
        docs = [
            Document(
                text="\n".join([
                    f"Name: {guest_dataset['name'][i]}",
                    f"Relation: {guest_dataset['relation'][i]}",
                    f"Description: {guest_dataset['description'][i]}",
                    f"Email: {guest_dataset['email'][i]}",
                ]),
                metadata={"name": guest_dataset['name'][i]}
            ) for i in range(len(guest_dataset))
        ]
        
        
        if confirm_load:
            
            for guest in docs:
                print(colorama.Fore.GREEN + f"✅ Added Guest: {guest.metadata}")
                
        
        return docs
                
    def get_guest_info(self, query: str) -> str:
        '''
            queries the `bm25_retriever` to determine if the user given in the query
            exists in the guest_book
            
            Args:
                query (str): string of the name, description or email or relationship of the guest to Mr. Wayne
            Returns:
                response (str): a string response that will indicate if the user(s) exist in the guest_book.
        '''
        found_results = self.bm25_retriever.retrieve(query)
        
        if found_results:
            return "/n/n".join([doc.text for doc in found_results[:3]])
        else:
            return "No matching results in the guest book"
