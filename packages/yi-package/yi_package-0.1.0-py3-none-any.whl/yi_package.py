#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 13:56:21 2022

@author: jpyi
1.  Install praw by performing a “pip install praw” from a conda shell or from linux shell.  Praw is an 
API that interfaces with the Reddit API.  The API enables a user to access both historical and 
real-time subreddit channel messages.
2. Sign up for a Reddit account if you don’t have one already
3. Create a Reddit App
4. Click onto 'Are you a developer? Create an app...'
5. Fill out the “Create Application” exactly as instructed on the website
6. Once you click the “create app” button, please scroll up and copy YOUR “personal use script” 
and “secret”:
7. Now go to the Python script called keys.py and paste your “client_id”, “client_secret”, 
“username”, “password” into the proper fields, as shown in the example below:
"""



import praw # enables a user to access both historical and real-time subreddit channel messages.
import pandas as pd
import numpy as np
import pytz # # allows accurate and cross platform timezone calculation
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')
subreddit_channel = 'politics'
import re
import nltk
from nltk.corpus import stopwords 
import spacy # for named entity recognition(NER)
# load the spacy large English model (en_core_web_lg)
from nltk.probability import FreqDist
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
# For importing our word cloud mask image and converting the content into bytes for the Image package
import requests
from io import BytesIO
from PIL import Image   # To read the image data
# Also import STOPWORDS, a set of common English words to remove from our potential words
from wordcloud import WordCloud, STOPWORDS


# developer's credentials for streaming comments, create your own, see above.
reddit = praw.Reddit(
     client_id="CQCXr5pT5FOWh1jYbBcm0A",
     client_secret="_S1EvYlUKoPWzR4UT5Uec70rXYQKzA",
     user_agent="testscript by u/fakebot3",
     username="psjyforte",
     password="Student0723",
     check_for_async=False
 )



def conv_time(var):
    """
    This function handles and converts different timezones by using the pytz module which helps
    convert a naive time and a tzinfo into an UTC time.
    It also converts a scalar, array-like, Series or DataFrame/dict-like to a Python pandas datetime object.

    Parameters
    ----------
    var : float
      Convert argument to datetime.

    Returns
    -------
    Date time object series.
        datetime.datetime
   
    Examples
    --------
    >>> from yi_package import yi_package
    >>> var = 3.0     # a float
    >>> conv_time(var)
    >>> datetime.datetime(1970, 1, 1, 0, 0, 3, tzinfo=<UTC>)
    
    >>> from yi_package import yi_package
    >>> var = 1670811629.485424     # another float
    >>> conv_time(var)
    >>> datetime.datetime(2022, 12, 12, 2, 20, 59, 787150, tzinfo=<UTC>)
    """         
    tmp_df = pd.DataFrame()
    tmp_df = tmp_df.append(
        {'created_at': var},ignore_index=True)
    tmp_df.created_at = pd.to_datetime(
        tmp_df.created_at, unit='s').dt.tz_localize(
            'utc').dt.tz_convert('US/Eastern') 
    return datetime.fromtimestamp(var).astimezone(pytz.utc)



def get_reddit_data(var_in):
    """
    This function returns a dictionary with 4 key-value pairs from streamed Reddit comments 
    # Our focus then will be extracting the values associated with key 'body'

    Parameters
    ----------
    var_in : a stream_generator of <class 'praw.models.reddit.comment.Comment'>

    Returns
    -------
    a dictinary of <class 'dict'>
   
    Examples
    --------
    >>> from yi_package import yi_package
    >>> var_in = reddit.subreddit(subreddit_channel).stream.comments() # <generator object stream_generator at 0x7fe21ef0f7b0>
    >>> for i in var_in:
            tmp_dict = get_reddit_data(i)
            print(tmp_dict)
    >>>       
{'msg_id': 'izv8u1o', 'author': 'Harpua44', 'body': 'And it would put him at odds with his masters', 'datetime': Timestamp('2022-12-12 02:26:57+0000', tz='UTC')}

{'msg_id': 'izv8u3u', 'author': 'DredZedPrime', 'body': "Doublethink.\n\nThese people are really good at holding two completely different and contradictory ideas in their head at the same time.\n\nIt's pretty much all they are really good at.", 'datetime': Timestamp('2022-12-12 02:26:58+0000', tz='UTC')}

