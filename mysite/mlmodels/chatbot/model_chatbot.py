#author:Haoqiu Wu Time 19.3.11
import pickle
import os


file_qrDict = 'qrDict.pk'
file_sentenceTokens = 'sentenceTokens.pk'
file_ql = 'ql.pk'

# read local serialized clean dataset
with open(os.path.join(os.path.dirname(__file__), '../picklized_files/'+file_qrDict) ,'rb') as f:
    qrDict = pickle.load(f)

with open(os.path.join(os.path.dirname(__file__), '../picklized_files/'+file_sentenceTokens) ,'rb') as f:
    sentenceTokens = pickle.load(f)

with open(os.path.join(os.path.dirname(__file__), '../picklized_files/'+file_ql) ,'rb') as f:
    ql = pickle.load(f)

"""
generate Response
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from nltk.stem import WordNetLemmatizer
import string



def sanitize_questions(question):
    sanitized_question = question.translate(str.maketrans('', '', string.punctuation)).rstrip().lstrip()
    return sanitized_question

# for a given sentence,return a lemmatized sentence
def lemTokens(tokens):
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(token) for token in tokens]


def generateResponse(userInput, sentences, askResponseDict, ql, similarityThredhold=0.7):
    # prevent bad input
    if ((similarityThredhold > 1) or (similarityThredhold < 0)):
        similarityThredhold = 0.7
    sentences.append(userInput)
    # vetorize sentences and userinput for fllowing similarity calculation
    vertorizedSentences = TfidfVectorizer(tokenizer=lemTokens, stop_words='english').fit_transform(sentences)
    vals = cosine_similarity(vertorizedSentences[-1], vertorizedSentences)
    # find index of sentences that has highest similarity with input
    valsWithoutLast = vals[0, :-1]
    idx = np.argmax(valsWithoutLast, axis=0)
    # return response
    if (vals[0][idx] < similarityThredhold):
        robotResponse = ["Your input keywords donot exist in my knowledge","I donot know what you are talking",'Sorry I have no idea','Sorry I donot understand'
            ,'Sorry I can not reply',"Pls change a topic","Looks like I still need to learn more"]
        import random
        index=random.randint(0,8)
        sentences.remove(userInput)
        return robotResponse[index]
    else:
        question = ql[idx]
        print("matched from db:"+question)
        robotResponse = '' + askResponseDict.get(question)
        sentences.remove(userInput)
        return robotResponse



def reply(userInput):
    userInput = sanitize_questions(userInput.lower())
    return generateResponse(userInput, sentenceTokens, qrDict, ql)


if __name__=='__main__':
    flag = True
    print("ROBO: Hello, I am a chatbot. Type Bye to exit")
    while (flag == True):
        userInput = input()
        userInput = sanitize_questions(userInput.lower())
        if (userInput != 'bye'):
            if (userInput == 'thanks' or userInput == 'thank you'):
                flag = False
                print("ROBO: You are welcome..")
            else:
                print("ROBO: " + reply(userInput))
                # sentenceTokens.remove(userInput)
        else:
            flag = False
            print("ROBO: Bye! take care..")
