# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.0.0] - 2026-01-15

### Added
- Initial release of Ontology & Knowledge Graph Intelligence Demo
- Streamlit web interface with three main tabs:
  - Interactive Chat for comparing Basic vs Enhanced approaches
  - View Data for exploring sales data with visualizations
  - Learn More for understanding ontology and knowledge graph concepts
- Basic Analyzer: Traditional LLM analysis with raw CSV data
- Enhanced Analyzer: LLM + Ontology + Knowledge Graph approach
- Sales domain ontology with 16 classes and 31 properties
- Reasoning capabilities with 9 reasoning concepts:
  - HighValueCustomer, FrequentBuyer, PremiumProduct
  - ExperiencedRep, RegionalPreference, IndustryFit
  - DiscountSensitive, SeasonalDemand, CustomerRetention
- Causal properties for "WHY" question answering:
  - causedBy, influences, correlatesWith, indicatesPreference
- Knowledge Graph with semantic triples and SPARQL queries
- Sample sales data generator (500 transactions)
- LLM prompt visibility feature showing actual prompts sent
- Data visualization with charts and filters
- Persistent chat history stored in JSON file
- Sample questions in sidebar for quick testing
- Comprehensive error handling and logging

### Features
- Side-by-side comparison of Basic vs Enhanced approaches
- Real-time LLM analysis with GPT-4
- Interactive question answering with causal reasoning
- Data exploration with multiple views (Sales, Customers, Products, Reps)
- Visual analytics with bar charts and time series
- Expandable prompt viewers for transparency
- Clear chat history functionality
- Auto-save chat history to file

### Technical Details
- Python 3.8+ support
- OpenAI GPT-4 integration
- RDFLib for ontology and knowledge graph
- SPARQL queries for semantic insights
- Streamlit for interactive UI
- Pandas for data manipulation
- Environment variable configuration

### Documentation
- Comprehensive README with setup instructions
- REASONING_DEMO explaining causal analysis capabilities
- Code comments and docstrings throughout
- Sample questions demonstrating features
- In-app educational content

### Infrastructure
- requirements.txt for dependency management
- .env.example for configuration template
- .gitignore for security and cleanliness
- Automated setup scripts
- Data directory structure

## [Unreleased]

### Planned Features
- [ ] Unit and integration tests
- [ ] Knowledge graph visualization
- [ ] Docker containerization
- [ ] Additional domain ontologies
- [ ] Export functionality for results
- [ ] Performance optimizations
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Real-time data streaming
- [ ] Custom ontology builder UI

### Known Issues
- None currently reported

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on contributing to this project.

## Version History

### Version Numbering
This project follows [Semantic Versioning](https://semver.org/):
- MAJOR version for incompatible API changes
- MINOR version for new functionality in a backwards compatible manner
- PATCH version for backwards compatible bug fixes
