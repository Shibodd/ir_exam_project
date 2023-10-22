def is_not_too_long(body):
  return True


def is_deleted(comment_body):
  return comment_body =='[removed]' or comment_body == '[deleted]'


def filter_comment_body(body):
  return (not is_deleted(body)) and is_not_too_long(body)