# Internal AI Engineering Documentation (2026 Standards)

This document serves as the internal reference guide for integrating Generative AI components using best practices for 2026. Please adhere to these guidelines to ensure consistency, scalability, and maintainability across the codebase.

---

## 1. dotenv Configuration Loading

**Always** secure secrets and environment variables using `python-dotenv`. Hardcoded credentials will fail CI/CD security checks.

* **Install**: 
  ```bash
  pip install python-dotenv
  ```
* **Usage**:
  ```python
  import os
  from dotenv import load_dotenv

  # Best practice: override=True ensures .env variables take precedence over system vars during development
  load_dotenv(override=True)
  
  API_KEY = os.environ.get("GROQ_API_KEY")
  ```
* **Common Mistakes**: 
  * Committing `.env` to Git. (Ensure `.env` is in your `.gitignore`!)
  * Initializing API clients before calling `load_dotenv()`.

---

## 2. Groq API with LangChain

Use Groq for ultra-fast inference on open-source Llama models.

* **Install**:
  ```bash
  pip install langchain-groq
  ```
* **Migration Note**: Older projects might have used `from langchain_community.chat_models import ChatGroq`. Always use the dedicated integration package `langchain_groq` now.
* **Initialization & Recommended Model Usage**:
  ```python
  import os
  from langchain_groq import ChatGroq

  # Recommended fast, instruction-tuned reasoning model for 2026
  llm = ChatGroq(
      model="meta-llama/llama-4-scout-17b-16e-instruct",
      temperature=0.1, # Low temperature for structured/analytical tasks
      max_retries=3,
      api_key=os.environ.get("GROQ_API_KEY")
  )
  ```
* **Common Mistakes**: Instantiating custom API wrappers instead of using the LangChain-native `ChatGroq`.

---

## 3. LangChain: LCEL & Modern Syntax

We strictly use the LangChain Expression Language (LCEL) over legacy constructs.

* **Install**:
  ```bash
  pip install langchain langchain-core
  ```
* **Migration Notes**: 
  * `LLMChain` and `.run()` are **deprecated**. 
  * Avoid generic string-based `PromptTemplate` if passing roles (user/system); use `ChatPromptTemplate` instead.

* **PromptTemplate**:
  ```python
  from langchain_core.prompts import ChatPromptTemplate

  prompt = ChatPromptTemplate.from_messages([
      ("system", "You are an expert data analyst."),
      ("user", "Extract key metrics from: {text}")
  ])
  ```

* **Output Parsers**: Use specific parsers to process the raw `AIMessage`.
  ```python
  from langchain_core.output_parsers import StrOutputParser
  # Extracts just the string content from the LLM's response
  parser = StrOutputParser() 
  ```

* **LCEL, RunnableSequence, & .invoke()**: Use the `|` operator to pipe outputs.
  ```python
  # Creates a RunnableSequence
  chain = prompt | llm | parser 
  
  # Execution uses .invoke()
  result = chain.invoke({"text": "Revenue grew by 20% to $50M."})
  ```

* **Structured Outputs**: With robust model support in 2026, rely directly on `.with_structured_output()` and `pydantic`.
  ```python
  from typing import Optional
  from pydantic import BaseModel, Field

  class FinancialMetrics(BaseModel):
      revenue: Optional[int] = Field(None, description="Revenue in whole numbers")
      growth_percentage: float
  
  # Bind schema directly to the model
  structured_llm = llm.with_structured_output(FinancialMetrics)
  chain = prompt | structured_llm
  ```

* **Best Folder Architecture**:
  To prevent "spaghetti chains", structure your LangChain features as follows:
  ```text
  src/
  ├── core/               # config.py, llm_builder.py
  ├── chains/             # Specialized LCEL chains (e.g., summarize_chain.py)
  ├── prompts/            # Centralized prompt templates 
  ├── tools/              # Custom agent tools
  ├── schemas/            # Pydantic models for structured outputs
  └── utils/              # Helper functions (e.g., text splitters)
  ```

