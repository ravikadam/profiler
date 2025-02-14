from tavily import TavilyClient
from typing import List, Dict, Any
import logging

class TavilySearcher:
    def __init__(self, api_key: str):
        self.client = TavilyClient(api_key=api_key)

    def search(self, query: str) -> Dict[str, Any]:
        try:
            # Perform search with topic extraction
            search_result = self.client.search(
                query=query,
                search_depth="advanced",
                include_answer=True,
                include_raw_content=True,
                max_results=5
            )
            
            # Extract and combine content
            combined_content = ""
            urls = []
            
            if search_result.get('answer'):
                combined_content += f"Summary: {search_result['answer']}\n\n"
            
            for result in search_result.get('results', []):
                urls.append(result.get('url', ''))
                if result.get('raw_content'):
                    combined_content += f"\nContent from {result['url']}:\n{result['raw_content']}\n"
                elif result.get('content'):
                    combined_content += f"\nContent from {result['url']}:\n{result['content']}\n"
            
            return {
                'content': combined_content,
                'urls': urls,
                'search_results': search_result
            }
            
        except Exception as e:
            logging.error(f"Error in Tavily search: {str(e)}")
            return {
                'content': '',
                'urls': [],
                'search_results': {}
            }