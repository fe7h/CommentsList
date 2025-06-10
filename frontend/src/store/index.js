import {createStore} from "vuex";


export default createStore({
    state: {
      nestedCommentsById: {}, // { [commentId]: [nestedCommentsArray] }
      replyToComment: null
  },
  getters: {
    TRACKED_BRANCHES: state => {
      return state.nestedCommentsById
    },
    GET_REPLY_ID: state => {
      return state.replyToComment.id
    },
    GET_REPLY_USER_NAME: state => {
      return state.replyToComment.user_name
    },
  },
  mutations: {
    ADD_BRANCHES: (state, { id, nestedComments }) => {
      state.nestedCommentsById[id] = nestedComments
    },
    SET_REPLY: (state, {comment}) => {
      state.replyToComment = comment
      console.log(state.replyToComment)
    },
    DEL_REPLY: state => {
      state.replyToComment = null
      console.log(state.replyToComment)
    },
  },
  actions: {},
})
