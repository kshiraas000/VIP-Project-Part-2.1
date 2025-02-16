import pandas as pd
import re

def split_into_sentences(text):
    if not isinstance(text, str) or not text:
        return []
    # Split on period followed by space or newline, question mark, or exclamation point
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z0-9])|(?<=[.!?])\s*$', text)
    return [s.strip() for s in sentences if s.strip()]

def process_articles(csv_path):
    # Read the CSV file
    df = pd.read_csv(csv_path)
    
    # Create a list to store all sentences
    all_sentences = []
    
    # Process each article
    for idx, row in df.iterrows():
        article_id = idx + 1
        sentences = split_into_sentences(row['Article'])
        
        # Add each sentence to our list
        for sent_idx, sentence in enumerate(sentences, 1):
            all_sentences.append({
                'article_id': article_id,
                'article_title': row['Article_title'],
                'date': row['Date'],
                'sentence_id': sent_idx,
                'sentence_text': sentence
            })
    
    # Convert to DataFrame and save to CSV
    sentences_df = pd.DataFrame(all_sentences)
    sentences_df.to_csv('sentences_output.csv', index=False)
    
    # Print some statistics
    print(f"Processed {len(df)} articles")
    print(f"Extracted {len(all_sentences)} sentences")
    
    return sentences_df

# Usage
if __name__ == "__main__":
    # Replace with your CSV path
    csv_path = '/Users/sadakshirsagar/Desktop/AS3/meta_articles.csv'
    sentences_df = process_articles(csv_path)
    
    # Display first few sentences from the first article as a sample
    print("\nSample output:")
    first_article = sentences_df[sentences_df['article_id'] == 1].head()
    for _, row in first_article.iterrows():
        print(f"[Article {row['article_id']}, Sentence {row['sentence_id']}] {row['sentence_text']}")