"""
LLM Integration for Sales Analysis
Provides two approaches: basic (no ontology) and enhanced (with ontology/KG)
"""
import os
from openai import OpenAI
import pandas as pd
import json
from typing import Dict, List, Tuple
from knowledge_graph import KnowledgeGraphBuilder
from ontology import SalesOntology

class SalesAnalyzer:
    """Base class for sales analysis"""
    
    def __init__(self, api_key: str = None):
        if api_key is None:
            api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4"
    
    def analyze(self, question: str) -> Tuple[str, Dict]:
        """Analyze a question and return answer with metadata"""
        raise NotImplementedError

class BasicAnalyzer(SalesAnalyzer):
    """Analyzes sales data without ontology or knowledge graph"""
    
    def __init__(self, api_key: str = None):
        super().__init__(api_key)
        self.data = None
        self.load_data()
    
    def load_data(self):
        """Load raw sales data"""
        try:
            df = pd.read_csv("data/sales_data.csv")
            self.data = df
            
            # Create basic summary statistics
            self.summary = {
                "total_records": len(df),
                "total_revenue": df['net_revenue'].sum(),
                "avg_revenue": df['net_revenue'].mean(),
                "date_range": f"{df['date'].min()} to {df['date'].max()}",
                "unique_customers": df['customer_id'].nunique(),
                "unique_products": df['product_id'].nunique()
            }
        except Exception as e:
            print(f"Error loading data: {e}")
            self.data = None
    
    def get_data_context(self, question: str) -> str:
        """Get relevant data context for the question"""
        if self.data is None:
            return "No data available"
        
        # Create a simple data summary
        sample_data = self.data.head(10).to_string()
        columns_info = ", ".join(self.data.columns)
        
        context = f"""
Sales Data Information:
- Total Records: {self.summary['total_records']}
- Date Range: {self.summary['date_range']}
- Total Revenue: ${self.summary['total_revenue']:,.2f}
- Average Deal Size: ${self.summary['avg_revenue']:,.2f}
- Unique Customers: {self.summary['unique_customers']}
- Unique Products: {self.summary['unique_products']}

Available Columns: {columns_info}

Sample Data (first 10 rows):
{sample_data}

Note: This is raw tabular data without semantic relationships or domain knowledge.
"""
        return context
    
    def analyze(self, question: str) -> Tuple[str, Dict]:
        """Analyze question using basic approach"""
        
        context = self.get_data_context(question)
        
        system_prompt = "You are a sales data analyst working with tabular data."
        
        user_prompt = f"""You are a sales data analyst. Answer the following question based on the raw sales data provided.

{context}

Question: {question}

Provide a clear, data-driven answer. If you need to calculate something, explain your reasoning.
Keep your answer concise but informative.
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            answer = response.choices[0].message.content
            
            metadata = {
                "approach": "Basic (No Ontology/KG)",
                "data_source": "Raw CSV data",
                "context_used": "Statistical summary + sample rows",
                "semantic_understanding": "Limited - relies on column names only",
                "reasoning_capability": "Basic - pattern matching in tabular data",
                "system_prompt": system_prompt,
                "user_prompt": user_prompt,
                "prompt_tokens": len(system_prompt.split()) + len(user_prompt.split()),
                "model": self.model
            }
            
            return answer, metadata
            
        except Exception as e:
            return f"Error: {str(e)}", {"error": str(e)}

class EnhancedAnalyzer(SalesAnalyzer):
    """Analyzes sales data using ontology and knowledge graph"""
    
    def __init__(self, api_key: str = None):
        super().__init__(api_key)
        self.kg = None
        self.load_knowledge_graph()
    
    def load_knowledge_graph(self):
        """Load knowledge graph"""
        try:
            ontology = SalesOntology()
            self.kg = KnowledgeGraphBuilder(ontology)
            self.kg.load_sales_data()
        except Exception as e:
            print(f"Error loading knowledge graph: {e}")
            self.kg = None
    
    def get_semantic_context(self, question: str) -> str:
        """Get semantic context from knowledge graph"""
        if self.kg is None:
            return "Knowledge graph not available"
        
        try:
            # Get insights from KG
            insights = self.kg.get_insights()
            
            # Get reasoning insights for causal analysis
            reasoning = self.kg.get_reasoning_insights()
        except Exception as e:
            print(f"Warning: Error getting insights: {e}")
            return "Knowledge graph available but insights could not be generated."
        
        # Get ontology structure
        ontology_info = """
