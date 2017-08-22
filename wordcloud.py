import re, string, operator
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


class Counter(dict):
    def __missing__(self, key):
        return 0



class Canvas():
    def __init__(self, height=1, width=1):
        self.height = height
        self.width = width
        self.boxes = []

    def find_position(self, lx, ly):
        return (0,0)

    def add(self,x,y,lx,ly):
        self.boxes.append([x,y,lx,ly])


        
        
def read_file(filename):
    return open(filename).read()


def text_to_words(text):
    return text.split()


def tokenize(word):
    word = word.lower() # to lower case
    word = word.translate({ord(c): None for c in string.punctuation})  # remove punctuations
    word = word.translate({ord(c): None for c in string.digits})  # remove numbers
    return word


def pre_process(words):
    '''
    words pre-processing

    R text process refs: https://cran.r-project.org/web/packages/tm/tm.pdf
    Python package: NLTK (but a heavy package)
    '''

    words = [tokenize(word) for word in words] # to lower case
    
    return words



    
def words_to_freq(words):
    freq = Counter()
    for word in words:
        freq[word] += 1
    return freq



def plot_from_freq(freq):
    freq = sorted(freq.items(), key=operator.itemgetter(1), reverse=True)
    freq = freq[:10]
    max_freq = float(freq[0][1])

    max_size = 40
    min_size = 3

    width = 10
    height = 10
    # plot = Canvas(width,height)
    # fig = plt.figure(frameon=False)
    f = plt.figure(frameon=False)
    ax = f.add_axes([0, 0, 1, 1])
    ax.axis('off')
    
    for word, f in freq:
        f_normalize = f/max_freq # normalize frequency
        size = (max_size - min_size) * f_normalize + min_size

        # x,y = plot.find_position()
        t = ax.text(0.5,0.5,word,fontsize=size)
        print(t.get_position())
        transf = ax.transData.inverted()
        bb = t.get_window_extent(renderer = f.canvas.renderer)
        bb_datacoords = bb.transformed(transf)
        print(t.get_unitless_position())
        exit()

    plt.savefig('test.pdf')   
    return



class WordCloud(object):
    def __init__(self):
        return

    
    def plot(freq):
        '''
        
        R world cloud refs: https://cran.r-project.org/web/packages/wordcloud/wordcloud.pdf
        
        '''
