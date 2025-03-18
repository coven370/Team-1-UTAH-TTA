import Vue from 'vue';
import Router from 'vue-router';

//import Login from '@/pages/LoginPage.vue'
//import CreateAccount from '@/pages/CreateAccount.vue'
import DashboardLayout from "@/pages/layout/DashboardLayout.vue";
import Home from '@/pages/HomePage.vue';
import Improve from "@/pages/ImprovePage.vue";
import Scenario from "@/pages/ScenarioPage.vue";

Vue.use(Router);

export default new Router({
    mode: 'history', // Removes hash from URL (e.g., /login instead of #/login)
    routes: [
        {
            path: '/',
            redirect: '/dashboard/home', // Redirects to the home page inside the dashboard
        },
        {
            path: '/dashboard',
            component: DashboardLayout,
            children: [
                {
                    path: 'home',
                    name: 'Home',
                    component: Home
                },
                {
                    path: 'scenario',
                    name: 'Scenario',
                    component: Scenario
                },
                {
                    path: 'improve',
                    name: 'ImproveAI',
                    component: Improve
                },
            ]
        }
    ]
});
