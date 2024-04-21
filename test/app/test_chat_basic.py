"""Test chat function without ai"""

# add root folder into syspath
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


from ai.conversation import ConversationManager
from ai.dbconnection import get_engine
from ai.make_prompt import get_system_prompt, get_role_prompt_and_desc
from app.chat_components import conv2text, text2conv, save_conversation


from ai.qianfan import Qianfan


def test_create_conversation_no_sentence():
    ai = Qianfan()

    ai.chat("test chat", set_response_txt='test response')

    ai.chat("test chat 2", set_response_txt='test response2')

    # some context
    user_name = 'test_local_user'
    case = 'test_local_case'

    # end conversation
    conversation = ai.conv
    conversation_json = conv2text(conversation)

    cm = ConversationManager()
    for c in conversation:
        sentence_from_user = c['role']
        # sentence_to_user = 'bot' if sentence_from_user == 'user' else 'user'
        sentence_text = c['content']
        cm.add_sentence(from_user= sentence_from_user, text=sentence_text)

    cm.create_conversation(user_name = user_name, conversation=conversation_json, notes = "Case: {}".format(case))

test_create_conversation()



# view conversation
def test_view_conversation():
    # get conversation
    cm = ConversationManager()
    conversations = cm.list_active_conversations_by_user('test_local_user', return_json=True)
    print(conversations)


def test_get_conversation_with_sentences():
    # get conversation
    cm = ConversationManager()
    conversations = cm.list_active_conversations_by_user('test_local_user', return_json=True)

test_view_conversation()