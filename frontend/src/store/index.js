import {createStore} from "vuex";


export default createStore({
    state: {
      nestedCommentsById: {}, // { [commentId]: [nestedCommentsArray] }
  },
  getters: {
    TRACKED_BRANCHES: state => {
      return state.nestedCommentsById
    },
  },
  mutations: {
    ADD_BRANCHES: (state, { id, nestedComments }) => {
      state.nestedCommentsById[id] = nestedComments
    },
  },
  actions: {},
})
