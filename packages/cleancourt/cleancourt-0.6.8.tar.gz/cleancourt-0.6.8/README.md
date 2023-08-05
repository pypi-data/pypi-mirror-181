
# cleancourt

[![PyPi page link -- version](https://img.shields.io/pypi/v/cleancourt.svg)](https://pypi.python.org/pypi/cleancourt)
[![Number of Downloads](https://img.shields.io/pypi/dm/cleancourt.svg)](https://pypistats.org/packages/cleancourt)
[![Current Issues](https://img.shields.io/bitbucket/issues/lsc_odga/cleancourt.svg)](https://bitbucket.org/lsc_odga/cleancourt/issues)


cleancourt cleans, standardizes, and links legal party names using  natural language processing and string similarity search algorithms. 

While this dataset has only been tested on party information in civil court cases, the methods may work in other contexts. These applications, however, are untested and, as such, we can make no assertions that the validity of their output.

## Set up

```bash
pip install --upgrade cleancourt
```

## Functionality
The cleancourt library has two central functionalities. The first is internal dataset cleaning, which takes in a list of party names and returns a sanitized list that makes a best guess effort at fuzzy matching party names. The second cleancourt functionality is party name comparison to an external dataset. This functionality, which employs similar methods to internal dataset cleaning, is used when comparing a list of 'messy' party names against a list of 'clean' party names.

### Main Functions

#### clean_full_names

```python
cleancourt.clean_full_names(messy_name_list, separate_management=False)
```
The clean_full_names function takes in a list of messy names in the dataset and applies all name cleaning functions to said dataset. The function first cleans the data using pattern matching, then separates the data based on whether a party name refers to an individual or a company. From there, the two datasets are cleaned in isolation using the format_people_names or the link_company_names discussed below. The datasets are then rejoined and linked one more time by removing spaces using the check_spaces function.

The clean_full_names function also takes in an optional boolean parameter to determine whether or not a party name should be separated into two separate lists when a management company is present. When set to True, the party name 'A doing business as B', for example, would be separated into two lists, where B is put in the original column, and A is added to a _managing companies_ column. When set to True, the function will return two lists.

#### compare_companies

```python
cleancourt.compare_companies(
	org_name_messy, 
	org_name_clean, 
	threshold=.25, 
	print_all_matches = False, 
	clean_org_names = [False, False])
```

The compare_companies function takes in a _messy_ list of party names and a _clean_ list of company names and filters out the individual names in the messy dataset before comparing both names. 

The function takes in a list of optional parameteres. _threshold_ is the maximum distance between two names being compared that will be included in the name matching. _print\_all\_matches_ is an internal print function to test functionality, matches returned are printed to a local CSV file. clean_org_names is a boolean array that takes in two values. When set to true, the function will apply the clean_data function to the corresponding list or party names. 


### Internal Dataset Cleaning

For cleaning datasets in isolation, cleancourt currently has four functions, each of which are detailed below. All functions, with the exception of clean_data, take in a list of party names, and return a dictionary with the original names as keys, and the mapped names as values.

#### clean_data
clean_data is the preprocessing function used to ensure that the data is in readable form, and that any minor changes to each string can be made. The method primarily employs regular expression formulas to format and edit the data. This preprocessing step is specifically geared towards cleaning civil court case party names. As such, you may wish to overwrite this function in favor of a data cleaning step that is more applicable to your data.

#### format_people_names
The format_people_names function uses the probablepeople library to find individual names (rather than corporate entities) in the dataset, and parse their first, middle, and last names. The function takes a Pandas DataFrame of names and outputs a dictionary of names in first, middle, last format. As an example, consider the following dataset:

|raw_name|
|--------|
|aldous huxley|
|huxley, aldous|
|ray bradbury|
|bradbury, ray|

The format_people_names function would then return the following dictionary:

```json 
{
"aldous huxley": "aldous huxley",
"huxley, aldous" : "aldous huxley",
"ray bradbury": "ray bradbury",
"bradbury, ray": "ray bradbury"
}
```

#### link_company_names

The link_company_names function takes in a Pandas DataFrame, along with an optional score threshold, and returns a dictionary of key-value pairs in which the key is a particular entry in the DataFrame and the associated value is the linked company determined to by similar to the key by a fuzzy match algorithm. To compute this similarity between strings at scale, we first begin by filtering company names from the dataset using the probablepeople library. 

Once a set of unique company names has been developed, the algorithms used to determine similarity between strings is dependent upon the number of company names being compared. If fewer than 500 company names exist, then we compute the Levenshtein distance. Otherwise we compute scores using Term Frequency Inverse Document Frequency (TF-IDF) and cosine similarities. These methods are used because Levenshtein distance is simple, but time intensive on larger datasets, while TF-IDF and cosine simmilarities scale well for larger datasets, but underperform on smaller datasets.  Both of these methods are discussed below.

##### Levenshtein Distance

This function employs the [RapidFuzz](https://github.com/maxbachmann/RapidFuzz) library to compute a similarity score between a particular name, and all other names in the dataset. By default, all names with a similarity score above 80% are considered the same and linked using a dictionary format. See below for a more detailed discussion of the link_company_names output.


##### TFIDF and Cosine similarities

For datasets larger than 500 names, when a particular string is determined to be a company name, we vectorize it using TF-IDF. Using an ngram of three characters, we first separate the company name into an array of chunks such that the company name 'wayne enterprises' will produce the following array:

```python
['way', 'ayn', 'yne', 'ne ', 'e e', ' en', 'ent', 'nte', 'ter', 'erp', 'rpr', 'pri', 'ris', 'ise', 'ses']
```


Once these arrays have been created for every company name in the dataset, we then create a sparse matrix, which contains all ngrams computed for all company names as one dimension, and all company names as the other dimension. The value at each index within this matrix is then the term frequency of an ngram chunk in a particular company name, multiplied by the inverse frequency of that ngram chunk across all company names. Thus, ngrams that appear frequently across all documents will bring the value at a particular index closer to 0.

In this case, ngrams of three characters were chosen as they are particularly effective at creating a sparse matrix of sufficient size, while also containing enough characters to make each individual ngram unique.

Once we have calculated the scores for each ngram chunk across each document, we then compute the cosine similarity between each document. The cosine similarity is computed by summing the products of each document vector, and dividing it by the square root of the sum of squares of each document vector, multiplied together. To illustrate how this works, consider the following two documents and their vectors computed using TF-IDF.

```python
doc1 = [0,2,1,3,5]
doc2 = [4,2,3,4,1]
```

The cosine similarity of these two documents would be:

```python
doc1 * doc2 = 0*4 + 2*2 + 1*3 + 3*4 + 5*1 = 24
||doc1|| = sqrt(0^2 + 2^2 + 1^2 + 3^2 + 5^2) = 6.1644...
||doc2|| = sqrt(4^2 + 2^2 + 3^2 + 4^2 + 1^2) = 6.7823...

cos_sim = 24 / (6.1644 * 6.7823) = .574

```

The resulting similarity score of these two documents is .574. Documents that are more similar will have a score closer to 1, while documents that are not similar will have a similarity score closer 0. Currently, this method considers all company names with a similarity score above .8 to be the same.


##### Output

Once the similarity scores have been computed, we take the resulting matches and place them in a dictionary where the key is the original company name, and the value is the company name that appears most frequently in the dataset. The following dataset, for example:

raw_name|raw_name_count
--------|--------------
wayne enterprise|10
wayne enterprises|2
wayn enterprises|4
lexcorp | 10
lexco | 5
lex corp. | 4

Would output the following dictionary:

```json
{
"wayne enterprises" : "wayne enterprise",
"wayn enterprises" : "wayne enterprise",
"lexco" : "lexcorp",
"lex corp." : "lexcorp"
}

```

#### check_spaces

The check_spaces is currently applied as a final step in the name standardization process. That is, check_spaces is intended to be run once all other methods have been completed. 

The function takes in a Pandas DataFrame and returns a dictionary of key-value pairs in which the key is a particular entry in the DataFrame and the associated value is a linked name found to contain the exact same characters, except for spaces. 

As with other functions in this library, the method for determining which value should be linked in the dataset is to select the value that appears the most in the dataset.

As an example consider the following dataset, which has grouped the original dataset by the raw name, counted the number of occurrences in the dataset, and also computed the equivalent name with no spaces:

raw_name | raw_name_count | no_space_name
-------- | -------------- | -------------
mary shelley | 10 | maryshelley
mary she lley | 1 | maryshelley
ma ryshelley | 1 | maryshelley
george orwell | 15 | georgeorwell
georg e orwell | 1 | georgeorwell
geor georwell | 3 | georgeorwell
g eorge orwell | 8 | georgeorwell


This dataframe will return the following dictionary:

```json 
{
"mary shelley": "mary shelley",
"mary she lley" : "mary shelley",
"ma ryshelley" : "mary shelley",
"george orwell": "george orwell",
"georg e orwell" : "george orwell",
"geor georwell" : "george orwell",
"g eorge orwell" : "george orwell"
}
```

Rather than return the relevant string with no spaces as the value, the function takes the string with the highest raw_name_count and returns the associated raw_name. This functionality is based on the assumption that the term that appears most frequently in the original dataset is the correct version.


### Dataset Comparisons

#### compare_companies
The compare_companies method takes in a list of 'messy' party names and a list of 'clean' party names and computes the nearest match in the messy dataset to the names in the clean dataset. The method is intended to be used when matching names in two datasets where the names being compared are not an exact match. In this case, the difference between the 'messy' and 'clean' datasets is that the latter is considered the correct value when a match is found between the two datsets.

The method implements a K-Nearest-Neighbors (KNN) search algorithm to compare the lists. Here, individual data points in the messy dataset are compared against the clean dataset. Specifically, with each party name in the messy dataset, the cosine similarity is compared to all values in the clean dataset. The clean string with the cosine similarity value closest to 1 is the nearest neighbor for that value and, if the similarity passes a certain threshold*, the value is considered a match and returned in a dictionary where 'key': party name from messy dataset and 'value': party name from clean dataset.  

*Note: Because KNN is a distance algorithm, the computed threshold is inverted. That is, values that are closer to 0 have less distance between them and are thus more similar. 

## Testing the Code
The data file contains a CSV detailing person and company names. These data were not taken from LSC plaintiff names and instead were adapted from a series of sample datasets, along with manual entry.

You can run all of the methods on this sample dataset by running the tests/sample_people_and_companies.test.py file using the following command: ```python3 -m pipenv run python tests/file_name.py```

Note: to find the files in the src folder, you will need to add the src folder to your python path using ```export PYTHONPATH=${PYTHONPATH}:${PWD}/src```

### sample_people_and_companies_test.py

Running the sample_people_and_companies_test script will create four files in the output directory. Three of the files are json files, which contain the dictionaries output from the link_company_names, format_people_names, and check_spaces functions. The fourth file is a CSV with seven columns. A table with the description for each column is detailed below.

Column Name | Description 
----------- | -----------
first_plaintiff | original value fed to the dataset
clean_names | output after feeding the first_column value to the clean_names function
people_names | output after feeding the clean_names column values to the format_people_names
company_names | output after feeding the clean_names column values to the link_company_names
all_names | combination of clean_names, people_names, and company_names columns
no_space | output after feeding all_names column values to the check_spaces function
all_names_no_space | combination of all_names and no_space columns

### sample_people_and_companies_test_simple.py

Running the sample_people_and_companies_test_simple script will create similar outputs to the sample_people_and_companies_test. However, in this case, only the dictionaries are saved as output. This is done to simplify the code used in the test file.

### sample_compare_companies_test.py
Running sample_compare_companies_test will take in both a 'messy' set of company names and a 'clean' set of company names from the sample dataset of S&P 600 companies. The dataset will then compute the similarity score between each of the companies using cosine similarity and output a dataframe with the mapped company name to the original dataset.

## Authors

Logan Pratico: praticol{at}lsc{dot}gov

## Acknowledgments and References

### ML Python Libraries:
* [probablepeople](https://github.com/datamade/probablepeople)
* [sklearn](https://scikit-learn.org/stable/)
* [SciPy](https://scipy.org/)
* [rapidfuzz](https://github.com/maxbachmann/RapidFuzz)

### Resources and Articles Used to Inform this Library
* [TF-IDF from scratch in python on a real-world dataset](https://towardsdatascience.com/tf-idf-for-document-ranking-from-scratch-in-python-on-real-world-dataset-796d339a4089) - William Scott
* [Fuzzy Matching at Scale](https://towardsdatascience.com/fuzzy-matching-at-scale-84f2bfd0c536) -- Josh Taylor
* [Cosine Similarity // Data Mining: Concepts and Techniques](https://www.sciencedirect.com/topics/computer-science/cosine-similarity) -- Jiawei Han, Micheline Kamber and Jian Pei
* [The Optimization of Fuzzy String Matching Using TF-IDF and KNN](https://audhiaprilliant.medium.com/fuzzy-string-matching-optimization-using-tf-idf-and-knn-b07fce69b58f) -- Audhi Aprilliant
* [Text Classification using K Nearest Neighbors](https://towardsdatascience.com/text-classification-using-k-nearest-neighbors-46fa8a77acc5) -- Sumit Dua
