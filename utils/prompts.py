class Prompts:
    @staticmethod
    def get_main_prompt(search_results: list[str], query: str):
        if not search_results:
            return
        else:
            search_results_string = "\n\n".join(search_results)

            enhanced_prompt = f"""As an intelligent assistant, your task is to synthesize a search experience that is both informative and relevant, strictly adhering to the top search results from the knowledgebase. You have been given these results and the user's query for reference. 

            Based on the provided search results:
            {search_results_string}

            And the user's query:
            {query}

            Your response should be a concise, accurate synthesis of the information contained within the search results. Do not extrapolate beyond the provided data or introduce external information. Craft a response that directly addresses the user's query using only the information from the search results.
            """
            return enhanced_prompt