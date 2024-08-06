import argparse
import os
import torch
from transformers import RagTokenizer, RagRetriever, RagSequenceForGeneration

def generate_text(model, tokenizer, retriever, context, top_k=5):
    # Tokenize the context
    inputs = tokenizer(context, return_tensors="pt")

    # Retrieve top-k documents
    question_hidden_states = model.question_encoder(input_ids=inputs["input_ids"])[0]
    docs_dict = retriever(input_ids=inputs["input_ids"], question_hidden_states=question_hidden_states, n_docs=top_k)

    # Generate response using retrieved documents
    generated_ids = model.generate(
        context_input_ids=docs_dict["context_input_ids"],
        context_attention_mask=docs_dict["context_attention_mask"],
        decoder_start_token_id=model.config.decoder_start_token_id
    )

    generated_text = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return generated_text

def process_text_files(model, tokenizer, retriever, text_folder, output_folder, top_k=5):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Process each text file in the input folder
    for text_file in os.listdir(text_folder):
        if text_file.endswith(".txt"):
            text_path = os.path.join(text_folder, text_file)
            with open(text_path, "r") as f:
                context = f.read()
            
            generated_text = generate_text(model, tokenizer, retriever, context, top_k)

            output_path = os.path.join(output_folder, f"generated_{text_file}")
            with open(output_path, "w") as out_f:
                out_f.write(generated_text)
            print(f"Generated text for {text_file} saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run inference with a trained RAG model on a folder of text files")
    parser.add_argument("--model_path", type=str, required=True, help="Path to the trained RAG model directory")
    parser.add_argument("--text_folder", type=str, required=True, help="Folder containing text files for input")
    parser.add_argument("--output_folder", type=str, required=True, help="Folder to save generated text files")
    parser.add_argument("--top_k", type=int, default=5, help="Number of top documents to retrieve")
    args = parser.parse_args()

    # Load the trained model and tokenizer
    model = RagSequenceForGeneration.from_pretrained(args.model_path)
    tokenizer = RagTokenizer.from_pretrained(args.model_path)

    # Initialize retriever
    retriever = RagRetriever.from_pretrained(
        "facebook/rag-token-nq",
        index_name="custom",
        passages_path=args.model_path + "/index"
    )

    # Process text files and generate responses
    process_text_files(model, tokenizer, retriever, args.text_folder, args.output_folder, args.top_k)

