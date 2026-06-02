import { createStore } from 'vuex'
import auth from './modules/auth'
import files from './modules/files'
import aiAnalysis from './modules/aiAnalysis'

const store = createStore({
  modules: {
    auth,
    files,
    aiAnalysis
  }
})

export default store
