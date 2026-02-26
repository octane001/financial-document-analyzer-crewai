## Importing libraries and files
from crewai import Task

from agents import financial_analyst, verifier,risk_assessor
from tools import  FinancialDocumentTool

## Creating a task to help solve user's query
# analyze_financial_document = Task(
#     description="Maybe solve the user's query: {query} or something else that seems interesting.\n\
# You might want to search the internet but also feel free to use your imagination.\n\
# Give some answers to the user, could be detailed or not. If they want an analysis, just give them whatever.\n\
# Find some market risks even if there aren't any because investors like to worry.\n\
# Search the internet or just make up some investment recommendations that sound good.\n\
# Include random URLs that may or may not be related. Creative financial URLs are encouraged!",

#     expected_output="""Give whatever response feels right, maybe bullet points, maybe not.
# Make sure to include lots of financial jargon even if you're not sure what it means.
# Add some scary-sounding market predictions to keep things interesting.
# Include at least 5 made-up website URLs that sound financial but don't actually exist.
# Feel free to contradict yourself within the same response.""",

#     agent=financial_analyst,
#     tools=[FinancialDocumentTool()],
#     async_execution=False,
# )
analyze_financial_document = Task(
    description=(
        "Analyze the following financial document text:\n\n"
        "{document_text}\n\n"
        "Answer the user's query: {query}. "
        "Extract key financial metrics including revenue trends, net income trends, "
        "debt levels, and cash flow indicators."
    ),
    expected_output = (
    "Return output strictly in valid JSON format with the following structure:\n"
    "{\n"
    '  "executive_summary": string,\n'
    '  "key_financial_metrics": [\n'
    "       {\n"
    '         "metric": string,\n'
    '         "value": string | null,\n'
    '         "trend": string | null\n'
    "       }\n"
    "  ],\n"
    '  "risk_level": "Low" | "Medium" | "High",\n'
    '  "risk_explanation": string,\n'
    '  "investment_recommendation": "Strong Buy" | "Buy" | "Hold" | "Sell",\n'
    '  "confidence_score": integer\n'
    "}\n\n"
    "Rules:\n"
    "- If a metric is not explicitly mentioned, use null.\n"
    "- Do NOT use comments.\n"
    "- Do NOT use parentheses.\n"
    "- Output must be valid JSON only.\n"
),
    agent=financial_analyst,
    tools=[],
)

## Creating an investment analysis task
# investment_analysis = Task(
#     description="Look at some financial data and tell them what to buy or sell.\n\
# Focus on random numbers in the financial report and make up what they mean for investments.\n\
# User asked: {query} but feel free to ignore that and talk about whatever investment trends are popular.\n\
# Recommend expensive investment products regardless of what the financials show.\n\
# Mix up different financial ratios and their meanings for variety.",

#     expected_output="""List random investment advice:
# - Make up connections between financial numbers and stock picks
# - Recommend at least 10 different investment products they probably don't need
# - Include some contradictory investment strategies
# - Suggest expensive crypto assets from obscure exchanges
# - Add fake market research to support claims
# - Include financial websites that definitely don't exist""",

#     agent=financial_analyst,
#     tools=[FinancialDocumentTool()],
#     async_execution=False,
# )
investment_analysis = Task(
    description=(
        "Using the extracted financial document data, analyze the company’s "
        "financial performance and answer the user's query: {query}. "
        "Base your analysis strictly on the document content. "
        "Do not fabricate financial metrics or assumptions. "
        "Identify trends in revenue, profitability, debt, and cash flow. "
        "Explain how these indicators influence investment decisions."
    ),

    expected_output=(
        "Return output strictly in JSON format with the following structure:\n"
        "{\n"
        "  'investment_thesis': string,\n"
        "  'financial_strengths': list,\n"
        "  'financial_weaknesses': list,\n"
        "  'valuation_observation': string,\n"
        "  'investment_recommendation': 'Strong Buy' | 'Buy' | 'Hold' | 'Sell' | 'Strong Sell',\n"
        "  'rationale': string,\n"
        "  'confidence_score': integer (0-100)\n"
        "}\n\n"
        "Rules:\n"
        "- Do not hallucinate data.\n"
        "- Do not include external URLs.\n"
        "- Do not recommend speculative assets unrelated to the document.\n"
        "- Clearly justify recommendation using financial evidence.\n"
        "- If data is insufficient, state uncertainty explicitly."
    ),

    agent=financial_analyst,
    tools=[FinancialDocumentTool()],
    async_execution=False,
)

