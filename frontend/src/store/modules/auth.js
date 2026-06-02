import api from '@/utils/api'

const state = {
  token: localStorage.getItem('token') || '',
  user: JSON.parse(localStorage.getItem('user') || 'null'),
  isLoggedIn: false
}

const getters = {
  isLoggedIn: state => !!state.token && !!state.user,
  token: state => state.token,
  user: state => state.user,
  userId: state => state.user?.id || null,
  userName: state => state.user?.username || '',
  userRole: state => state.user?.role || 'staff',
  userPhone: state => state.user?.phone || ''
}

const mutations = {
  SET_TOKEN(state, token) {
    state.token = token
    localStorage.setItem('token', token)
  },
  SET_USER(state, user) {
    state.user = user
    localStorage.setItem('user', JSON.stringify(user))
  },
  LOGOUT(state) {
    state.token = ''
    state.user = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }
}

const actions = {
  async login({ commit }, credentials) {
    try {
      const response = await api.post('/auth/login/', credentials)
      commit('SET_TOKEN', response.data.token)
      commit('SET_USER', {
        id: response.data.user_id,
        username: response.data.username,
        role: response.data.role,
        phone: response.data.phone
      })
      return response.data
    } catch (error) {
      throw error
    }
  },

  async register({ commit }, userData) {
    try {
      const response = await api.post('/auth/register/', userData)
      return response.data
    } catch (error) {
      throw error
    }
  },

  logout({ commit }) {
    commit('LOGOUT')
  },

  async fetchUser({ commit, state }) {
    if (!state.token) return
    try {
      const response = await api.get(`/auth/users/${state.user.id}/`)
      commit('SET_USER', response.data)
      return response.data
    } catch (error) {
      if (error.response?.status === 401) {
        commit('LOGOUT')
      }
      throw error
    }
  }
}

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
}
