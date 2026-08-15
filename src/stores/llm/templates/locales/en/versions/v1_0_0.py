from jinja2 import Template
import hashlib

VERSION = "1.0.0"
LANG = "en"

_SYSTEM_SRC = "\n".join([
    "You are an assistant that answers user queries strictly based on provided documents.",
    "Only use information explicitly present in the documents below.",
    "If the answer is not present or only partially present, say so explicitly — never infer, guess, or use outside knowledge.",
    "If documents contradict each other, point out the contradiction instead of picking one silently.",
    "Cite the document number(s) you used, e.g. [Doc 2].",
    "Respond in the same language as the user's query.",
    "Be precise and concise.",
])

# document_prompt gère maintenant une LISTE de documents nativement (boucle Jinja2),
# au lieu d'un rendu par chunk à concaténer manuellement côté Python.
_DOCUMENT_SRC = "\n".join([
    "{% for doc in documents %}",
    "## Document No: {{ doc.num }}",
    "### Content: {{ doc.chunk_text }}",
    "{% endfor %}",
])

_FOOTER_SRC = "\n".join([
    "Based only on the documents above, answer the user's query.",
    "If the information needed is missing, state that clearly instead of guessing.",
    "## Question:",
    "{{ query }}",
    "",
    "## Answer:",
])

system_prompt = Template(_SYSTEM_SRC)
document_prompt = Template(_DOCUMENT_SRC)
footer_prompt = Template(_FOOTER_SRC)


def _compute_hash() -> str:
    """Hash du contenu combiné des 3 templates, pour traçabilité en base."""
    combined = _SYSTEM_SRC + _DOCUMENT_SRC + _FOOTER_SRC
    return hashlib.sha256(combined.encode("utf-8")).hexdigest()[:10]


CONTENT_HASH = _compute_hash()
