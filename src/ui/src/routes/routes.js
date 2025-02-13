import Vue from 'vue';
import Router from 'vue-router';

//import Login from '@/pages/LoginPage.vue'
//import CreateAccount from '@/pages/CreateAccount.vue'
import Home from '@/pages/HomePage.vue';
import Dashboard from '@/pages/Dashboard.vue'

Vue.use(Router);

export default new Router({
    mode: 'history', // Removes hash from URL (e.g., /login instead of #/login)
    routes: [
        {
            path: '/',
            redirect: '/home' // Redirect the home page to Login
        },
        /*{
            path: '/login',
            name: 'Login',
            component: Login
        },
        {
            path: '/createAccount',
            name: 'CreateAccount',
            component: CreateAccount
        },*/
        {
            path: '/home',
            name: 'Home',
            component: Home
        },
        {
            path: '/dashboard',
            name: 'Dashboard',
            component: Dashboard
        }
    ]
});
