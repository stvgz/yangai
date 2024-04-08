from .config import *

#opacity
# 0.9 is a good number  0.97 for better charts 
content_style_inner_opacity=0.9
sidebar_content_style_inner_opacity=0.9


content_style = {
    "padding-top": "3rem",
    "padding-left": "3rem",
    "padding-right": "4rem",
    "padding-bottom": "2rem",
    "margin-top": "2rem",
    "margin-top": "2rem",
    "margin-top": "2rem",
    "margin-top": "2rem",

}

content_style_bg = {

    "margin-top": "2rem",
    "margin-top": "2rem",
    "margin-top": "2rem",
    "margin-top": "2rem",
    'width': '100%',
    'height': '100vh',
    'background': CONTENT_BG_PIC,
    'background-size': '100% 100%',
    'background-attachment': 'fixed' # 不设置的话页面滑动时，背景会不铺满*/
}

#inner content container as white
content_style_inner = {
    # "padding-top": "1rem",
    # "padding-left": "1rem",
    "padding-right": "0px",
    "padding-bottom": "0px",
    "margin-top": "0px",
    "margin-top": "0px",
    "margin-top": "0px",
    "margin-top": "0px",
    'background': '#FFFFFF',
    'opacity': content_style_inner_opacity,
    'height': '100vh',

}


footer_style = {
    'background-color': NAVBAR_BGCOLOR,
    'height': "4vh",
    'width': '100%',
    'display': 'flex',
    'justify-content': 'center',
    'align-items': 'center',
    'padding-top': '0px',
    'padding-right': '0px',
    'padding-bottom': '0px',
    'padding-left': '0px',
    'color': '#FFFFFF',
}

content_style_home = {
    # "padding-top": "3rem",
    # "padding-left": "0px",
    # "padding-right": "0px",
    # "padding-bottom": "0px",
    # "margin-top": "0rem",
    # "margin-top": "0rem",
    # "margin-top": "0rem",
    # "margin-top": "0rem",

    "padding-top": "0px",
    "padding-left": "0px",
    "padding-right": "0px",
    "padding-bottom": "0px",
    "margin-top": "0px",
    "margin-top": "0px",
    "margin-top": "0px",
    "margin-top": "0px",
    # "border-style": "solid",
    # "border-color": "#ff0000"

    "min-height":'100vh',
    # 'display':'flex'

}




# 9/01 copied from content_style_inner
sidebar_content_style = {
    "padding-top": "1rem",
    "padding-left": "1rem",
    "padding-right": "0px",
    "padding-bottom": "0px",
    "margin-top": "0px",
    "margin-top": "0px",
    "margin-top": "0px",
    "margin-top": "0px",
    # "border-style": "solid",
    # "border-color": "#ff0000",
    'background': '#FFFFFF',
    'opacity': sidebar_content_style_inner_opacity  # 0.9 is a good number  0.97 for better charts 
    # 'width': '100%',
    # 'height': '100%',
    # 'background': 'url(../assets/background/1.jpg) no-repeat',
    # 'background-size': '100% 100%',
    # 'background-attachment': 'fixed' # 不设置的话页面滑动时，背景会不铺满*/
}

button_style = {
  "display": "inline-block",
  "height": 38,
  "padding": "0 30",
  "color": "#555",
  "textAlign": "center",
  "fontSize": 11,
  "fontWeight": 600,
  # "lineHeight": 38,
  "letterSpacing": .1,
  "textTransform": "uppercase",
  "textDecoration": "none",
  "whiteSpace": "nowrap",
  "backgroundColor": "transparent",
  "borderRadius": 4,
  "border": "1 solid #bbb",
  "cursor": "pointer",
  "boxSizing": "border-box"
}

