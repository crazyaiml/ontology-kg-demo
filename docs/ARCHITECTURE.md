# Architecture Documentation

## 🏛️ System Architecture

This document provides a detailed architectural overview of the Ontology & Knowledge Graph Intelligence Demo.

## 📐 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Streamlit Web UI                        │
│                         (app.py)                             │
└────────────────┬────────────────────────────┬────────────────┘
                 │                            │
        ┌────────▼────────┐          ┌────────▼─────────┐
        │ Basic Analyzer   │          │ Enhanced Analyzer │
        │ (CSV → LLM)      │          │ (KG → LLM)       │
        └────────┬─────────┘          └────────┬─────────┘
                 │                             │
                 │                    ┌────────▼──────────┐
                 │                    │ Knowledge Graph   │
                 │                    │ (RDF/SPARQL)     │
                 │                    └────────┬──────────┘
                 │                             │
                 │                    ┌────────▼──────────┐
                 │                    │ Sales Ontology    │
                 │                    │ (OWL/RDFS)       │
                 │                    └───────────────────┘
                 │
        ┌────────▼──────────────────────────────────────┐
        │            OpenAI GPT-4 API                    │
        └────────────────────────────────────────────────┘
```

## 🧩 Component Details

### 1. User Interface Layer (`app.py`)

**Purpose**: Interactive web interface for comparing analysis approaches

**Key Components**:
- **Interactive Chat Tab**: Question input, side-by-side answer comparison
- **View Data Tab**: Data exploration with visualizations
- **Learn More Tab**: Educational content about ontologies and KGs

**Responsibilities**:
- User input handling
- Session state management
- Chat history persistence
- Result visualization
- LLM prompt display

**Technologies**: Streamlit, Pandas, JSON

---

### 2. Analyzer Layer (`llm_analyzer.py`)

#### 2.1 BasicAnalyzer

**Purpose**: Traditional approach using raw CSV data

**Process Flow**:
```
CSV Data → Statistical Summary → LLM Prompt → GPT-4 → Answer
```

**Context Provided**:
- Column names and types
- Statistical aggregates (count, mean, sum)
- Sample rows (first 10)
- Basic data structure

**Limitations**:
- No semantic understanding
- No relationship awareness
- Cannot answer "WHY" questions
- Surface-level insights only

#### 2.2 EnhancedAnalyzer

**Purpose**: Advanced approach using Ontology + Knowledge Graph

**Process Flow**:
```
CSV → Ontology → Knowledge Graph → SPARQL Queries → 
Semantic Context → Enhanced LLM Prompt → GPT-4 → Deep Answer
```

**Context Provided**:
- Domain ontology structure (classes, properties, hierarchies)
- Reasoning concepts (HighValueCustomer, PremiumProduct, etc.)
- Causal properties (causedBy, influences, correlatesWith)
- Knowledge graph insights (revenue by region/type, top products)
- Reasoning insights (product-customer fit, regional patterns)
- Multi-hop relationship paths

**Advantages**:
- Semantic understanding
- Relationship traversal
- Causal reasoning
- Deep contextual insights
- Answers "WHY" questions

---

### 3. Ontology Layer (`ontology.py`)

**Purpose**: Define domain knowledge structure

**Key Classes**:
```
Core Classes:
- Sale (transaction)
- Customer (Enterprise, SMB, MidMarket)
- Product (Electronics, Furniture)
- SalesRepresentative
- Region
- Category (hierarchical)
- Industry

Reasoning Concepts:
- HighValueCustomer (>$500K revenue)
- FrequentBuyer (>10 purchases)
- PremiumProduct (>$1000 price)
- ExperiencedRep (>3 years)
- RegionalPreference
- IndustryFit
- DiscountSensitive
- SeasonalDemand
- CustomerRetention
```

**Key Properties**:
```
Object Properties:
- soldTo: Sale → Customer
- soldBy: Sale → SalesRepresentative
- locatedIn: Customer → Region
- belongsToCategory: Product → Category
- belongsToIndustry: Customer → Industry
- operatesIn: SalesRepresentative → Region

Causal Properties (for reasoning):
- causedBy: Identifies causes
- influences: Shows influence factors
- correlatesWith: Reveals correlations
- indicatesPreference: Customer preferences

Data Properties:
- hasRevenue, hasQuantity, hasDiscount
- hasName, hasEmail, hasExperience
- hasPrice, hasDescription
```

**Reasoning Rules**:
- Automatic classification based on attributes
- Inference of new relationships
- Causal chain identification

---

### 4. Knowledge Graph Layer (`knowledge_graph.py`)

**Purpose**: Populate and query semantic graph

**Components**:

#### 4.1 Graph Population
```python
CSV Row → RDF Triples:
- Create individual nodes (ex:Sale_1, ex:Customer_1)
- Add type assertions (rdf:type ex:Sale)
- Add property links (ex:soldTo ex:Customer_1)
- Add data property values (ex:hasRevenue 5000)
```

#### 4.2 SPARQL Query Engine

**Basic Insights**:
```sparql
- Revenue by Region
- Top Products by Revenue
- Revenue by Customer Type
- Sales Representative Performance
```

**Reasoning Insights** (for WHY questions):
```sparql
1. Product-Customer Affinity
   - Which products sell to which customer types
   - Average deal sizes
   - Category patterns

