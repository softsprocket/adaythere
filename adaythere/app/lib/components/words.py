
import string


class WordCount ():

    words_to_skip = [
        "a", "all", "an", "and", "another", "any", "anybody", "anyone", "anything", 
        "both", "but", "each", "either", "everybody", "everyone", "everything", "few", "for",
        "he", "her", "hers", "herself", "him", "himself", "his", "I", "it", "its", "itself", "many",
        "me", "mine", "more", "most", "much", "my", "myself", "neither", "nobody",
        "none", "nor", "nothing", "one", "or", "other", "others", "or", "our", "ours", "ourselves",
        "several", "she", "so", "some", "somebody", "someone", "something", "that",
        "the","their", "theirs", "them", "themselves", "these", "they", "this", "those",
        "us", "we", "what", "whatever", "which", "whichever", "who", "whoever",
        "whom", "whomever", "whose", "yet", "you", "your", "yours", "yourself", "yourselves"
    ]

    def count (self, word_str):
    
        word_list = word_str.lower ().split ()
        stripped_word_list = map(lambda x: string.strip (x, string.punctuation), word_list)

        word_count_list = {}
        for word in stripped_word_list:
            if word == "" or word in WordCount.words_to_skip:
                continue

            wc = word_count_list.get (word, 0)
            wc += 1
            word_count_list[word] = wc

        return word_count_list



