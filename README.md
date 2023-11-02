# Installation
Clone this repo: `git clone https://github.com/Shibodd/ir_exam_project` <br/>
Cd to the repo folder: `cd ir_exam_project`

Optionally, but recomended: <br/>
Create a venv: `python3 -m venv venv` <br/>
Activate it: `./venv/Scripts/Activate.sh` or `./venv/Scripts/Activate.ps1` <br/>

Install the dependencies with: `pip install -r requirements.txt`

Download the index (1.2GiB) at `https://github.com/Shibodd/ir_exam_project/releases/download/index-v3/indexdir.7z` and extract the index directory with your favourite archive manager.

# Usage

To run benchmark and display results: `python3 benchmark.py indexdir ./the_benchmark -g`

To perform a search: `python3 search.py indexdir <main_query> [sentiment_query]`

To create the index from scratch: `python3 async_index_creator.py indexdir`

To count the documents in the index: `python3 count_documents.py indexdir`

To update an old index version: `python3 update_indexpy indexdir <from_version> <to_version>`

# Benchmarks

### Sentiment might mildly help recall in very specific queries, but it is used only for ranking. Query terms are ORed by default. Sentiment query is optional.
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
**UIN 4**: "I remember a show of which opening was a cover of a hungarian song. What's the show called?" <br/>
**Content**: hungarian song cover <br/>
**Sentiment**: EMPTY

Comments from which the user can infer the correct show title are scored 2.
Comments which hint at the opening are scored 1.
Misleading comments are scored 0, together with unrelevant ones.

In this query, a comment from the wrong show but with the correct context (in the thread, they're talking about the correct show, but the comment itself doesn't make it explicit) is indipendently ranked second, without displaying any context.
This results in the user being mislead by the wrong show title.


### Documents and queries are preprocessed by tokenizing (on whitespace), lowercasing, removing stopwords and finally stemming.
**UIN 5**: "I heard about a show in which the protagonist owns a fearsome flying turtle pet which has a laser cannon and can drop acid. What's it called?" <br/>
**Content**: the flying acidic TurTle with LASER cannon <br/>
**Sentiment**: fear

Comments which talk about the correct flying turtle and mention something about it that makes it fearsome are ranked 2.
Comments which just talk about the correct flying turtle are ranked 1.

Note that we intentionally insert stopwords, add stems to terms and randomly use uppercase letters in the query. All of this is fixed by the preprocessing step.


### Proximity searches to improve precision.
**UIN 6**: "I remember a show about this girl skipping the qualifiers of a very important championship to go on a class trip. What show was that?" <br/>
**Content**: skip AND qualifier <br/>
**Sentiment**: EMPTY

Compare the above with 

**UIN 7**: The same as **UIN 6** <br/>
**Content**: "skip qualifier"~4 <br/>
**Sentiment**: EMPTY

Note that because the UIN is the same, the comment scores are also the same.


### Sentiment heavily affects the results of generic queries.
**UIN 8**: "I love when characters develop in unpredictable ways. What are some shows i could watch?" <br/>
**Content**: character development<br/>
**Sentiment**: surprise

Compare with

**UIN 9**: "I'd like not to watch any shows for which people got angry at the character development. What shows should i avoid?"<br/>
**Content**: character development<br/>
**Sentiment**: anger OR disgust

Please note that when benchmarking such generic queries the IDCG lower bound is worthless, as just a small part of the results has been scored.
The other UINs, however, have been handpicked so that the result collection is known, and thus the IDCG lower bound is a decent approximation of the real value.
