def is_not_too_long(content):
  return len(content) < 100

def is_deleted(content):
  return content =='[removed]' or content == '[deleted]'

def filter_comment_content(content):
  return (not is_deleted(content)) and is_not_too_long(content) 

def filter_comment(comment):
  return filter_comment_content(comment['content'])