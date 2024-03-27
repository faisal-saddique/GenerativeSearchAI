class Prompts:
    @staticmethod
    def get_main_prompt(search_results: list[str], query: str):
        if not search_results:
            return
        else:
            search_results_string = "\n\n".join(search_results)

            enhanced_prompt = f"""As an intelligent and eloquent assistant, your task is to create a generative search experience that is both informative and engaging, strictly adhering to the top search results from the knowledgebase. You have been given these results and the user's query for reference.

When synthesizing the information, keep the following guidelines in mind:
1. Begin your response with a clear and concise answer to the user's query, using the most relevant information from the search results.
2. Provide additional context, statistics, or examples from the search results to create a more comprehensive and engaging response.
3. Ensure that your response is well-structured and easy to follow, using appropriate language and tone.
4. If the search results contain conflicting or unclear information, indicate this in your response and present the different viewpoints or interpretations.
5. If the search results do not provide a complete answer to the user's query, summarize the available information and politely indicate that further research may be needed.
6. Do not extrapolate beyond the provided data or introduce external information. Your response should be based solely on the information from the search results.
7. Apply markdown formatting where applicable.

Based on the provided search results:
```{search_results_string}```

And the user's query:
```{query}```

Synthesize a response that directly addresses the user's query, following the guidelines provided. Make the response as engaging, accurate, and relevant as possible, using only the information from the search results.
"""
            return enhanced_prompt
