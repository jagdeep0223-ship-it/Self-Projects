// Import React and hooks for state and effects.
import React, { useState, useEffect } from 'react';
// Import Queue component.
import Queue from './Queue';
// Import MyTasks component.
import MyTasks from './MyTasks';
// Import API functions.
import { getQueue, getMyTasks, keepTask, assignTask, startTask, stopTask } from './api';
// Import CSS for styling.
import './App.css';  // Optional styling

// Define the main App component.
function App() {
  // State for username input.
  const [username, setUsername] = useState('');
  // State for login status.
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  // State for queue tasks.
  const [queueTasks, setQueueTasks] = useState([]);
  // State for user's tasks.
  const [myTasks, setMyTasks] = useState([]);

  // Define async function to fetch data.
  const fetchData = async () => {
    // Fetch queue tasks.
    const queue = await getQueue();
    // Update queue state.
    setQueueTasks(queue);
    // If logged in, fetch my tasks.
    if (isLoggedIn) {
      // Fetch my tasks with username.
      const tasks = await getMyTasks(username);
      // Update my tasks state.
      setMyTasks(tasks);
    }
  };

  // Use effect for polling data.
  useEffect(() => {
    // Initial data fetch.
    fetchData();  // Initial fetch
    // Set interval for polling every 5 seconds.
    const interval = setInterval(fetchData, 5000);  // Poll every 5s
    // Return cleanup function to clear interval.
    return () => clearInterval(interval);  // Cleanup
  // Dependencies: re-run if isLoggedIn or username changes.
  }, [isLoggedIn, username]);

  // Define function to handle actions.
  const handleAction = async (actionType, taskId) => {
    // If no username, return early.
    if (!username) return;
    // Switch based on action type.
    switch (actionType) {
      // Case for assign.
      case 'assign':
        // Call assignTask API.
        await assignTask(taskId, username);
        // Break switch.
        break;
      // Case for keep.
      case 'keep':
        // Call keepTask API.
        await keepTask(taskId, username);
        // Break switch.
        break;
      // Case for start.
      case 'start':
        // Call startTask API.
        await startTask(taskId, username);
        // Break switch.
        break;
      // Case for stop.
      case 'stop':
        // Call stopTask API.
        await stopTask(taskId, username);
        // Break switch.
        break;
      // Default case (do nothing).
      default:
        // Break switch.
        break;
    }
    // Refetch data after action.
    fetchData();  // Refetch immediately after action for instant update
  };

  // Define function to handle username submission.
  const handleSubmitUsername = (e) => {
    // Prevent default form submission.
    e.preventDefault();
    // If username is not empty, proceed.
    if (username.trim()) {
      // Set logged in to true.
      setIsLoggedIn(true);
      // Clear any old data.
      setQueueTasks([]);
      setMyTasks([]);
      // Fetch fresh data after login.
      setTimeout(fetchData, 500);  // Small delay to ensure state updates
    }
  };

  // Return the JSX for the App.
  return (
    // Main div with App class.
    <div className="App">
      {/* Heading for the app. */}
      <h1>Task Manager</h1>
      {/* Conditional: if not logged in, show form. */}
      {!isLoggedIn ? (
        // Form for username input.
        <form onSubmit={handleSubmitUsername}>
          {/* Label for input. */}
          <label>Enter Username: </label>
          {/* Input field for username. */}
          <input
            // Set type to text.
            type="text"
            // Bind value to state.
            value={username}
            // Update state on change.
            onChange={(e) => setUsername(e.target.value)}
          />
          {/* Submit button. */}
          <button type="submit">Enter</button>
        </form>
      ) : (
        // Else, show welcome and components.
        <>
          {/* Welcome message with username. */}
          <p>Welcome, {username}!</p>
          <div className="dashboard">
            <Queue tasks={queueTasks} username={username} onAction={handleAction} />
            <MyTasks tasks={myTasks} username={username} onAction={handleAction} />
          </div>
        </>
      )}
    </div>
  );
}

// Export App as default.
export default App;