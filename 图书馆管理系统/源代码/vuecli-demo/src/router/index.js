import Vue from 'vue'
import VueRouter from 'vue-router'
import HelloWorld from "../components/HelloWorld.vue"
import Login from '../components/Login.vue'
import Library from '../components/Library.vue'

import Welcome from '../components/Welcome.vue'
import Books from '../components/Books.vue'
import Stocks from '../components/Stocks.vue'
import Borrowing from '../components/Borrowing.vue'
import ReaderInfo from '../components/ReaderInfo.vue'

Vue.use(VueRouter)

const routes = [{
    path: '/helloworld',
    name: 'helloworld',
    component: HelloWorld
  },
  {
    // 路由重定向
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'login',
    component: Login,
    meta: {
      requireAuth: true
    }
  },
  {
    path: '/library',
    name: 'library',
    component: Library,
    children: [
      // {
      //   path: '',
      //   redirect: '/library/welcome'
      // },
      // Library组件把user_type, user_id获取，然后push跳转
      {
        path: 'welcome',
        name: 'welcome',
        component: Welcome
      },
      {
        path: 'books',
        name: 'books',
        component: Books
      },
      {
        path: 'stocks',
        name: 'stocks',
        component: Stocks
      },
      {
        path: 'borrowing',
        name: 'borrowing',
        component: Borrowing
      },
      {
        path: 'readerinfo',
        name: 'readerinfo',
        component: ReaderInfo
      },
    ],
  }
]

const router = new VueRouter({
  mode: 'history', // 去掉地址栏中的'#'
  routes
})


// 每次路由访问之前的导航钩子
router.beforeEach(function (to, from, next) {
  const status = router.app.$cookies.get("status");
  // console.log("status = " + status);

  if (to.matched.some(record => record.meta.requireAuth)) {
    next() //如果路由中有meta的requireAuth，且为true，就不进行登录验证，否则进行登录验证
  } else {
    if (status) {
      next()
    } else {
      if (to.path === "/login") {
        next()
      } else {
        next({
          path: '/login'
        })
      }
    }
  }
})

export default router