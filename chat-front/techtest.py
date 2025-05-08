import gradio as gr

with gr.Blocks() as demo:

    # Чатбот с историей сообщений
    chatbox = gr.Chatbot(label="Чат", type="messages")

    # Текстовое поле для ввода
    text_input = gr.Textbox(label="Введите сообщение")
    
    # Кнопка отправки
    send_button = gr.Button("Отправить")

    # Изображение (например, для отображения лица)
    image_display = gr.Image(label="Лицо")

demo.launch()
