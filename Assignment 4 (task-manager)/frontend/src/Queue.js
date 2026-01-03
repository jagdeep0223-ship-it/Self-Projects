// Import React library for building components.
import React from 'react';

// Define the Queue component with props for tasks, username, and onAction.
const Queue = ({ tasks, username, onAction }) => {
  // Return the JSX structure for the component.
  return (
    // Outer div for the queue section.
    <div className="card">
        <h2>Task Queue</h2>

        {tasks.length === 0 ? (
            <p className="empty">Queue is empty</p>
        ) : (
            <ul>
            {tasks.map(task => (
                <li key={task.id} className="task-item">
                <strong>{task.title}</strong>

                <div className="actions">
                    <button
                    className="btn assign"
                    onClick={() => onAction('assign', task.id)}
                    >
                    Assign & Start
                    </button>

                    <button
                    className="btn keep"
                    onClick={() => onAction('keep', task.id)}
                    >
                    Keep
                    </button>
                </div>
                </li>
            ))}
            </ul>
        )}
    </div>
  );
};

// Export the Queue component as default.
export default Queue;