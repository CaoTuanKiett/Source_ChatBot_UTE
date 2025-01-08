import { useAuthStore } from '@/stores/auth'
import 'aos/dist/aos.css'
import { createRouter, createWebHistory } from 'vue-router'

export enum RoutePrefix {
    Auth = '/auth',
    Admin = '/admin',
    Chatbot = '/chatbot',
    Management = '/management',
    Default = ''
}

export enum RoutePath {
    Home = RoutePrefix.Default + '/',
    About = RoutePrefix.Default + '/about',
    NotFound = RoutePrefix.Default + '/404',
    /*******/
    Login = RoutePrefix.Auth + '/login',
    Register = RoutePrefix.Auth + '/register',
    /*******/
    // Chatbot = RoutePrefix.Chatbot + '/chatbot',
    ChatbotRegister = RoutePrefix.Chatbot + '/register',
    // ChatbotManagement = RoutePrefix.Chatbot + '/management',
    ChatbotDetail = RoutePrefix.Chatbot + '/detail/:id',

    //MANAGEMENT
    Management = RoutePrefix.Management + '/',
    ManagementChatbot = RoutePrefix.Management + '/chatbot',
    ManagementRole = RoutePrefix.Management + '/role',
    ManagementUser = RoutePrefix.Management + '/user',
    ManagementQuestion = RoutePrefix.Management + '/question',
    ManagementFeedback = RoutePrefix.Management + '/feedback',
    ManagementSchool = RoutePrefix.Management + '/school',
    ManagementDocument = RoutePrefix.Management + '/document',

    //management chatbot
    ChatbotManagementUser = RoutePrefix.Chatbot + '/management/user',
    ChatbotManagementUserDetail = RoutePrefix.Chatbot + '/management/user/:id',
    // ChatbotManagementUserDetailEdit = RoutePrefix.Chatbot + '/management/user/:id/edit',
    // ChatbotManagementUserDetailDelete = RoutePrefix.Chatbot + '/management/user/:id/delete',
    ChatbotManagementUserDetailAdd = RoutePrefix.Chatbot + '/management/user/add',

    //management question
    ChatbotManagementQuestion = RoutePrefix.Chatbot + '/management/question',
    ChatbotManagementQuestionDetail = RoutePrefix.Chatbot + '/management/question/:id',

    AdminTab1Sub1 = RoutePrefix.Admin + '/tab1/sub1',
    AdminTab1Sub2 = RoutePrefix.Admin + '/tab1/sub2',
    AdminTab2 = RoutePrefix.Admin + '/tab2',
    AdminTab3 = RoutePrefix.Admin + '/tab3'
}

