import axios from 'axios'
import { ElMessage } from 'element-plus'

const api = axios.create({
  baseURL: '',
  timeout: 15000
})

// 请求拦截器 - 添加 token
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// 响应拦截器 - 统一错误处理
api.interceptors.response.use(
  response => response,
  error => {
    const status = error.response?.status

    // 401 未授权 - 跳转登录（但如果已在登录页则不跳转，让页面自行处理错误）
    if (status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('userInfo')
      if (!window.location.pathname.startsWith('/login')) {
        window.location.href = '/login'
      }
      return Promise.reject(error)
    }

    // 403 无权限
    if (status === 403) {
      ElMessage.error('没有权限执行此操作')
      return Promise.reject(error)
    }

    // 404 和其他错误 - 静默处理，不弹全局提示（由各页面自行处理）
    // 只有非预期错误才弹提示
    if (status && status >= 500) {
      ElMessage.error('服务器错误，请稍后重试')
    }

    return Promise.reject(error)
  }
)

export default api
