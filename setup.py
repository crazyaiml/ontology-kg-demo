"""
Setup script to initialize the entire demo
Run this to set up data, ontology, and knowledge graph
"""
import os
import sys

def setup_demo():
    """Run all setup steps"""
    
    print("="*80)
    print("🧠 Ontology & Knowledge Graph Demo - Setup")
    print("="*80)
    
    # Check for .env file
    print("\n1️⃣  Checking environment configuration...")
    if not os.path.exists(".env"):
        print("   ⚠️  .env file not found")
        print("   Creating .env from .env.example...")
        
        if os.path.exists(".env.example"):
            import shutil
            shutil.copy(".env.example", ".env")
            print("   ✅ .env created. Please add your OpenAI API key!")
            print("   Edit .env and add: OPENAI_API_KEY=sk-your-key-here")
            
            response = input("\n   Have you added your API key? (y/n): ")
            if response.lower() != 'y':
                print("   Please add your API key to .env and run setup again.")
                return False
        else:
            print("   ❌ .env.example not found")
            return False
    else:
        # Check if API key is set
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key or api_key == "your_openai_api_key_here":
            print("   ⚠️  OpenAI API key not configured in .env")
            print("   Please edit .env and add your API key")
            return False
        else:
            print("   ✅ Environment configured")
    
    # Create data directory
    print("\n2️⃣  Creating data directory...")
    os.makedirs("data", exist_ok=True)
    print("   ✅ Data directory ready")
    
    # Generate sales data
    print("\n3️⃣  Generating sample sales data...")
    try:
        from generate_data import generate_sales_data
        df, metadata = generate_sales_data(500)
        print("   ✅ Sales data generated")
    except Exception as e:
        print(f"   ❌ Error generating data: {e}")
        return False
    
    # Create ontology
    print("\n4️⃣  Creating sales domain ontology...")
    try:
        from ontology import create_ontology
        ontology = create_ontology()
        print("   ✅ Ontology created")
    except Exception as e:
        print(f"   ❌ Error creating ontology: {e}")
        return False
    
    # Build knowledge graph
    print("\n5️⃣  Building knowledge graph...")
    try:
        from knowledge_graph import build_knowledge_graph
        kg = build_knowledge_graph()
        print("   ✅ Knowledge graph built")
    except Exception as e:
        print(f"   ❌ Error building knowledge graph: {e}")
        return False
    
    # Verify files
    print("\n6️⃣  Verifying setup...")
    required_files = [
        "data/sales_data.csv",
        "data/metadata.json",
        "data/sales_ontology.ttl",
        "data/knowledge_graph.ttl"
    ]
    
    all_good = True
    for filepath in required_files:
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            print(f"   ✅ {filepath} ({size:,} bytes)")
        else:
            print(f"   ❌ {filepath} - NOT FOUND")
            all_good = False
    
    if all_good:
        print("\n" + "="*80)
        print("🎉 Setup Complete!")
        print("="*80)
        print("\n🚀 To run the demo:")
        print("   streamlit run app.py")
        print("\n💡 The browser will open at http://localhost:8501")
        print("\n📖 See README.md for more information")
        print("="*80)
        return True
    else:
        print("\n❌ Setup incomplete - some files are missing")
        return False

if __name__ == "__main__":
    success = setup_demo()
    sys.exit(0 if success else 1)
