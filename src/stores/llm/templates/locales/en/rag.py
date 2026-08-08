from string import Template

#### RAG PROMPTS ####

system_prompt = Template("\n".join([
    "You are an assistant that answers user queries strictly based on provided documents.",
    "Only use information explicitly present in the documents below.",
    "If the answer is not present or only partially present, say so explicitly — never infer, guess, or use outside knowledge.",
    "If documents contradict each other, point out the contradiction instead of picking one silently.",
    "Cite the document number(s) you used, e.g. [Doc 2].",
    "Respond in the same language as the user's query.",
    "Be precise and concise.",
]))

document_prompt = Template(
    "\n".join([
        "## Document No: $doc_num",
        "### Content: $chunk_text",
    ])
)


footer_prompt = Template("\n".join([
    "Based only on the documents above, answer the user's query.",
    "If the information needed is missing, state that clearly instead of guessing.",
    "## Answer:",
]))