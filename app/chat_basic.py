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
    
    # return Qianfan()
    return Moonshot()

# Instantiate the Dash app
def make_app(flask_app = None):

    tailwind_css_url = "https://cdn.jsdelivr.net/npm/tailwindcss@2.2.16/dist/tailwind.min.css"
    # tailwind_css_url = "/assets/dist/tailwind.min.css"

    app = dash.Dash(__name__,
    server=flask_app,
    url_base_pathname='/ai/',
    external_stylesheets=[tailwind_css_url],
    )

    app.title = '智能陪练'

    app.layout = html.Div(
        id = 'main_div',
        children=
        [
        
        dcc.Store(id = 'conversation_mem', storage_type= 'memory'),
        dcc.Store(id = 'background_mem', storage_type= 'memory'),
        dcc.Store(id = 'score_mem', storage_type= 'memory'),



        # Headers
        html.Div(
                [
                    html.H2("您的个人训练助理",
                    className="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate"),

                    # User info and Login button
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.Span("您好用户，", className="text-gray-900"),
                                            html.Span("未登录用户", id = 'user_name',
                                                className="text-gray-900 font-bold"),
                                        ],
                                        className="flex items-center"
                                    ),

                                    # Login button
                                    html.Div(
                                        [
                                            html.Button("登录", 
                                            id = 'button_login',
                                            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"),
                                        ],
                                        className="flex items-center"
                                    ),

                                    # Login Modal
                                    dbc.Modal(
                                        [
                                            dbc.ModalHeader("登录，请输入"),
                                            dbc.ModalBody([

                                                dcc.Input(id='login_modal_input', type='text', placeholder='请输入内容'),
                                                html.Button('提交', id='login_modal_submit', n_clicks=0, className='btn btn-primary')
                                                ])
                                        ],
                                        id = 'login_modal',
                                        is_open = True,
                                    )

                                ],
                                className="flex items-center"
                            ),
                        ],
                        className="flex items-center justify-between w-full"
                    ),
                ], 
                
                style={'padding': 20}),
        



        dcc.Tabs(
            # style of tabs
            style={'height': '50px', 'display': 'flex', 'flex-direction': 'row', 
            # 'justify-content': 'space-around'
            },
            children =
            [
            dcc.Tab(label='对话', 
                # tab style should be horizontal
                style={'display': 'flex', 'flexDirection': 'row'},

                children=[

                # dcc.Input(id='input-name', type='text', placeholder='留下你的名字', 
                #     style={'width':'100%'},
                #     className='mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
                #     ),

                html.Button('开启对话', id='button_start', n_clicks=0,
                style={'width': '100%'},
                className='bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded',
                ),
            
                # placeholder for background information

                html.Div(id='background-info',
                    style={'padding': '10px', 'margin-top': '10px', 'background-color': '#f3f4f6'},
                    className='bg-gray-100'
                ),


                dcc.Loading(
                    children=[
                        
                        html.Div(id='conversation',
                            style={'background-color': '#ebf8ff', 
                                'height': 'auto', 
                                'padding-bottom': '8rem'},
                            children = [

                            ]),
                        html.Div(id='place',
                            style = {'height': '10rem'}
                                )
                    ],
                    type="circle",
                ),

                html.Div([
                    dcc.Input(id='input-text', type='text', placeholder='请输入对话', 
                    className='mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                    
                    ),
                    html.Button('发送', id='submit-button', n_clicks=0,
                        style={'width': '100%', 'height': '3rem'},
                        className='bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded',
                        ),
                    html.Button('结束对话并且保存', id='end-button', n_clicks=0,
                        style={'width': '100%', 'height': '3rem'},
                        className='bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded',
                        ),
                ], style={'position': 'fixed', 'bottom': 0, 'left': 0, 'right': 0, 'display': 'flex', 'flexDirection': 'column'}),

                    ]),

            
            ##### Tab 2 #####
            dcc.Tab(label='场景管理', children=[

                # single selector for scene
                dcc.RadioItems(id='scene-selector', options=[
                    {'label': '场景1：默认场景，10客户随机', 'value': '1'},
                    {'label': '场景2：测试场景', 'value': '2'},
                    {'label': '场景3：测试场景', 'value': '3'},
                    {'label': '场景4：测试场景', 'value': '4'},
                    {'label': '场景5：测试场景', 'value': '5'},
                    {'label': '场景6：测试场景', 'value': '6'},
                    {'label': '场景7：测试场景', 'value': '7'},
                    {'label': '场景10：数据库数据', 'value': '10'}
                    ],

                    style={'width': '50%', 'margin': '0 auto', 'font-size': '1.25rem'},
                    className='text-center',
                    
                    value='1',

                ),

            # make tabe as 2 horizontal

            
                    # end tab 2
                    ]),

            #### tab 3 #### 
            dcc.Tab(label='历史记录', children=[
                
                # A table of conversation history including user name, created_at, conversation, button to view
                dcc.Loading(
                html.Div(id='conversation_history',
                    style={'padding': '10px', 'margin-top': '10px', 'background-color': '#f3f4f6'},
                    className='bg-gray-100'
                ),),

                # invisible modal for view single history
                dbc.Modal(
                    [
                        dbc.ModalHeader("历史记录"),
                        dbc.ModalBody([

                            html.Div(id='history_modal_view_content',
                                style={'padding': '10px', 'margin-top': '10px', 'background-color': '#f3f4f6'},
                                className='bg-gray-100'
                            ),
                            ]),
                    ],
                    id = 'history_modal_view',
                    is_open = False,
                ),

                html.Div([

                    html.Button('查看历史', id='history_button_show', n_clicks=0,
                        style={'width': '100%', 'height': '3rem'},
                        className='bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded',
                        ),
                    ],
                    style={'position': 'fixed', 'bottom': 0, 'left': 0, 'right': 0, 'display': 'flex', 'flexDirection': 'column'}),
                

                ]),


            #### tab 4 ####

            dcc.Tab(label='打分', children=[
                
                # A table of conversation history including user name, created_at, conversation, button to view
                dcc.Loading(
                html.Div(id='score_history',
                    style={'padding': '10px', 'margin-top': '10px', 'background-color': '#f3f4f6'},
                    className='bg-gray-100'
                    ),),

                # invisible modal for view single history
                dbc.Modal(
                    [
                        dbc.ModalHeader("对话打分"),
                        dbc.ModalBody([
                            
                            # button to submit score result
                            html.Button('提交打分', id='score_modal_submit', n_clicks=0,
                                style={'width': '100%', 'height': '3rem'},
                                className='bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded',
                                ),
                            dcc.Store(id = 'score_modal_conversation_id', storage_type= 'memory'),
                            fac.AntdRate(id = 'score_modal_conversation_score', count=5, value=0),
                            dcc.Textarea(id = 'score_modal_conversation_label_text', placeholder = '请输入您的评价'),

                            # for sentences
                            dcc.Store(id = 'score_modal_sentence_id', storage_type= 'memory'),
                            html.Div(id='score_modal_content',
                                style={'padding': '10px', 'margin-top': '10px', 'background-color': '#f3f4f6'},
                                className='bg-gray-100'
                            ),
                            ]),
                    ],
                    id = 'score_modal',
                    is_open = False,
                    ),

                dbc.Modal(
                    [
                        dbc.ModalHeader("保存成功"),
                        dbc.ModalBody([
                            html.P("保存成功"),
                            
                            ]),


                    ],
                    id = 'score_modal_finish',
                    is_open = False,
                
                    ),

                html.Div([

                    html.Button('查看所有对话进行打分', id='score_button_showall', n_clicks=0,
                        style={'width': '100%', 'height': '3rem'},
                        className='bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded',
                        ),
                    ],
                    style={'position': 'fixed', 'bottom': 0, 'left': 0, 'right': 0, 'display': 'flex', 'flexDirection': 'column'}),
                

                    ]),
                ]),


        # end main div children    
        ],


        
        # end main div
        )




    ### init settings ### 

    # @app.callback(
    #     Output('background-info', 'children'),
    #     Input('button_start', 'n_clicks'),
    #     prevent_initial_call=True)
    # def start_background_info(n_clicks):
    #     if n_clicks > 0:
    #         return dcc.Markdown("""
    #             ```
    #             这是一个培训的模拟场景，你需要扮演一个顾客，尽量模拟真实的对话场景，\\
    #             1. 使用口语化的沟通方式
    #             2. 并且更频繁的使用语气词，比如是不是
    #             3. 在回答之后，可以在括号中加上你的情绪状态，比如（开心）（非常开心），（非常意外），\\
    #                 （非常生气），（惊讶），（无奈），（意外）等等。
    #                 比如 “ 你好，你是谁？（惊讶）”
    #             4. 请记住每一次只输出一句话，然后等待对方回复。
    #             5. 客户一般不会特别主动说自己的名称，或者进行比较长的自我介绍
    #             6. 客户一般不会主动介绍自己的个人信息，在询问之后看个人的性格，可能会有一些回答
    #             ```
    #         """)
    #     else:
    #         return None

    # ###########   LoginLogic   #####
    @app.callback(
    Output("login_modal", "is_open"),
    Output('user_name', 'children'),

    [Input("button_login", "n_clicks"), 
    Input("login_modal_submit", "n_clicks")],

    [State("login_modal", "is_open")],
    State('login_modal_input', 'value'),
    )
    def toggle_modal(n1, n2, is_open, login_input_text):
        if not login_input_text:
            login_input_text = "未登录用户"
        else:
            login_input_text = login_input_text
        if n1 or n2:
            return not is_open, login_input_text
        return is_open, login_input_text

    # @app.callback(
    #     Output('scene-selector', 'options'),
    #     Input('button_start', 'n_clicks'),
    #     prevent_initial_call=True)
    # def update_scene_info(n_clicks):
    #     pass

    #     return [{'label': '场景1：默认场景，10客户随机', 'value': '1'},
    #             {'label': '场景2：测试场景', 'value': '2'},
    #             {'label': '场景3：备选数据', 'value': '3'}]

    # Define the callback function
    @app.callback(
    Output('conversation', 'children'),
    Output('conversation_mem','data'),
    Output('input-text', 'value'),
    Output('background-info', 'children'),

    Input('submit-button', 'n_clicks'),
    Input('button_start', 'n_clicks'),
    Input('end-button', 'n_clicks'),

    State('user_name', 'children'),
    State('input-text', 'value'),
    State('conversation', 'children'),
    State('conversation_mem','data'),
    State('background-info', 'children'),
    State('scene-selector', 'value'),
    
    prevent_initial_call=True
    )
    def update_output(n_clicks, n_clicks_start, n_clicks_end, input_name, input_text, 
                    conversation,conversation_mem, background_info, scene_selector):

        ####### Read input ############
        # check which button was clicked
        ctx = dash.callback_context

        if not ctx.triggered:
            button_id = 'No clicks yet'
        else:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id == 'submit-button':
            mode = 'submit'

        elif button_id == 'button_start':
            mode = 'start'
        
        elif button_id == 'end-button':
            mode = 'end'
        
        input_text = "" if input_text is None else input_text

        logger.info("conversation Status Now {}",format(conversation))

        ###### check name ######
        if input_name is None:
            return ["身份不对{}，你输入的身份是".format(input_name),None,""]
            
        else:
            if input_name[:3] != "666":
                return ["身份不对{}，你输入的身份是".format(input_name), None,""]
        

        if conversation_mem is not None:
            conversation = conversation_mem
            logger.info("Clcik {}, Get Memory with {}".format(n_clicks, len(conversation_mem)))
        else:
            conversation = []
            
        # scence
        case = int(scene_selector)

        # init chat
        bot = "assistant"
        user = "user"

        # some settings from hair
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.dirname(__file__)))
        sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))


        system_prompt = get_system_prompt(case = case)
        
        ai = get_ai()

        if mode == 'start':
            
            role_prompt, role_desc = get_role_prompt_and_desc(case = case)

            prompt_start = system_prompt + role_prompt

            ai.chat(prompt_start)

            return conv2markdown(ai.conv, user= user, bot = bot), ai.conv, "", role_desc

        if mode == 'submit':
            
            # get conversation from history
            ai.conv = conversation
            
            user_input = input_text 

            # add another prompt into input text
            # user_input += "  (请注意你持续需要扮演顾客的角色不要忘记)"
            
            # add system prompt into input text
            # not really working
            # user_input  = input_text + system_prompt

            ai.chat(user_input)

            # Return the generated text as the output with different markdowns
            conversation = ai.conv

            return conv2markdown(ai.conv, user= user, bot = bot), conversation, "", background_info

        if mode == 'end':
            # conversation end and save conversation
            user_name = input_name
            conversation_json = conv2text(conversation)

            cm = ConversationManager()
            for c in conversation:
                sentence_from_user = c['role']
                sentence_text = c['content']
                cm.add_sentence(from_user= sentence_from_user, text=sentence_text)

            cm.create_conversation(user_name, 
                            conversation=conversation_json, 
                            role_info = background_info,
                            notes = "Case: {}".format(case))

            cm.close_session()
            # new_conversation = save_conversation(conversation_json, user_name, engine=get_engine())
            
            return "对话结束，谢谢", None,"","请再次点击开始以便进行下一次对话"


    # history management
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


        page_content = []
        for item in ordered_conversations_list:
            page_content.append(hist_template(item['id'], item['user_name'], item['created_at'], item['conversation']))

        cm.close_session()
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
            return False, no_update

        if sum(n_clicks_label) == 0:
            # 如果没有查看按钮被点击，不更新任何输出
            return False, no_update

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
            
            cm.close_session()
            return True, c

        elif button_type == 'type_history_button_delete':
            # 处理删除按钮的逻辑
            # 假设有一个函数 delete_conversation(hist_id) 处理删除逻辑
            cm.delete_conversation(conversation_id)
            cm.close_session()
            # 更新页面或显示删除成功的消息
            return True, f"对话 {conversation_id} 已被删除。"
        else:
            cm.close_session()
            return no_update, no_update


    ################# Call Back For Score ##################
    # call back for list all conversation for score
    @app.callback(
        Output('score_history', 'children'),
        Input('score_button_showall', 'n_clicks'),
        prevent_initial_call=True)
    def update_score_history(n_clicks):
        """
        1. Get all conversation. Show a) user_name, b) created_at, c) conversation  d) score status
        2. Show all conversation in cards, have a button to score

        """

        # get all conversation
        cm = ConversationManager()
        list_conversation = cm.list_conversations(return_json=True)
            # 如果没有找到任何对话
        if not list_conversation:
            
            return html.Div([
                html.P("没有找到历史记录", className="text-gray-500 text-center py-4")
            ], className="bg-blue-100 rounded-lg shadow p-4")

        # change order 
        desired_order = ["id","user_name",  "created_at","conversation", "label_score",
                        "label_text", 'label_created_at','role_info']

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

        page_content = []
        for item in ordered_conversations_list:
            page_content.append(hist_template_for_score(convid = item['id'], 
                                                        role_info = item['role_info'],
                                                        user_name= item['user_name'], 
                                                        created_at = item['created_at'],
                                                        content = item['conversation'],
                                                        label_score = item['label_score'],
                                                        label_text = item['label_text'],
                                                        label_created_at = item['label_created_at']
                                                        ))


        cm.close_session()
        return page_content

    
    # call back for score button clicked
    # ”对话打分“
    
    @app.callback(
        Output('score_modal', 'is_open'),
        Output('score_modal_conversation_score', 'value'),
        Output('score_modal_conversation_label_text', 'value'),
        Output('score_modal_content', 'children'),
        Output('score_modal_conversation_id', 'data'),
        Output('score_modal_sentence_id', 'data'),

        [Input({'type': 'type_score_button_label', 'index': ALL}, 'n_clicks'),
        Input({'type': 'type_score_button_delete', 'index': ALL}, 'n_clicks'),
        ],


        [State('user_name', 'children')],
        prevent_initial_call=True)
    def dynamic_score_action(n_clicks_label, n_clicks_delete, user_name):
        ctx = callback_context

        if not ctx.triggered:
            # 如果没有触发事件，不更新任何输出
            return False, no_update, no_update, no_update, no_update, no_update

        if sum(n_clicks_label) == 0:
            # 如果没有查看按钮被点击，不更新任何输出
            return False, no_update, no_update, no_update, no_update, no_update

        # 获取触发回调的按钮ID和类型
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        button_info = json.loads(button_id.replace('\'', '\"'))
        button_index = button_info['index']
        button_type = button_info['type']

        conversation_id = int(button_index.split('_')[-1])

        # get conversation
        cm = ConversationManager()
        conversation = cm.get_conversation(conversation_id, return_json=True)
        senteces = cm.get_sentence_by_conversation(conversation_id, return_json=True)
        # remove 1st sentence
        senteces = senteces[1:]

        # information of current conversation
        # existing score
        conversation_id = conversation['id']
        score = conversation['label_score']
        label_text = conversation['label_text']
        
        component_list = []
        
        # header
        # only keep minutes
        created_at = conversation['created_at']
        created_at = created_at.strftime("%Y-%m-%d %H:%M")

        header = html.Div([
            html.P("用户: {} 时间{} 对话ID {}".format(conversation['user_name'], created_at, conversation_id)),
        ])
        component_list.append(header)
        
        # sentences
        for s in senteces:
            sentence = html.Div(
                style = {'backgroundColor': 'lightblue'} if s['from_user'] == 'assistant' else {},
                children = [
                html.Div([
                    html.Div("{}".format(s['text']), style={'width': '75%', 
                            'display': 'inline-block', 
                            'overflow': 'auto', 
                            'text-overflow': 'ellipsis', 
                            
                            }),
                    # dropdown for score
                    dcc.Dropdown(id = {'type': 'score_modal_sentence', 
                                    'index':'score_modal_sentence_{}'.format(s['id'])
                                        },
                        options=[{'label': '1', 'value': 1}, 
                                 {'label': '2', 'value': 2}, 
                                 {'label': '3', 'value': 3},
                                 {'label': '4', 'value': 4}, 
                                 {'label': '5', 'value': 5}],
                        value= s['label_score'],
                        style={'width': '25%', 'display': 'inline-block'})
                ], style={'display': 'flex', 'flex-direction': 'row'})
                ])
            
            component_list.append(sentence)

        # list of sentence id
        sentence_id = [s['id'] for s in senteces]
        
        cm.close_session()
        return 1, score, label_text, component_list, conversation_id, sentence_id


    # call back for score modal submit button clicked
    @app.callback(

        Output('score_mem', 'data'),
        Output('score_modal_finish', 'is_open'),

        [Input('score_modal_submit', 'n_clicks'),
        ],

        [State('user_name', 'children'),
        State('score_modal_conversation_id', 'data'),
        State('score_modal_conversation_score', 'value'),
        State('score_modal_conversation_label_text', 'value'),
        
        State('score_modal_sentence_id', 'data'),
        State({'type': 'score_modal_sentence', 'index': ALL}, 'value'),
        # State({'type': 'score_modal_sentence', 'index': ALL}, 'id'),
        ],
        prevent_initial_call=True)
    def dynamic_score_action_submit(n_clicks, 
                                    
                                    user_name, 
                                    conversation_id, 
                                    conversation_score,
                                    conversation_label_text,

                                    sentence_ids,
                                    score_sentence, 
                                    # sentence_id                                
                                    ):
        ctx = callback_context

        if not ctx.triggered:
            # 如果没有触发事件，不更新任何输出
            return "No submit"

        if n_clicks == 0:
            # 如果没有查看按钮被点击，不更新任何输出
            return "No submit"


        if not ctx.triggered:
            # 如果没有触发事件，不更新任何输出
            return False, no_update

        # 获得conversation_id
        conversation_id = conversation_id
        cm = ConversationManager()
        # get conversation
        conversation = cm.get_conversation(conversation_id, return_json=True)
        # get sentences
        sentences = cm.get_sentence_by_conversation(conversation_id, return_json=True)
        # remove 1st sentence
        sentences = sentences[1:]
        # update score of conversation
        cm.add_label_conversation(conversation_id,label_from_user=user_name, label_score= conversation_score, label_text= conversation_label_text)

        # update score of sentences
        for idx, s_id in enumerate(sentence_ids):
            
            sentence_score = score_sentence[idx]
            cm.add_label_sentence(sentence_id=s_id, label_score= sentence_score, label_from_user= user_name)
        
        score_finished_result = 1

        cm.close_session()
        return 1,score_finished_result


    # end of app
    return app



if __name__ == '__main__':
  app = make_app()
  app.run_server(debug=True)