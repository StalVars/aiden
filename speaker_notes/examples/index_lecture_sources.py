import argparse
import torch
from transformers import DPRContextEncoder, DPRContextEncoderTokenizer

def index_corpus(corpus_path, output_path):
    # Load corpus
    with open(corpus_path, 'r') as f:
        corpus = f.readlines()

    # Initialize DPR context encoder and tokenizer
    context_encoder_model_name = "facebook/dpr-ctx_encoder-multiset-base"
    context_encoder_tokenizer = DPRContextEncoderTokenizer.from_pretrained(context_encoder_model_name)
    context_encoder = DPRContextEncoder.from_pretrained(context_encoder_model_name)

    # Encode the corpus
    encoded_corpus = []
    for passage in corpus:
        inputs = context_encoder_tokenizer(passage, return_tensors='pt', truncation=True, padding=True)
        outputs = context_encoder(**inputs)
        encoded_corpus.append(outputs.pooler_output.detach().cpu().numpy())

    encoded_corpus = torch.tensor(encoded_corpus)

    # Save the encoded corpus to disk
    torch.save(encoded_corpus, output_path)
    print(f"Encoded corpus saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Index a corpus using DPR context encoder")
    parser.add_argument("--corpus_path", type=str, required=True, help="Path to the corpus file")
    parser.add_argument("--output_path", type=str, required=True, help="Path to save the encoded corpus")
    args = parser.parse_args()

    index_corpus(args.corpus_path, args.output_path)

