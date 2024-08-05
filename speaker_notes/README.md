To train a speaker notes

''' Create sample speaker notes '''
# LLM based annotation



''' Train T5-RAG from speaker notes created '''
 
Indexing:
```sh
python index_corpus.py --corpus_path path/to/your/corpus.txt --output_path path/to/save/encoded_corpus.pt

```


Train RAG
```sh
python train_rag.py --encoded_corpus_path path/to/save/encoded_corpus.pt --output_dir path/to/save/trained_model

```
