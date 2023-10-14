
import pandas as pd
import praw
from sentiment import sentiment_analysis

reddit = praw.Reddit(
  client_id="fyFBUMdaXtoogBzfHs-FQg",
  client_secret="1Wkzf7IRXGgHnd_HScgPpFJUwc6IZg",
  password="thequickbrownfoxjumpsoverthelazydog",
  user_agent="unimore-ir-sentiment-analysis",
  username="Extension_Pudding570",
)

#df = pd.DataFrame()
#titles=["Sword art online","Pizzeria de Mario"]
#ids =["11234","234214"]
#scores = ["3000000","328481248"]

# Create sub-reddit instance
subreddit_name = "deeplearning"
subreddit = reddit.subreddit(subreddit_name)

df = pd.DataFrame() # creating dataframe for displaying scraped data

# creating lists for storing scraped data
titles=[]
content=[]
sentiment=[]
scores=[]
list_episode=[]
ids=[]

# looping over posts and scraping it
for submission in subreddit.top(limit=21):
    titles.append(submission.title)
    scores.append(submission.content) #upvotes
    sentiment.append(sentiment_analysis.classify_text())
    list_episode.append(submission.list_number)
    ids.append(submission.id)
    
    
df['Title'] = titles
df['Content']=content
df['Sentiment']=sentiment
df['List_Episode']=list_episode
df['Id'] = ids
df['Upvotes'] = scores #upvotes

print(df.shape)
df.head(10)