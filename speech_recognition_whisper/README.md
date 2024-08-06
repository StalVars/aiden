# Install requirements
pip install -r requirements.txt


# Download trascripts from a list of youtube urls

bash scripts/download_multiple_ytube_tr.sh data/list_of_videos_johnhopkins.txt 


# Create paragraphs from transcripts using sentence embeddings
bash scripts/create_paras_from_tr.sh


# Index using bm25 pyserini


