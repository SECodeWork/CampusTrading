import request from './request';

// 租赁商品相关API接口
export const rentAPI = {
  // 获取租赁商品列表
  getRentItems: (params?: {
    page?: number;
    pageSize?: number;
    category?: string;
    keyword?: string;
    priceMin?: number;
    priceMax?: number;
    sortBy?: string;
    sortOrder?: 'asc' | 'desc';
    status?: string;
  }) => {
    return request.get('/items', { params: { ...params, transaction_type: 'rent' } });
  },

  // 获取租赁商品详情
  getRentItemDetail: (id: string) => {
    return request.get(`/items/${id}`);
  },

  // 创建租赁商品
  createRentItem: (itemData: {
    title: string;
    description: string;
    categoryId: string;
    tags?: string[];
    images: string[];
    location?: string;
    status?: string;
    rental_price_day: number;
    rental_price_week?: number;
    rental_price_month?: number;
    deposit?: number;
    max_rental_days: number;
  }) => {
    return request.post('/items', { ...itemData, transaction_type: 'rent' });
  },

  // 更新租赁商品
  updateRentItem: (id: string, itemData: {
    title?: string;
    description?: string;
    categoryId?: string;
    tags?: string[];
    images?: string[];
    location?: string;
    status?: string;
    rental_price_day?: number;
    rental_price_week?: number;
    rental_price_month?: number;
    deposit?: number;
    max_rental_days?: number;
  }) => {
    return request.put(`/items/${id}`, { ...itemData, transaction_type: 'rent' });
  },

  // 申请租赁
  applyForRental: (data: {
    item_id: string;
    rental_days: number;
    start_date: string;
    end_date: string;
    total_amount: number;
    deposit: number;
  }) => {
    return request.post('/rent/request', { ...data, transaction_type: 'rent' });
  },

  // 获取租赁订单
  getRentalOrders: (params?: {
    page?: number;
    pageSize?: number;
    status?: string;
  }) => {
    return request.get('/transactions', { params: { ...params, transaction_type: 'rent' } });
  },

  // 获取租赁订单详情
  getRentalOrderDetail: (id: string) => {
    return request.get(`/transactions/${id}`);
  },

  // 取消租赁订单
  cancelRentalOrder: (id: string) => {
    return request.put(`/transactions/${id}/cancel`);
  },

  // 确认租赁订单
  confirmRentalOrder: (id: string) => {
    return request.put(`/rent/${id}/confirm`);
  },

  // 完成租赁订单
  completeRentalOrder: (id: string) => {
    return request.put(`/transactions/${id}/complete`);
  },

  // 评价租赁订单
  rateRentalOrder: (id: string, data: {
    rating: number;
    comment: string;
    item_id: string;
  }) => {
    return request.post(`/transactions/${id}/rate`, data);
  },

  // 延长租赁时间
  extendRental: (id: string, data: {
    days: number;
    total_amount: number;
    end_date: string;
  }) => {
    return request.put(`/transactions/${id}/extend`, data);
  },

  // 计算租赁价格
  calculateRentalPrice: (data: {
    item_id: string;
    rental_days: number;
  }) => {
    return request.post('/items/calculate-rental-price', data);
  },

  // 获取用户租赁记录
  getUserRentalRecords: (params?: {
    page?: number;
    pageSize?: number;
    type?: 'renter' | 'owner';
    status?: string;
  }) => {
    return request.get('/users/rental-records', { params });
  },

  // 获取租赁统计信息
  getRentalStats: () => {
    return request.get('/rent/stats');
  },

  // 举报租赁商品
  reportRentItem: (id: string, data: {
    reason: string;
    description?: string;
  }) => {
    return request.post(`/items/${id}/report`, data);
  },

  // 收藏租赁商品
  favoriteRentItem: (id: string) => {
    return request.post(`/items/${id}/favorite`);
  },

  // 取消收藏租赁商品
  unfavoriteRentItem: (id: string) => {
    return request.delete(`/items/${id}/favorite`);
  },

  // 获取收藏的租赁商品
  getFavoriteRentItems: (params?: {
    page?: number;
    pageSize?: number;
  }) => {
    return request.get('/items/favorites', { params: { ...params, transaction_type: 'rent' } });
  },

  // 浏览租赁商品
  viewRentItem: (id: string) => {
    return request.post(`/items/${id}/view`);
  }
};

export default rentAPI;

// 导出单独的函数以便直接使用
export const getRentItems = rentAPI.getRentItems;
export const getRentItemDetail = rentAPI.getRentItemDetail;
export const createRentItem = rentAPI.createRentItem;
export const updateRentItem = rentAPI.updateRentItem;
export const applyForRental = rentAPI.applyForRental;
export const getRentalOrders = rentAPI.getRentalOrders;
export const getRentalOrderDetail = rentAPI.getRentalOrderDetail;
export const cancelRentalOrder = rentAPI.cancelRentalOrder;
export const confirmRentalOrder = rentAPI.confirmRentalOrder;
export const completeRentalOrder = rentAPI.completeRentalOrder;
export const rateRentalOrder = rentAPI.rateRentalOrder;
export const extendRental = rentAPI.extendRental;
export const calculateRentalPrice = rentAPI.calculateRentalPrice;
export const getUserRentalRecords = rentAPI.getUserRentalRecords;
export const getRentalStats = rentAPI.getRentalStats;
export const reportRentItem = rentAPI.reportRentItem;
export const favoriteRentItem = rentAPI.favoriteRentItem;
export const unfavoriteRentItem = rentAPI.unfavoriteRentItem;
export const getFavoriteRentItems = rentAPI.getFavoriteRentItems;
export const viewRentItem = rentAPI.viewRentItem;