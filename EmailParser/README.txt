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

2/23/15 @ 1630:
        - renamed removeReplies to formatEmail
        - fixed bug where individual sentences weren't being checked

2/26/15 @ 0037:
        - took out an unnecessary "if" statement
        - added directory as an argument with a default value
        - added a line to allow run on mine and Brenden's with no edits to the code
        - changed function names and variable names to more pythonic style
        - other cleanup


TODO:
    - remove replies
    - improve performance
    - elastic searching/case ignore

