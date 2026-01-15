# Contributing to Ontology & Knowledge Graph Demo

Thank you for your interest in contributing to this project! This document provides guidelines for contributing.

## 🛠️ Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone <your-fork-url>
   cd Ontology
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Add your OpenAI API key to .env
   ```

5. **Generate test data**
   ```bash
   python generate_data.py
   python ontology.py
   python knowledge_graph.py
   ```

## 📝 Code Style

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and modular

## 🧪 Testing

Before submitting a pull request:

1. **Test data generation**
   ```bash
   python generate_data.py
   python ontology.py
   python knowledge_graph.py
   ```

2. **Test the Streamlit app**
   ```bash
   streamlit run app.py
   ```

3. **Test both analyzers**
   - Try sample questions from the sidebar
   - Verify both Basic and Enhanced approaches work
   - Check that prompts are displayed correctly

## 🔧 Areas for Contribution

### High Priority
- [ ] Add unit tests for core functions
- [ ] Add integration tests for analyzers
- [ ] Improve error handling and logging
- [ ] Add more sample questions
- [ ] Enhance SPARQL queries

### Medium Priority
- [ ] Add knowledge graph visualization
- [ ] Support for additional data sources
- [ ] Export functionality for results
- [ ] Performance optimizations
- [ ] Docker containerization

### Low Priority
- [ ] Additional reasoning rules
- [ ] More domain ontologies
- [ ] Advanced analytics features
- [ ] Multi-language support

## 📋 Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clear, concise commit messages
   - Keep commits focused and atomic
   - Update documentation as needed

3. **Test thoroughly**
   - Ensure all existing functionality still works
   - Test your new feature with various inputs
   - Check for edge cases

4. **Update documentation**
   - Update README.md if adding new features
   - Add inline code comments for complex logic
   - Update REASONING_DEMO.md if adding reasoning capabilities

5. **Submit pull request**
   - Provide a clear description of changes
   - Reference any related issues
   - Include screenshots for UI changes

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Description**: Clear description of the bug
2. **Steps to reproduce**: Detailed steps to reproduce the issue
3. **Expected behavior**: What you expected to happen
4. **Actual behavior**: What actually happened
5. **Environment**: OS, Python version, dependency versions
6. **Screenshots**: If applicable
7. **Error messages**: Full error traceback

## 💡 Feature Requests

For feature requests, please include:

1. **Use case**: Why this feature is needed
2. **Proposed solution**: How you envision it working
3. **Alternatives**: Other solutions you've considered
4. **Additional context**: Any other relevant information

## 🔒 Security

If you discover a security vulnerability:

1. **DO NOT** open a public issue
2. Email the maintainers directly
3. Include details of the vulnerability
4. Allow time for a fix before public disclosure

## 📜 Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Assume good intentions
- Keep discussions professional

## 📄 License

By contributing, you agree that your contributions will be licensed under the same license as the project.

## ❓ Questions?

If you have questions about contributing:
- Check existing issues and pull requests
- Review the documentation
- Open a discussion thread

Thank you for contributing! 🎉
