import axios from 'axios'

const host = import.meta.env.VITE_API_HOST
console.log(`host=${host}`)

const apiChat = axios.create({ baseURL: `${host}:5121` })
const apiFrai = axios.create({ baseURL: `${host}:5101` })
const apiDev = axios.create({ baseURL: `${host}:5103` })
const apiSTT = axios.create({ baseURL: `${host}:5233` })
const apiTTS = axios.create({ baseURL: `${host}:5243` })
const apiVision = axios.create({ baseURL: `${host}:5251` })
const apiScreenVision = axios.create({ baseURL: `${host}:5261` })
const apiActuators = axios.create({ baseURL: `${host}:5271` })
const apiEngine = axios.create({ baseURL: `${host}:6000` })
const apiHub = axios.create({ baseURL: `${host}:5105` }) // 🆕 добавлено

export {
  apiChat,
  apiFrai,
  apiDev,
  apiSTT,
  apiTTS,
  apiVision,
  apiScreenVision,
  apiActuators,
  apiEngine,
  apiHub, // 🆕 экспортировано
}
