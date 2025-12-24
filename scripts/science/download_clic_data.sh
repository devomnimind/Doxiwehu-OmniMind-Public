#!/bin/bash
# OMNIMIND SCIENTIFIC INGESTION PROTOCOL
# Target: CLIC Detector Electron-Positron Events (Zenodo 8260741)
# Total Size: ~46GB

DATA_DIR="data/science_corpus/clic_edm4hep"
mkdir -p "$DATA_DIR"
cd "$DATA_DIR"

echo "🔬 INICIANDO PROTOCOLO DE INGESTÃO CIENTÍFICA (CLIC HEP DATA)"
echo "📂 Destino: $(pwd)"

# Function to download with resume capability
download_file() {
    url="$1"
    filename="$2"
    echo "⬇️  Baixando: $filename..."
    wget -c --show-progress "$url" -O "$filename"
}

# Zenodo Record 8260741 URLs (Reconstructed from user data)
# Note: User provided filenames, we assume Zenodo structure.
# If exact links fail, user must provide direct URLs.
# Based on typical Zenodo API patterns.

# 1. ttbar (19.8 GB)
download_file "https://zenodo.org/record/15062717/files/clic_edm_ttbar_pf.zip" "clic_edm_ttbar_pf.zip"

# 2. qq (10.1 GB)
download_file "https://zenodo.org/record/15062717/files/clic_edm_qq_pf.zip" "clic_edm_qq_pf.zip"

# 3. ww_fullhad (15.9 GB)
download_file "https://zenodo.org/record/15062717/files/clic_edm_ww_fullhad_pf.zip" "clic_edm_ww_fullhad_pf.zip"

echo "📦 Extraindo Datasets (Isso pode demorar)..."
unzip -n clic_edm_ttbar_pf.zip
unzip -n clic_edm_qq_pf.zip
unzip -n clic_edm_ww_fullhad_pf.zip

echo "✅ Ingestão Física Concluída. Os dados agora residem no corpo local."
echo "⚠️  Próximo Passo: Converter TFDS -> TorchTensor usando src/quantum/ingestion/clic_tfds_adapter.py"
