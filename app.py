"""
Streamlit Chat Interface
Interactive comparison of Basic vs Enhanced (Ontology + KG) approaches
"""
import streamlit as st
import os
from dotenv import load_dotenv
from llm_analyzer import BasicAnalyzer, EnhancedAnalyzer, compare_approaches
import json
from pathlib import Path

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Ontology & Knowledge Graph Demo",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .approach-card {
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .basic-card {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
    }
    .enhanced-card {
        background-color: #d1ecf1;
        border-left: 5px solid #17a2b8;
    }
    .metadata-badge {
        display: inline-block;
        padding: 0.3rem 0.6rem;
        margin: 0.2rem;
        border-radius: 5px;
        font-size: 0.85rem;
        background-color: #e9ecef;
    }
    .comparison-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def load_chat_history():
    """Load chat history from file"""
    history_file = Path("data/chat_history.json")
    if history_file.exists():
        try:
            with open(history_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading chat history: {e}")
    return []

def save_chat_history(history):
    """Save chat history to file"""
    history_file = Path("data/chat_history.json")
    try:
        with open(history_file, 'w') as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        print(f"Error saving chat history: {e}")

def initialize_session_state():
    """Initialize session state variables"""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = load_chat_history()
    if 'analyzers_ready' not in st.session_state:
        st.session_state.analyzers_ready = False
    if 'basic_analyzer' not in st.session_state:
        st.session_state.basic_analyzer = None
    if 'enhanced_analyzer' not in st.session_state:
        st.session_state.enhanced_analyzer = None

def check_setup():
    """Check if data and knowledge graph are set up"""
    data_exists = Path("data/sales_data.csv").exists()
    kg_exists = Path("data/knowledge_graph.ttl").exists()
    api_key = os.getenv("OPENAI_API_KEY")
    
    return data_exists, kg_exists, bool(api_key)

def setup_sidebar():
    """Configure sidebar with information and settings"""
    with st.sidebar:
        st.title("Ontology & KG Demo")
        
        st.markdown("""
        ### About
        
        This application demonstrates how **Ontology** and **Knowledge Graphs** 
        enhance LLM-based data analysis intelligence.
        
        #### Two Approaches:
        
        **1. 🔸 Basic Approach**
        - Raw CSV data
        - No semantic understanding
        - Limited to basic queries
        
        **2. 🔹 Enhanced Approach**
        - Semantic Knowledge Graph
        - Domain Ontology
        - Rich relationships
        - Deep insights
        """)
        
        st.divider()
        
        # System status
        st.subheader("📊 System Status")
        data_exists, kg_exists, has_api_key = check_setup()
        
        st.write("Data File:", "✅" if data_exists else "❌")
        st.write("Knowledge Graph:", "✅" if kg_exists else "❌")
        st.write("OpenAI API Key:", "✅" if has_api_key else "❌")
        
        if not all([data_exists, kg_exists, has_api_key]):
            st.warning("⚠️ Setup incomplete. Please run setup scripts.")
            if st.button("View Setup Instructions"):
                st.session_state.show_setup = True
        
        st.divider()
        
        # Sample questions
        st.subheader("💡 Sample Questions")
        sample_questions = [
            "Why is Laptop Pro 15 our top-selling product?",
            "Why do enterprise customers spend more than SMB customers?",
            "What makes North America our best performing region?",
            "Why do experienced sales reps close bigger deals?",
            "Which products work best for enterprise customers and why?",
            "Why do certain products sell better in specific regions?",
            "What factors influence discount effectiveness?",
            "Why do technology companies prefer electronics products?",
            "What drives customer purchase patterns by segment?",
            "Why is there a correlation between industry and product preference?"
        ]
        
        for i, question in enumerate(sample_questions):
            if st.button(question, key=f"sample_{i}", use_container_width=True):
                st.session_state.selected_question = question
                st.rerun()
        
        st.divider()
        
        # Data Files Section
        st.subheader("📁 Data & Knowledge Files")
        st.markdown("*Files powering the Enhanced approach*")
        
        data_files = {
            "sales_data.csv": "Sales transactions",
            "metadata.json": "Customers & Products",
            "sales_ontology.ttl": "Domain ontology",
            "knowledge_graph.ttl": "Semantic graph"
        }
        
        for filename, description in data_files.items():
            filepath = Path(f"data/{filename}")
            if filepath.exists():
                with st.expander(f"📄 {filename}"):
                    st.caption(description)
                    
                    # Show file size
                    file_size = filepath.stat().st_size
                    if file_size > 1024*1024:
                        size_str = f"{file_size / (1024*1024):.2f} MB"
                    elif file_size > 1024:
                        size_str = f"{file_size / 1024:.2f} KB"
                    else:
                        size_str = f"{file_size} bytes"
                    st.caption(f"Size: {size_str}")
                    
                    # Show file preview
                    try:
                        if filename.endswith('.json'):
                            import json
                            with open(filepath, 'r') as f:
                                content = json.load(f)
                                st.json(content)
                        elif filename.endswith('.csv'):
                            import pandas as pd
                            df = pd.read_csv(filepath)
                            st.caption(f"Rows: {len(df)} | Columns: {len(df.columns)}")
                            st.dataframe(df.head(10), use_container_width=True)
                        elif filename.endswith('.ttl'):
                            with open(filepath, 'r', encoding='utf-8') as f:
                                lines = f.readlines()
                                # Show first 50 lines
                                preview = ''.join(lines[:50])
                                if len(lines) > 50:
                                    preview += f"\n... ({len(lines) - 50} more lines)"
                                st.code(preview, language="turtle")
                                st.caption(f"Total lines: {len(lines)}")
                    except Exception as e:
                        st.error(f"Error reading file: {e}")

def display_answer_comparison(question, basic_result, enhanced_result):
    """Display side-by-side comparison of both approaches"""
    
    st.markdown(f"### 🤔 Question: *{question}*")
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔸 Basic Approach (No Ontology)")
        st.markdown('<div class="approach-card basic-card">', unsafe_allow_html=True)
        st.markdown(basic_result['answer'])
        st.markdown('</div>', unsafe_allow_html=True)
        
        with st.expander("📋 View LLM Prompt (Basic)"):
            st.markdown("**System Prompt:**")
            st.code(basic_result['metadata'].get('system_prompt', 'N/A'), language="text")
            st.markdown("**User Prompt:**")
            st.text_area("", basic_result['metadata'].get('user_prompt', 'N/A'), height=300, key=f"basic_prompt_{hash(question)}", disabled=True)
            st.caption(f"Approximate tokens: {basic_result['metadata'].get('prompt_tokens', 0)} | Model: {basic_result['metadata'].get('model', 'N/A')}")
        
        with st.expander("📊 Approach Details"):
            meta = basic_result['metadata']
            for key, value in meta.items():
                if key not in ['system_prompt', 'user_prompt', 'prompt_tokens', 'model']:
                    st.markdown(f"**{key.replace('_', ' ').title()}:** {value}")
    
    with col2:
        st.markdown("#### 🔹 Enhanced Approach (Ontology + KG)")
        st.markdown('<div class="approach-card enhanced-card">', unsafe_allow_html=True)
        st.markdown(enhanced_result['answer'])
        st.markdown('</div>', unsafe_allow_html=True)
        
        with st.expander("📋 View LLM Prompt (Enhanced)"):
            st.markdown("**System Prompt:**")
            st.code(enhanced_result['metadata'].get('system_prompt', 'N/A'), language="text")
            st.markdown("**User Prompt:**")
            st.text_area("", enhanced_result['metadata'].get('user_prompt', 'N/A'), height=400, key=f"enhanced_prompt_{hash(question)}", disabled=True)
            st.caption(f"Approximate tokens: {enhanced_result['metadata'].get('prompt_tokens', 0)} | Model: {enhanced_result['metadata'].get('model', 'N/A')}")
        
        with st.expander("📊 Approach Details"):
            meta = enhanced_result['metadata']
            for key, value in meta.items():
                if key not in ['system_prompt', 'user_prompt', 'prompt_tokens', 'model']:
                    st.markdown(f"**{key.replace('_', ' ').title()}:** {value}")
    
    # Key differences
    st.markdown("---")
    st.markdown("### 🎯 Key Differences")
    
    diff_col1, diff_col2, diff_col3 = st.columns(3)
    
    with diff_col1:
        st.metric(
            label="Data Understanding",
            value="Enhanced",
            delta="Semantic vs Tabular"
        )
    
    with diff_col2:
        st.metric(
            label="Relationship Awareness",
            value="Enhanced",
            delta="Graph vs Flat"
        )
    
    with diff_col3:
        st.metric(
            label="Insight Depth",
            value="Enhanced",
            delta="Contextual vs Surface"
        )
    
    # Prompt comparison
    st.markdown("---")
    st.markdown("### 🔍 Prompt Engineering Comparison")
    
    with st.expander("📝 See How Prompts Differ", expanded=False):
        st.markdown("""
        The power of ontology and knowledge graphs is revealed in how they transform the LLM prompts.
        Compare the context provided to the LLM in each approach:
        """)
        
        prompt_col1, prompt_col2 = st.columns(2)
        
        with prompt_col1:
            st.markdown("**🔸 Basic Prompt Context:**")
            st.code("""
• Statistical summary (count, avg, sum)
• Sample rows (first 10 records)
• Column names
• Basic data types

NO semantic relationships
NO domain knowledge
NO reasoning rules
            """, language="text")
        
        with prompt_col2:
            st.markdown("**🔹 Enhanced Prompt Context:**")
            st.code("""
• Domain ontology structure
• Semantic relationships (soldTo, locatedIn)
• Reasoning concepts (HighValueCustomer)
• Causal properties (causedBy, influences)
• Product-Customer affinity patterns
• Regional-Industry correlations
• Sales rep effectiveness factors
• Discount impact insights
• Multi-hop reasoning paths

PLUS all the basic stats
            """, language="text")
        
        st.info("""
        💡 **Key Insight**: The Enhanced prompt contains 5-10x more contextual information,
        but it's *structured semantic knowledge* - not just more data. This enables the LLM
        to reason causally and answer "WHY" questions.
        """)

def display_data_view():
    """Display the actual data being analyzed"""
    
    st.markdown("## 📊 Sales Data Overview")
    st.markdown("This is the actual data that both approaches analyze. See how the **Enhanced approach** uses ontology to understand relationships.")
    
    import pandas as pd
    import json
    
    # Load data
    try:
        df = pd.read_csv("data/sales_data.csv")
        with open("data/metadata.json", "r") as f:
            metadata = json.load(f)
        
        # Summary metrics
        st.markdown("### 📈 Key Metrics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Sales", len(df))
        with col2:
            st.metric("Total Revenue", f"${df['net_revenue'].sum():,.0f}")
        with col3:
            st.metric("Avg Deal Size", f"${df['net_revenue'].mean():,.0f}")
        with col4:
            completed = (df['status'] == 'Completed').sum()
            st.metric("Completed Sales", f"{completed} ({completed/len(df)*100:.0f}%)")
        
        st.divider()
        
        # Tabs for different data views
        data_tab1, data_tab2, data_tab3, data_tab4, data_tab5 = st.tabs([
            "📋 Sales Transactions", 
            "👥 Customers", 
            "📦 Products", 
            "💼 Sales Reps",
            "📊 Visualizations"
        ])
        
        with data_tab1:
            st.markdown("#### Sales Transactions (Sample)")
            st.markdown("*This is what the **Basic Approach** sees - flat tabular data*")
            
            # Filters
            col1, col2, col3 = st.columns(3)
            with col1:
                status_filter = st.multiselect("Status", df['status'].unique(), default=["Completed"])
            with col2:
                region_filter = st.multiselect("Region", df['customer_region'].unique())
            with col3:
                customer_type_filter = st.multiselect("Customer Type", df['customer_type'].unique())
            
            # Filter data
            filtered_df = df.copy()
            if status_filter:
                filtered_df = filtered_df[filtered_df['status'].isin(status_filter)]
            if region_filter:
                filtered_df = filtered_df[filtered_df['customer_region'].isin(region_filter)]
            if customer_type_filter:
                filtered_df = filtered_df[filtered_df['customer_type'].isin(customer_type_filter)]
            
            st.dataframe(
                filtered_df[[
                    'sale_id', 'date', 'customer_name', 'customer_type', 
                    'product_name', 'quantity', 'net_revenue', 'discount_percentage', 
                    'sales_rep_name', 'status'
                ]].head(100),
                use_container_width=True
            )
            
            st.markdown(f"*Showing {min(100, len(filtered_df))} of {len(filtered_df)} filtered sales*")
        
        with data_tab2:
            st.markdown("#### Customer Information")
            st.markdown("*The **Enhanced Approach** understands customer types, regions, and industries as semantic concepts*")
            
            customers_df = pd.DataFrame(metadata['customers'])
            st.dataframe(customers_df, use_container_width=True)
            
            # Customer distribution
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Customers by Type**")
                type_counts = customers_df['type'].value_counts()
                st.bar_chart(type_counts)
            
            with col2:
                st.markdown("**Customers by Region**")
                region_counts = customers_df['region'].value_counts()
                st.bar_chart(region_counts)
        
        with data_tab3:
            st.markdown("#### Product Catalog")
            st.markdown("*The **Enhanced Approach** knows product categories form hierarchies and have industry affinities*")
            
            products_df = pd.DataFrame(metadata['products'])
            st.dataframe(products_df, use_container_width=True)
            
            # Product analysis
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Products by Category**")
                cat_counts = products_df['category'].value_counts()
                st.bar_chart(cat_counts)
            
            with col2:
                st.markdown("**Price Distribution**")
                st.bar_chart(products_df.set_index('name')['price'])
        
        with data_tab4:
            st.markdown("#### Sales Representatives")
            st.markdown("*The **Enhanced Approach** understands rep experience influences performance*")
            
            reps_df = pd.DataFrame(metadata['sales_reps'])
            st.dataframe(reps_df, use_container_width=True)
            
            # Rep analysis
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Experience Distribution**")
                st.bar_chart(reps_df.set_index('name')['experience_years'])
            
            with col2:
                st.markdown("**Reps by Region**")
                region_counts = reps_df['region'].value_counts()
                st.bar_chart(region_counts)
        
        with data_tab5:
            st.markdown("#### Data Visualizations")
            
            # Revenue by region
            st.markdown("**Revenue by Region**")
            region_revenue = df.groupby('customer_region')['net_revenue'].sum().sort_values(ascending=False)
            st.bar_chart(region_revenue)
            
            # Revenue by customer type
            st.markdown("**Revenue by Customer Type**")
            type_revenue = df.groupby('customer_type')['net_revenue'].sum().sort_values(ascending=False)
            st.bar_chart(type_revenue)
            
            # Top products
            st.markdown("**Top 10 Products by Revenue**")
            product_revenue = df.groupby('product_name')['net_revenue'].sum().sort_values(ascending=False).head(10)
            st.bar_chart(product_revenue)
            
            # Sales over time
            st.markdown("**Sales Over Time**")
            df['date'] = pd.to_datetime(df['date'])
            daily_sales = df.groupby('date')['net_revenue'].sum().sort_index()
            st.line_chart(daily_sales)
        
        st.divider()
        
        # Knowledge Graph comparison
        st.markdown("### 🧠 How Enhanced Approach Sees This Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🔸 Basic Approach")
            st.code("""
# Flat table view:
sales_data.csv
- Just columns and rows
- No relationships
- No semantic meaning
- Limited to SQL-like queries
            """)
        
        with col2:
            st.markdown("#### 🔹 Enhanced Approach")
            st.code("""
# Knowledge Graph view:
Sale → soldTo → Customer
  ↓              ↓
Product    locatedIn → Region
  ↓              ↓
Category   belongsToIndustry → Industry

• Semantic relationships
• Multi-hop traversal
• Causal reasoning
• Domain knowledge
            """)
        
        st.info("""
        💡 **Key Insight**: The same data, but the Enhanced approach understands it as a connected knowledge 
        graph with semantic relationships. This enables answering "WHY" questions through causal reasoning!
        """)
        
    except FileNotFoundError as e:
        st.error("Data files not found. Please run setup scripts first.")
        st.code("""
python3 generate_data.py
python3 ontology.py
python3 knowledge_graph.py
        """)

def display_ontology_explanation():
    """Display explanation of ontology and knowledge graph benefits"""
    
    st.markdown("## 🎓 Understanding the Intelligence Boost")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📚 Ontology", "🕸️ Knowledge Graph", "🚀 Benefits", "🧠 Reasoning"])
    
    with tab1:
        st.markdown("""
        ### What is an Ontology?
        
        An **ontology** is a formal representation of knowledge that defines:
        
        - **Classes**: Types of entities (Customer, Product, Sale, etc.)
        - **Properties**: Attributes and relationships
        - **Hierarchies**: Parent-child relationships (Enterprise is-a Customer)
        - **Constraints**: Business rules and logic
        
        #### Our Sales Ontology:
        
        ```
        Customer
        ├── EnterpriseCustomer
        ├── MidMarketCustomer
        └── SMBCustomer
        
        Product
        ├── ElectronicsProduct
        └── FurnitureProduct
        
        Relationships:
        - Sale soldTo Customer
        - Sale soldBy SalesRepresentative
        - Customer locatedIn Region
        - Product belongsToCategory
        ```
        
        This structure gives the LLM **domain knowledge** and **semantic understanding**.
        """)
    
    with tab2:
        st.markdown("""
        ### What is a Knowledge Graph?
        
        A **Knowledge Graph** connects data through relationships:
        
        - **Nodes**: Entities (specific customers, products, sales)
        - **Edges**: Relationships (sold_to, located_in, belongs_to)
        - **Properties**: Attributes on nodes and edges
        
        #### Why It Matters:
        
        1. **Graph Traversal**: Follow relationships to find patterns
           - "Find products bought by enterprise customers in tech industry"
        
        2. **Semantic Queries**: Ask about meaning, not just columns
           - "What's the relationship between X and Y?"
        
        3. **Inference**: Derive new knowledge from existing relationships
           - If Customer → Region → SalesRep, can infer best rep for customer
        
        4. **Context**: Rich context around each entity
           - A customer isn't just data—it's connected to region, industry, purchases
        """)
    
    with tab3:
        st.markdown("""
        ### 🚀 How This Increases LLM Intelligence
        
        #### Without Ontology/KG (Basic Approach):
        ❌ Treats data as flat tables  
        ❌ No understanding of relationships  
        ❌ Limited to column-based queries  
        ❌ **Cannot answer WHY questions**  
        ❌ **No causal reasoning**  
        ❌ Shallow insights  
        
        #### With Ontology/KG (Enhanced Approach):
        ✅ Understands domain concepts  
        ✅ Knows semantic relationships  
        ✅ Can traverse connected data  
        ✅ **Answers WHY through causal reasoning**  
        ✅ **Performs diagnostic analysis**  
        ✅ Makes logical inferences  
        ✅ Provides deep, contextual insights  
        
        ---
        
        ### 🧠 The Reasoning Advantage
        
        **Example: "Why is Laptop Pro 15 selling more?"**
        
        **Basic Approach (No Reasoning):**
        - "Laptop Pro 15 has $627K revenue with 560 units sold"
        - Just states the numbers
        - No explanation of WHY
        
        **Enhanced Approach (With Reasoning):**
        1. **Traces relationships**: Laptop → Electronics → Enterprise Customers → Technology Industry
        2. **Applies domain knowledge**: Premium products ($1,299) fit enterprise budgets
        3. **Identifies patterns**: Tech companies need computers for their work
        4. **Considers context**: North America has many tech companies
        5. **Explains causation**: "Laptops sell well BECAUSE:
           - Technology companies are our largest customer segment
           - Enterprise customers have budgets for premium products
           - North America (our biggest region) has concentration of tech firms
           - Essential tool for their business operations
           - Sales reps can demonstrate ROI for work productivity"
        
        ---
        
        ### 🔍 Diagnostic Reasoning Examples
        
        **Q: "Why do experienced reps close bigger deals?"**
        
        **Reasoning Path:**
        ```
        Sales Rep → experienceYears → averageDealSize
              ↓
        operatesIn → Region → Customers → Industry
              ↓
        madeSale → Sale → netRevenue → Product
        ```
        
        **Causal Factors Identified:**
        1. Experience → Better customer relationships
        2. Experience → Understanding customer needs
        3. Regional knowledge → Industry expertise
        4. Trust building → Higher value sales
        5. Solution selling → Premium product positioning
        
        **Conclusion:** Experience enables consultative selling, not just transactional
        
        ---
        
        ### 📊 Pattern Recognition Through Graph Traversal
        
        The knowledge graph enables multi-hop reasoning:
        
        ```
        Product "Laptop Pro" 
          → belongsToCategory "Electronics"
          → soldTo "Acme Corp" (Enterprise)
          → locatedIn "North America"
          → belongsToIndustry "Technology"
          → soldBy "John Smith" (5 years exp)
        ```
        
        **Insights from Pattern:**
        - Premium electronics → Tech enterprises → North America
        - This pattern repeats consistently
        - **Causal reasoning**: Tech companies need electronics for operations
        - **Predictive**: Target similar companies with same products
        
        ---
        
        ### Real-World Impact:
        
        **Scenario:** *"Sales declining for Product X in Region Y"*
        
        **Basic Approach:**
        - "Product X revenue decreased 15% in Region Y"
        - End of analysis
        
        **Enhanced Approach with Reasoning:**
        1. **Analyzes relationships**: Product X → Customer segments in Region Y
        2. **Identifies changes**: Shift in customer industry mix
        3. **Traces causation**: New industries don't need Product X functionality
        4. **Cross-references**: Similar regions show same pattern
        5. **Root cause**: Market demographic shift
        6. **Recommendation**: Introduce Product Z for new industries OR target different regions
        
        **Result:** Actionable diagnosis with clear next steps!
        """)
    
    with tab4:
        st.markdown("""
        ### 🎯 Reasoning Rules in Our Ontology
        
        Our sales ontology includes reasoning concepts that enable causal analysis:
        
        #### Defined Reasoning Classes:
        
        - **HighValueCustomer**: Customer with average deal size > $5000
          - *Why matters*: Different sales approach needed
        
        - **FrequentBuyer**: Customer with multiple purchases  
          - *Why matters*: Loyalty patterns indicate satisfaction
        
        - **PremiumProduct**: Product with price > $400
          - *Why matters*: Targets specific customer segments
        
        - **ExperiencedRep**: Sales rep with > 5 years experience
          - *Why matters*: Higher success rates, bigger deals
        
        - **RegionalPreference**: Product-Region affinity pattern
          - *Why matters*: Cultural/market fit influences sales
        
        - **IndustryFit**: Product-Industry compatibility
          - *Why matters*: Functional needs drive purchases
        
        - **DiscountSensitive**: Customer segment responding to discounts
          - *Why matters*: Price optimization strategy
        
        #### Causal Relationship Properties:
        
        - **causedBy**: Direct causal relationship
        - **influences**: Factor that affects outcomes
        - **correlatesWith**: Statistical correlation
        - **indicatesPreference**: Shows buying patterns
        
        #### How LLM Uses These:
        
        When you ask "Why?", the LLM:
        1. Identifies relevant reasoning classes
        2. Traces causal properties in the graph
        3. Applies domain rules from ontology
        4. Explains relationships in business context
        5. Provides actionable insights
        
        This transforms correlation into causation!
        """)

def main():
    """Main application"""
    
    initialize_session_state()
    
    # Header
    st.markdown('<div class="main-header">🧠 Ontology & Knowledge Graph Intelligence Demo</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">See how semantic understanding transforms LLM-based data analysis</div>', unsafe_allow_html=True)
    
    # Sidebar
    setup_sidebar()
    
    # Check if setup is complete
    data_exists, kg_exists, has_api_key = check_setup()
    
    if not all([data_exists, kg_exists]):
        st.error("⚠️ Data not found. Please run setup scripts first:")
        st.code("""
python generate_data.py
python ontology.py
python knowledge_graph.py
        """)
        st.stop()
    
    if not has_api_key:
        st.error("⚠️ OpenAI API key not found. Please set it in .env file:")
        st.code("OPENAI_API_KEY=your_key_here")
        st.stop()
    
    # Initialize analyzers
    if not st.session_state.analyzers_ready:
        with st.spinner("Initializing analyzers..."):
            try:
                st.session_state.basic_analyzer = BasicAnalyzer()
                st.session_state.enhanced_analyzer = EnhancedAnalyzer()
                st.session_state.analyzers_ready = True
            except Exception as e:
                st.error(f"Error initializing analyzers: {e}")
                st.stop()
    
    # Main interface tabs
    tab1, tab2, tab3, tab5 = st.tabs(["💬 Interactive Chat", "📊 View Data", "📖 Learn More", "🚀 Scaling to Production"])
    
    with tab1:
        st.markdown("### Ask Questions About Sales Data")
        st.info("💡 **Try WHY questions** to see reasoning in action! The ontology enables causal analysis.")
        
        # Initialize question input value
        default_question = ""
        if 'selected_question' in st.session_state:
            default_question = st.session_state.selected_question
            st.session_state.current_question = default_question
            del st.session_state.selected_question
        elif 'current_question' in st.session_state:
            default_question = st.session_state.current_question
        
        # Question input
        question = st.text_input(
            "Enter your question:",
            value=default_question,
            placeholder="e.g., Why is Laptop Pro 15 our top-selling product?",
            key="question_input"
        )
        
        # Update current question in session state
        if question:
            st.session_state.current_question = question
        
        if st.button("🔍 Analyze", type="primary") and question:
            with st.spinner("Analyzing with both approaches..."):
                try:
                    # Get answers from both approaches
                    basic_answer, basic_meta = st.session_state.basic_analyzer.analyze(question)
                    enhanced_answer, enhanced_meta = st.session_state.enhanced_analyzer.analyze(question)
                    
                    # Display comparison
                    display_answer_comparison(
                        question,
                        {"answer": basic_answer, "metadata": basic_meta},
                        {"answer": enhanced_answer, "metadata": enhanced_meta}
                    )
                    
                    # Add to history
                    st.session_state.chat_history.append({
                        "question": question,
                        "basic": {"answer": basic_answer, "metadata": basic_meta},
                        "enhanced": {"answer": enhanced_answer, "metadata": enhanced_meta}
                    })
                    
                    # Save history to file
                    save_chat_history(st.session_state.chat_history)
                    
                except Exception as e:
                    st.error(f"Error during analysis: {e}")
        
        # Display chat history
        if st.session_state.chat_history:
            st.markdown("---")
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown("### 📜 Previous Questions")
            with col2:
                if st.button("🗑️ Clear History"):
                    st.session_state.chat_history = []
                    save_chat_history([])
                    st.rerun()
            
            # Show most recent questions first (up to 10)
            for i, item in enumerate(reversed(st.session_state.chat_history[-10:])):
                with st.expander(f"Q: {item['question']}", expanded=False):
                    display_answer_comparison(
                        item['question'],
                        item['basic'],
                        item['enhanced']
                    )
    
    with tab2:
        display_data_view()
    
    with tab3:
        display_ontology_explanation()
    
    with tab5:
        st.markdown("## 🚀 Scaling to Billions of Records")
        
        st.info("💡 **Key Question:** How does this work with terabytes of data and billions of records?")
        
        st.markdown("""
        ### 📊 The Challenge
        
        This demo works with **500 sales records** (~5,800 triples). Real enterprise scenarios involve:
        - 🔢 **Billions of transactions**
        - 💾 **Terabytes of data**
        - 👥 **Millions of entities**
        - ⚡ **Real-time queries**
        """)
        
        st.divider()
        
        st.markdown("""
        ### 🎯 Key Principle: Separation of Concerns
        
        The secret is **NOT loading everything into memory**. Instead:
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### 📚 Ontology Layer
            **Size:** Small & Static (~KB-MB)
            
            - Domain model definition
            - Reasoning rules
            - Class hierarchies
            
            ✅ **Stays constant regardless of data size**
            """)
        
        with col2:
            st.markdown("""
            #### 🕸️ Knowledge Graph Layer
            **Size:** Large & Dynamic (GB-TB)
            
            - Stored in graph database
            - Queried on-demand
            - Indexed for performance
            
            ✅ **Scales horizontally**
            """)
        
        st.divider()
        
        st.markdown("### 💡 How LLM Gets Context Without Loading Billions of Records")
        
        scale_tabs = st.tabs(["1️⃣ Pre-Compute Patterns", "2️⃣ Query on Demand", "3️⃣ Semantic Summaries"])
        
        with scale_tabs[0]:
            st.markdown("""
            #### Pre-Compute Reasoning Patterns
            
            Instead of reasoning over raw data, pre-compute common patterns nightly.
            
            **Example Pattern:**
            ```
            "Premium electronics sell 3x better to technology 
             companies in North America"
            ```
            
            ✅ **Result:** LLM gets insights, not billions of rows
            """)
        
        with scale_tabs[1]:
            st.markdown("""
            #### Query on Demand (Indexed, Fast)
            
            Use graph databases with proper indexing:
            - Indexed lookups: O(log n) instead of O(n)
            - Only returns what's needed
            - No full table scans
            - Distributed across nodes
            """)
        
        with scale_tabs[2]:
            st.markdown("""
            #### Provide Semantic Summaries to LLM
            
            **Don't send:** Raw transactions  
            **Do send:** Semantic patterns and statistics
            
            ```
            - Customer Segment Patterns:
              * Enterprise customers: avg $8.5K deals
              * SMB customers: avg $2.1K deals
            
            - Product-Industry Affinity:
              * Technology → Electronics (85%)
              * Healthcare → Furniture (72%)
            ```
            
            ✅ **LLM reasons about patterns, not individual records**
            """)
        
        st.divider()
        
        st.markdown("### ⚡ Performance at Scale")
        
        perf_col1, perf_col2 = st.columns(2)
        
        with perf_col1:
            st.markdown("""
            #### Demo Setup
            - **Data:** 500 records
            - **Storage:** 5 MB in memory
            - **Query Time:** 0.01 seconds
            - **Cost:** $0/month
            """)
        
        with perf_col2:
            st.markdown("""
            #### Production Setup
            - **Data:** 1 Billion records
            - **Storage:** 500 GB (compressed)
            - **Query Time:** 0.05 seconds
            - **Cost:** $500-2000/month
            """)
        
        st.divider()
        
        st.markdown("### 🛠️ Production Technology Stack")
        
        tech_col1, tech_col2, tech_col3 = st.columns(3)
        
        with tech_col1:
            st.markdown("""
            #### Graph Databases
            - **Neo4j**
            - **Amazon Neptune**
            - **TigerGraph**
            
            **Why:** Billions of nodes
            """)
        
        with tech_col2:
            st.markdown("""
            #### Processing
            - **Apache Spark**
            - **Kafka**
            - **Redis**
            
            **Why:** Distributed processing
            """)
        
        with tech_col3:
            st.markdown("""
            #### Vector Search
            - **FAISS**
            - **Pinecone**
            - **Milvus**
            
            **Why:** Semantic search at scale
            """)
        
        st.divider()
        
        st.success("""
        ### 🎯 Key Takeaways
        
        **1. Ontology stays small** - It's the schema (KB-MB range)
        
        **2. Knowledge Graph scales** - Graph databases handle billions
        
        **3. LLM sees patterns** - Not raw data
        
        **4. Same intelligence boost** - Semantic understanding at any scale!
        """)
        
        st.info("""
        💡 **Bottom Line:** This demo shows the *concept*. For production with billions of 
        records, use the same concepts with industrial-strength infrastructure: graph databases, 
        distributed processing, and semantic layers.
        
        The intelligence boost comes from **semantic understanding**, not loading all data!
        """)
        
        st.caption("📚 **Learn More:** See SCALABILITY.md on GitHub for detailed implementation examples")

if __name__ == "__main__":
    main()