{'msg_id': 'izv8uah', 'author': 'disabledreplies', 'body': "Because they're lazy assholes from the one-star state.\n\nPar for the course, really.\n\nCry about your government, don't do the bare minimum to fix it.\n\nApathetic losers.", 'datetime': Timestamp('2022-12-12 02:27:00+0000', tz='UTC')}

{'msg_id': 'izv8uuv', 'author': 'MississippiJoel', 'body': '>While the administration downplayed the threat, a senior administration official acknowledged that the White House had been misled about the role of the Russian photographer\n\nLol "Hey, I have a camera I will be pointing at your president, but I will only say \'click, click\' with my mouth. No photos, I promise!"', 'datetime': Timestamp('2022-12-12 02:27:07+0000', tz='UTC')}
    """             
    tmp_dict = pd.DataFrame()
    tmp_time = None
    try:
        tmp_dict = tmp_dict.append({"created_at": conv_time(
                                        var_in.created_utc)},
                                    ignore_index=True)
        tmp_time = tmp_dict.created_at[0] 
    except Exception as e:
        print (e)
        pass
    tmp_dict = {'msg_id': str(var_in.id),
                'author': str(var_in.author),
                'body': var_in.body,
                'datetime': tmp_time
               }
    return tmp_dict



def get_comment_lst(n_comments):
    """
    This function takes in a varaible of int type so as to give users flexbility 
    of streaming the exact number of comments desired.
    Since the focus here is to extract the 'body' of the above dict tmp_dict,
    It then appends the values associated with the key 'body' to a comment_lst
    The streaming process will terminate once the list reaches n_comments

    Parameters
    ----------
    n_comments : an int type 

    Returns
    -------
    a list type
   
    Examples
    --------
    >>> from yi_package import yi_package
    >>> my_list = get_comment_lst(11)
    >>> print(my_list)
    
 ['Republicans in 2016:\n\n“Quit being dramatic, he’s fine. Better than the alternative.”\n\nRepublicans now, after Trump has actively destroyed the Republican Party from the inside out for the past 6 years:\n\n“…”',
 'But “arbitrary” means based on whim or personal convenience rather than reason or a system. 10 can be arbitrarily close to 0, or a million. It’s arbitrary!',
 'Ayn Rand was a sick-fuck apologist for pathological assholes.',
 'We can hope!!!!',
 'Damn, I just realized I might be Xenophobic.',
 'Win what?',
 'Sounds like a confession to me',
 'What are you saying, please reword this.',
 "What you mean they're not represented? Every vote is represented. Every vote is counted.  Every vote is equal.  And the plurality of the votes will determine the outcome.  Regardless of whether that plurality equals 90%, 50% or even some number much lower than 50% (If there are more than two choices).\n\nAnd that's how the Democratic process works.\n\nThis is literally democracy.",
 "I the Republicans have shown that policy doesn't mean shit.",
 'It has happened *once*. Citation needed on any other races that recounts of digitally reorded votes changed the result of. (Remember, Trump v Gore was what drove states into using digital voting machines.) What do you mean it happens far more than it should?']
    """         
    comment_lst = [] # a list of str 
    for comment in reddit.subreddit(subreddit_channel).stream.comments():
        tmp_df = get_reddit_data(comment)
        comment_lst.append(tmp_df['body']) 

        if len(comment_lst) == n_comments:
            break
    return comment_lst



def clean_text(str_in):
    """
    This function takes in a str type object and converts it to all lowercase and 
    replaces everything but letters, with white space
    AND removes stopwords in comments so as to reduce noises for downstream analyses
    for our purposes, I also added new words to the stopwords list 
    
    Parameters
    ----------
    str_in : a str type object 

    Returns
    -------
    a str type object
   
    Examples
    --------
    >>> from yi_package import yi_package
    >>> str_in = "It has happened *once*. Citation needed on any other races that recounts of digitally reorded votes changed the result of. (Remember, Trump v Gore was what drove states into using digital voting machines.) What do you mean it happens far more than it should?"     
    >>> clean_text(str_in)
    >>> 'happened citation needed races recounts digitally reorded votes changed result remember trump v gore drove states using digital voting machines mean happens far' 
    """             
    cleaned = re.sub(r'[^A-Za-z]+', ' ', str_in.lower())
    sw = stopwords.words('english') # a list
    update_words = ['http', 'https','r', 'www', 'reddit', 'com', 'wiki','index','approveddomainslist','list','bot','subreddit', 'sounds', 'seems', 'like', 'would', 'could','also', 'still', 'en','org']
    for i in update_words:
        sw.append(i) # update sw list
    tmp = [word for word in cleaned.split() if word not in sw]
    tmp = ' '.join(tmp)   
    return tmp



def get_df(comment_lst):
    """
    This function takes in a list of comments, cleans each comment in that inputted list，
    then creates a dataframe out of the list of cleaned comments.
    It also applies three lambda functions on the cleaned_comments column, adding three separate columns to the df
    In particular, the named entity extraction using spacy is a good primer for extracting frequently occuring tokens

    Parameters
    ----------
    commen_lst : a list type object

    Returns
    -------
    a pandas Dataframe type
   
    Examples
    --------
    >>> from yi_package import yi_package
  
    >>> comment_lst = ['Republicans in 2016:\n\n“Quit being dramatic, he’s fine. Better than the alternative.”\n\nRepublicans now, after Trump has actively destroyed the Republican Party from the inside out for the past 6 years:\n\n“…”',
 'But “arbitrary” means based on whim or personal convenience rather than reason or a system. 10 can be arbitrarily close to 0, or a million. It’s arbitrary!',
 'Ayn Rand was a sick-fuck apologist for pathological assholes.',
 'We can hope!!!!',
 'Damn, I just realized I might be Xenophobic.',
 'Win what?',
 'Sounds like a confession to me',
 'What are you saying, please reword this.',
 "What you mean they're not represented? Every vote is represented. Every vote is counted.  Every vote is equal.  And the plurality of the votes will determine the outcome.  Regardless of whether that plurality equals 90%, 50% or even some number much lower than 50% (If there are more than two choices).\n\nAnd that's how the Democratic process works.\n\nThis is literally democracy.",
 "I the Republicans have shown that policy doesn't mean shit.",
 'It has happened *once*. Citation needed on any other races that recounts of digitally reorded votes changed the result of. (Remember, Trump v Gore was what drove states into using digital voting machines.) What do you mean it happens far more than it should?']
 
    >>> reddit = get_df(comment_lst)
    >>> print(reddit)    
   cleaned_comments	word_count	letter_count	named_entity
