# Legal Knowledge Base (`data/`)

Place official Indian legal PDF documents in this folder before generating embeddings.

### Recommended Documents
- `Constitution_of_India.pdf`
- `Indian_Penal_Code.pdf` (or Bharatiya Nyaya Sanhita)
- `Indian_Contract_Act.pdf`
- `Indian_Evidence_Act.pdf`

### Generate the Vector Store
After adding your PDFs here, run:
```bash
python create_embeddings.py
