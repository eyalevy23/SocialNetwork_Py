# Define constants for update types
FOLLOW = 'follow'
UNFOLLOW = 'unfollow'
LOGIN = 'login'
LOGOUT = 'logout'
PUBLISH_POST = 'publish_post'
LIKE = 'like'
COMMENT = 'comment'
DISCOUNT = 'discount'
SOLD = 'sold'
UNKNOWN = 'Unknown'
INFO = 'network_info'

# Define constants for PostFactory class
TEXT = 'Text'
IMAGE = 'Image'
SALE = 'Sale'

# Define constants for notifaction types
PRINT_MESSAGES = {
    FOLLOW : '{} started following {}',
    UNFOLLOW: '{} unfollowed {}',
    LOGIN : '{} connected',
    LOGOUT : '{} disconnected',
    PUBLISH_POST : '{}',
    LIKE : 'notification to {}: {} liked your post',
    COMMENT : 'notification to {}: {} commented on your post: {}',
    DISCOUNT : 'Discount on {} product! The new price is: {}',
    SOLD : "{}'s product is sold",
    INFO : 'The social network {}:',
    UNKNOWN : 'Unknown update type'
}

NOTIFI_NEWPOST = 'new_post'
NOTIFI_LIKE = 'like'
NOTIFI_COMMENT = 'comment'
NOTIFI_SOLD = 'sold'

NOTIFICATION_MESSAGES = {
    NOTIFI_NEWPOST : '{} has a new post',
    NOTIFI_LIKE : '{} liked your post',
    NOTIFI_COMMENT : '{} commented on your post',
    NOTIFI_SOLD : 'Your post is sold.',
    UNKNOWN : 'unknown message'
}