import gradio as gr

# Состояние чата
chat_history = []

def respond(message, history):
    response = f"AI: {message[::-1]}"  # Простейший ответ — реверс строки
    history.append((message, response))
    return history, history

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column(scale=3):
            chatbot = gr.Chatbot(label="Чат", height=400)
            msg = gr.Textbox(label="Введите сообщение")
            send = gr.Button("Отправить")

        with gr.Column(scale=2):
            log_output = gr.Textbox(label="Лог", lines=20)
            face_canvas = gr.ImageEditor(label="Лицо", shape=(200, 200))

    def handle_send(message, history):
        updated_history, full_history = respond(message, history)
        log_text = "\n".join([f"{m} -> {r}" for m, r in full_history])
        return updated_history, "", log_text

    send.click(
        fn=handle_send,
        inputs=[msg, chatbot],
        outputs=[chatbot, msg, log_output]
    )

demo.launch()
