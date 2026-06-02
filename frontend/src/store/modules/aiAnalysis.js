import api from '@/utils/api'

const state = {
  analysisResults: [],
  currentAnalysis: null,
  analysisHistory: [],
  loading: false
}

const getters = {
  analysisResults: state => state.analysisResults,
  currentAnalysis: state => state.currentAnalysis,
  analysisHistory: state => state.analysisHistory,
  loading: state => state.loading
}

const mutations = {
  SET_ANALYSIS_RESULTS(state, results) {
    state.analysisResults = results
  },
  SET_CURRENT_ANALYSIS(state, analysis) {
    state.currentAnalysis = analysis
  },
  SET_ANALYSIS_HISTORY(state, history) {
    state.analysisHistory = history
  },
  SET_LOADING(state, loading) {
    state.loading = loading
  },
  ADD_ANALYSIS_RESULT(state, result) {
    state.analysisResults.unshift(result)
  },
  UPDATE_ANALYSIS_RESULT(state, updatedResult) {
    const index = state.analysisResults.findIndex(r => r.id === updatedResult.id)
    if (index !== -1) {
      state.analysisResults[index] = updatedResult
    }
    if (state.currentAnalysis?.id === updatedResult.id) {
      state.currentAnalysis = updatedResult
    }
  }
}

const actions = {
  async fetchAnalysisResults({ commit }) {
    commit('SET_LOADING', true)
    try {
      const response = await api.get('/ai/results/')
      commit('SET_ANALYSIS_RESULTS', response.data.results || response.data)
    } catch (error) {
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async fetchAnalysisById({ commit }, analysisId) {
    try {
      const response = await api.get(`/ai/results/${analysisId}/`)
      commit('SET_CURRENT_ANALYSIS', response.data)
      return response.data
    } catch (error) {
      throw error
    }
  },

  async fetchAnalysisHistory({ commit }, analysisId) {
    try {
      const response = await api.get('/ai/history/', {
        params: { analysis: analysisId }
      })
      commit('SET_ANALYSIS_HISTORY', response.data.results || response.data)
    } catch (error) {
      throw error
    }
  },

  async startAnalysis({ commit }, fileId) {
    try {
      const response = await api.post('/ai/results/analyze/', { file_id: fileId })
      return response.data
    } catch (error) {
      throw error
    }
  },

  async updateAnalysis({ commit }, { analysisId, data }) {
    try {
      const response = await api.post(`/ai/results/${analysisId}/update_result/`, data)
      commit('UPDATE_ANALYSIS_RESULT', response.data)
      return response.data
    } catch (error) {
      throw error
    }
  },

  async qaAnalysis({ commit }, { analysisId, question }) {
    try {
      const response = await api.post(`/ai/results/${analysisId}/qa/`, { question })
      return response.data
    } catch (error) {
      throw error
    }
  },

  async selectVersion({ commit }, analysisId) {
    try {
      const response = await api.post(`/ai/results/${analysisId}/select_version/`)
      commit('UPDATE_ANALYSIS_RESULT', response.data)
      return response.data
    } catch (error) {
      throw error
    }
  },

  async getSelectedVersion({ commit }, fileId) {
    try {
      const response = await api.get('/ai/results/get_selected_version/', {
        params: { file_id: fileId }
      })
      commit('SET_CURRENT_ANALYSIS', response.data)
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
