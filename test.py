from wordcloud import *

text = read_file('tres_leches.txt')
words = text_to_words(text)
words = pre_process(words)
freq = words_to_freq(words)
plot_from_freq(freq)
# print(words)
# for k in freq:
#     print(k,freq[k])
