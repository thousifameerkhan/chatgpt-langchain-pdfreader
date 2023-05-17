import gradio as gr

def add_text(history, text):
    global valid_file
    print(history)
    history = history + [(text, None)]
    print(history)
    history = history + [(None,"Response")]
    print(history)
    print("In Add Text")
    return history, ""

def bot(history):
    global valid_file
    print("In Bot Response")
    print(history)
    valid_file = True
    return history

def main():
    with gr.Blocks(title="OFSLL DataMapper") as demo:
        chatbot = gr.Chatbot([], elem_id="chatbot").style(height=750)

        with gr.Row():
            with gr.Column(scale=0.85):
                txt = gr.Textbox(
                    show_label=False,
                    placeholder="Enter text and press enter, or upload csv",
                ).style(container=False)

            with gr.Column(scale=0.15, min_width=0):
                # Allow only CSV files
                btn = gr.UploadButton("📁", file_types=["csv"])
    

        txt.submit(add_text, [chatbot, txt], [chatbot, txt]).then(
            bot, chatbot, chatbot
        )

    demo.launch()

if __name__ == '__main__':
    main()
