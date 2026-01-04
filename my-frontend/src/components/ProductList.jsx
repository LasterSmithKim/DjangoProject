// src/components/ProductList.jsx
import api from '../services/api'

function ProductList({ products, isLoggedIn, onDeleteSuccess }) {
  
  const handleDelete = async (id) => {
    if (!window.confirm("确定要删除这个产品吗？")) return;
    
    try {
      await api.delete(`/products/api/${id}/`);
      alert("删除成功！");
      onDeleteSuccess(); // 触发刷新
    } catch (err) {
      alert("删除失败，可能你没有权限。");
    }
  };

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 p-6">
      {products.map(product => (
        <div key={product.id} className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-xl transition-shadow duration-300 border border-gray-100">
          <div className="h-48 bg-gray-200">
            {product.image ? (
              <img src={product.image} alt={product.name} className="w-full h-full object-cover" />
            ) : (
              <div className="flex items-center justify-center h-full text-gray-400">暂无图片</div>
            )}
          </div>
          <div className="p-4">
            <h3 className="text-lg font-bold text-gray-800">{product.name}</h3>
            <p className="text-gray-600 text-sm mt-1 h-10 overflow-hidden">{product.description}</p>
            <div className="flex justify-between items-center mt-4">
              <span className="text-xl font-semibold text-orange-500">￥{product.price}</span>
              {isLoggedIn && (
                <button 
                  onClick={() => handleDelete(product.id)}
                  className="p-2 bg-red-50 text-red-500 rounded-full hover:bg-red-500 hover:text-white transition-colors"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              )}
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}
export default ProductList