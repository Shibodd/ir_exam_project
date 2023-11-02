# Benchmarks


### Sentiment might mildly help recall. Query terms are ORed by default. Sentiment query is optional.
For this, note that the show title is shown together with the comment content in the results.

There are only 2 comments which describe the scene in detail and they have score 2.
Comments which hint about the scene but do not explicitly describe it are scored 1.

The search engine fails to recall the second comment scored 2.

**UIN 1**: "I remember a show in which the protagonist punched her schoolmate in the face, after turning around to check if the teacher was looking. What is the show called?" <br/>
**Content**: punch face check teacher <br/>
**Sentiment**: <ins>EMPTY</ins>

Compare results with:

**UIN 2**: "I remember a show in which the protagonist punched her schoolmate in the face, after turning around to check if the teacher was looking. <ins>I remember it being a really funny scene </ins>. What is the show called?" <br/>
**Content**: punch face check teacher <br/>
**Sentiment**: <ins>joy</ins>


### Can search by part of title together with content. Can specify AND to have an intersection in the boolean matcher. Sentiment is fundamental for this UIN.
Any comment which explicily expresses hate against the character is scored 2.
Mild hate is scored 1.

**UIN 3**: "I want to read hate comments against Kaya from Watashi no Shiawase na Kekkon." <br/>
**Content**: kaya AND title:(shiawase kekkon) <br/>
**Sentiment**: anger disgust


### Comments are assumed to be independent and the submission is not used as context.
Comments from which the user can infer the correct show title are scored 2.
Comments which hint at the opening are scored 1.
Misleading comments are scored 0, together with unrelevant ones.

In this query, a comment with the correct context (in the thread, they're talking about the correct show) is indipendently ranked second, without displaying any context.
This results in the user being mislead by the wrong show title.

**UIN 4**: "I remember a show of which opening was a cover of a hungarian song. What's the show called?"
**Content**: hungarian song cover
**Sentiment**: EMPTY


### Documents and queries are preprocessed by tokenizing (on whitespace), lowercasing, removing stopwords and finally stemming.

**UIN 5**: "I heard about a show in which the protagonist owns a fearsome flying turtle pet which has a laser cannon and can drop acid. What's it called?"
**Content**: fly the TurTlIng acidic LASER cannon
**Sentiment**: fear