
from langchain_core.prompts import ChatPromptTemplate
from LLMManger import LLMManager
from PineconeDBManager import PineconeDBManager
from typing import List
import re

class Reasoner:
    def __init__(self):
        self.llm_manager = LLMManager()
        self.PineconeDBManager = PineconeDBManager()
    
    def parse_response(self, text: str) -> dict:
        pattern = re.compile(
            r"Thought:\s*(.*?)\s*Workflow:\s*(.*?)\s*Output Message:\s*(.*)",
            re.DOTALL
        )
        match = pattern.search(text)
        if match:
            thought = match.group(1).strip()
            # Split the workflow steps into a list of strings
            workflow = match.group(2).strip().splitlines()
            output_message = match.group(3).strip()
            return {
                "thought": thought,
                "workflow": workflow,
                "output_message": output_message
            }
        else:
            raise ValueError("The provided text does not match the expected format.")

    def format_questions_workflows(self, data: list) -> str:
        formatted_str = ""
        for i, item in enumerate(data, start=1):
            formatted_str += f"### Example {i}\n"
            formatted_str += "User Instruction:\n"
            formatted_str += f"{item.get('question', '')}\n\n"
            
            formatted_str += "**Thought**:\n"
            formatted_str += f"{item.get('thought', '')}\n\n"
            
            formatted_str += "**Workflow**:\n"
            workflow = item.get("workflow", [])
            # If workflow is a list of steps, print each step on a new line.
            if isinstance(workflow, list):
                for step in workflow:
                    formatted_str += f"{step}\n"
            else:
                formatted_str += f"{workflow}\n"
            formatted_str += "\n"
            
            formatted_str += "**Output Message**:\n"
            formatted_str += f"{item.get('output_message', '')}\n\n"
        return formatted_str

    async def run(self, state: dict) -> dict:
        question = state["complete_user_query"]
        output = self.PineconeDBManager.retrieve_top_k_examples(question)
        examples = self.format_questions_workflows(output)
      
        prompt = ChatPromptTemplate.from_messages([
            ("system", '''You are a domain-specific **workflow** generator which takes a user instruction as input and generate a **workflow* as output. The domain is for analyzing yield based on test data collected from a semiconductor chip production line.  
A **workflow** contains a sequence of **Steps**. When you generate the **workflow**, please try to use **Steps** that are as simple and specific as possible. Also, before the **workflow**, please generate a **thought** process behind the workflow and an **output message** after the workflow. 
I'm building a domain-specific AI agent which take a user instruction as input and generate a workflow as output. The domain is for analyzing yield based on test data collected from a semiconductor chip production line. Below is the semiconductor test context. 
Context:
In semiconductor test, we collect test data, say weekly. Test data are organized as a table. The test process looks like this. Lets focus on wafer-level testing here. At wafer-level, tests are applied to one wafer at a time. When I say “tests”, I mean each test is like a test program. A test program applies one or more test measurements on every die (unpackaged chip) on the wafer. The application process is parallelized. A tester has a probe that can test NxN dies at the same time. For example, 12x12 at the same time. A wafer usually contains many more than NxN dies. Thus, the probe needs to touch the wafer one time, move to a different region, and touch the wafer again, and move to another region, and touch the wafer again, and so on.  
Each die is tested by a number of test programs. Each test program can contain many test measurements and hence, a large number of test measurements are applied.  
There are two types of test measurements: logical test and parametric test. A logical test results in a binary pass/fail outcome. A parametric test gives a value. Then, a test limit is applied to determine if this value is passing or failing. If a die fails any test measurement, it is considered as a failing die.  
There are two primary types of yields we are watching typically: lot-level yield and wafer-level yield. Yield can be calculated on every wafer. A lot contains 25 wafers collectively. Hence, a lot yield can be calculated for all wafers in the lot as well.  
Failure statistics are organized in terms of test bins. Usually we can have 50-100 test bins pre-defined. A test bin is defined according to a family of test measurements. A family means that those test measurements are similar, e.g. testing the same characteristics but on slightly different locations. Thus, we can consider each test bin represent a particular type of failure mode.  
Usually, a target yield at the lot level is set. For example, in a period of 3 months, we are expecting to see that lot yield is at or above 95%. If for a particular lot, its yield is below that, this raises a warning signal. But one lot might not be enough to trigger a concern. However, if we see the trend, such as based on consecutive lots, is going below 95%, then this is clearly a concern. When this happens, it should trigger further analysis and action trying to bring the yield back up.  
When we analyze a yield issue, the issue might be due to many reasons. Usually, we can check if the issue is due to an anomaly in the foundries, test house, testers, handler, prober, or load board in use. The test process may utilize multiple test house, each test house can have many testers, a tester might use a specific load board, and so on.  
In addition, we would like to know what kind of test measurement or test measurements is the main source for the yield issue. For example, we might find that the unexpected yield drop is due to a family of voltage measurements that intend to characterize some performance metric of the chip.  
On every wafer, a set of so-called E-tests are also measured. The set of E-test measurements is done at multiple sites on a wafer. Each E-test is an indicator of some health metric of the wafer coming out of the manufacturing process. Every E-test results in a value. There is no pass/fail on this value. The value just fluctuates from site to site slightly and can fluctuate more from wafer to wafer. Foundry can change a E-test value statistics by changing their manufacturing process.  
When we discover that a yield problem is due to a test measurement, for example, we can try to correlate the wafer-to-wafer statistics of this measurement to an E-test. If a high correlation can be found, then the yield problem might be fixable by asking the foundry to adjust their manufacturing process.   
When we analyze a yield issue, sometime the issue may manifest itself as an unusual wafer map pattern. For example, the failing dies form a cluster and concentrate on the upper-left region of the wafer. And if this pattern persistent across consecutive lots, then it is a clear indication that the yield issue is due to the manufacturing process.  
Sometime, we can also see wafer map pattern like a grid pattern. A grid pattern means that the dies failing map looks like a checker board, that for example, failures occur on every other 2 dies vertically and horizontally.  
There are other commonly known patterns, such as a edge-ring pattern where most of the dies located on the edge of wafer are failing and a center pattern where the cluster of failing dies concentrate on the center of the wafer, etc.  
{examples}
'''),
            ("human", """User Instruction: {question}
**Thought**:
**Workflow**:
**Output Message**:""")
        ])
        response = await self.llm_manager.invoke(prompt, question = question, examples = examples) 
        parsed_response = self.parse_response(response.content)
        return parsed_response