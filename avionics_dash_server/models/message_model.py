# Third-Party Library
from course_model import Submission


class Message:
    from_user: str
    subject: str
    content: str


class DirectMessage(Message):
    to_user: str
    has_read: bool


class DiscussionMessage(Message):
    submission: Submission