export const PUBLIC_ROUTE_PATHS: string[] = [
    RoutePath.Login,
    RoutePath.Register,
    RoutePath.Home,
    RoutePath.About,
    RoutePath.NotFound
]

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: RoutePrefix.Default,
            children: [
                {
                    path: RoutePath.Home,
                    name: 'home',
                    component: () => import('../views/HomPage.vue'),
                    // component: () => import('../views/home/index.vue'),
                    meta: {
                        layout: 'home-page'
                    }
                },

                {
                    path: RoutePath.NotFound,
                    name: '404',
                    component: () => import('../views/404/index.vue'),
                    meta: {
                        title: '404'
                    }
                }
            ]
        },
        {
            path: RoutePrefix.Auth,
            meta: {
                layout: 'auth'
            },
            children: [
                {
                    path: RoutePath.Login,
                    name: 'Login',
                    component: () => import('../views/login/index.vue'),
                    meta: {
                        title: 'Đăng nhập'
                    }
                },
                {
                    path: RoutePath.Register,
                    name: 'Register',
                    component: () => import('../views/register/index.vue'),
                    meta: {
                        title: 'Đăng ký'
                    }
                }
            ]
        },

        {
            path: RoutePrefix.Management,
            meta: {
                layout: 'management'
            },
            children: [
                {
                    path: RoutePath.ManagementChatbot,
                    name: 'ChatbotManagement',
                    component: () => import('../views/chatbot/ManagementChatbot.vue'),
                    meta: {
                        title: 'Quản lý Chatbot'
                    }
                },
                {
                    path: RoutePath.ManagementRole,
                    name: 'RoleManagement',
                    component: () => import('../views/management/user/ManagementRole.vue'),
                    meta: {
                        title: 'Quản lý Vai trò'
                    }
                },
                {
                    path: RoutePath.ManagementUser,
                    name: 'UserManagement',
                    component: () => import('../views/management/user/ManagementUser.vue'),
                    meta: {
                        title: 'Quản lý Tài khoản'
                    }
                },
                {
                    path: RoutePath.ManagementQuestion,
                    name: 'QuestionManagement',
                    component: () => import('../views/management/question/ManagementQuestion.vue'),
                    meta: {
                        title: 'Quản lý Câu hỏi'
                    }
                },
                {
                    path: RoutePath.ManagementFeedback,
                    name: 'FeedbackManagement',
                    component: () => import('../views/management/feedback/ManagementFeedback.vue'),
                    meta: {
                        title: 'Quản lý Góp ý'
                    }
                },
                {
                    path: RoutePath.ManagementSchool,
                    name: 'SchoolManagement',
                    component: () => import('../views/management/school/ManagementSchool.vue'),
                    meta: {
                        title: 'Quản lý Trường học'
                    }
                },
                {
                    path: RoutePath.ManagementDocument,
                    name: 'DocumentManagement',
                    component: () => import('../views/management/document/ManagementDocument.vue'),
                    meta: {
                        title: 'Quản lý Tài liệu'
                    }
                }
            ]
        },
        {
            path: RoutePrefix.Chatbot,
            meta: {
                layout: 'default'
            },
            children: [
                // {
                //     path: RoutePath.ChatbotRegister,
                //     name: 'ChatbotRegister',
                //     component: () => import('../views/chatbot/RegisterChatbot.vue'),
                //     meta: {
                //         title: 'Đăng ký Chatbot'
                //     }
                // },
                // {
                //     path: RoutePath.ChatbotManagement,
                //     name: 'ChatbotManagement',
                //     component: () => import('../views/chatbot/ManagementChatbot.vue'),
                //     meta: {
                //         title: 'Quản lý Chatbot'
                //     }
                // },
                // {
                //     path: RoutePath.ChatbotDetail,
                //     name: 'ChatbotDetail',
                //     component: () => import('../views/chatbot/RegisterChatbot.vue'),
                //     meta: {
                //         title: 'Chi tiết Chatbot'
                //     }
                // }
            ]
        }
    ]
})

router.beforeEach(async (to, from, next) => {
    // console.info(':::Router -> Enter', to.path)
    // AOS.init() // Initialize AOS

    // const existingPages = router.getRoutes().map((route) => route.path)

    // if (!existingPages.includes(to.path)) {
    //     console.info(`:::Router -> '${to.path}' not found, redirect to 404 page`)
    //     return RoutePath.NotFound
    // }

    // Kiểm tra xem route có hợp lệ không
    if (!to.matched.length) {
        console.info(`:::Router -> '${to.path}' not found, redirect to 404 page`)
        return RoutePath.NotFound
    }

    const toAuthRequiredRoutes = !PUBLIC_ROUTE_PATHS.includes(to.path)
    const authStore = useAuthStore()

    if (toAuthRequiredRoutes && !authStore.isLoggedIn) {
        console.info(`:::Router -> '${to.path}' requires authentication, redirect to login page`)
        authStore.returnUrl = to.fullPath
        return next({ path: RoutePath.Login })
    }

    const defaultTitle = 'UTE Chatbot'
    const title = (to.meta.title as string) || defaultTitle
    document.title = title

    next()
    // next()
})

export default router
