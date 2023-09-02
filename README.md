# COMP6714 Boolean Retrivel by using shunting yard algorithm

## Project: Westlaw alike queries

As presented in the lecture, Westlaw is a popular commercial information retrieval system. You can search for documents by Boolean Terms and Connector queries. For example:
STATUTE ACTION /S FEDERAL /2 TORT /3 CLAIM

where **STATUTE, ACTION, FEDERAL, TORT, CLAIM** are the search terms and _space, /S, /2, /3_ are the connectors.

In this project, you are going to implement a retrieval system in Python3 called SimplyBoolean, which you have already encountered in the assignment. As a core requirement for this project, you must implement SimplyBoolean using a **positional index**.

SimplyBoolean is a retrieval system that supports Westlaw alike queries. It supports the following reduced set of connectors:

`" ", space, +n, /n, +s, /s, &`

as well as parentheses. Note that the connectors of your query will be processed in exactly the order above. Further details of these connectors can be found in the Quick Reference Guide of WestLaw available from WebCMS.

Different to Westlaw, SimplyBoolean does not support various forms of search terms, except a normal search term (i.e. single-word, those without " ") and a phrase.

Term matching (including terms in a phrase) in SimplyBoolean follows the below:

- Search in SimplyBoolean is case insensitive.
- Full stops for abbreviations are ignored. e.g., U.S., US are the same.
- Singular/Plural is ignored. e.g., cat, cats, cat's, cats' are all the same.
- Tense is ignored. e.g., breaches, breach, breached, breaching are all the same.
- A sentence can only end with a full stop, a question mark, or an exclammation mark.
- Except the above, all other punctuation should be treated as token dividers.
- All (whole) numeric tokens such as years, decimals, integers are ignored. You should not index these tokens and hence should not consider them for proximity queries such as +n. E.g. you should not index '123' (wholly numeric) but should index 'abc123' (partially numeric).

You are provided with approximately 1000 small documents (named with their document IDs). Your submitted project will be tested against a similar collection of up to 1000 documents (i.e., we may replace some of these documents to avoid any hard-coded solutions).

Your submission must include 2 main programs: index.py and search.py as described below.

### The Indexer

```
$ python3 index.py [folder-of-documents] [folder-of-indexes]
```

where [folder-of-documents] is the path to the directory for the collection of documents to be indexed and [folder-of-indexes] is the path to the directory containing the index file(s) be created. All the files in [folder-of-documents] should be opened as read-only, as you may not have the write permission for these files. If [folder-of-indexes] does not exist, create a new directory as specified. You may create multiple index files although too many index files may slow down your performance. The total size of all your index files generated shall not exceed 20MB (which should be plenty for this project).

After the indexing is completed, it will output the total number of documents, the total number of tokens (after any preprocessing and filtering) to be indexed, and the total number of terms to be indexed. The following example illustrates the required input and output formats:

```
$ python3 index.py ~/Desktop/MyDataFolder ./MyTestIndex
Total number of documents: 672
Total number of tokens: 638321
Total number of terms: 13297
```

Note: the output of index.py ends with one newline ('\n') character.

### Searching

```
$ python3 search.py [folder-of-indexes]
```

where [folder-of-indexes] is the path to the directory containing the index file(s) that are generated by the indexer. After the above command is executed, it will accept a search query from the standard input and output the result to the standard output as a sequence of document names (the same as their document IDs) one per line and sorted in an ascending order by their numeric values (e.g., 72 will be output before 125). It will then continue to accept the search queries from the standard input and output the results to the standard output until the end (i.e., a Ctrl-D). The following example illustrates the required input and output formats:

```
$ python3 search.py ~/Proj/MyTestIndex
company inc & revenue
9
17
33
185
share +5 investor & US
3
67
271
365
499
625
$
```

### Chaining Mixed Connectors

Example:

`a b /s c`

Explanation: As per the WestLaw guide, following the precedence rules for this example, OR (the space) has higher priority. Because OR is a boolean connector, we can re-write the query into an equivalent form below:

`(a /s c) (b /s c)`

Chaining Non-boolean Connectors
Example:

`a +n b /s c`

Explanation: The connector precedence here lies with '+n' first, then '/s'. This query can be understood as the equivalent of doing (a +n b) first, then only among the documents (and more importantly, their postings), we will output the documents for which (a /s c) (for the same posting 'a') or (b /s c) (for the same posting 'b') is true. To further explain in english, the query wants documents where either:

- there is 'a' which precedes 'b' by at most 'n' terms, that same occurrence of 'a' is in a sentence with 'c'
- there is 'a' which precedes 'b' by at most 'n' terms, that same occurrence of 'b' is in a sentence with 'c'

Another example:

`a +n (b /s c)`

Explanation: With the presence of parentheses, this query will have (b /s c) processed first. From the resulting document postings, we will output the documents for which (a +n b) (for the same posting 'b') or (a +n c) (for the same posting 'c') is true. To further explain in english, the query wants documents where either:

- there is 'b' in a sentence with 'c', that same occurrence of 'b' occurs at most 'n' terms after 'a'
- there is 'b' in a sentence with 'c', that same occurrence of 'c' occurs at most 'n' terms after 'a'
