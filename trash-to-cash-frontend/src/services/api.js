


import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000/api/";

export const scanBottle = (user_id) => axios.post(`${API_BASE_URL}upload/scan/`, { user_id });
export const getUserProfile = (username) => axios.get(`${API_BASE_URL}user/profile/`, { params: { username } });
export const updateRecyclingCount = (user_id, materialType) =>
  axios.post(`${API_BASE_URL}user/update_recycling/`, { user_id, materialType });
export const updateClassification = (data) =>
  axios.post(`${API_BASE_URL}classification/update/`, data);
export const uploadImage = (data) => axios.post(`${API_BASE_URL}upload/image/`, data);
