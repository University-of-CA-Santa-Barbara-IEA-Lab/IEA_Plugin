# IEA-Plugin Repository
by Seoyeon Kim and Yu Su

This repository contains additional experiment data that we were not able to include in the IEA-Plugin paper PDF, due to space limitation.

We will upload the LangGraph code for IEA-Plugin AI agent workflow reasoner here during our Spring quarter (April - June). In the Spring quarter 2025, we are teaching a new course at UCSB titled "AI Agents for Semiconductor Industry" and our IEA-Plugin code will serve as a platform to derive homework assignments for the students. After we re-organize the IEA-Plugin code and make the homework assignments, we will release the organized IEA-Plugin code.

Currently, we do not have the permission to upload the code for the Data agent, due to its connection to the database whose schema is confidential to Qualcomm. We are working on building a separate graph database using public data. When that is done, we will release the code for the Data agent here. We expect this can be resolved before the ITC event time.

## Folder Structure

The folder is structured according to the paper organization:

- `README.md` -- this file
- `IEA-Plugin Paper 2025.pdf` -- the paper

### Section 2 Queries
- Prompt (to GPT-4o)
- Dataset of original 80 generated queries
- Dataset of additional 40 generated queries
- 1.5 page Scope Description

### Section 3 Workflows
- Prompt P[+4] (to GPT-o3-mini)
- Dataset of generated workflows for original 80 queries
- Dataset of generated workflows for additional 40 queries

### Section 4 APIs
- Instruction Classification Promt (to GPT-4o)
- API Generation Prompt (to GPT-o3-mini-high)
- (from the query-workflow pairs of the original 80 queries)
- Generated API Spec by GPT-o3-mini-high for Analysis category
- Generated API Spec by GPT-o3-mini-high for Output category