2. Regional Performance
   - Region + Industry + Product patterns
   - Geographic preferences
   - Market characteristics

3. Sales Rep Effectiveness
   - Experience correlation with deal size
   - Regional expertise impact
   - Customer relationship value

4. Discount Impact
   - Customer type sensitivity
   - Discount patterns
   - ROI analysis
```

**Graph Statistics**:
- ~5,800+ semantic triples
- Full transaction history
- Multi-hop relationship paths
- Inferred knowledge

---

### 5. Data Generation Layer (`generate_data.py`)

**Purpose**: Create realistic synthetic sales data

**Features**:
- 500 sales transactions
- 10 customers (varied types)
- 10 products (varied categories)
- 5 sales representatives
- 3 regions
- 8 industries
- Realistic patterns and correlations

**Patterns Built In**:
- Enterprise customers buy premium products
- Tech industry prefers electronics
- Regional preferences
- Seasonal variations
- Discount strategies by customer type

---

## 🔄 Data Flow

### Query Processing Flow

```
1. User enters question
   ↓
2. Question sent to both analyzers in parallel
   ↓
3a. BASIC PATH:                3b. ENHANCED PATH:
    CSV → Summary                 KG → SPARQL Queries
    ↓                             ↓
    Build Basic Prompt            Get Semantic Context
    ↓                             ↓
    GPT-4                         Build Enhanced Prompt
    ↓                             ↓
    Surface Answer                GPT-4
                                  ↓
                                  Deep Answer
   ↓                             ↓
4. Display both answers side-by-side
   ↓
5. Save to chat history
```

### Context Building (Enhanced Analyzer)

```
1. Load Ontology Structure
   ↓
2. Execute Basic Insights SPARQL
   - Revenue by region
   - Top products
   - Customer segments
   ↓
3. Execute Reasoning SPARQL
   - Product-customer fit
   - Regional patterns
   - Rep effectiveness
   - Discount patterns
   ↓
4. Combine into Rich Context
   ↓
5. Build Enhanced Prompt
   - System: Role + ontology
   - User: Question + context
   ↓
6. Send to GPT-4
```

---

## 🔐 Security Considerations

### API Key Management
- Stored in `.env` file (not in git)
- Loaded via `python-dotenv`
- Never logged or displayed

### Data Privacy
- Sample data is synthetic
- No real customer information
- Safe for demonstration

### Input Validation
- User questions sanitized
- SPARQL injection prevented
- Error handling for malformed queries

---

## 📊 Performance Characteristics

### Response Times
- **Basic Analyzer**: ~2-5 seconds
  - CSV reading: <100ms
  - Summary generation: <100ms
  - LLM call: 2-4 seconds

- **Enhanced Analyzer**: ~3-7 seconds
  - Graph loading: ~200ms
  - SPARQL queries: ~500ms
  - Context building: ~200ms
  - LLM call: 2-5 seconds

### Memory Usage
- Ontology: ~1-2 MB
- Knowledge Graph: ~5-10 MB
- Session State: ~1-5 MB
- Total: ~20-30 MB

### Scalability
- **Current**: 500 transactions, ~5,800 triples
- **Tested**: Up to 10,000 transactions
- **Bottleneck**: SPARQL query time on large graphs
- **Solution**: Graph database (e.g., GraphDB, Stardog) for production

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| UI | Streamlit | Web interface |
| Backend | Python 3.8+ | Core logic |
| LLM | OpenAI GPT-4 | Natural language understanding |
| Ontology | OWL/RDFS | Knowledge representation |
| KG Storage | RDFLib | In-memory graph store |
| Query | SPARQL | Semantic queries |
| Data | Pandas | Data manipulation |
| Config | python-dotenv | Environment management |

---

## 🔮 Future Enhancements

### Planned Improvements
1. **Graph Database**: Replace RDFLib with production graph DB
2. **Caching**: Cache SPARQL results for common queries
3. **Async Processing**: Parallel query execution
4. **Real-time Updates**: Stream new data into KG
5. **Visualization**: Interactive graph explorer
6. **Multi-tenancy**: Support multiple datasets
7. **API**: REST API for programmatic access
8. **Monitoring**: Performance metrics and logging

### Architectural Patterns
- Consider event-driven architecture for real-time
- Implement CQRS for read/write separation
- Add graph cache layer for performance
- Microservices for scaling individual components

---

## 📝 Design Decisions

### Why RDFLib?
- ✅ Pure Python, easy setup
- ✅ Standard-compliant (OWL, RDFS, SPARQL)
- ✅ Good for demos and small datasets
- ❌ Limited scalability for production

### Why Streamlit?
- ✅ Rapid prototyping
- ✅ Python-native
- ✅ Automatic UI updates
- ✅ Built-in state management
- ❌ Limited customization vs React

### Why GPT-4?
- ✅ Best-in-class reasoning
- ✅ Strong context handling
- ✅ Reliable API
- ❌ Cost for production use
- Alternative: Fine-tuned open models

---

## 📚 References

- [RDF 1.1 Concepts](https://www.w3.org/TR/rdf11-concepts/)
- [OWL 2 Web Ontology Language](https://www.w3.org/TR/owl2-overview/)
- [SPARQL 1.1 Query Language](https://www.w3.org/TR/sparql11-query/)
- [RDFLib Documentation](https://rdflib.readthedocs.io/)
- [Streamlit Documentation](https://docs.streamlit.io/)
