// Import React library for building components.
import React from 'react';

const getStatus = (task) => {
  if (!task.start_time) return 'KEPT';
  if (task.start_time && !task.stop_time) return 'RUNNING';
  return 'COMPLETED';
};

// Fixed formatter for Indian Standard Time (IST) - always shows correct India time
const istFormatter = new Intl.DateTimeFormat('en-GB', {
  year: 'numeric',
  month: '2-digit',
  day: '2-digit',
  hour: '2-digit',
  minute: '2-digit',
  second: '2-digit',
  hour12: true,          // AM/PM format
  timeZone: 'Asia/Kolkata'  // Forces IST (+5:30) regardless of system timezone
});

const formatIST = (dateString, use24Hour = false) => {
  if (!dateString) return '—';

  const date = new Date(dateString + 'Z'); // Force UTC

  return new Intl.DateTimeFormat('en-IN', {
    dateStyle: 'medium',
    timeStyle: 'medium',
    hour12: !use24Hour,
    timeZone: 'Asia/Kolkata'
  }).format(date);
};


// Define the MyTasks component with props.
const MyTasks = ({ tasks, username, onAction }) => {
  // Return the JSX structure for the component.
  return (
    // Outer div for the my tasks section.
    <div className="card">
        <h2>My Tasks</h2>

        {tasks.length === 0 ? (
            <p className="empty">No tasks assigned to you</p>
        ) : (
            <ul>
            {tasks.map(task => {
                const status =
                !task.start_time ? 'KEPT' :
                task.start_time && !task.stop_time ? 'RUNNING' :
                'COMPLETED';

                return (
                <li key={task.id} className="task-item">
                    {/* HEADER */}
                    <div className="task-header">
                    <span className="task-title">{task.title}</span>
                    <span className={`badge ${status.toLowerCase()}`}>
                        {status}
                    </span>
                    </div>

                    {/* TIME */}
                    <div className="time-box">
                    <div>🟢 <b>Start:</b> {task.start_time ? formatIST(task.start_time) + ' IST' : '—'}</div>
                    <div>🔴 <b>Stop:</b> {task.stop_time ? formatIST(task.stop_time) + ' IST' : '—'}</div>
                    </div>

                    {/* ACTIONS */}
                    <div className="task-footer">
                    <button
                        className="btn start"
                        disabled={task.start_time}
                        onClick={() => onAction('start', task.id)}
                    >
                        ▶ Start
                    </button>

                    <button
                        className="btn stop"
                        disabled={!task.start_time || task.stop_time}
                        onClick={() => onAction('stop', task.id)}
                    >
                        ⏹ Stop
                    </button>
                    </div>
                </li>
                );
            })}
            </ul>
        )}
    </div>
  );
};

// Export the MyTasks component as default.
export default MyTasks;