---

## 4. LangSmith: Observability & Tracing

Visibility into chain execution is mandatory for production tooling.

* **Environment Setup**: In your `.env` file, add:
  ```env
  LANGCHAIN_TRACING_V2=true
  LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
  LANGCHAIN_API_KEY="ls__..."
  LANGCHAIN_PROJECT="GenAI_Task_3_DEV"
  ```
* **Tracing**: When variables are set, tracing happens automatically. Do not write manual print statements for full trace debugging.
* **Tags**: Tag executions to filter runs by workload or prompt version:
  ```python
  chain.invoke(
      {"text": "Data"}, 
      config={"tags": ["v2-prompt", "finance-test"]}
  )
  ```
* **Debugging Runs**: Use the LangSmith dashboard to quickly identify latency bottlenecks and exact parameters failing output parsers.
* **Best Practices**:
  * Set different `LANGCHAIN_PROJECT` names for Dev vs. Prod environments.
  * Tag errors properly via exceptions to quickly isolate them in the dashboard.

---

## 5. Gradio: UI & Launchers

Gradio `Blocks` are designated for all complex tooling. We prefer fine-grained control over `gr.Interface`.

* **Install**:
  ```bash
  pip install gradio pandas
  ```
* **Layouts**: Use `Tabs` and specialized components like `File`, `Textbox`, and `Dataframe` for a premium UX.
  ```python
  import gradio as gr
  import pandas as pd

  def process_file(pdf_file):
      # Dummy function representing LCEL chain logic
      df = pd.DataFrame({"Entity": ["Acme Corp"], "Revenue": ["$50M"]})
      return "Successfully parsed file.", df

  with gr.Blocks(theme=gr.themes.Soft()) as demo:
      gr.Markdown("# GenAI Data Extractor")
      
      with gr.Tabs():
          with gr.Tab("Ingestion"):
              file_input = gr.File(label="Upload Contract", file_types=[".pdf"])
              submit_btn = gr.Button("Extract Data", variant="primary")
              status_out = gr.Textbox(label="Status", interactive=False)
              
          with gr.Tab("Results Table"):
              data_table = gr.Dataframe(headers=["Entity", "Revenue"], interactive=True)
              
      submit_btn.click(
          fn=process_file, 
          inputs=[file_input], 
          outputs=[status_out, data_table]
      )

  # Launch Patterns
  if __name__ == "__main__":
      # use share=False for security; 0.0.0.0 exposes to local network
      demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
  ```
* **Common Mistakes**: 
  * Passing a list of strings instead of a valid file path to file extractors in Gradio.
  * Setting `share=True` permanently in a corporate setting. (A security violation).

---

## 6. PDF Parsing Best Practices

* **Install**:
  ```bash
  pip install pypdf langchain-community pdfplumber
  ```
* **Choosing the Right Library**:
  * **`pypdf` (**`PyPDFLoader`**)**: Fast and standard choice for plain text. Lightweight.
    ```python
    from langchain_community.document_loaders import PyPDFLoader
    loader = PyPDFLoader("document.pdf")
    docs = loader.load()
    ```
  * **`pdfplumber` (**`PDFPlumberLoader`**)**: Best for complex layouts that include columns, borders, and structured tables. Avoids line-wrap breaks where possible.
    ```python
    from langchain_community.document_loaders import PDFPlumberLoader
    loader = PDFPlumberLoader("complex_financial_report.pdf")
    docs = loader.load()
    ```
* **Best Practices & Pipeline Rules**:
  * **Never text-dump raw PDFs to the LLM directly**: Always chunk the returned `docs` using a `RecursiveCharacterTextSplitter` before analyzing to respect Context Windows.
  * Retrieve metadata (`doc.metadata["page"]`) to enrich prompt context so AI knows which page it is observing.
  * **Common Mistakes**: Expecting parsed text data to inherently keep spatial table layout without specialized structure instructions or multi-modal models.
