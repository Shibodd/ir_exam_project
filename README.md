# Installation
Clone this repo: `git clone https://github.com/Shibodd/ir_exam_project` <br/>
Cd to the repo folder: `cd ir_exam_project`

Optionally, but recomended: <br/>
Create a venv: `python3 -m venv venv` <br/>
Activate it: `./venv/Scripts/Activate.sh` or `./venv/Scripts/Activate.ps1` <br/>

Install the dependencies with: `pip install -r requirements.txt`

Download the index (1.2GiB): `wget URL`

# Usage

To run benchmark and display results: `python3 benchmark.py indexdir ./the_benchmark -g`

To perform a search: `python3 search.py indexdir <main_query> [sentiment_query]`

To create the index from scratch: `python3 async_index_creator.py indexdir`

To count the documents in the index: `python3 count_documents.py indexdir`

To update an old index version: `python3 update_indexpy indexdir <from_version> <to_version>`

# Benchmarks

### Sentiment might mildly help recall in very specific queries. Query terms are ORed by default. Sentiment query is optional.
**UIN 1**: "I remember a show in which the protagonist punched her schoolmate in the face, after turning around to check if the teacher was looking. What is the show called?" <br/>
**Content**: punch face check teacher <br/>
**Sentiment**: <ins>EMPTY</ins>

Compare results with:

**UIN 2**: "I remember a show in which the protagonist punched her schoolmate in the face, after turning around to check if the teacher was looking. <ins>I remember it being a really funny scene </ins>. What is the show called?" <br/>
**Content**: punch face check teacher <br/>
**Sentiment**: <ins>joy</ins>

For this benchmark, note that the show title is shown together with the comment content in the results.

There are only 2 comments which describe the scene in detail and they have score 2.
Comments which hint about the scene but do not explicitly describe it are scored 1.

The search engine fails to recall the second comment scored 2.


### Can search by part of title together with content. Can specify AND to have an intersection in the boolean matcher. Sentiment is fundamental for this UIN. High quality results for simple and generic queries.
**UIN 3**: "I want to read hate comments against Kaya from Watashi no Shiawase na Kekkon." <br/>
**Content**: kaya AND title:(shiawase kekkon) <br/>
**Sentiment**: anger disgust

Any comment which explicily expresses hate against the character is scored 2.
Mild hate is scored 1.


### Comments are assumed to be independent and their tree structure is not used for context.
**UIN 4**: "I remember a show of which opening was a cover of a hungarian song. What's the show called?"
**Content**: hungarian song cover
**Sentiment**: EMPTY

Comments from which the user can infer the correct show title are scored 2.
Comments which hint at the opening are scored 1.
Misleading comments are scored 0, together with unrelevant ones.

In this query, a comment with the correct context (in the thread, they're talking about the correct show) is indipendently ranked second, without displaying any context.
This results in the user being mislead by the wrong show title.


### Documents and queries are preprocessed by tokenizing (on whitespace), lowercasing, removing stopwords and finally stemming.
**UIN 5**: "I heard about a show in which the protagonist owns a fearsome flying turtle pet which has a laser cannon and can drop acid. What's it called?"
**Content**: the flying acidic TurTle with LASER cannon
**Sentiment**: fear

Comments which talk about the correct flying turtle and mention something that induces fear are ranked 2.
Comments which just talk about the correct flying turtle are ranked 1.

Note that we intentionally insert stopwords, add stems to terms and randomly use uppercase letters in the query. All of this is fixed by the preprocessing step.