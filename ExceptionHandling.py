class SocialNetworkError(Exception):
    """Base class for social network related errors."""
    def __init__(self, *args):
        super().__init__(self.ERROR_MESSAGE.format(*args))

class UserNotCoonectedError(SocialNetworkError):
    """Exception raised when a user is not connected and tring to interact with social network."""
    ERROR_MESSAGE = "User : {} Not Conncted while atempting to interact with {}"

class UserAlreadyExistsError(SocialNetworkError):
    """Exception raised when attempting to add a user that already exists."""
    ERROR_MESSAGE = "'{}' already exists in the social network."

class UserNotFoundError(SocialNetworkError):
    """Exception raised when a user is not found in the social network."""
    ERROR_MESSAGE = "user : {} not exist"

class SingletonClassError(SocialNetworkError):
    """Exception raised when attempting to create multiple instances of a singleton class."""
    ERROR_MESSAGE = 'This is a singalton class and you already have SocialNetwork class called : {}'

class InvalidPostType(SocialNetworkError):
    """Exception raised when main send unknoen type of post"""
    ERROR_MESSAGE = 'Invalid post type : {} support only for ("Text", "Image", "Sale")'

class PasswordError(SocialNetworkError):
    """Base class for for invalid passwords."""
    ERROR_MESSAGE = 'Invalid password'

class PasswordNotMatchingError(PasswordError):
    """Exception raised when tring to accses user with wrong password"""
    ERROR_MESSAGE = 'Someone tring to accses "{}" with wrong password'

class SingupPasswordError(PasswordError):
    """Exception raised when while signup user chose invilid password that is not between 4 to 8 digit"""
    ERROR_MESSAGE = ""

class FollowError(SocialNetworkError):
    """Base class for follow-related errors."""


class UserAlreadyFollowedError(FollowError):
    """Exception raised when attempting to follow a user already being followed."""
    ERROR_MESSAGE = '{} already follow {}'


class CannotFollowYourselfError(FollowError):
    """Exception raised when attempting to follow yourself."""
    ERROR_MESSAGE = "{} try to follow himself"


class CannotUnfollowYourselfError(FollowError):
    """Exception raised when attempting to unfollow yourself."""
    ERROR_MESSAGE = "cant unfollow yourself"

class UserNotFollowingError(FollowError):
    """Exception raised when attempting to unfollow a user not being followed."""
    ERROR_MESSAGE = "{} tring to unfollow {} but don't follow {}"