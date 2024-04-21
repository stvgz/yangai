import os
import openai  # pip install openai
import dash
from dash import Dash,dcc, html, Input, Output, State, callback_context, no_update  # pip install dash
from dash.dependencies import Input, Output, State, ALL, MATCH
import dash_table
import dash_bootstrap_components as dbc
import feffery_antd_components as fac  

from .chat_components import *
from .chat_settings import *

import sys
import os
import re
from datetime import datetime, timedelta
import json 

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from ai.qianfan import Qianfan
from ai.moonshot import Moonshot

import logging
logger = logging.getLogger('chatbot')

from ai.conversation import ConversationManager
from ai.dbconnection import get_engine
from ai.make_prompt import get_system_prompt, get_role_prompt_and_desc

def get_ai():
    
    return Qianfan()
    # return Moonshot()




# Instantiate the Dash app
def make_app(flask_app = None):

    tailwind_css_url = "https://cdn.jsdelivr.net/npm/tailwindcss@2.2.16/dist/tailwind.min.css"
    # tailwind_css_url = "/assets/dist/tailwind.min.css"

    app = dash.Dash(__name__,
    server=flask_app,
    url_base_pathname='/score/',
    external_stylesheets=[tailwind_css_url],
    )

    app.title = '智能陪练'

    app.layout = html.Div([
        
        dcc.Store(id = 'conversation_mem', storage_type= 'memory'),
        dcc.Store(id = 'background_mem', storage_type= 'memory'),


        dcc.Tabs([
            dcc.Tab(label='打分', children=[
                html.Div([
                    html.P('设置页面')
                ])
            ]),
            
            ],
            style={'height': '50px', 'display': 'flex', 'flex-direction': 'row', 'justify-content': 'space-around'},
            )


            ])

    @app.callback(
        Output('conversation_history', 'children'),
        Input('history_button_show', 'n_clicks'),

        State('user_name', 'children'),

        prevent_initial_call=True)
    def update_history(n_clicks, user_name):

        cm = ConversationManager()
        list_conversation = cm.list_active_conversations_by_user(return_json=True, user_name= user_name)

        # 如果没有找到任何对话
        if not list_conversation:
            
            return html.Div([
                html.P("没有找到历史记录", className="text-gray-500 text-center py-4")
            ], className="bg-blue-100 rounded-lg shadow p-4")

        # change order 
        desired_order = ["id","user_name",  "created_at","conversation"]

        # 创建一个新的列表，其中的字典将按照 desired_order 中的键的顺序来创建
        ordered_conversations_list = []

        for conv in list_conversation:
            ordered_conv = {key: conv[key] for key in desired_order if key in conv}
            ordered_conversations_list.append(ordered_conv)

        # format time
        for item in ordered_conversations_list:
            # change timezone from utc to utc+8
            # datetime_object = datetime.datetime.strptime(item['created_at'], "%Y-%m-%d %H:%M:%S")
            datetime_utc8 = item['created_at'] + timedelta(hours=8)
            item['created_at'] = datetime_utc8.strftime("%Y-%m-%d %H:%M:%S")


        ### Add buttons in the table
        for item in ordered_conversations_list:
            item['actions'] = '''
            <button class="view-button" onclick="alert('查看ID为{}的条目');">查看</button>
            <button class="delete-button" onclick="alert('删除ID为{}的条目');">删除</button>
            '''.format(item['id'], item['id'])


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

        page_content = []
        for item in ordered_conversations_list:
            page_content.append(hist_template(item['id'], item['user_name'], item['created_at'], item['conversation']))

        return page_content


    ######## Check History Button Clicked ########

    @app.callback(
        Output('history_modal_view', 'is_open'),
        Output('history_modal_view_content', 'children'),
        [Input({'type': 'type_history_button_label', 'index': ALL}, 'n_clicks'),
        Input({'type': 'type_history_button_delete', 'index': ALL}, 'n_clicks')],
        [State('user_name', 'children')],
        prevent_initial_call=True)
    def dynamic_history_action(n_clicks_label, n_clicks_delete, user_name):
        ctx = callback_context
        
        if not ctx.triggered:
            # 如果没有触发事件，不更新任何输出
            return no_update, no_update

        # 获取触发回调的按钮ID和类型
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        button_info = json.loads(button_id.replace('\'', '\"'))
        button_index = button_info['index']
        button_type = button_info['type']

        conversation_id = int(button_index.split('_')[-1])

        cm = ConversationManager()

        if button_type == 'type_history_button_label':
            # 处理查看/打分按钮的逻辑
            # 这里应该是打开模态框并显示对应历史记录的详细信息
            # 假设有一个函数 fetch_conversation_details(hist_id) 返回对话详情
            conversation_details = cm.get_sentence_by_conversation(conversation_id, return_json=True)
            # make dict a list 
            conversation_list = [{'role':s['from_user'], 'content':s['text']} for s in conversation_details]
            
            c = conv2markdown(conversation=conversation_list, user = 'user', bot = 'assistant')
            
            return True, c
        elif button_type == 'type_history_button_delete':
            # 处理删除按钮的逻辑
            # 假设有一个函数 delete_conversation(hist_id) 处理删除逻辑
            cm.delete_conversation(conversation_id)
            # 更新页面或显示删除成功的消息
            return True, f"对话 {conversation_id} 已被删除。"
        else:
            return no_update, no_update

    return app

if __name__ == '__main__':
  app = make_app()
  app.run_server(debug=True)