Domain Ontology Structure:
- Classes: Sale, Customer (Enterprise/SMB/MidMarket), Product (Electronics/Furniture), 
           SalesRepresentative, Region, Category, Industry
- Reasoning Concepts: HighValueCustomer, FrequentBuyer, PremiumProduct, ExperiencedRep,
                      RegionalPreference, IndustryFit, DiscountSensitive
- Key Relationships:
  * Sales are soldTo Customers and soldBy SalesRepresentatives
  * Customers locatedIn Regions and belongsToIndustry
  * Products belongsToCategory with hierarchical subcategories
  * SalesRepresentatives operatesIn specific Regions
- Causal Properties:
  * causedBy: Enables causal reasoning
  * influences: Shows influence factors
  * correlatesWith: Identifies correlations
  * indicatesPreference: Reveals preference patterns
- Semantic Rules:
  * Customer types have different purchasing patterns (WHY: budget, needs, scale)
  * Regional sales reps handle customers in their regions (WHY: local knowledge, relationships)
  * Product categories have parent-child relationships (WHY: functionality grouping)
  * Premium products attract enterprise customers (WHY: budget availability, quality needs)
  * Experience impacts sales effectiveness (WHY: expertise, relationships, credibility)
"""
        
        # Format insights
        insights_text = f"""
Knowledge Graph Insights:

Revenue by Region:
"""
        for item in insights.get('revenue_by_region', []):
            insights_text += f"  • {item['region']}: ${item['revenue']:,.2f} from {item['sales']} sales\n"
        
        insights_text += "\nTop Products:\n"
        for item in insights.get('top_products', [])[:5]:
            insights_text += f"  • {item['product']}: ${item['revenue']:,.2f} ({item['units_sold']} units)\n"
        
        insights_text += "\nRevenue by Customer Segment:\n"
        for item in insights.get('revenue_by_customer_type', []):
            insights_text += f"  • {item['customer_type']}: ${item['total_revenue']:,.2f} (avg deal: ${item['avg_revenue']:,.2f})\n"
        
        # Add reasoning insights for WHY questions
        reasoning_text = """
REASONING & CAUSAL INSIGHTS (for WHY questions):

1. Product-Customer Affinity (Why certain products sell more to specific customers):
"""
        for item in reasoning.get('product_customer_fit', [])[:5]:
            reasoning_text += f"   • {item['product']} → {item['customer_type']}: {item['sales_count']} sales, ${item['avg_deal']:,.2f} avg\n"
            reasoning_text += f"     WHY: {item['category']} products fit {item['customer_type']} needs and budgets\n"
        
        reasoning_text += "\n2. Regional Performance Patterns (Why regions differ):\n"
        for item in reasoning.get('regional_patterns', [])[:5]:
            reasoning_text += f"   • {item['region']} + {item['industry']} → {item['product']}: {item['sales_count']} sales\n"
            reasoning_text += f"     WHY: Industry-Product fit + regional market characteristics\n"
        
        reasoning_text += "\n3. Sales Rep Effectiveness (Why some reps perform better):\n"
        for item in reasoning.get('rep_effectiveness', [])[:3]:
            reasoning_text += f"   • {item['rep']} ({item['experience']}y exp, {item['region']}): ${item['avg_deal']:,.2f} avg deal\n"
            reasoning_text += f"     WHY: Experience + regional knowledge + customer relationships\n"
        
        reasoning_text += "\n4. Discount Impact Patterns (Why discounts work differently):\n"
        for item in reasoning.get('discount_patterns', []):
            reasoning_text += f"   • {item['customer_type']}: {item['avg_discount']:.1f}% avg discount → ${item['avg_revenue']:,.2f} deals\n"
            reasoning_text += f"     WHY: Different price sensitivity and volume leverage\n"
        
        context = ontology_info + insights_text + reasoning_text
        
        context += """
Enhanced Capabilities with REASONING:
- Semantic relationships between entities are explicitly modeled
- Domain knowledge is encoded in the ontology
- CAUSAL REASONING: Can answer WHY questions by analyzing relationships
- DIAGNOSTIC ANALYSIS: Can identify root causes and influencing factors
- PATTERN RECOGNITION: Discovers hidden correlations through graph traversal
- INFERENCE: Makes logical conclusions based on entity relationships and rules
- PREDICTIVE INSIGHTS: Suggests what might work based on patterns

