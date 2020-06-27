# socialmedia

Design an API for a posts like/dislike system for a social media site similar to facebook, instagram, etc... the system allows users to see posts that have been added by the admin (user won't be able to submit posts, only read them for now). users are allowed to either like or dislike the posts and the next set of posts should be based on posts users previously liked or disliked.

Example:
  Admin added a post about cats containing 3 images of cats, and a cute description and adds 3 tags A, B, C with corresponding weight.
  The Admin then goes about adding another 100 posts, out of which 7 posts have the tags A, B, C. Now, if a user is shown the cat post and they decides to like it, then they will be shown one or more posts from the 7 posts that was similar to the cat post according to their tag's weight. But, if the user were to dislike the cat post then they would be shown none of the 7 similar posts rather these posts would be push down in the list of post for the particular user
