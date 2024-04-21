# component of chat_basic.py


# A card for display sentence


# import div etc.
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import re

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





# cars for displya conversation and also for it's sentence

# card for each history 
def hist_template(hist_id, user_name, created_at, content):
    # remove continuous spaces in content
    content = re.sub(r"\s+", " ", content)
    max_length = 10
    content = content[:max_length] + "..." if len(content) > max_length else content
    return html.Div([
        html.Div([
            html.Span("对话时间: ", className="font-bold"),
            html.Span("{}".format(created_at), className="text-gray-600")  # 示例时间，应替换为动态数据
        ], className="mb-2"),
        html.Div([
            html.Span("用户: ", className="font-bold"),
            html.Span("{}".format(user_name), className="text-gray-600")  # 示例内容，应替换为动态数据
        ], className="mb-4"),
        html.Button("查看对话", 
                id= {
                        "type":'type_history_button_label',
                        "index":"history_button_label_{}".format(hist_id), 
                    },
                
                n_clicks=0, 
                className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mr-2"),
        html.Button("删除", 
                id={
                    "type":'type_history_button_delete',
                    "index":"history_button_delete_{}".format(hist_id)
                },

                n_clicks=0, className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded")
        ], className="p-4 border border-gray-200 rounded-lg")

# card for each history 
def hist_template_for_score(convid = None, user_name = None, created_at = None, content = None, **kwargs):
    # remove continuous spaces in content
    content = re.sub(r"\s+", " ", content)
    max_length = 10
    content = content[:max_length] + "..." if len(content) > max_length else content

    # score status
    label_text = kwargs.get('label_text', None)
    label_score = kwargs.get('label_score', None)
    label_created_at = kwargs.get('label_created_at', None)

    if (label_text is None) and (label_score is None):
        label_show = "未评分"
    else:
        label_show = "{}".format(label_score)

    return html.Div([
        html.Div([
            html.Span("对话ID {} 对话时间: {}".format(convid, created_at), className="font-bold"),
        ], className="mb-2"),
        html.Div([
            html.Span("用户: {} 打分：{} ".format(user_name, label_show), className="font-bold"),
            
        ], className="mb-4"),
        html.Button("对话打分", 
                id= {
                        "type":'type_score_button_label',
                        "index":"score_button_label_{}".format(convid), 
                    },
                
                n_clicks=0, 
                className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mr-2"),

        ], className="p-4 border border-gray-200 rounded-lg")
