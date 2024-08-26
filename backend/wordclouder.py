import pandas as pd
from wordclouder import WordCloud
import matplotlib.pyplot as plt

# Load the CSV file
df = pd.read_csv('uploads/generated.csv')

# Generate a dictionary from the wordlist
word_freq = dict(zip(df['word'], df['count']))

# Generate the word cloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_freq)

# Display the word cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()