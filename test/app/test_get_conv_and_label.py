"""test get conversation and label"""


# add path for import
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# import conversation manager 
from ai.conversation import ConversationManager


conversations = cm.list_active_conversations_by_user('test_local_user', return_json=True)