When answering WHY questions:
1. Identify the entities and their relationships in the knowledge graph
2. Trace causal paths (e.g., Product → Customer Type → Region → Industry)
3. Apply domain rules (e.g., Enterprise customers have higher budgets)
4. Explain patterns using semantic understanding (not just correlations)
5. Provide actionable insights based on causal reasoning
"""
        
        return context
    
    def generate_sparql_if_needed(self, question: str) -> str:
        """Generate SPARQL query if question requires specific data"""
        
        # Common query patterns
        sparql_templates = """
Available SPARQL Query Patterns:

1. Revenue by dimension:
   SELECT ?dimension (SUM(?revenue) as ?total)
   WHERE { ?sale sales:soldTo/sales:locatedIn/sales:regionName ?dimension }
   
2. Top performers:
   SELECT ?name (SUM(?revenue) as ?total)
   ORDER BY DESC(?total) LIMIT N
   
3. Customer insights:
   SELECT ?customer ?type ?industry
   WHERE { ?customer a sales:Customer }
   
4. Product relationships:
   SELECT ?product ?category ?subcategory
   WHERE { ?product sales:belongsToCategory ?cat }
"""
        return sparql_templates
    
    def analyze(self, question: str) -> Tuple[str, Dict]:
        """Analyze question using enhanced approach with KG"""
        
        semantic_context = self.get_semantic_context(question)
        sparql_info = self.generate_sparql_if_needed(question)
        
        system_prompt = """You are an advanced sales intelligence system with semantic 
understanding of the sales domain through ontology and knowledge graphs. You can reason about 
relationships, hierarchies, and domain concepts."""
        
        user_prompt = f"""You are an advanced sales intelligence analyst with access to a semantic knowledge graph 
and domain ontology. You understand not just the data, but the relationships and meaning behind it.

{semantic_context}

{sparql_info}

Question: {question}

Provide a comprehensive, insight-driven answer that:
1. Leverages semantic relationships in the knowledge graph
2. Applies domain knowledge from the ontology
3. Makes inferences based on entity relationships
4. Provides context and actionable insights

Your answer should demonstrate understanding beyond simple data aggregation.
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=600
            )
            
            answer = response.choices[0].message.content
            
            metadata = {
                "approach": "Enhanced (Ontology + Knowledge Graph)",
                "data_source": "Semantic Knowledge Graph",
                "context_used": "Domain ontology + semantic relationships + graph insights",
                "semantic_understanding": "Deep - understands entity types, relationships, hierarchies",
                "reasoning_capability": "Advanced - can make inferences and traverse relationships",
                "system_prompt": system_prompt,
                "user_prompt": user_prompt,
                "prompt_tokens": len(system_prompt.split()) + len(user_prompt.split()),
                "model": self.model
            }
            
            return answer, metadata
            
        except Exception as e:
            return f"Error: {str(e)}", {"error": str(e)}

def compare_approaches(question: str, api_key: str = None) -> Dict:
    """Compare both approaches for the same question"""
    
    basic = BasicAnalyzer(api_key)
    enhanced = EnhancedAnalyzer(api_key)
    
    basic_answer, basic_meta = basic.analyze(question)
    enhanced_answer, enhanced_meta = enhanced.analyze(question)
    
    return {
        "question": question,
        "basic": {
            "answer": basic_answer,
            "metadata": basic_meta
        },
        "enhanced": {
            "answer": enhanced_answer,
            "metadata": enhanced_meta
        }
    }

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    # Test questions
    questions = [
        "Which region has the highest revenue?",
        "What products should we promote to enterprise customers in North America?",
        "How does customer type affect purchase patterns?"
    ]
    
    for question in questions:
        print(f"\n{'='*80}")
        print(f"Question: {question}")
        print('='*80)
        
        result = compare_approaches(question)
        
        print("\n--- BASIC APPROACH (No Ontology) ---")
        print(result['basic']['answer'])
        
        print("\n--- ENHANCED APPROACH (With Ontology + KG) ---")
        print(result['enhanced']['answer'])
