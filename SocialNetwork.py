from Dictionary import *

# Decorator function to ensure that the user interacting with the SocialNetwork is connected.
def require_connection(func):
    def wrapper(self,*args):
        if isinstance(self, Post) and isinstance(user:=args[0], User):
            user.network.if_user_not_connected_exaption(user)
        elif isinstance(self, Post):
            self.owner.network.if_user_not_connected_exaption(self.owner)
        elif isinstance(self, User):
            self.network.if_user_not_connected_exaption(self)
        return func(self,*args)
    return wrapper

class SocialNetwork:
    _instance = None

    #singleton class
    # Ensure that only one instance of the SocialNetwork class is created.
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        else:
            raise Exception("SocialNetwork is a singleton class")
        return cls._instance

    def __init__(self, network_name):
        self.network_name = network_name
        self.users = {}
        self.posts = []

    #  Create a new user and add them to the social network.
    def sign_up(self, username, password):
        if username in self.users:
            return self.users[username]
        if self.password_check(password):
            raise Exception('Invalid password')
        new_user = User(username, password, self)
        self.users[username] = [new_user, True]
        return new_user
    
    def if_user_not_connected_exaption(self, user):
        if not self.users[user.username][1]:
            raise Exception('user not connected')
    
    def upload_posts(self, post):
        self.posts.append(post)
        self.notify_followers(post)
        self.update_network(PUBLISH_POST, post)
    
    def password_check(self,password):
        return len(password) < 4 or 8 < len(password) 

    def log_out(self, username):
        if username not in self.users:
            raise Exception('user not exist')
        self.users[username][1] = False
        self.update_network(LOGOUT, username)
    
    def log_in(self, username, password):
        if username not in self.users:
            raise Exception('user not exist')
        if password != self.users[username][0].password:
            raise Exception('password not matching')
        self.users[username][1] = True
        self.update_network(LOGIN, username)

    # Notify followers of a user about a new post.
    def notify_followers(self, post):
        for user in post.owner.following:
            user.update(NOTIFI_NEWPOST, post.owner.username)

    #  Method to print updates based on the updates in SocialNetwork
    #  when user post ,like, comment etc ... 
    def update_network(self, update_type, *args):
        message_format = PRINT_MESSAGES.get(update_type, PRINT_MESSAGES[UNKNOWN])
        print(message_format.format(*args))

    def __str__(self):
        network_info = [PRINT_MESSAGES[INFO].format(self.network_name)]
        network_info.extend(str(user[0]) for user in self.users.values())
        return '\n'.join(network_info)


class User():
    def __init__(self, username, password, network):
        self.username = username
        self.password = password
        self.network = network
        self.followers = set()
        self.following = set()
        self.posts = []
        self.notifications = []

    # Update the user with a notification.  
    def update(self, type, username = None):
        message_format = NOTIFICATION_MESSAGES.get(type, NOTIFICATION_MESSAGES[UNKNOWN])
        self.notifications.append(message_format.format(username))

    @require_connection
    def follow(self, other_user):
        self.followers.add(other_user)
        other_user.following.add(self)
        self.network.update_network(FOLLOW, self.username, other_user.username)

    @require_connection
    def unfollow(self, other_user):
        self.followers.remove(other_user)
        other_user.following.remove(self)
        self.network.update_network(UNFOLLOW, self.username, other_user.username)

    @require_connection
    def publish_post(self, type, post_content, *args):
        post = PostFactory.create_post(self, type, post_content, *args)
        self.posts.append(post)
        self.network.upload_posts(post)
        return post

    def print_notifications(self):
        print(f"{self.username}'s notifications:")
        for notification in self.notifications:
            print(notification)

    def __str__(self):
        return f"User name: {self.username}, Number of posts: {len(self.posts)}, Number of followers: {len(self.following)}"


# Factory pattern
class PostFactory:
    @staticmethod
    def create_post(owner, type, *args):
        if type == TEXT:
            return TextPost(owner, *args)
        elif type == IMAGE:
            return ImagePost(owner, *args)
        elif type == SALE:
            return SalePost(owner, *args)
        else:
            raise ValueError("Invalid post type")

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
            self.owner.update(NOTIFI_LIKE, user.username)
            self.owner.network.update_network(LIKE, self.owner.username, user.username)

    @require_connection
    def comment(self, user, comment):
        self.comments.append((user, comment))
        if user is not self.owner:
            self.owner.update(NOTIFI_COMMENT, user.username)
        self.owner.network.update_network(COMMENT, self.owner.username, user.username, comment)

# Subclasses of Post
class TextPost(Post):
    def __str__(self):
        return f'{self.owner.username} published a post:\n{self.content}\n'

class ImagePost(Post):
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
            self.owner.update(NOTIFI_SOLD)
            self.owner.network.update_network(SOLD, self.owner.username)

    @require_connection
    def discount(self, discount_percentage, password):
        if self.owner.password == password:
            self.price *= (1 - (discount_percentage/100))
            self.owner.network.update_network(DISCOUNT, self.owner.username, self.price)
        
    
    def __str__(self):
        availability = "For sale" if self.is_available else "Sold"
        return (f'{self.owner.username} posted a product for sale:\n'
                f'{availability} {self.content}, price: {self.price}, pickup from: {self.location}\n')
