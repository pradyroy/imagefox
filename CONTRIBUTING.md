# 🤝 Contributing to imagefox

Thanks for your interest in contributing!

We welcome:
- 🔧 Bug fixes
- 🌟 New features or enhancements
- 🧪 Unit tests
- 🧹 Code cleanup or documentation

## 🛠️ Development Setup

```bash
git clone https://github.com/pradyroy/imagefox.git
cd imagefox
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 🧪 Testing

This project uses `pytest` for testing. Run tests with:

```bash
pytest tests/
```

Please include unit tests for any new functionality.

## 💬 Code Guidelines

- Follow [PEP8](https://peps.python.org/pep-0008/)
- Use clear, descriptive variable and function names
- Keep CLI logic (`cli.py`) separate from internal logic (`compressor.py`, `converter.py`, etc.)
- Document public functions with docstrings

## 🔁 Pull Request Process

1. Fork the repo
2. Create your feature branch (`git checkout -b feat/new-feature`)
3. Commit your changes with clear messages
4. Push to your fork
5. Open a Pull Request (PR) and describe your changes

Thanks for contributing to open-source!
