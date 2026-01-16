# Quick Reference Guide

## 🚀 Quick Start Commands

```bash
# Setup (one-time)
pip install -r requirements.txt
cp .env.example .env
# Add your OpenAI API key to .env

# Generate data
python generate_data.py
python ontology.py
python knowledge_graph.py

# Run application
streamlit run app.py
```

## 📁 File Purpose Reference

| File | Purpose | When to Edit |
|------|---------|-------------|
| `app.py` | Streamlit UI and main interface | Modify UI, add features |
| `llm_analyzer.py` | Basic & Enhanced analyzers | Change LLM logic, prompts |
| `ontology.py` | Domain ontology definition | Add classes, properties, rules |
| `knowledge_graph.py` | KG builder and SPARQL queries | Add queries, modify graph |
| `generate_data.py` | Sample data generator | Change data patterns |
| `requirements.txt` | Python dependencies | Add new packages |
| `.env` | API keys (gitignored) | Configure secrets |
| `.env.example` | Template for .env | Document required keys |

## 🔧 Common Tasks

### Adding a New Question Type

1. **For Basic Analysis**: No changes needed
2. **For Enhanced Analysis**:
   - Add SPARQL query in `knowledge_graph.py`
   - Update context in `llm_analyzer.py`

### Adding a New Ontology Class

```python
# In ontology.py
def _define_classes(self):
    # Add your class
    self.g.add((EX.YourNewClass, RDF.type, OWL.Class))
    self.g.add((EX.YourNewClass, RDFS.subClassOf, EX.ParentClass))
```

### Adding a New SPARQL Query

```python
# In knowledge_graph.py get_insights() or get_reasoning_insights()
query = """
    PREFIX sales: <http://example.org/sales#>
    SELECT ?var WHERE {
        # Your SPARQL pattern
    }
"""
results = self.graph.query(query)
```

### Customizing Sample Questions

```python
# In app.py setup_sidebar()
sample_questions = [
    "Your new question here?",
    # ...
]
```

## 🐛 Troubleshooting Quick Fixes

| Error | Quick Fix |
|-------|-----------|
| "Module not found" | `pip install -r requirements.txt` |
| "Data files not found" | Run data generation scripts |
| "OpenAI API error" | Check `.env` has valid `OPENAI_API_KEY` |
| "Knowledge graph empty" | Run `python knowledge_graph.py` |
| Streamlit warnings | Restart with `streamlit run app.py` |

## 📊 Data Files

| File | Size | Purpose | Regenerate With |
|------|------|---------|----------------|
| `sales_data.csv` | ~250KB | Sales transactions | `python generate_data.py` |
| `metadata.json` | ~10KB | Customer/product info | `python generate_data.py` |
| `sales_ontology.ttl` | ~20KB | Ontology definition | `python ontology.py` |
| `knowledge_graph.ttl` | ~1MB | Populated KG | `python knowledge_graph.py` |
| `chat_history.json` | varies | Q&A history | Auto-saved by app |

## 🎯 Key Endpoints

- **Web UI**: http://localhost:8501
- **Streamlit Admin**: http://localhost:8501/_stcore/health
- **API Docs** (if enabled): http://localhost:8501/docs

## 🔑 Environment Variables

```bash
# Required
OPENAI_API_KEY=sk-...

# Optional (with defaults)
OPENAI_MODEL=gpt-4           # or gpt-3.5-turbo
OPENAI_TEMPERATURE=0.7
MAX_TOKENS=1500
```

## 📈 Performance Tips

- **Slow SPARQL queries**: Add indexes or limit result count
- **High memory usage**: Reduce data size in generate_data.py
- **Slow LLM responses**: Use gpt-3.5-turbo instead of gpt-4
- **UI lag**: Clear chat history periodically

## 🎓 Learning Resources

### Understanding the Code
1. Start with `app.py` (UI layer)
2. Read `llm_analyzer.py` (LLM integration)
3. Study `ontology.py` (knowledge representation)
4. Explore `knowledge_graph.py` (graph queries)

### Key Concepts
- **Ontology**: Domain knowledge structure
- **Knowledge Graph**: Interconnected data
- **SPARQL**: Graph query language
- **RDF/OWL**: Semantic web standards

## 🚢 Deployment Checklist

- [ ] Set production OpenAI API key
- [ ] Review rate limits and costs
- [ ] Configure caching for SPARQL queries
- [ ] Set up monitoring and logging
- [ ] Use production-grade graph database
- [ ] Implement authentication if needed
- [ ] Set up CI/CD pipeline
- [ ] Configure environment-specific settings

## 🔄 Git Commands Reference

```bash
# Check status
git status

# View changes
git diff

# Stage files
git add <file>
git add .

# Commit
git commit -m "Your message"

# Push to remote
git push origin main

# Pull updates
git pull origin main

# Create branch
git checkout -b feature/your-feature

# View history
git log --oneline

# Create tag
git tag -a v1.0.0 -m "Release 1.0.0"
git push origin v1.0.0
```

## 📞 Support

- **Documentation**: README.md, ARCHITECTURE.md
- **Issues**: Check CONTRIBUTING.md for bug reporting
- **Questions**: Review docs first, then open discussion

## 🎯 Quick Test

```bash
# Verify everything works
cd /Users/bhanu/MyCode/Ontology

# 1. Check dependencies
pip list | grep -E "streamlit|openai|rdflib|pandas"

# 2. Verify data exists
ls -lh data/

# 3. Quick ontology test
python -c "from ontology import SalesOntology; s = SalesOntology(); print(f'Classes: {len(list(s.g.subjects(RDF.type, OWL.Class)))}')"

# 4. Quick KG test
python -c "from knowledge_graph import KnowledgeGraphBuilder; k = KnowledgeGraphBuilder(); print(f'Triples: {len(k.graph)}')"

# 5. Run app
streamlit run app.py
```

## 🏷️ Version Info

- **Current Version**: 1.0.0
- **Python**: 3.8+
- **Streamlit**: 1.29.0
- **OpenAI**: 1.3.0
- **RDFLib**: 7.0.0

---

**Need more details?** See [README.md](README.md) for comprehensive documentation.
