"""Setence modulle
A setence is basic part of a conversation

Some attributes are

0. id
1. from
2. to (optional)
3. text
4. type
5. model
6. created
7. type (type of this conversation )
8. notes
9. conversation id

"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

