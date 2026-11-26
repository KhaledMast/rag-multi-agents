from jinja2 import Template
import hashlib

VERSION = "1.0.0"
LANG = "fr"

_SYSTEM_SRC = "\n".join([
    "Tu es un assistant qui répond aux questions de l'utilisateur en te basant strictement sur les documents fournis.",
    "Utilise uniquement les informations explicitement présentes dans les documents ci-dessous.",
    "Si la réponse n'est pas présente ou seulement partiellement présente, dis-le clairement — ne devine jamais et n'utilise pas de connaissances externes.",
    "Si les documents se contredisent, signale la contradiction au lieu de choisir silencieusement une version.",
    "Cite le(s) numéro(s) de document utilisé(s), par exemple [Doc 2].",
    "Réponds dans la même langue que la question de l'utilisateur.",
    "Sois précis et concis.",
])

# document_prompt gère maintenant une LISTE de documents nativement (boucle Jinja2),
# au lieu d'un rendu par chunk à concaténer manuellement côté Python.
_DOCUMENT_SRC = "\n".join([
    "{% for doc in documents %}",
    "## Numéro de document: {{ doc.num }}",
    "### Contenu: {{ doc.chunk_text }}",
    "{% endfor %}",
])

_FOOTER_SRC = "\n".join([
    "En te basant uniquement sur les documents ci-dessus, réponds à la question de l'utilisateur.",
    "Si l'information nécessaire est manquante, indique-le clairement au lieu de deviner.",
    "## Question:",
    "{{ query }}",
    "",
    "## Réponse :",
])

system_prompt = Template(_SYSTEM_SRC)
document_prompt = Template(_DOCUMENT_SRC)
footer_prompt = Template(_FOOTER_SRC)


def _compute_hash() -> str:
    """Hash du contenu combiné des 3 templates, pour traçabilité en base."""
    combined = _SYSTEM_SRC + _DOCUMENT_SRC + _FOOTER_SRC
    return hashlib.sha256(combined.encode("utf-8")).hexdigest()[:10]


CONTENT_HASH = _compute_hash()
