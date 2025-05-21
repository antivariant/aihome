import { defineStore } from 'pinia';
import { apiChat } from 'src/api'


interface Message {
  id: string;
  text: string;
  fromUser: boolean;
  timestamp: string;
  interaction_id?: string;

}

export const useChatStore = defineStore('chat', {
  state: () => ({
    messages: [] as Message[],
    interaction_id: '', // 🆕 добавили сюда interaction_id
  }),

  actions: {
    async sendMessage(text: string) {
      const userMessage: Message = {
        id: Math.random().toString(36).substring(2, 8),
        text,
        fromUser: true,
        timestamp: new Date().toISOString(),
      };

      this.messages.push(userMessage);

      try {
        const form = new FormData();
        form.append('device_id', 'dev001');
        form.append('user_id', 'user123');
        form.append('text', text);

        const res = await apiChat.post('/question', form, {
          headers: {
            Authorization: 'Bearer supersecuretoken',
          },
        });

        const reply: Message = {
          id: Math.random().toString(36).substring(2, 8),
          text: res.data.response,
          fromUser: false,
          timestamp: new Date().toISOString(),
          interaction_id: res.data.interaction_id // 🆕 добавлено
        };

        this.messages.push(reply);

        // 🆕 сохраняем interaction_id
        this.setInteractionId(res.data.interaction_id);

      } catch (err) {
        console.error('Ошибка отправки сообщения:', err);
      }
    },

    setInteractionId(id: string) {
      this.interaction_id = id;
    },
  },
});
