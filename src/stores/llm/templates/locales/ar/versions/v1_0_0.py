from jinja2 import Template
import hashlib

VERSION = "1.0.0"
LANG = "ar"

_SYSTEM_SRC = "\n".join([
    "أنت مساعد يجيب على أسئلة المستخدم بالاعتماد حصريًا على الوثائق المزوّدة.",
    "استخدم فقط المعلومات الموجودة صراحةً في الوثائق أدناه.",
    "إذا لم تكن الإجابة موجودة، أو موجودة جزئيًا فقط، صرّح بذلك بوضوح — لا تخمّن أبدًا ولا تستخدم معرفة خارجية.",
    "إذا تعارضت الوثائق مع بعضها، أشر إلى التعارض بدلاً من اختيار نسخة واحدة بصمت.",
    "اذكر رقم (أرقام) الوثيقة التي استخدمتها، مثال: [Doc 2].",
    "أجب بنفس لغة سؤال المستخدم.",
    "كن دقيقًا ومختصرًا.",
])

# document_prompt gère maintenant une LISTE de documents nativement (boucle Jinja2),
# au lieu d'un rendu par chunk à concaténer manuellement côté Python.
_DOCUMENT_SRC = "\n".join([
    "{% for doc in documents %}",
    "## رقم المستند: {{ doc.num }}",
    "### محتوى: {{ doc.chunk_text }}",
    "{% endfor %}",
])

_FOOTER_SRC = "\n".join([
    "بالاعتماد فقط على الوثائق أعلاه، أجب عن سؤال المستخدم.",
    "إذا كانت المعلومة المطلوبة غير متوفرة، صرّح بذلك بوضوح بدلاً من التخمين.",
    "## السؤال:",
    "{{ query }}",
    "",
    "## الإجابة:",
])

system_prompt = Template(_SYSTEM_SRC)
document_prompt = Template(_DOCUMENT_SRC)
footer_prompt = Template(_FOOTER_SRC)


def _compute_hash() -> str:
    """Hash du contenu combiné des 3 templates, pour traçabilité en base."""
    combined = _SYSTEM_SRC + _DOCUMENT_SRC + _FOOTER_SRC
    return hashlib.sha256(combined.encode("utf-8")).hexdigest()[:10]


CONTENT_HASH = _compute_hash()
