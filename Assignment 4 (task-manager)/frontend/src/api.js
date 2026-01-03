// Import axios library for making HTTP requests.
import axios from 'axios';

// Define the base URL for the backend API.
const API_BASE_URL = 'http://127.0.0.1:8000';  // Backend URL

// Define async function to fetch the task queue.
export const getQueue = async () => {
  try {
    // Make GET request to /queue endpoint.
    const response = await axios.get(`${API_BASE_URL}/queue`);
    // Return the data from the response.
    return response.data;
  } catch (error) {
    // Improved error logging.
    console.error('Error fetching queue:', error.message);
    if (error.response) {
      console.error('Response data:', error.response.data);
      console.error('Status:', error.response.status);
    }
    // Return empty array on error.
    return [];
  }
};

// Define async function to fetch user's tasks.
export const getMyTasks = async (username) => {
  try {
    // Make GET request to /my_tasks with username query param.
    const response = await axios.get(`${API_BASE_URL}/my_tasks?username=${username}`);
    // Return the data from the response.
    return response.data;
  } catch (error) {
    // Improved error logging.
    console.error('Error fetching my tasks:', error.message);
    if (error.response) {
      console.error('Response data:', error.response.data);
    }
    // Return empty array on error.
    return [];
  }
};

// (Keep the rest of the functions the same — keepTask, assignTask, etc.)
export const keepTask = async (taskId, username) => {
  try {
    await axios.post(`${API_BASE_URL}/keep/${taskId}`, { username });
  } catch (error) {
    console.error('Error keeping task:', error.message);
  }
};

export const assignTask = async (taskId, username) => {
  try {
    await axios.post(`${API_BASE_URL}/assign/${taskId}`, { username });
  } catch (error) {
    console.error('Error assigning task:', error.message);
  }
};

export const startTask = async (taskId, username) => {
  try {
    await axios.post(`${API_BASE_URL}/start/${taskId}`, { username });
  } catch (error) {
    console.error('Error starting task:', error.message);
  }
};

export const stopTask = async (taskId, username) => {
  try {
    await axios.post(`${API_BASE_URL}/stop/${taskId}`, { username });
  } catch (error) {
    console.error('Error stopping task:', error.message);
  }
};