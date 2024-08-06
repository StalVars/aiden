#Speaker Notes

''' Create text files from pdfs '''
```sh
python examples/create_text_files_from_pdfs.py --input_dir path_to_lecture_pdfs 
```

''' LLM based speaker notes creation/annotation '''
```sh
python examples/create_speaker_notes_with_llm.py --input_dir path_to_lecture_pdfs 
```



''' Train T5-RAG from speaker notes created '''
 
Indexing:
```sh
python index_corpus.py --corpus_path path/to/your/corpus.txt --output_path path/to/save/encoded_corpus.pt
```

Train RAG
```sh
python train_rag.py --encoded_corpus_path path/to/save/encoded_corpus.pt --output_dir path/to/save/trained_model
```

''' Own RAG based speaker notes creation '''
```sh
python examples/generate_speaker_notes_t5_rag.py --model_path path/to/saved_model --text_folder path/to/text_folder --output_folder path/to/output_folder --top_k 5
```

