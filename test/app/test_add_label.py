"""Test add label on a conversation and sentenece."""


# add path for import
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# import conversation manager 
from ai.conversation import ConversationManager

# test case add label on a conversation
def test_add_label_on_conversation():
    """Test add label on a conversation and sentenece."""
    # create a conversation manager
    conversation_manager = ConversationManager()

    # create a conversation
    conversation = conversation_manager.create_conversation("user1", "{}")

    # get id of the conversation
    conversation_id = conversation.id

    # add a label
    label = conversation_manager.add_label_conversation(user_name="user1", label_text="label1", label_score=1, conversation_id=conversation_id)

    # get the conversation by id
    conversation = conversation_manager.get_conversation(conversation_id)

    # check the label of this conversation
    assert conversation.label_text == "label1"

# test case
def test_add_label_on_sentence():
    """Test add label on a conversation and sentenece."""
    # create a conversation manager
    conversation_manager = ConversationManager()

    # create a conversation and add sentence
    conversation = conversation_manager.create_conversation(user_name="user1", conversation="{}", notes='default notes')
    sentence = conversation_manager.create_sentence(text="local test sentence", from_user='local_test')

    # add a label on sentence
    label = conversation_manager.add_label_sentence(sentence_id=sentence.id, label_text="label1", label_score=1, label_from_user="local_test")

    # get the updated sentence
    sentence = conversation_manager.get_sentence(sentence.id)

    # check sentence label
    assert sentence.label_text == "label1"
    assert sentence.label_score == 1

# run case
# test_add_label_on_conversation()
test_add_label_on_sentence()