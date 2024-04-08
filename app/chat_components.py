# component of chat_basic.py


# A card for display sentence


# import div etc.
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

# a div to represent a sentence

s_id = "sentence_{}".format(1)

sentence_div = html.Div(

            [
            dbc.Row([
                # dbc.Col(html.I(className="fas fa-user-circle"), width=2),
                dbc.Col(html.P("This is a sample text."), width=10),
                dbc.Col(dbc.Button("Evaluate", color="primary"), width=2),
            ])
            ]
        )



def save_conversation(conversation, user_name):
    # save conversation
    engine = get_engine()
    cm = ConversationManager()
    cm.create_conversation(user_name, conversation)
    cm.close_session()
    return


def conv2text(conv):
    """ Conv = [
        {"role": "user", "content": "hello"},
        {"role": "bot", "content": "hi"},
    ]
    Make conv list into json format text"""

    import json
    dict_of_conv= {i: d for i, d in enumerate(conv)}

    j = json.dumps(dict_of_conv, indent=4, ensure_ascii=False, sort_keys=True)

    return j

def text2conv(text):
    """ Conv = [
        {"role": "user", "content": "hello"},
        {"role": "bot", "content": "hi"},
    ]
    Make conv as json format text"""

    import json
    conv = json.loads(text)
    
    # make it into list
    conv = [v for k, v in conv.items()]

    return conv


def conv2markdown(conversation, user = None, bot = None, hide_1 = True):
    out = []
    id = 1
    
    idx = 0
    for msg in conversation:
        
        if idx == 0 and hide_1:
            idx += 1
            continue

        role = msg['role']
        content = msg['content']

        if  role == user:
            out.append(dcc.Markdown(id = 'cov'+ str(id), 
                        children = content,
                        style={'padding': '10px', 'margin-top': '10px'},
                        className='bg-blue-50'
                        ))
        elif role == bot:
            out.append(dcc.Markdown(id = 'cov'+ str(id), 
            children = content,
            # style={'background-color': 'lightcoral', 'padding': '10px', 'margin-top': '10px'},
            style={'padding': '10px', 'margin-top': '10px'},
            className='bg-pink-50'
            ))
        else:
            pass

        id +=1
        idx +=1

    
    return out
