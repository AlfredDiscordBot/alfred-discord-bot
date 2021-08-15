import requests
import traceback
import json
from typing import List, Dict, Union


class CodeExecutor:
    """
    Base class for code executing utilities.
    """

    def __init__(self) -> None:
        self.runtimes = self.get_runtimes()

    @staticmethod
    def get_runtimes() -> List[Dict[str, Union[str, List[str]]]]:
        """
        Returns a list of all available runtimes in the piston api.
        """
        try:
            runtime_url = "https://emkc.org/api/v2/piston/runtimes"
            r = requests.get(runtime_url)
            data = json.loads(r.text)
            runtimes: List[Dict[str, Union[str, List[str]]]] = []
            for langs in data:
                runtimes.append({
                    "language": langs["language"],
                    "version": langs["version"],
                    "aliases": [i for i in langs["aliases"]]
                })

            return runtimes

        except Exception as e:
            traceback.print_exc(e)

    def execute_code(self, language: str, version: str = "latest", files: List[Dict[str, str]] = []) -> str:
        """
        Executes the given code in the given language and version.
        """
        try:
            execute_url = "https://emkc.org/api/v2/piston/execute"

            if language not in [lang["language"] for lang in self.runtimes]:
                return f"Language {language} is not supported."

            if version == "latest":
                for runtime in self.runtimes:
                    if runtime["language"] == language:
                        version = runtime["version"]
                        break
                else:
                    return f"No version found for language {language}"

            payload = {
                "language": language,
                "version": version,
                "files": files
            }

            resp = requests.post(execute_url, json=payload)

            if resp.status_code == 200:
                data = json.loads(resp.text)

                run_data = data["run"]

                return f'''
Status Code: {run_data["code"]}

Output:
```
{run_data["output"]}
```
                '''

            else:
                return f"Error: {resp.status_code}"

        except Exception as e:
            traceback.print_exc(e)
            return "Couldn't connect at the moment."


if __name__ == "__main__":
    rce = CodeExecutor()
    print(rce.runtimes)
    # print(rce.execute_code(
    #     language="python", version="latest", files=[{"name": "prog.py", "content":"print('hello)"}]))
