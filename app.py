import user, rm_predict
import gradio as gr

app1 = user.demo  
app2 = rm_predict.demo

gr.Tabs([app1, app2]).launch()