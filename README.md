# 🦊 imagefox

**imagefox** is a sleek, powerful, and offline-friendly CLI toolkit for image processing.  
Compress, convert, or cleanse your images — all with one clever fox.  
Built with open-source Python libraries and designed for maximum usability.

> #imagecompression #exifremoval #imageconversion #metadataedit #opensource #pythoncli #privacytools

---

## ✨ Features

- 🗜️ Compress JPEG/PNG/WebP by adjusting quality or dimensions
- 🔄 Convert image formats (JPEG ↔ PNG ↔ BMP ↔ WebP)
- 🧹 Read, remove, and edit EXIF metadata (camera model, GPS, date, etc.)
- 💬 Clean, UNIX-style CLI interface
- 🧪 Includes full unit test suite for reliability
- 🧰 No external APIs, works 100% offline

---

## 🧩 Dependencies

- Python ≥ 3.13
- [Pillow](https://pypi.org/project/Pillow/)
- [piexif](https://pypi.org/project/piexif/)

Install via:

```bash
pip install -r requirements.txt
```

---

## 💻 Local Setup

Clone the repository and run the CLI locally:

```bash
git clone https://github.com/pradyroy/imagefox.git
cd imagefox
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

---

## 🧰 CLI Usage

```bash
# Compress image
python -m imagefox compress input.jpg --quality 70 --resize 1024x768

# Convert format
python -m imagefox convert input.png --to jpeg

# View metadata
python -m imagefox metadata view input.jpg

# Remove metadata
python -m imagefox metadata remove input.jpg --output clean.jpg

# Edit metadata (e.g., camera model)
python -m imagefox metadata edit input.jpg --field Model --value "MyCustomCamera" --output edited.jpg
```

Use `--help` with any command:

```bash
python -m imagefox --help
python -m imagefox metadata --help
```

---

## 🧪 Sample Input/Output

| Action        | Input         | Output              |
|---------------|---------------|---------------------|
| Compress      | `photo.jpg`   | `photo_compressed.jpg` |
| Convert       | `logo.png`    | `logo.jpeg`         |
| Remove EXIF   | `img.jpg`     | `img_clean.jpg`     |
| Edit EXIF     | `raw.jpg`     | `raw_edited.jpg`    |

---

## 🤝 Contributing

We welcome contributions!  
Please see the [CONTRIBUTING.md](CONTRIBUTING.md) file for setup, coding guidelines, and pull request instructions.

---

## ⚖️ License

This project is licensed under the [MIT License](LICENSE).

© 2025 Pradyumna Das Roy. All rights reserved.
