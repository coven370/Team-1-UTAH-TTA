import Vue from 'vue';
import Vuex from 'vuex';
import createPersistedState from 'vuex-persistedstate';

Vue.use(Vuex);
export const store = new Vuex.Store({
    plugins: [createPersistedState({
        storage: window.sessionStorage,
    })],
    state: {
        user: null,
        loggedIn: false,
        improveAccepted: false,
    },
    actions: {
        ADD_USER({ commit }, user) {
            commit('SET_USER', user);
        },

        SET_LOGGED_IN({ commit }, loggedIn) {
            commit('SET_LOGIN', loggedIn);
        },

        LOGOUT({ commit }) {
            commit('SET_LOGOUT');
        },

        ACCEPT_IMPROVE({ commit }) {
            commit('ACCEPT_IMPROVE');
        },
    },

    mutations: {

        SET_LOGIN(state, loggedIn) {
            state.loggedIn = loggedIn;
        },

        SET_USER(state, user) {
            state.user = user;
        },

        SET_LOGOUT(state) {
            state.user = null;
            state.loggedIn = false;
            state.improveAccepted = false
            sessionStorage.clear();
        },

        ACCEPT_IMPROVE(state){
            state.improveAccepted = true
        }
    },

    getters: {
        user: state => state.user,
        loggedIn: state => state.loggedIn,
        improveAccepted: state => state.improveAccepted,
    },
});
