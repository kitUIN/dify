import json
from typing import Any, Dict, List, Union

import requests

from core.tools.entities.tool_entities import ToolInvokeMessage
from core.tools.tool.builtin_tool import BuiltinTool


class SauceNAOSearchTool(BuiltinTool):
    def _invoke(self,
                user_id: str,
                tool_parameters: Dict[str, Any],
                ) -> Union[ToolInvokeMessage, List[ToolInvokeMessage]]:
        """
            invoke tools
        """
        query_url = tool_parameters['query_url']
        api_key = self.runtime.credentials['saucenao_api_key']
        params: dict[str, Any] = {
            "url": query_url,
            "output_type": 2,
        }
        if api_key is not None:
            params["api_key"] = api_key
        resp = requests.get("https://saucenao.com/search.php", params=params,
                            headers={
                                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"
                            })
        result = resp.json()["results"]
        return self.create_text_message(text=json.dumps(result, separators=(",", ":"), ensure_ascii=False))
