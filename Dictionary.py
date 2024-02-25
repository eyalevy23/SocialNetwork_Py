
from enum import Enum
from enum import Enum, auto

class UpdateType(Enum):
    START_UP = auto()
    FOLLOW = auto()
    UNFOLLOW = auto()
    LOGIN = auto()
    LOGOUT = auto()
    PUBLISH_POST = auto()
    LIKE = auto()
    COMMENT = auto()
    DISCOUNT = auto()
    SOLD = auto()
    SHOW_PIC = auto()
    UNKNOWN = auto()

    def format_message(self, *args):
        message_formats = {
            UpdateType.START_UP: 'The social network {} was created!',
            UpdateType.FOLLOW: '{} started following {}',
            UpdateType.UNFOLLOW: '{} unfollowed {}',
            UpdateType.LOGIN: '{} connected',
            UpdateType.LOGOUT: '{} disconnected',
            UpdateType.PUBLISH_POST: '{}',
            UpdateType.LIKE: 'notification to {}: {} liked your post',
            UpdateType.COMMENT: 'notification to {}: {} commented on your post: {}',
            UpdateType.DISCOUNT: 'Discount on {} product! the new price is: {}',
            UpdateType.SOLD: "{}'s product is sold",
            UpdateType.SHOW_PIC: 'Shows picture',
            UpdateType.UNKNOWN: 'Unknown update type'
        }
        return message_formats.get(self).format(*args)


class PostType:
    TEXT = 'Text'
    IMAGE = 'Image'
    SALE = 'Sale'

class NotificationType(Enum):
    NEW_POST = auto()
    LIKE = auto()
    COMMENT = auto()
    SOLD = auto()
    UNKNOWN = auto()

    def format_message(self, username):
        message_formats = {
            NotificationType.NEW_POST : '{} has a new post',
            NotificationType.LIKE : '{} liked your post',
            NotificationType.COMMENT : '{} commented on your post',
            NotificationType.SOLD : 'Your post is sold.',
            NotificationType.UNKNOWN : 'unknown message'
        }
        return message_formats.get(self).format(username)

class ConnectionState(Enum):
    CONNECTED = True
    DISCONNECTED = False

