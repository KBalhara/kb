import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from  string  import punctuation
from heapq import nlargest

text = "In the not-so-distant future, autonomous vehicles are poised to revolutionize transportation. These self-driving cars use advanced technologies such as lidar, radar, and artificial intelligence to navigate streets and highways without human intervention. Proponents argue that autonomous vehicles have the potential to reduce traffic accidents, decrease traffic congestion, and enhance mobility for individuals with disabilities. However, challenges remain, including legal and ethical concerns, as well as the need for infrastructure upgrades to accommodate this new mode of transportation. The race to fully integrate autonomous vehicles into our daily lives continues, with automakers and tech giants competing to lead the way in this transformative industry"

def summarizer(rawdocs):
  stop_words = list(STOP_WORDS)
  #print(stop_words)
  nlp = spacy.load("en_core_web_sm")
  doc = nlp(rawdocs)
  #print(doc)
  tokens = [token.text for token in doc]
  #print(tokens)
  word_freq = {}
  for word in doc:
    if word.text.lower() not in stop_words and word.text.lower() not in punctuation:
      if word.text not in word_freq.keys():
        word_freq[word.text] = 1
      else:
        word_freq[word.text] += 1
  #print(word_freq)
  max_freq = max(word_freq.values())
  #print(max_freq)
  for word in word_freq.keys():
    word_freq[word] = word_freq[word]/max_freq
  #print(word_freq)
  sent_tokens = [sent for sent in doc.sents]
  #print(sent_tokens)
  sent_scores = {}
  for sent in sent_tokens:
    for word in sent:
      if word.text in word_freq.keys():
        if sent not in sent_scores.keys():
          sent_scores[sent] = word_freq[word.text]
        else:
          sent_scores[sent] += word_freq[word.text]
  #print(sent_scores)
  select_len = int(len(sent_tokens) * 0.3)
  #print(select_len)
  summary = nlargest(select_len, sent_scores, key = sent_scores.get)
  #print(summary)
  final_summary = [word.text for word in summary]
  summary = ''.join(final_summary)
  #print(text)
  #print(summary)
  #print("Length of original text",len(text.split()))
  #print("Length of summary text",len(summary.split()))

  return summary, doc, len(rawdocs.split()), len(summary.split())