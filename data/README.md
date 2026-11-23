# Legal Knowledge Base (`data/`)

Place official Indian legal PDF documents in this folder before generating the vector database.

### Recommended Documents
* `Constitution_of_India.pdf`
* `Indian_Penal_Code.pdf` (or Bharatiya Nyaya Sanhita)
* `Indian_Contract_Act.pdf`
* `Indian_Evidence_Act.pdf`

### How to Build the Vector Store
After adding your PDFs to this folder, run the following command from the root directory:

```bash
python create_embeddings.py
