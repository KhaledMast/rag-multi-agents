# test_migration.py (à la racine ou dans un dossier tests/, à supprimer après)
from stores.llm.templates.template_parser import TemplateParser

parser = TemplateParser()

# Test system_prompt (pas de vars)
system = parser.get("rag", "system_prompt", {})
assert system, "system_prompt vide ou None"
print("✅ system_prompt OK")

# Test document_prompt avec plusieurs documents (le vrai test de la migration)
docs = parser.get("rag", "document_prompt", {
    "documents": [
        {"num": 1, "chunk_text": "Contenu test 1"},
        {"num": 2, "chunk_text": "Contenu test 2"},
    ]
})
assert "Contenu test 1" in docs and "Contenu test 2" in docs
assert docs.count("## Numéro de document") == 2, "La boucle Jinja2 n'a pas généré 2 entrées"
print("✅ document_prompt OK (boucle multi-documents)")

# Test document_prompt avec liste vide (edge case)
empty = parser.get("rag", "document_prompt", {"documents": []})
assert empty is not None
print("✅ document_prompt liste vide OK")

# Test footer_prompt
footer = parser.get("rag", "footer_prompt", {"query": "Test question ?"})
assert "Test question ?" in footer
print("✅ footer_prompt OK")

# Test langue AR
parser_ar = TemplateParser()
system_ar = parser_ar.get("rag", "system_prompt", {})
assert system_ar
print("✅ AR OK")

# Test langue EN
parser_en = TemplateParser()
system_en = parser_en.get("rag", "system_prompt", {})
assert system_en
print("✅ EN OK")

# Test langue FR
parser_fr = TemplateParser()
parser_fr = parser_en.get("rag", "system_prompt", {})
assert parser_fr
print("✅ FR OK")

# Test langue CH
parser_ch = TemplateParser()
parser_ch = parser_en.get("rag", "system_prompt", {})
assert parser_ch
print("✅ CH OK")

print("\n🎉 Migration validée")