0	republicans quit dramatic fine better alternat...	15	107	((republicans), (republicans), (trump), (repub...
1	arbitrary means based whim personal convenienc...	13	92	((million),)
2	ayn rand sick fuck apologist pathological assh...	7	44	((ayn, rand),)
3	hope	1	4	()
4	damn realized might xenophobic	4	27	()
...	...	...	...	...
    """             
    new_body = [clean_text(sent) for sent in comment_lst]
    reddit = pd.DataFrame(data=new_body, columns=['cleaned_comments'])
    reddit['word_count'] = reddit.cleaned_comments.apply(lambda x: len(x.split()))
    reddit['letter_count'] = reddit.cleaned_comments.apply(lambda x: len(x) - x.count(' ')) # excludes white spaces
    nlp = spacy.load('en_core_web_lg')
    reddit['named_entity'] = reddit.cleaned_comments.apply(lambda x: nlp(x).ents)  
    return reddit



def get_unigrams(data): # data is a df
    """
    This function takes in a pandas df and creates 50 most used words/unigrams
    out of the cleaned_comments column using nltk library

    Parameters
    ----------
    data : a pandas Dataframe type

    Returns
    -------
    A list of tuples
   
    Examples
    --------
    >>> from yi_package import yi_package
    >>> data = reddit # see above
    >>> get_unigrams(reddit)
    >>> [('people', 57),
         ('vote', 32),
         ('trump', 31),
         ('politics', 28),
         ('right', 27),
         ('one', 25),
         ('get', 22),
         ('election', 21),
         ('make', 21),
         ('even', 20),
         ('please', 18),
         ('party', 17),
         ('us', 15),
         ('republicans', 14),
         ('every', 14),
         ('see', 14),
         ('know', 14),
         ('democrats', 14),
         ('way', 14),
         ('think', 14),
         ('gop', 13),
         ('votes', 12),
         ('state', 12),
         ('voters', 12),
         ('want', 12),
         ('good', 12),
         ('time', 12),
         ('texas', 12),
         ('mean', 11),
         ('place', 11),
         ('money', 11),
         ('always', 11),
         ('lot', 11),
         ('believe', 11),
         ('mtg', 11),
         ('next', 11),
         ('better', 10),
         ('million', 10),
         ('win', 10),
         ('much', 10),
         ('states', 10),
         ('voting', 10),
         ('care', 10),
         ('comments', 10),
         ('questions', 10),
         ('new', 10),
         ('help', 10),
         ('anyone', 10),
         ('voted', 10),
         ('office', 10)]
    """          
    concat_str = data['cleaned_comments'].str.cat(sep=' ') # concatenate all the comments in one single long str
    fdist = FreqDist(concat_str.split()) # takes in a word list
    unigram = fdist.most_common(50)
    return unigram



def get_bigrams(data):
    """
    This function takes in a pandas df and creates 50 most common word combo/bigrams
    out of the cleaned_comments column using nltk library
    
    Parameters
    ----------
    data : a pandas Dataframe type

    Returns
    -------
    A list of tuples
   
    Examples
    --------
    >>> from yi_package import yi_package
    >>> data = reddit # see above
    >>> get_bigrams(reddit)
    [(('instagram', 'p'), 8),
     (('next', 'f'), 8),
     (('f', 'instagram'), 7),
     (('young', 'people'), 6),
     (('help', 'make'), 5),
     (('politics', 'comments'), 5),
     (('moderators', 'message'), 5),
     (('message', 'compose'), 5),
     (('compose', 'politics'), 5),
     (('reminder', 'civil'), 4),
     (('civil', 'discussion'), 4),
     (('discussion', 'politics'), 4),
     (('politics', 'civil'), 4),
     (('civil', 'general'), 4),
     (('general', 'courteous'), 4),
     (('courteous', 'others'), 4),
     (('others', 'debate'), 4),
     (('debate', 'discuss'), 4),
     (('discuss', 'argue'), 4),
     (('argue', 'merits'), 4),
     (('merits', 'ideas'), 4),
     (('ideas', 'attack'), 4),
     (('attack', 'people'), 4),
     (('people', 'personal'), 4),
     (('personal', 'insults'), 4),
     (('insults', 'shill'), 4),
     (('shill', 'troll'), 4),
     (('troll', 'accusations'), 4),
     (('accusations', 'hate'), 4),
     (('hate', 'speech'), 4),
     (('speech', 'suggestion'), 4),
     (('suggestion', 'support'), 4),
     (('support', 'harm'), 4),
     (('harm', 'violence'), 4),
     (('violence', 'death'), 4),
     (('death', 'rule'), 4),
     (('rule', 'violations'), 4),
     (('violations', 'result'), 4),
     (('result', 'permanent'), 4),
     (('permanent', 'ban'), 4),
     (('ban', 'see'), 4),
     (('see', 'comments'), 4),
     (('comments', 'violation'), 4),
     (('violation', 'rules'), 4),
     (('rules', 'please'), 4),
     (('please', 'report'), 4),
     (('report', 'questions'), 4),
     (('questions', 'regarding'), 4),
     (('regarding', 'media'), 4),
     (('media', 'outlets'), 4)]
    """
    concat_str = data['cleaned_comments'].str.cat(sep=' ') # concatenate all the comments in one single long str
    bigrams = nltk.bigrams(concat_str.split())
    fdist_bi = FreqDist(bigrams)
    bigram = fdist_bi.most_common(50)
    return bigram



def word_in_text(word_in, str_in):
    """
    This function takes in two varaibles both of str type, 
    and checks how many times the 1st varibale word_in occurs in the 2nd var str_in

    Parameters
    ----------
    word_in : a str
    str_in: a str

    Returns
    -------
    an int type
   
    Examples
    --------
    >>> from yi_package import yi_package
    >>> word_in = 'biden'
    >>> str_in = 'biden is the current U.S. president
    >>> word_in_text(word_in, str_in)
    >>> 1
    """         
    match = re.findall(word_in, str_in)
    if match:
        return len(match)
    return 0



def plot_key_words(list_in, count_in):
    """
    This function takes in two varaibles of list type and creates a bar chart using seaborn library
    
    Parameters
    ----------
    list_in : a list
    count_in: a list

    Returns
    -------
    a bar chart 
   
    Examples
    --------
    >>> from yi_package import yi_package
    >>> names = ['biden', 'sanders', 'trump', 'cruz']
    >>> name_count = [7,4,31,3]
    >>> plot_key_words(names, name_count)
    >>> Please refer to Reddit_project_presentation.ipynb located in the same directory as this .py file for the outputted bar chart.
    """             
    sns.set_style('whitegrid')
    sns.set(color_codes=True) # set seaborn style
    ax = sns.barplot(list_in, count_in)
    ax.set(ylabel='count')
    return plt.show()



def plot_unigrams(df_in):
    """
    This function takes in a pandas df and plot the 20 most frequently occuring 
    words using nltk and seaborn libraries
    
    Parameters
    ----------
    df_in : a pandas DataFrame

    Returns
    -------
    a bar plot 
   
    Examples
    --------
    >>> from yi_package import yi_package
    >>> df_in = reddit
    >>> plot_unigrams(reddit)
    >>> Please refer to Reddit_project_presentation.ipynb located in the same directory as this .py file for the outputted barplot.
    """       
    plt.figure(figsize=(15,5))
    concat_str = df_in['cleaned_comments'].str.cat(sep=' ')
    fdist = FreqDist(concat_str.split()) # takes in a word list
    words_df = pd.DataFrame({'word': list(fdist.keys()), 'count': list(fdist.values())})
    # DataFrame.nlargest(n, columns)
    # Returns the first n rows ordered by columns in descending order.
    d = words_df.nlargest(n = 20, columns="count") # another df
    # plot the 50 most common words
    ax = sns.barplot(data=d, x= "word", y = "count")
    ax.set(xlabel='20 Most Common Words/Unigrams in the Streamed Reddit Comments for Politics', ylabel = 'Word Frequency')
    plt.show()
    

def plot_bigrams(df_in):
    """
    This function takes in a pandas df and plot the 20 most frequently occuring 
    bigrams using nltk and matplotlib libraries
    
    Parameters
    ----------
    df_in : a pandas DataFrame

    Returns
    -------
    a histogram
   
    Examples
    --------
    >>> from yi_package import yi_package
    >>> df_in = reddit
    >>> plot_unigrams(reddit)
    >>> Please refer to Reddit_project_presentation.ipynb located in the same directory as this .py file for the outputted histogram.
    """           
    fig = plt.figure(figsize = (15, 5))
    first_ele = [str(i[0]) for i in get_bigrams(df_in)]
    second_ele = [i[1] for i in get_bigrams(df_in)]    
    x = first_ele
    y = second_ele
    # print(x)
    # print(y)
    plt.bar(first_ele, second_ele, color ='green')
    # add labels
    plt.xlabel("20 Most Common Words/bigrams in the Streamed Reddit Comments for Politics")
    plt.ylabel("Word Frequency")
    plt.xticks(x, rotation=90)    
    plt.show()
    


def word_cloud(df_in):
    """
    This function takes in a pandas dataframe and plot out a word cloud from 
    the inputted dataframe's cleaned_comments column using a Trump silouette 
    mask image as the word cloud's background image
    
    Parameters
    ----------
    df_in : a pandas DataFrame

    Returns
    -------
    a word cloud
   
    Examples
    --------
    >>> from yi_package import yi_package
    >>> df_in = reddit
    >>> word_cloud(reddit)
    >>> Please refer to Reddit_project_presentation.ipynb located in the same directory as this .py file for the outputted wordclouds.
    """      
    concat_str = df_in['cleaned_comments'].str.cat(sep=' ') # concatenate all the comments in one single long str    
    # Load the Trump mask image path
    url = 'https://www.wpclipart.com/dl.php?img=/American_History/presidents/additional_images/Donald_Trump/Trump_silhouette.png'    
    # Use requests to get the image data and then uses BytesIO and Image.open() to import the image
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    # Create the wave_mask by converting the image data into a numpy array
    wave_mask = np.array(img)        
    # Make the figure from the concatenated reddit comments
    wordcloud = WordCloud(mask=wave_mask, random_state=80, contour_width=1,
                          contour_color='orange').generate(concat_str)    
    # Create matplotlib figure
    fig = plt.figure(figsize=(15, 10))  
    # Display image on our figure
    plt.imshow(wordcloud, interpolation="bilinear")   
    # Turn off axes and set a dark background to avoid a white area saved around the image
    plt.axis("off")
    plt.style.use('dark_background')
    plt.show()

 

