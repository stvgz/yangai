
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.db.db import get_engine
engine = get_engine()


from model import Conversation, Sentence
# , Label, LabelSentence

# init all

Sentence.metadata.create_all(engine)
Conversation.metadata.create_all(engine)

# Label.metadata.create_all(engine)
# LabelSentence.metadata.create_all(engine)


# User.metadata.create_all(engine)



# # use reflection to update metadata
# Label.metadata.reflect(engine)
# LabelSentence.metadata.reflect(engine)
# Conversation.metadata.reflect(engine)
# User.metadata.reflect(engine)
# Sentence.metadata.reflect(engine)
