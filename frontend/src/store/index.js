import {createStore} from "vuex";

export default createStore({
    state: {
      apiBaseUrl: 'http://localhost:8000/api/',
      trackedCommentsById: {}, // { [commentId (or 'top')]: [commentsArray] }
      replyToComment: null,
      isFormVisible: false,
      socket: null,
  },
  getters: {
    API_URL: state => {
      return state.apiBaseUrl
    },

    TRACKED_BRANCHES: state => {
      console.log(state.trackedCommentsById)
      return state.trackedCommentsById
    },

    GET_REPLY_ID: state => {
      return state.replyToComment.id
    },
    GET_REPLY_USER_NAME: state => {
      return state.replyToComment.user_name
    },

    GET_FORM_STATE: state => {
      return state.isFormVisible
    },
  },
  mutations: {
    ADD_BRANCHES: (state, { id, commentsBranch }) => {
      state.trackedCommentsById[id] = commentsBranch

      state.socket.send(
          JSON.stringify({
            tracked_branches: Object.keys(state.trackedCommentsById)
          })
      )
    },

    SET_REPLY: (state, {comment}) => {
      state.replyToComment = comment
      state.isFormVisible = true
      console.log(state.replyToComment)
    },
    DEL_REPLY: state => {
      state.replyToComment = null
    },

    FORM_VISIBLE: state => {
      state.isFormVisible = !state.isFormVisible
    },

    SET_SOCKET(state, socket) {
      state.socket = socket
    },
  },
  actions: {
    createWebSocket({ commit, getters }, url) {
      const socket = new WebSocket(url)

      socket.onmessage = function(event) {
        const data = JSON.parse(event.data)
        const comment = data.comment

        const branches = getters.TRACKED_BRANCHES
        if (comment.parent_comment_id) {
          branches[comment.parent_comment_id].push(comment)
        } else {
          branches["top"].unshift(comment)
        }
      }

      socket.onerror = function(error) {
        console.log(`[error]`, error);
      }

      commit('SET_SOCKET', socket)
      return socket
    }
  },
})
