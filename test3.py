

#!/usr/bin/python
import praw
import re

def isThreadOpen(comment):
	parent_comment = comment.parent().body
	searchObj = re.search('/open', parent_comment, re.I)
	if searchObj:
		return True
	else:
		return False
		
def isDeleted(comment_id, file):
	if comment_id in open(file).read():
		return True
	else:
		return False
	

reddit = praw.Reddit('bot')
subreddit = reddit.subreddit("strictReply")
submission = reddit.submission(url="https://www.reddit.com/r/strictReply/comments/azvbkn/subreddit_to_test_bot_that_trims_comment_trees/")


thread_number = 0 #counter to track threads
deleted_comments = open("deleted_post_ids.txt", "a+")
#deleted_posts = []
for submission in subreddit.new(limit=5):
	comments = submission.comments
	comments.replace_more(limit=None)
	for comment in comments: #loops through root comments in submission
		rootAuthor = comment.author #stores the author name of current root comment
		reply_list = comment.replies #creates a CommentForest object with all replies to root comment
		f_reply_list = reply_list.list() #converts the CommentForest to a flat list in order to iterate through it
		thread_number +=1 #increments thread counter
		i=0 #initialise i, which is used to iterate through all comments in a thread
		while i<len(f_reply_list): #iterates through replies in current thread
		#debugging print statements 
			print("("+str(thread_number)+")")
			print("Author: ")
			print(f_reply_list[i].author)
			print("Replied to :")
			print(f_reply_list[i].parent().author)
			if f_reply_list[i].author==rootAuthor:
				print("rootAuthor reply!")
			if (f_reply_list[i].parent().author!=rootAuthor and f_reply_list[i].author!=rootAuthor) and not isThreadOpen(f_reply_list[i]): 
				#if the parent comments' author is not the rootAuthor AND the author of the reply is not the rootAuthor AND the thread has been declared 'open':
				#start the process of removing the comment
				badcomment_id = f_reply_list[i].id #comment id of comment to be removed
				badcomment_author = str(f_reply_list[i].author) #author name of comment to be removed
				badcomment_parent = str(f_reply_list[i].parent().author) #author name of parent comment of comment to be removed
				bad_comment_submission_link = str(f_reply_list[i].submission.permalink) #submission link
				badcomment = reddit.comment(badcomment_id) #the bad comment
				
				if not isDeleted(badcomment_id,"deleted_post_ids.txt") : #checks if the comment already been deleted (had problems with multiple deletions of same comment due to moderators ability to see deleted comments)
					deleted_comments.write(str(badcomment_id)+"\n") #add the badcomment_id to a txt file
					badcomment.mod.remove() #remove the comment
					reddit.redditor(badcomment_author).message('Comment removal', 
					'Your reply to user "' +badcomment_parent+ '" on this submission: ' +bad_comment_submission_link+' has been removed as it does not comply with our posting guidelines. The guidelines can be found on the sidebar of /r/strictReply', 
					from_subreddit='strictReply') #msg the author of removed comment
					#deleted_posts.append(badcomment_id) 
					print("COMMENT REMOVED!")
				
			print("-------------------------------------------------------------------------------")
			
			i+=1
	
	
	
		
		
		
			
			
		
		
		#comment_list = reddit.submission.comments.list()
		#print(submission.comments[0].body)
		
    
