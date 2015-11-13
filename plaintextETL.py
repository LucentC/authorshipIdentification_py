import nltk
import re


def splitToTokens(sentence):
    previous = ""
    tokens = nltk.word_tokenize(sentence)
    for index in range(len(tokens)):
        if re.match(r'.*\w', tokens[index]):
            print "Match word: ", tokens[index]
            if not previous:
                previous = tokens[index]
                continue

            previous = tokens[index]
        else:
            print "Match non-word: ", tokens[index]


text = "this\'s a sent tokenize test. this is sent two. is this sent three? sent 4 is cool! Now it\'s your turn."

sentences = nltk.sent_tokenize(text)

for i in range(len(sentences)):
    print "sen_id: ", i + 1, "\nSentence: " + sentences[i]
    splitToTokens(sentences[i])
