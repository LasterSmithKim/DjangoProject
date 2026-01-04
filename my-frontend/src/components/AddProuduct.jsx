import { useState, useEffect } from 'react' // 1. 引入 useEffect
import api from '../services/api'

function AddProuduct({ onAddSuccess }) {
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [price, setPrice] = useState('')
  const [category, setCategory] = useState('')
  const [image, setImage] = useState(null)
  
  // --- 新增：存放从后端拿到的分类列表 ---
  const [categories, setCategories] = useState([])

  // --- 2. 页面加载时，先去拿分类数据 ---
  useEffect(() => {
    const fetchCategories = async () => {
      try {
        // 请求你之前在 Django 路由里配置的分类接口
        const response = await api.get('/products/api/categories/') 
        setCategories(response.data.results || response.data)
        
        // 默认选中第一个分类（可选）
        if (response.data.length > 0) setCategory(response.data[0].id)
      } catch (err) {
        console.error("获取分类失败", err)
      }
    }
    fetchCategories()
  }, [])

  const addproduct = async (e) => {
    e.preventDefault()
    const formData = new FormData()
    formData.append('name', name)
    formData.append('description', description)
    formData.append('price', price)
    formData.append('category', category) // 这里现在拿到的是下拉框选中的 ID
    if (image) formData.append('image', image)

    try {
      await api.post('/products/api/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      alert("发布成功！")
      onAddSuccess()
    } catch (err) {
      alert("发布失败，请检查数据")
    }
  }

  return (
    <div className="p-8">
      <h2 className="text-2xl font-black mb-6 text-gray-800">发布新产品</h2>
      <form onSubmit={addproduct} className="space-y-5">
        <input className="w-full p-3 border rounded-lg" type="text" placeholder="产品名称" onChange={e => setName(e.target.value)} required />
        <textarea className="w-full p-3 border rounded-lg" placeholder="产品描述" onChange={e => setDescription(e.target.value)} />
        
        <div className="flex gap-2">
          <input className="w-1/2 p-3 border rounded-lg" type="number" step="0.01" placeholder="价格" onChange={e => setPrice(e.target.value)} required />
          
          {/* --- 3. 将输入框改为下拉选择框 --- */}
          <select 
            className="w-1/2 p-3 border rounded-lg bg-white"
            value={category}
            onChange={e => setCategory(e.target.value)}
            required
          >
            <option value="">选择分类</option>
            {categories.map(cat => (
              <option key={cat.id} value={cat.id}>
                {cat.name}
              </option>
            ))}
          </select>
        </div>

        <div className="border-2 border-dashed border-gray-300 p-4 rounded-lg text-center">
          <input type="file" onChange={e => setImage(e.target.files[0])} className="text-sm" />
        </div>
        
        <button type="submit" className="w-full bg-blue-600 text-white py-4 rounded-xl font-bold hover:bg-blue-700 transition-all">
          立即发布
        </button>
      </form>
    </div>
  )
}

export default AddProuduct