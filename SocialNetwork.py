from Dictionary import *
from ExceptionHandling import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def require_connection(func):
    # Check for user conncetion
    def wrapper(self, *args):
        user = getattr(self, 'owner', self)
        if isinstance(self, Post) and isinstance(args[0], User):
            user = args[0]
            
        if user.connction_state == ConnectionState.DISCONNECTED:
            raise UserNotCoonectedError(user.username, user.network.network_name)

        return func(self, *args)
    return wrapper

class UsersList(dict):
    def __missing__(self, __key):
        raise UserNotFoundError(__key)
    
    def __setitem__(self, __key, __value) -> None:
        if __key in self:
            raise UserAlreadyExistsError(__key) 
        return super().__setitem__(__key, __value)
    
class Singalton:
    _instance = None
    def __new__(cls, *args, **kwargs) -> object:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        else:
            raise SingletonClassError(cls._instance.network_name)
        return cls._instance

class SocialNetwork(Singalton):
    def __init__(self, network_name):
        self.network_name = network_name
        self.users_list = UsersList()
        self.feed = []
        self.update_network(UpdateType.START_UP, network_name)

    #  Create a new user and add them to the social network.
    def sign_up(self, username, password):
        self.validate_password(password)
        new_user = User(username, password, self)
        self.users_list[username] = new_user
        return new_user
        
    def upload_posts(self, post):
        self.attached_post(post)
        self.notify_followers(post)
        self.update_network(UpdateType.PUBLISH_POST, post)
    
    # attached post to owner and SocialNetwork
    def attached_post(self,post):
        self.feed.append(post)
        post.owner.posts.append(post)

    def validate_password(self,password):
        if not 4 <= len(password) <= 8:
            raise SingupPasswordError()

    def log_out(self, username):
        self.users_list[username].disconnect()
        self.update_network(UpdateType.LOGOUT, username)
    
    def log_in(self, username, password):
        user = self.users_list[username]
        if password != user.password:
            raise PasswordNotMatchingError(username)
        user.connect()
        self.update_network(UpdateType.LOGIN, username)

    # Notify followers of a user about a new post.
    def notify_followers(self, post):
        for user in post.owner.following:
            user.update(NotificationType.NEW_POST, post.owner.username)

    #  Method to print updates based on the updates in SocialNetwork
    #  when user post ,like, comment etc ... 
    def update_network(self, update_type, *args):
        message_format = UpdateType.format_message(update_type, *args)
        print(message_format)

    def __str__(self):
        network_info = '\n'.join(str(user) for user in self.users_list.values())
        return f'{self.network_name} social network:\n{network_info}\n'

class CustomList(list):
    def __init__(self, onwer):
        super().__init__()
        self.owner = onwer

    def append(self, __object) -> None:
        if __object in self:
            raise UserAlreadyFollowedError(self.owner, __object.username)
        if self.owner is __object.username:
            raise CannotFollowYourselfError(self.owner)
        return super().append(__object)
    
    def remove(self, __value) -> None:
        if self.owner is __value.username:
            raise CannotUnfollowYourselfError()
        if __value not in self:
            raise UserNotFollowingError(self.owner, __value.username, __value.username)
        return super().remove(__value)

class User():
    def __init__(self, username, password, network):
        self.username = username
        self.password = password
        self.connction_state = ConnectionState.CONNECTED
        self.network = network
        self.followers = CustomList(username)
        self.following = CustomList(username)
        self.posts = []
        self.notifications = []

    # Update the user with a notification.  
    def update(self, type, username = None):
        message_format = NotificationType.format_message(type, username)
        self.notifications.append(message_format)

    def connect(self):
        self.connction_state = ConnectionState.CONNECTED

    def disconnect(self):
        self.connction_state = ConnectionState.DISCONNECTED

    @require_connection
    def follow(self, other_user):
        self.followers.append(other_user)
        other_user.following.append(self)
        self.network.update_network(UpdateType.FOLLOW, self.username, other_user.username)

    @require_connection
    def unfollow(self, other_user):
        self.followers.remove(other_user)
        other_user.following.remove(self)
        self.network.update_network(UpdateType.UNFOLLOW, self.username, other_user.username)

    @require_connection
    def publish_post(self, type, post_content, *args):
        post = PostFactory.create_post(self, type, post_content, *args)
        self.network.upload_posts(post)
        return post

    def print_notifications(self):
        header = f"{self.username}'s notifications:\n"
        notifications_block = '\n'.join(self.notifications)
        print(header + notifications_block)

    def __str__(self):
        return f"User name: {self.username}, Number of posts: {len(self.posts)}, Number of followers: {len(self.following)}"


# Factory pattern
class PostFactory:
    @staticmethod
    def create_post(owner, post_type, *args):
        if post_type == PostType.TEXT:
            return TextPost(owner, *args)
        if post_type == PostType.IMAGE:
            return ImagePost(owner, *args)
        if post_type == PostType.SALE:
            return SalePost(owner, *args)
        else:
            raise InvalidPostType(post_type)

class Post:
    def __init__(self, owner, content):
        self.owner = owner
        self.content = content
        self.likes = set()
        self.comments = []

    @require_connection
    def like(self, user):
        self.likes.add(user)
        if user is not self.owner:
            self.owner.update(NotificationType.LIKE, user.username)
            self.owner.network.update_network(UpdateType.LIKE, self.owner.username, user.username)

    @require_connection
    def comment(self, user, comment):
        self.comments.append((user, comment))
        if user is not self.owner:
            self.owner.update(NotificationType.COMMENT, user.username)
            self.owner.network.update_network(UpdateType.COMMENT, self.owner.username, user.username, comment)

# Subclasses of Post
class TextPost(Post):
    def __str__(self):
        return f'{self.owner.username} published a post:\n"{self.content}"\n'

class ImagePost(Post):
    def display(self):
       img = mpimg.imread(self.content)
       plt.imshow(img)
       plt.show()
       self.owner.network.update_network(UpdateType.SHOW_PIC)

    def __str__(self):
        return f'{self.owner.username} posted a picture\n'

class SalePost(Post):
    def __init__(self, owner, content, price, location):
        super().__init__(owner, content)
        self.price = price
        self.location = location
        self.is_available = True

    @require_connection
    def sold(self, password):
        if self.owner.password == password:
            self.is_available = False
            self.owner.update(NotificationType.SOLD)
            self.owner.network.update_network(UpdateType.SOLD, self.owner.username)
        else:
            raise PasswordNotMatchingError(self.owner.username)

    @require_connection
    def discount(self, discount_percentage, password):
        if self.owner.password == password:
            self.price *= 1 - discount_percentage/100
            self.owner.network.update_network(UpdateType.DISCOUNT, self.owner.username, self.price)
        else:
            raise PasswordNotMatchingError(self.owner.username)
    
    def __str__(self):
        availability = "For sale" if self.is_available else "Sold"
        return (f'{self.owner.username} posted a product for sale:\n'
                f'{availability}! {self.content}, price: {self.price}, pickup from: {self.location}\n')
