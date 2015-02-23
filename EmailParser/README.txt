DEPENDENCIES:
    - nltk (from nltk.org, I installed with 'sudo pip install -U nltk')
        *Note: will need to download the 'punkt' package as well. To
         do this open IDLE and type 'import nltk' and then
         'nltk.download()' then browse and download the package.


The main purpose of this document is to keep anyone collaborating
with me (Luke Lindsey) on this up to date with progress.

From now on, place comments about what was worked on with each
commit (or each session if you want to commit frequently). Also,
a to do section is at the bottom.

2/22/15 @ 1920:
        - added a processEmail method to clean it the main method
        - added an extractSentences method that appears to be
        working (needs testing)
        - added a removeReplies (if you want to rename, please do)
        method that doesn't have any functionality but will need to
        be implemented soon


TODO:
    - remove replies
    - send sentence (along with info) along to DB
    - improve performance
    - elastic searching

