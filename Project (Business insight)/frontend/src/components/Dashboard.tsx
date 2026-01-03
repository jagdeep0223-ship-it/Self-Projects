// Import React and hooks.
import React, { useState, useEffect } from 'react';
// Import axios for API calls.
import axios from 'axios';
// Import Recharts components for charting.
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
// Import jsPDF for PDF export.
import jsPDF from 'jspdf';
// Import auth hook.
import { useAuth } from '../hooks/useAuth';
import html2canvas from "html2canvas";

// Define the Dashboard component.
const Dashboard: React.FC = () => {
  // State for datasets list.
  const [datasets, setDatasets] = useState<any[]>([]);
  // State for selected dataset ID.
  const [selectedDatasetId, setSelectedDatasetId] = useState<number | null>(null);
  // State for insights.
  const [insights, setInsights] = useState<any[]>([]);
  // State for uploaded file.
  const [file, setFile] = useState<File | null>(null);
  const { logout } = useAuth();  // Get logout function.

  // Effect to fetch datasets on mount.
  useEffect(() => {
    fetchDatasets();  // Call fetch function.
  }, []);  // Empty dependency array for once on mount.

  // Async function to fetch datasets.
  const fetchDatasets = async () => {
    try {
      const response = await axios.get('http://localhost:8000/datasets');  // GET datasets.
      setDatasets(response.data);  // Update state.
    } catch (error) {
      console.error('Error fetching datasets', error);  // Log error.
    }
  };

  // Async function to fetch insights for a dataset.
  const fetchInsights = async (id: number) => {
    try {
      const response = await axios.get(`http://localhost:8000/insights/${id}`);  // GET insights.
      setInsights(response.data);  // Update state.
    } catch (error) {
      console.error('Error fetching insights', error);  // Log error.
    }
  };

  // Function to handle file upload.
  const handleUpload = async () => {
    if (!file) return;  // Exit if no file.
    const formData = new FormData();  // Create form data.
    formData.append('file', file);  // Append file.
    try {
      await axios.post('http://localhost:8000/upload', formData, {  // POST upload.
        headers: { 'Content-Type': 'multipart/form-data' },  // Set headers.
      });
      alert('Upload successful');  // Alert success.
      fetchDatasets();  // Refresh datasets.
    } catch (error) {
      alert('Upload failed');  // Alert failure.
    }
  };

  // Function to select a dataset.
  const handleSelectDataset = (id: number) => {
    setSelectedDatasetId(id);  // Update selected ID.
    fetchInsights(id);  // Fetch insights.
  };

  // Function to export insights to PDF.
//   const exportPDF = () => {
//     const doc = new jsPDF();  // Create new PDF document.
//     doc.text('InsightForge Report', 10, 10);  // Add title.
//     insights.forEach((insight, index) => {  // Loop through insights.
//       doc.text(`Prediction ${index + 1}: ${insight.insight_text}`, 10, 20 + index * 10);  // Add text.
//     });
//     doc.save('insights.pdf');  // Save PDF.
//   };

    const exportPDF = async () => {
    const doc = new jsPDF("p", "mm", "a4");

    // 1️⃣ Add title
    doc.setFontSize(16);
    doc.text("InsightForge Report", 10, 10);

    // 2️⃣ Add insights text
    let y = 20;
    insights.forEach((insight, index) => {
        const cleanText = insight.insight_text.replace(/[^\x00-\x7F]/g, "");
        const lines = doc.splitTextToSize(
        `Prediction ${index + 1}: ${cleanText}`,
        180
        );
        doc.text(lines, 10, y);
        y += lines.length * 8;
    });

    // 3️⃣ Capture chart as image
    const chartElement = document.getElementById("chart-section");
    if (chartElement) {
        const canvas = await html2canvas(chartElement);
        const imgData = canvas.toDataURL("image/png");

        // Add new page for chart
        doc.addPage();
        doc.text("Trend Graph", 10, 10);
        doc.addImage(imgData, "PNG", 10, 20, 180, 100);
    }

    // 4️⃣ Save PDF
    doc.save("insights.pdf");
    };

  // Dummy chart data for demo (in prod, fetch real data).
  const chartData = [
    { date: '2023-01', value: 100 },  // Sample historical data point.
    { date: '2023-02', value: 120 },  // Another data point.
    // ... add more from sample CSV
    { date: 'Predicted', value: insights[0]?.predicted_value || 0 },  // Add predicted value.
  ];

  // Render the dashboard UI.
  return (
    <div className="container-fluid app-container">

      {/* 2️⃣ NAVBAR */}
      <nav className="navbar navbar-light bg-white mb-4 rounded px-3">
        <span className="navbar-brand mb-0 h4">InsightForge Dashboard</span>
        <button className="btn btn-outline-danger btn-sm" onClick={logout}>
          Logout
        </button>
      </nav>

      {/* 3️⃣ UPLOAD CARD */}
      <div className="card p-3 mb-4">
        <h5>Upload Dataset (Admin)</h5>
        <input
          type="file"
          className="form-control mb-2"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
        />
        <button className="btn btn-primary" onClick={handleUpload}>
          Upload CSV
        </button>
      </div>

      {/* 4️⃣ DATASETS CARD */}
      <div className="card p-3 mb-4">
        <h5>Datasets</h5>
        <ul className="list-group">
          {datasets.map((ds) => (
            <li
              key={ds.id}
              className="list-group-item list-group-item-action"
              onClick={() => handleSelectDataset(ds.id)}
              style={{ cursor: 'pointer' }}
            >
              {ds.filename}
            </li>
          ))}
        </ul>
      </div>

      {/* INSIGHTS + CHART (ONLY IF DATASET SELECTED) */}
      {selectedDatasetId && (
        <>
          <h4 className="mb-3">Insights for Dataset {selectedDatasetId}</h4>

          {/* 5️⃣ INSIGHT CARDS */}
          {insights.map((insight, index) => (
            <div key={index} className="card p-3 mb-3">
              <p>
                <strong>Insight:</strong> {insight.insight_text}
              </p>
              <p>
                Predicted Value: <strong>{insight.predicted_value}</strong>
              </p>
              <p>
                Confidence: {insight.confidence.toFixed(2)}
              </p>
            </div>
          ))}

          {/* 7️⃣ EXPORT PDF BUTTON */}
          <button className="btn btn-success mb-4" onClick={exportPDF}>
            Export PDF Report
          </button>

          {/* 6️⃣ CHART CARD */}
          <div className="card p-3 mt-4" id="chart-section">
            <h5>Trend Analysis</h5>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="value" stroke="#4f46e5" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </>
      )}
    </div>
  );
};

export default Dashboard;  // Export component.