// src/App.jsx
import { useState, useEffect } from 'react'
import './App.css'
import LoginForm from './components/LoginForm'   // 导入子组件
import ProductList from './components/ProductList' // 导入子组件
import AddProuduct from './components/AddProuduct'
import api from './services/api' // 引入管家

function App() {
  const [products, setProducts] = useState([])
  const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem('access'))
  const [refreshCount, setRefreshCount] = useState(0) 
  const [showAddModal, setShowAddModal] = useState(false); // 默认隐藏
  const [currentUsername, setCurrentUsername] = useState(localStorage.getItem('username')) 
  const [searchQuery, setSearchQuery] = useState('')  // --- 新增：搜索关键词状态 ---
  const [debouncedSearchQuery, setDebouncedSearchQuery] = useState('') // 真正用来搜索的内容

  const handleLogout = () => {
    localStorage.removeItem('access')
    localStorage.removeItem('refresh')
    localStorage.removeItem('username')
    setProducts([])
    setIsLoggedIn(false)
    setCurrentUsername('')
  }

  // --- 逻辑 A：负责“延迟更新”搜索词 ---
  useEffect(() => {
    // 开启一个定时器，500毫秒后更新真正的搜索词
    const timer = setTimeout(() => {
      setDebouncedSearchQuery(searchQuery)
    }, 2000) 

    // 重要：如果用户在500毫秒内又打字了，就清除上一个定时器，重新计时
    return () => clearTimeout(timer) 
  }, [searchQuery])


  useEffect(() => {
    
    const fetchProducts = async () => {
      if (!localStorage.getItem('access')) return

      try {
        // 没有任何 Headers，没有任何完整地址
        // 管家已经在后台帮你贴好 Token 了
        const response = await api.get('/products/api/',
          {
          params: {
            search: debouncedSearchQuery, // 使用延迟后的词
          }
        }
        )
        setProducts(response.data.results || response.data)
      } catch (err) {
        console.error("抓取失败:", err)
      }
    }
    fetchProducts()
  }, [isLoggedIn,refreshCount,debouncedSearchQuery])

  return (
        <div className="App min-h-screen bg-gray-50 p-4">
      <h1 className="text-3xl font-black text-center text-gray-800 my-8">
        2026 现代商城
      </h1>
      <div className="max-w-4xl mx-auto mb-8 px-4">
        {/* --- 搜索框区域 --- */}
        <div className="flex gap-4 items-center">
          <input 
            type="text" 
            placeholder="搜一搜你想要的产品..." 
            className="flex-1 p-4 rounded-2xl border-none shadow-inner bg-white focus:ring-2 focus:ring-blue-400 outline-none"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)} // 实时同步输入内容
          />
          
          {/* 这里是之前的登录/发布按钮逻辑 */}
          <div className="flex items-center gap-2">
            {isLoggedIn && (
               <button onClick={() => setShowAddModal(true)} className="...">+ 发布</button>
            )}
          </div>
        </div>
      </div>

      {/* --- 顶部导航/操作区 --- */}
      <div className="max-w-4xl mx-auto flex justify-between items-center mb-8 px-4">
        {!isLoggedIn ? (
          <LoginForm onLoginSuccess={(name) => {setIsLoggedIn(true);setCurrentUsername(name)}} />
        ) : (
          <>
            <div className="flex items-center gap-4">
              <span className="text-gray-600 font-medium">欢迎回来，{currentUsername}  </span>
              <button onClick={handleLogout} className="text-sm text-red-500 hover:underline">退出登录</button>
            </div>
            
            {/* 1. 触发弹窗的按钮 */}
            <button 
              onClick={() => setShowAddModal(true)}
              className="bg-blue-600 text-white px-6 py-2 rounded-full font-bold shadow-lg hover:bg-blue-700 transition-all transform hover:scale-105"
            >
              + 发布新产品
            </button>
          </>
        )}
      </div>

      {/* --- 2. 弹窗层 (Modal) --- */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          {/* 背景遮罩：点击背景可以关闭 */}
          <div 
            className="absolute inset-0 bg-black/50 backdrop-blur-sm" 
            onClick={() => setShowAddModal(false)}
          ></div>

          {/* 弹窗主体 */}
          <div className="relative bg-white rounded-3xl shadow-2xl w-full max-w-md overflow-hidden animate-in fade-in zoom-in duration-200">
            {/* 关闭按钮 */}
            <button 
              onClick={() => setShowAddModal(false)}
              className="absolute top-4 right-4 text-gray-400 hover:text-gray-600"
            >
              ✕
            </button>

            {/* 注入你的 AddProuduct 组件 */}
            <AddProuduct onAddSuccess={() => {
              setRefreshCount(prev => prev + 1); // 刷新列表
              setShowAddModal(false);            // 成功后自动关闭弹窗
            }} />
          </div>
        </div>
      )}

      {/* --- 产品展示区 --- */}
      <ProductList products={products} isLoggedIn={isLoggedIn} onDeleteSuccess={() => setRefreshCount(prev => prev + 1)}/>
    </div>
  )
}

export default App