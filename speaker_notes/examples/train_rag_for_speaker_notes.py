import argparse
import json
import torch
from transformers import (
    RagTokenizer,
    RagRetriever,
    RagSequenceForGeneration,
    T5ForConditionalGeneration,
    Trainer,
    TrainingArguments,
)
from datasets import Dataset, DatasetDict

def load_custom_dataset(json_path):
    with open(json_path, 'r') as f:
        squad_dict = json.load(f)

    contexts = []
    questions = []
    for group in squad_dict['data']:
        for paragraph in group['paragraphs']:
            context = paragraph['context']
            for qa in paragraph['qas']:
                question = qa['question']
                contexts.append(context)
                questions.append(question)

    return Dataset.from_dict({"context": contexts, "question": questions})

def train_rag(encoded_corpus_path, dataset_path, output_dir):
    # Load custom dataset
    dataset = load_custom_dataset(dataset_path)
    dataset = DatasetDict({"train": dataset, "validation": dataset})  # Split the dataset if needed

    # Initialize T5 model
    t5_model_name = "t5-small"
    seq2seq_model = T5ForConditionalGeneration.from_pretrained(t5_model_name)

    # Initialize RAG tokenizer
    rag_tokenizer = RagTokenizer.from_pretrained("facebook/rag-token-nq")

    # Initialize RAG retriever with the encoded corpus
    rag_retriever = RagRetriever.from_pretrained(
        "facebook/rag-token-nq",
        index_name="custom",
        passages_path=encoded_corpus_path
    )

    # Initialize RAG model
    rag_model = RagSequenceForGeneration.from_pretrained(
        "facebook/rag-sequence-nq",
        question_encoder=seq2seq_model,
        retriever=rag_retriever
    )

    # Tokenize data
    def preprocess_function(examples):
        contexts = examples['context']
        questions = examples['question']
        inputs = rag_tokenizer(contexts, padding=True, truncation=True, return_tensors="pt")
        targets = rag_tokenizer(questions, padding=True, truncation=True, return_tensors="pt")
        inputs["input_ids"] = inputs["input_ids"].tolist()
        inputs["attention_mask"] = inputs["attention_mask"].tolist()
        inputs["labels"] = targets["input_ids"]
        return inputs

    tokenized_datasets = dataset.map(preprocess_function, batched=True)

    # Define training arguments
    training_args = TrainingArguments(
        output_dir=output_dir,
        evaluation_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=2,
        per_device_eval_batch_size=2,
        num_train_epochs=3,
        weight_decay=0.01,
        logging_dir='./logs',
    )

    # Initialize Trainer
    trainer = Trainer(
        model=rag_model,
        args=training_args,
        train_dataset=tokenized_datasets['train'],
        eval_dataset=tokenized_datasets['validation']
    )

    # Train model
    trainer.train()

    # Save model
    rag_model.save_pretrained(output_dir)
    rag_tokenizer.save_pretrained(output_dir)
    print(f"Model and tokenizer saved to {output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a RAG model with a pre-indexed corpus")
    parser.add_argument("--encoded_corpus_path", type=str, required=True, help="Path to the encoded corpus file")
    parser.add_argument("--dataset_path", type=str, required=True, help="Path to the custom dataset JSON file")
    parser.add_argument("--output_dir", type=str, required=True, help="Directory to save the trained model and tokenizer")
    args = parser.parse_args()

    train_rag(args.encoded_corpus_path, args.dataset_path, args.output_dir)

