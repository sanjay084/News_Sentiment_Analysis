from newsapi import NewsApiClient
import pandas as pd
from textblob import TextBlob
from gtts import gTTS
import streamlit as st
import os

# Initialize NewsApiClient
newsapi = NewsApiClient(api_key='a60685db32634d14975f088dd25f65f0')

# Function to fetch news
def fetch_news(company_name, max_articles=10):
    articles = newsapi.get_everything(q=company_name, 
                                      language='en', 
                                      sort_by='relevancy',  # Corrected sort_by value
                                      page_size=max_articles)
    
    if articles['totalResults'] == 0:
        return pd.DataFrame()
    
    news_list = []
    for article in articles['articles']:
        news_list.append({
            'Title': article['title'],
            'Summary': article['description'] or "No Summary Available",
            'URL': article['url']
        })
    
    return pd.DataFrame(news_list)

# Function for sentiment analysis
def sentiment_analysis(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0:
        return 'Positive'
    elif polarity < 0:
        return 'Negative'
    else:
        return 'Neutral'

# Function for comparative sentiment analysis
def comparative_analysis(df):
    sentiment_counts = df['Sentiment'].value_counts()
    return sentiment_counts

# Function to convert text to Hindi speech
def text_to_speech_hindi(text, filename="output.mp3"):
    tts = gTTS(text=text, lang='hi')
    tts.save(filename)
    return filename

# Streamlit web app
def main():
    st.title("News Summarization and Sentiment Analysis")
    st.write("Input a company name to fetch news, analyze sentiment, and generate Hindi TTS.")

    # User input
    company_name = st.text_input("Enter Company Name:", "Tesla")

    if st.button("Fetch News"):
        st.write(f"Fetching news for: {company_name}")
        
        # Fetch news
        news_df = fetch_news(company_name)
        
        if not news_df.empty:
            # Perform sentiment analysis
            news_df['Sentiment'] = news_df['Summary'].apply(sentiment_analysis)
            
            # Display news articles
            st.dataframe(news_df[['Title', 'Summary', 'Sentiment']])
            
            # Comparative analysis
            sentiment_counts = comparative_analysis(news_df)
            st.bar_chart(sentiment_counts)
            
            # Generate TTS for first article
            summary_text = " ".join(news_df['Summary'].tolist())
            audio_file = text_to_speech_hindi(summary_text)
            
            # Play audio
            st.audio(audio_file, autoplay= True)
        else:
            st.write("No articles found.")

# Run the app
if __name__ == "__main__":
    main()
