import pandas as pd
import random
from langdetect import detect

# Path to CSV file
file_path = '/Users/sadakshirsagar/Desktop/AS3/nasdaq_exteral_data.csv'
random_seed = 903960825
random.seed(random_seed)

def contains_meta_reference(row):
    if pd.isna(row['Article_title']) or pd.isna(row['Stock_symbol']):
        return False
    
    # Convert to lowercase for case-insensitive matching
    title = str(row['Article_title']).lower()
    ticker = str(row['Stock_symbol']).lower()
    
    # Words to exclude
    exclude_words = ['metal', 'metals', 'precious metals']
    if any(word in title for word in exclude_words):
        return False
    
    # More precise Meta identifiers with word boundaries
    meta_keywords = [
        r'\bfacebook\b',
        r'\bfb\b',
        r'\binstagram\b',
        r'\bzuckerberg\b',
        r'\bwhatsapp\b',
        r'\bmeta platforms\b'
    ]
    
    # Check if it's specifically Meta's stock symbol
    is_meta_ticker = ticker in ['meta', 'fb']
    
    # Check if the title contains Meta-specific keywords
    has_meta_keyword = any(keyword.strip() in title for keyword in meta_keywords)
    
    # For non-Meta tickers, the article must prominently feature Facebook/Meta
    if not is_meta_ticker:
        # Count mentions of Facebook/Meta keywords
        keyword_count = sum(1 for keyword in meta_keywords if keyword.strip() in title)
        # If it's not Meta's ticker, require at least two keyword mentions or Facebook/Meta
        # to be mentioned first in the title
        return keyword_count >= 2 or title.startswith(('facebook', 'meta platforms'))
    
    return is_meta_ticker or has_meta_keyword

def is_english(text):
    try:
        return detect(str(text)[:1000]) == 'en'
    except:
        return False

def filter_data(df):
    print(f"Initial rows: {len(df)}")
    
    # Create a copy of the dataframe to avoid SettingWithCopyWarning
    filtered_df = df.copy()
    
    # Filter 1: Check if news is about Meta
    filtered_df['is_meta_article'] = filtered_df.apply(contains_meta_reference, axis=1)
    filtered_df = filtered_df.loc[filtered_df['is_meta_article'] == True]
    print(f"After Meta filter: {len(filtered_df)} rows")
    
    # Filter 2: Check if article is English
    filtered_df['is_english'] = filtered_df['Article'].apply(lambda x: is_english(x) if pd.notna(x) else False)
    filtered_df = filtered_df.loc[filtered_df['is_english'] == True]
    print(f"After English language filter: {len(filtered_df)} rows")
    
    # Filter 3: Remove rows with empty content
    filtered_df = filtered_df.loc[filtered_df['Article'].notna() & (filtered_df['Article'].str.strip() != '')]
    print(f"After non-empty article filter: {len(filtered_df)} rows")
    
    return filtered_df

def main():
    # Load and filter the data
    df = pd.read_csv(file_path)
    filtered_df = filter_data(df)
    
    if len(filtered_df) < 10:
        print("Not enough Meta articles after filtering! Consider choosing another company.")
        return
    
    # Sample 10 articles
    sampled_df = filtered_df.sample(10, random_state=random_seed)
    
    # Save to CSV
    output_file = 'meta_articles.csv'
    sampled_df.to_csv(output_file, index=False)
    print(f"\nSampled articles saved to '{output_file}'")
    
    # Display sample of articles
    print("\nSample of Meta article titles:")
    for _, row in sampled_df.head().iterrows():
        print(f"Title: {row['Article_title']}")
        print(f"Ticker: {row['Stock_symbol']}")
        print("-" * 80)
    
    # Print additional statistics
    print(f"\nTotal Meta articles found: {len(filtered_df)}")
    print(f"Number of articles sampled: {len(sampled_df)}")

if __name__ == '__main__':
    main()