"""
Knowledge Graph Builder
Populates the knowledge graph with sales data based on the ontology
"""
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, OWL, XSD
import pandas as pd
import json
from ontology import SalesOntology

class KnowledgeGraphBuilder:
    """Build and query knowledge graph from sales data"""
    
    def __init__(self, ontology: SalesOntology):
        self.ontology = ontology
        self.graph = Graph()
        
        # Copy ontology to knowledge graph
        for triple in ontology.graph:
            self.graph.add(triple)
        
        # Bind namespaces
        self.SALES = ontology.SALES
        self.graph.bind("sales", self.SALES)
        self.graph.bind("owl", OWL)
    
    def load_sales_data(self, csv_path="data/sales_data.csv", metadata_path="data/metadata.json"):
        """Load sales data and populate the knowledge graph"""
        
        df = pd.read_csv(csv_path)
        
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        # Add entities
        self._add_regions()
        self._add_industries()
        self._add_categories()
        self._add_products(metadata['products'])
        self._add_customers(metadata['customers'])
        self._add_sales_reps(metadata['sales_reps'])
        self._add_sales(df)
        
        print(f"Knowledge graph populated with {len(self.graph)} triples")
    
    def _add_regions(self):
        """Add region entities"""
        regions = ["North America", "Europe", "Asia"]
        for region in regions:
            region_uri = self.SALES[region.replace(" ", "_")]
            self.graph.add((region_uri, RDF.type, self.SALES.Region))
            self.graph.add((region_uri, self.SALES.regionName, Literal(region)))
    
    def _add_industries(self):
        """Add industry entities"""
        industries = ["Technology", "Consulting", "Creative", "Finance", "Retail", 
                     "Manufacturing", "Healthcare", "Education"]
        for industry in industries:
            industry_uri = self.SALES[industry]
            self.graph.add((industry_uri, RDF.type, self.SALES.Industry))
            self.graph.add((industry_uri, self.SALES.industryName, Literal(industry)))
    
    def _add_categories(self):
        """Add product categories"""
        categories = {
            "Electronics": ["Computers", "Accessories", "Displays", "Mobile Devices"],
            "Furniture": ["Seating", "Desks", "Lighting", "Storage"]
        }
        
        for category, subcategories in categories.items():
            cat_uri = self.SALES[category]
            self.graph.add((cat_uri, RDF.type, self.SALES.Category))
            self.graph.add((cat_uri, self.SALES.categoryName, Literal(category)))
            
            for subcat in subcategories:
                subcat_uri = self.SALES[subcat.replace(" ", "_")]
                self.graph.add((subcat_uri, RDF.type, self.SALES.Category))
                self.graph.add((subcat_uri, self.SALES.categoryName, Literal(subcat)))
                self.graph.add((subcat_uri, self.SALES.hasSubcategory, cat_uri))
    
    def _add_products(self, products):
        """Add product entities"""
        for product in products:
            prod_uri = self.SALES[product['id']]
            
            # Type based on category
            if product['category'] == 'Electronics':
                self.graph.add((prod_uri, RDF.type, self.SALES.ElectronicsProduct))
            else:
                self.graph.add((prod_uri, RDF.type, self.SALES.FurnitureProduct))
            
            self.graph.add((prod_uri, self.SALES.productId, Literal(product['id'])))
            self.graph.add((prod_uri, self.SALES.productName, Literal(product['name'])))
            self.graph.add((prod_uri, self.SALES.unitPrice, Literal(product['price'], datatype=XSD.decimal)))
            
            # Link to category
            cat_uri = self.SALES[product['category']]
            self.graph.add((prod_uri, self.SALES.belongsToCategory, cat_uri))
            
            subcat_uri = self.SALES[product['subcategory'].replace(" ", "_")]
            self.graph.add((prod_uri, self.SALES.belongsToCategory, subcat_uri))
    
    def _add_customers(self, customers):
        """Add customer entities"""
        for customer in customers:
            cust_uri = self.SALES[customer['id']]
            
            # Type based on size
            if customer['type'] == 'Enterprise':
                self.graph.add((cust_uri, RDF.type, self.SALES.EnterpriseCustomer))
            elif customer['type'] == 'SMB':
                self.graph.add((cust_uri, RDF.type, self.SALES.SMBCustomer))
            else:
                self.graph.add((cust_uri, RDF.type, self.SALES.MidMarketCustomer))
            
            self.graph.add((cust_uri, self.SALES.customerId, Literal(customer['id'])))
            self.graph.add((cust_uri, self.SALES.customerName, Literal(customer['name'])))
            self.graph.add((cust_uri, self.SALES.customerType, Literal(customer['type'])))
            
            # Link to region and industry
            region_uri = self.SALES[customer['region'].replace(" ", "_")]
            self.graph.add((cust_uri, self.SALES.locatedIn, region_uri))
            
            industry_uri = self.SALES[customer['industry']]
            self.graph.add((cust_uri, self.SALES.belongsToIndustry, industry_uri))
    
    def _add_sales_reps(self, sales_reps):
        """Add sales representative entities"""
        for rep in sales_reps:
            rep_uri = self.SALES[rep['id']]
            self.graph.add((rep_uri, RDF.type, self.SALES.SalesRepresentative))
            self.graph.add((rep_uri, self.SALES.repId, Literal(rep['id'])))
            self.graph.add((rep_uri, self.SALES.repName, Literal(rep['name'])))
            self.graph.add((rep_uri, self.SALES.experienceYears, Literal(rep['experience_years'], datatype=XSD.integer)))
            
            region_uri = self.SALES[rep['region'].replace(" ", "_")]
            self.graph.add((rep_uri, self.SALES.operatesIn, region_uri))
    
    def _add_sales(self, df):
        """Add sale transaction entities"""
        for _, row in df.iterrows():
            sale_uri = self.SALES[row['sale_id']]
            self.graph.add((sale_uri, RDF.type, self.SALES.Sale))
            
            # Sale attributes
            self.graph.add((sale_uri, self.SALES.saleId, Literal(row['sale_id'])))
            self.graph.add((sale_uri, self.SALES.saleDate, Literal(row['date'], datatype=XSD.date)))
            self.graph.add((sale_uri, self.SALES.quantity, Literal(row['quantity'], datatype=XSD.integer)))
            self.graph.add((sale_uri, self.SALES.grossRevenue, Literal(row['gross_revenue'], datatype=XSD.decimal)))
            self.graph.add((sale_uri, self.SALES.netRevenue, Literal(row['net_revenue'], datatype=XSD.decimal)))
            self.graph.add((sale_uri, self.SALES.discountPercentage, Literal(row['discount_percentage'], datatype=XSD.decimal)))
            self.graph.add((sale_uri, self.SALES.status, Literal(row['status'])))
            
            # Relationships
            cust_uri = self.SALES[row['customer_id']]
            self.graph.add((sale_uri, self.SALES.soldTo, cust_uri))
            
            prod_uri = self.SALES[row['product_id']]
            self.graph.add((sale_uri, self.SALES.productSold, prod_uri))
            
            rep_uri = self.SALES[row['sales_rep_id']]
            self.graph.add((sale_uri, self.SALES.soldBy, rep_uri))
    
    def query_sparql(self, query):
        """Execute SPARQL query"""
        return self.graph.query(query)
    
    def get_insights(self):
        """Generate analytical insights using SPARQL queries"""
        
        insights = {}
        
        # Total revenue by region
        query_region = """
        PREFIX sales: <http://example.org/sales#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        
        SELECT ?regionName (SUM(?revenue) AS ?totalRevenue) (COUNT(?sale) AS ?saleCount)
        WHERE {
            ?sale a sales:Sale ;
                  sales:soldTo ?customer ;
                  sales:netRevenue ?revenue ;
                  sales:status "Completed" .
            ?customer sales:locatedIn ?region .
            ?region sales:regionName ?regionName .
        }
        GROUP BY ?regionName
        ORDER BY DESC(?totalRevenue)
        """
        
        results = self.query_sparql(query_region)
        insights['revenue_by_region'] = [
            {
                'region': str(row.regionName),
                'revenue': float(row.totalRevenue),
                'sales': int(row.saleCount)
            }
            for row in results
        ]
        
        # Top products
        query_products = """
        PREFIX sales: <http://example.org/sales#>
        
        SELECT ?productName (SUM(?revenue) AS ?totalRevenue) (SUM(?quantity) AS ?totalQuantity)
        WHERE {
            ?sale a sales:Sale ;
                  sales:productSold ?product ;
                  sales:netRevenue ?revenue ;
                  sales:quantity ?quantity ;
                  sales:status "Completed" .
            ?product sales:productName ?productName .
        }
        GROUP BY ?productName
        ORDER BY DESC(?totalRevenue)
        LIMIT 5
        """
        
        results = self.query_sparql(query_products)
        insights['top_products'] = [
            {
                'product': str(row.productName),
                'revenue': float(row.totalRevenue),
                'units_sold': int(row.totalQuantity)
            }
            for row in results
        ]
        
        # Sales by customer type
        query_customer_type = """
        PREFIX sales: <http://example.org/sales#>
        
        SELECT ?customerType (SUM(?revenue) AS ?totalRevenue) (AVG(?revenue) AS ?avgRevenue)
        WHERE {
            ?sale a sales:Sale ;
                  sales:soldTo ?customer ;
                  sales:netRevenue ?revenue ;
                  sales:status "Completed" .
            ?customer sales:customerType ?customerType .
        }
        GROUP BY ?customerType
        ORDER BY DESC(?totalRevenue)
        """
        
        results = self.query_sparql(query_customer_type)
        insights['revenue_by_customer_type'] = [
            {
                'customer_type': str(row.customerType),
                'total_revenue': float(row.totalRevenue),
                'avg_revenue': float(row.avgRevenue)
            }
            for row in results
        ]
        
        return insights
    
    def get_reasoning_insights(self):
        """Generate causal and diagnostic insights through reasoning"""
        
        reasoning = {}
        
        # Why are certain products selling more? - Product-Customer affinity
        query_product_customer_fit = """
        PREFIX sales: <http://example.org/sales#>
        
        SELECT ?productName ?customerType ?category 
               (COUNT(?sale) AS ?salesCount) 
               (SUM(?revenue) AS ?totalRevenue)
               (AVG(?revenue) AS ?avgDeal)
        WHERE {
            ?sale a sales:Sale ;
                  sales:soldTo ?customer ;
                  sales:productSold ?product ;
                  sales:netRevenue ?revenue ;
                  sales:status "Completed" .
            ?customer sales:customerType ?customerType .
            ?product sales:productName ?productName ;
                     sales:belongsToCategory ?cat .
            ?cat sales:categoryName ?category .
        }
        GROUP BY ?productName ?customerType ?category
        HAVING (COUNT(?sale) > 5)
        ORDER BY DESC(?totalRevenue)
        """
        
        results = self.query_sparql(query_product_customer_fit)
        reasoning['product_customer_fit'] = [
            {
                'product': str(row.productName),
                'customer_type': str(row.customerType),
                'category': str(row.category),
                'sales_count': int(row.salesCount),
                'revenue': float(row.totalRevenue),
                'avg_deal': float(row.avgDeal)
            }
            for i, row in enumerate(results) if i < 10
        ]
        
        # Why certain regions perform better? - Regional patterns with industries
        query_regional_patterns = """
        PREFIX sales: <http://example.org/sales#>
        
        SELECT ?regionName ?industry ?productName
               (COUNT(?sale) AS ?salesCount)
               (SUM(?revenue) AS ?revenue)
        WHERE {
            ?sale a sales:Sale ;
                  sales:soldTo ?customer ;
                  sales:productSold ?product ;
                  sales:netRevenue ?revenue ;
                  sales:status "Completed" .
            ?customer sales:locatedIn ?region ;
                     sales:belongsToIndustry ?ind .
            ?region sales:regionName ?regionName .
            ?ind sales:industryName ?industry .
            ?product sales:productName ?productName .
        }
        GROUP BY ?regionName ?industry ?productName
        HAVING (COUNT(?sale) > 3)
        ORDER BY DESC(?revenue)
        """
        
        results = self.query_sparql(query_regional_patterns)
        reasoning['regional_patterns'] = [
            {
                'region': str(row.regionName),
                'industry': str(row.industry),
                'product': str(row.productName),
                'sales_count': int(row.salesCount),
                'revenue': float(row.revenue)
            }
            for i, row in enumerate(results) if i < 10
        ]
        
        # Sales rep effectiveness - experience impact
        query_rep_effectiveness = """
        PREFIX sales: <http://example.org/sales#>
        
        SELECT ?repName ?experience ?regionName
               (COUNT(?sale) AS ?salesCount)
               (SUM(?revenue) AS ?totalRevenue)
               (AVG(?revenue) AS ?avgDeal)
        WHERE {
            ?sale a sales:Sale ;
                  sales:soldBy ?rep ;
                  sales:netRevenue ?revenue ;
                  sales:status "Completed" .
            ?rep sales:repName ?repName ;
                 sales:experienceYears ?experience ;
                 sales:operatesIn ?region .
            ?region sales:regionName ?regionName .
        }
        GROUP BY ?repName ?experience ?regionName
        ORDER BY DESC(?avgDeal)
        """
        
        results = self.query_sparql(query_rep_effectiveness)
        reasoning['rep_effectiveness'] = [
            {
                'rep': str(row.repName),
                'experience': int(row.experience),
                'region': str(row.regionName),
                'sales_count': int(row.salesCount),
                'revenue': float(row.totalRevenue),
                'avg_deal': float(row.avgDeal)
            }
            for row in results
        ]
        
        # Discount patterns and effectiveness
        query_discount_patterns = """
        PREFIX sales: <http://example.org/sales#>
        
        SELECT ?customerType 
               (AVG(?discount) AS ?avgDiscount)
               (AVG(?revenue) AS ?avgRevenue)
               (COUNT(?sale) AS ?salesCount)
        WHERE {
            ?sale a sales:Sale ;
                  sales:soldTo ?customer ;
                  sales:discountPercentage ?discount ;
                  sales:netRevenue ?revenue ;
                  sales:status "Completed" .
            ?customer sales:customerType ?customerType .
            FILTER(?discount > 0)
        }
        GROUP BY ?customerType
        """
        
        results = self.query_sparql(query_discount_patterns)
        reasoning['discount_patterns'] = [
            {
                'customer_type': str(row.customerType),
                'avg_discount': float(row.avgDiscount),
                'avg_revenue': float(row.avgRevenue),
                'sales_count': int(row.salesCount)
            }
            for row in results
        ]
        
        return reasoning
    
    def save(self, filepath="data/knowledge_graph.ttl"):
        """Save knowledge graph to file"""
        self.graph.serialize(destination=filepath, format="turtle")
        print(f"Knowledge graph saved to {filepath}")

def build_knowledge_graph():
    """Main function to build knowledge graph"""
    import os
    os.makedirs("data", exist_ok=True)
    
    # Create ontology
    ontology = SalesOntology()
    
    # Build knowledge graph
    kg = KnowledgeGraphBuilder(ontology)
    kg.load_sales_data()
    kg.save()
    
    # Get some insights
    print("\n=== Knowledge Graph Insights ===")
    insights = kg.get_insights()
    
    print("\nRevenue by Region:")
    for item in insights['revenue_by_region']:
        print(f"  {item['region']}: ${item['revenue']:,.2f} ({item['sales']} sales)")
    
    print("\nTop 5 Products:")
    for item in insights['top_products']:
        print(f"  {item['product']}: ${item['revenue']:,.2f} ({item['units_sold']} units)")
    
    print("\nRevenue by Customer Type:")
    for item in insights['revenue_by_customer_type']:
        print(f"  {item['customer_type']}: ${item['total_revenue']:,.2f} (avg: ${item['avg_revenue']:,.2f})")
    
    return kg

if __name__ == "__main__":
    build_knowledge_graph()
