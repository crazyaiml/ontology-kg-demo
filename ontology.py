"""
Sales Domain Ontology Definition
This module defines the ontology for the sales domain using RDF/OWL
"""
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, OWL, XSD
import json

class SalesOntology:
    """Define and manage the Sales domain ontology"""
    
    def __init__(self):
        self.graph = Graph()
        
        # Define namespaces
        self.SALES = Namespace("http://example.org/sales#")
        self.graph.bind("sales", self.SALES)
        self.graph.bind("owl", OWL)
        self.graph.bind("rdfs", RDFS)
        
        # Build the ontology
        self._define_classes()
        self._define_properties()
        self._define_axioms()
        self._define_reasoning_rules()
    
    def _define_classes(self):
        """Define the main classes in our ontology"""
        
        # Core classes
        classes = {
            "Sale": "A sales transaction",
            "Customer": "A customer entity",
            "Product": "A product or service",
            "SalesRepresentative": "A sales team member",
            "Region": "Geographical region",
            "Category": "Product category",
            "Industry": "Customer industry sector"
        }
        
        for class_name, description in classes.items():
            class_uri = self.SALES[class_name]
            self.graph.add((class_uri, RDF.type, OWL.Class))
            self.graph.add((class_uri, RDFS.label, Literal(class_name)))
            self.graph.add((class_uri, RDFS.comment, Literal(description)))
        
        # Subclasses
        self.graph.add((self.SALES.EnterpriseCustomer, RDFS.subClassOf, self.SALES.Customer))
        self.graph.add((self.SALES.SMBCustomer, RDFS.subClassOf, self.SALES.Customer))
        self.graph.add((self.SALES.MidMarketCustomer, RDFS.subClassOf, self.SALES.Customer))
        
        self.graph.add((self.SALES.ElectronicsProduct, RDFS.subClassOf, self.SALES.Product))
        self.graph.add((self.SALES.FurnitureProduct, RDFS.subClassOf, self.SALES.Product))
    
    def _define_properties(self):
        """Define object and data properties"""
        
        # Object Properties (relationships between entities)
        object_properties = {
            "soldTo": ("Sale", "Customer", "Links a sale to a customer"),
            "soldBy": ("Sale", "SalesRepresentative", "Links a sale to the sales rep"),
            "productSold": ("Sale", "Product", "Links a sale to the product"),
            "locatedIn": ("Customer", "Region", "Customer's geographical location"),
            "operatesIn": ("SalesRepresentative", "Region", "Region where sales rep operates"),
            "belongsToCategory": ("Product", "Category", "Product's category"),
            "belongsToIndustry": ("Customer", "Industry", "Customer's industry"),
            "hasSubcategory": ("Category", "Category", "Hierarchical category relationship"),
        }
        
        for prop_name, (domain, range_class, description) in object_properties.items():
            prop_uri = self.SALES[prop_name]
            self.graph.add((prop_uri, RDF.type, OWL.ObjectProperty))
            self.graph.add((prop_uri, RDFS.domain, self.SALES[domain]))
            self.graph.add((prop_uri, RDFS.range, self.SALES[range_class]))
            self.graph.add((prop_uri, RDFS.comment, Literal(description)))
        
        # Data Properties (attributes)
        data_properties = {
            "saleId": ("Sale", XSD.string, "Unique sale identifier"),
            "saleDate": ("Sale", XSD.date, "Date of sale"),
            "quantity": ("Sale", XSD.integer, "Quantity sold"),
            "grossRevenue": ("Sale", XSD.decimal, "Revenue before discount"),
            "netRevenue": ("Sale", XSD.decimal, "Revenue after discount"),
            "discountPercentage": ("Sale", XSD.decimal, "Discount applied"),
            "status": ("Sale", XSD.string, "Sale status"),
            
            "customerId": ("Customer", XSD.string, "Customer identifier"),
            "customerName": ("Customer", XSD.string, "Customer name"),
            "customerType": ("Customer", XSD.string, "Customer business size"),
            
            "productId": ("Product", XSD.string, "Product identifier"),
            "productName": ("Product", XSD.string, "Product name"),
            "unitPrice": ("Product", XSD.decimal, "Product unit price"),
            
            "repId": ("SalesRepresentative", XSD.string, "Sales rep identifier"),
            "repName": ("SalesRepresentative", XSD.string, "Sales rep name"),
            "experienceYears": ("SalesRepresentative", XSD.integer, "Years of experience"),
            
            "regionName": ("Region", XSD.string, "Region name"),
            "categoryName": ("Category", XSD.string, "Category name"),
            "industryName": ("Industry", XSD.string, "Industry name"),
        }
        
        for prop_name, (domain, range_type, description) in data_properties.items():
            prop_uri = self.SALES[prop_name]
            self.graph.add((prop_uri, RDF.type, OWL.DatatypeProperty))
            self.graph.add((prop_uri, RDFS.domain, self.SALES[domain]))
            self.graph.add((prop_uri, RDFS.range, range_type))
            self.graph.add((prop_uri, RDFS.comment, Literal(description)))
    
    def _define_axioms(self):
        """Define logical axioms and constraints"""
        
        # Inverse properties
        self.graph.add((self.SALES.soldTo, OWL.inverseOf, self.SALES.hasPurchase))
        self.graph.add((self.SALES.soldBy, OWL.inverseOf, self.SALES.madeSale))
        
        # Functional properties (single value)
        self.graph.add((self.SALES.saleDate, RDF.type, OWL.FunctionalProperty))
        self.graph.add((self.SALES.saleId, RDF.type, OWL.FunctionalProperty))
    
    def _define_reasoning_rules(self):
        """Define reasoning rules for causal and diagnostic analysis"""
        
        # Define reasoning concepts
        rules = {
            "HighValueCustomer": "Customer with average deal size > $5000",
            "FrequentBuyer": "Customer with multiple purchases",
            "PremiumProduct": "Product with price > $400",
            "BudgetProduct": "Product with price < $100",
            "ExperiencedRep": "Sales rep with > 5 years experience",
            "SeasonalPattern": "Sales influenced by time period",
            "RegionalPreference": "Product-Region affinity pattern",
            "IndustryFit": "Product-Industry compatibility",
            "DiscountSensitive": "Customer segment responding to discounts",
        }
        
        for concept, description in rules.items():
            concept_uri = self.SALES[concept]
            self.graph.add((concept_uri, RDF.type, OWL.Class))
            self.graph.add((concept_uri, RDFS.comment, Literal(description)))
        
        # Causal relationship properties
        causal_props = {
            "causedBy": "Indicates causal relationship",
            "influences": "Indicates influence factor",
            "correlatesWith": "Indicates correlation",
            "indicatesPreference": "Shows preference pattern",
        }
        
        for prop, desc in causal_props.items():
            prop_uri = self.SALES[prop]
            self.graph.add((prop_uri, RDF.type, OWL.ObjectProperty))
            self.graph.add((prop_uri, RDFS.comment, Literal(desc)))
    
    def save(self, filepath="data/sales_ontology.ttl"):
        """Save ontology to file"""
        self.graph.serialize(destination=filepath, format="turtle")
        print(f"Ontology saved to {filepath}")
    
    def get_ontology_summary(self):
        """Get a summary of the ontology"""
        classes = set()
        properties = set()
        
        for s, p, o in self.graph:
            if p == RDF.type:
                if o == OWL.Class:
                    classes.add(str(s).split("#")[-1])
                elif o in [OWL.ObjectProperty, OWL.DatatypeProperty]:
                    properties.add(str(s).split("#")[-1])
        
        return {
            "classes": sorted(classes),
            "properties": sorted(properties),
            "total_triples": len(self.graph)
        }

def create_ontology():
    """Create and save the sales ontology"""
    import os
    os.makedirs("data", exist_ok=True)
    
    ontology = SalesOntology()
    ontology.save()
    
    summary = ontology.get_ontology_summary()
    print("\nOntology Summary:")
    print(f"Classes: {len(summary['classes'])}")
    for cls in summary['classes']:
        print(f"  - {cls}")
    print(f"\nProperties: {len(summary['properties'])}")
    print(f"Total Triples: {summary['total_triples']}")
    
    return ontology

if __name__ == "__main__":
    create_ontology()