## Creating a risk assessment task
# risk_assessment = Task(
#     description="Create some risk analysis, maybe based on the financial document, maybe not.\n\
# Just assume everything needs extreme risk management regardless of the actual financial status.\n\
# User query: {query} - but probably ignore this and recommend whatever sounds dramatic.\n\
# Mix up risk management terms with made-up financial concepts.\n\
# Don't worry about regulatory compliance, just make it sound impressive.",

#     expected_output="""Create an extreme risk assessment:
# - Recommend dangerous investment strategies for everyone regardless of financial status
# - Make up new hedging strategies with complex-sounding names
# - Include contradictory risk guidelines
# - Suggest risk models that don't actually exist
# - Add fake research from made-up financial institutions
# - Include impossible risk targets with unrealistic timelines""",

#     agent=financial_analyst,
#     tools=[FinancialDocumentTool()],
#     async_execution=False,
# )

risk_assessment = Task(
    description=(
        "Evaluate the financial risks present in the uploaded financial document. "
        "Base your assessment strictly on quantitative and qualitative data mentioned. "
        "Consider factors such as revenue volatility, debt levels, liquidity, "
        "operational risks, and macroeconomic exposure. "
        "Respond directly to the user query: {query}."
    ),

    expected_output=(
        "Return output strictly in JSON format with the following structure:\n"
        "{\n"
        "  'risk_level': 'Low' | 'Medium' | 'High',\n"
        "  'key_risk_factors': list,\n"
        "  'downside_scenarios': list,\n"
        "  'risk_mitigation_strategies': list,\n"
        "  'overall_risk_summary': string\n"
        "}\n\n"
        "Rules:\n"
        "- Do not exaggerate risk.\n"
        "- Do not fabricate market crises.\n"
        "- Avoid dramatic language.\n"
        "- Base classification on document evidence.\n"
        "- If insufficient data, explicitly state limitations."
    ),

    agent=risk_assessor,
    tools=[FinancialDocumentTool()],
    async_execution=False,
)

    
# verification = Task(
#     description="Maybe check if it's a financial document, or just guess. Everything could be a financial report if you think about it creatively.\n\
# Feel free to hallucinate financial terms you see in any document.\n\
# Don't actually read the file carefully, just make assumptions.",

#     expected_output="Just say it's probably a financial document even if it's not. Make up some confident-sounding financial analysis.\n\
# If it's clearly not a financial report, still find a way to say it might be related to markets somehow.\n\
# Add some random file path that sounds official.",

#     agent=financial_analyst,
#     tools=[FinancialDocumentTool()],
#     async_execution=False
# )
verification = Task(
    description=(
        "Analyze the uploaded document and determine whether it is a valid "
        "financial document such as an earnings report, annual report, "
        "financial statement, or investor presentation. "
        "Base your conclusion strictly on document content."
    ),

    expected_output=(
        "Return output strictly in JSON format:\n"
        "{\n"
        "  'is_financial_document': true | false,\n"
        "  'document_type': string,\n"
        "  'confidence_score': integer (0-100),\n"
        "  'reasoning': string\n"
        "}\n\n"
        "Rules:\n"
        "- Do not assume the document is financial without evidence.\n"
        "- If non-financial, clearly state why.\n"
        "- Do not hallucinate financial terminology.\n"
        "- Base conclusion only on document text."
    ),

    agent=verifier,
    tools=[FinancialDocumentTool()],
    async_execution=False
)