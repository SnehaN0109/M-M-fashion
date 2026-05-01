const BASE_URL = "http://localhost:5000/api";

export const fetchProducts = async (filters = {}) => {
  const domain = window.location.hostname;
  const queryParams = new URLSearchParams({
    domain,
    ...filters
  });
  const response = await fetch(`${BASE_URL}/products/?${queryParams}`);
  if (!response.ok) throw new Error("Failed to fetch products");
  return response.json();
};

export const fetchProductById = async (id) => {
  const domain = window.location.hostname;
  const response = await fetch(`${BASE_URL}/products/${id}?domain=${domain}`);
  if (!response.ok) throw new Error("Product not found");
  return response.json();
};

export const checkHealth = async () => {
  const response = await fetch(`${BASE_URL}/health`);
  return response.json();
};
