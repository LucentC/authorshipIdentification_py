import nltk
import re


def match_tokens_to_bigrams(sentence):
    """This is the description"""
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

#paragraphs = nltk.corpus.gutenberg.paras("shakespeare-caesar.txt")
corpus = nltk.corpus.reader.plaintext.PlaintextCorpusReader("./data", "test.txt")
paragraphs = corpus.paras()

for para in paragraphs:
    print para, "\n\n"
    for sentence in para:
        for word in sentence:
            previous = ""
            if re.match(r'.*\w', word):
                print "Match word: ", word
                if not previous:
                    previous = word
                    continue

                previous = word
            else:
                print "Match non-word: ", word


#sentences = nltk.sent_tokenize(text)

#for i in range(len(sentences)):
#    print "sen_id: ", i + 1, "\nSentence: " + sentences[i]
#    splitToTokens(sentences[i])
