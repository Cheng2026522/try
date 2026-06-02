import api from '@/utils/api'

const state = {
  files: [],
  categories: [],
  loading: false,
  currentFile: null
}

const getters = {
  files: state => state.files,
  categories: state => state.categories,
  loading: state => state.loading,
  currentFile: state => state.currentFile
}

const mutations = {
  SET_FILES(state, files) {
    state.files = files
  },
  SET_CATEGORIES(state, categories) {
    state.categories = categories
  },
  SET_LOADING(state, loading) {
    state.loading = loading
  },
  SET_CURRENT_FILE(state, file) {
    state.currentFile = file
  },
  ADD_FILE(state, file) {
    state.files.unshift(file)
  },
  UPDATE_FILE(state, updatedFile) {
    const index = state.files.findIndex(f => f.id === updatedFile.id)
    if (index !== -1) {
      state.files[index] = updatedFile
    }
  },
  DELETE_FILE(state, fileId) {
    state.files = state.files.filter(f => f.id !== fileId)
  }
}

const actions = {
  async fetchFiles({ commit }) {
    commit('SET_LOADING', true)
    try {
      const response = await api.get('/files/files/')
      commit('SET_FILES', response.data.results || response.data)
    } catch (error) {
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async fetchCategories({ commit }) {
    try {
      const response = await api.get('/files/categories/')
      commit('SET_CATEGORIES', response.data.results || response.data)
    } catch (error) {
      throw error
    }
  },

  async uploadFile({ commit }, formData) {
    try {
      const response = await api.post('/files/files/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      commit('ADD_FILE', response.data)
      return response.data
    } catch (error) {
      throw error
    }
  },

  async deleteFile({ commit }, fileId) {
    try {
      await api.delete(`/files/files/${fileId}/`)
      commit('DELETE_FILE', fileId)
    } catch (error) {
      throw error
    }
  },

  async updateFile({ commit }, { fileId, data }) {
    try {
      const response = await api.patch(`/files/files/${fileId}/`, data)
      commit('UPDATE_FILE', response.data)
      return response.data
    } catch (error) {
      throw error
    }
  },

  async createCategory({ commit }, categoryData) {
    try {
      const response = await api.post('/files/categories/', categoryData)
      commit('SET_CATEGORIES', prev => [...prev, response.data])
      return response.data
    } catch (error) {
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
