import React, { useState } from "react";
import axios from "axios";

function App() {
    const [file, setFile] = useState(null);
    const [quiz, setQuiz] = useState([]);
    const [loading, setLoading] = useState(false);
    const [documentId, setDocumentId] = useState(null);
    const handleUpload = async () => {
        if (!file) {
            alert("Please select a file before uploading.");
            return;
        }

        const formData = new FormData();
        formData.append("file", file);

        setLoading(true);
        try {
            const response = await axios.post("http://localhost:8000/upload", formData);
            setDocumentId(response.data.document_id); // Save the document ID
            console.log(response.data);
            alert("Document uploaded successfully!");
        } catch (error) {
            console.error(error);
            alert("Failed to upload document. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    const handleGenerateQuiz = async () => {
        setLoading(true);
        console.log(documentId)
        try {
            const response = await axios.post(`http://localhost:8000/generate-quiz?document_id=${documentId}`); // Replace with dynamic document_id if needed
            setQuiz(response.data.questions);
            alert("Quiz generated successfully!");
        } catch (error) {
            console.error(error);
            alert("Failed to generate quiz. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
            <h1 style={{ textAlign: "center" }}>Quiz App</h1>
            
            {/* Upload Section */}
            <div style={{ marginBottom: "30px" }}>
                <h2>Upload Document</h2>
                <input
                    type="file"
                    accept=".pdf"
                    onChange={(e) => setFile(e.target.files[0])}
                />
                <button
                    onClick={handleUpload}
                    disabled={loading}
                    style={{
                        marginLeft: "10px",
                        padding: "10px 15px",
                        backgroundColor: "#007bff",
                        color: "#fff",
                        border: "none",
                        borderRadius: "5px",
                        cursor: loading ? "not-allowed" : "pointer",
                    }}
                >
                    {loading ? "Uploading..." : "Upload"}
                </button>
            </div>

            {/* Generate Quiz Section */}
            <div style={{ marginBottom: "30px" }}>
                <h2>Generate Quiz</h2>
                <button
                    onClick={handleGenerateQuiz}
                    disabled={loading}
                    style={{
                        padding: "10px 15px",
                        backgroundColor: "#28a745",
                        color: "#fff",
                        border: "none",
                        borderRadius: "5px",
                        cursor: loading ? "not-allowed" : "pointer",
                    }}
                >
                    {loading ? "Generating..." : "Generate Quiz"}
                </button>
            </div>

            {/* Quiz Display Section */}
            <div>
                <h2>Quiz Questions</h2>
                {quiz.length > 0 ? (
                    quiz.map((q, index) => (
                        <div
                            key={index}
                            style={{
                                marginBottom: "20px",
                                padding: "10px",
                                border: "1px solid #ddd",
                                borderRadius: "5px",
                                backgroundColor: "#f9f9f9",
                            }}
                        >
                            <h3>{q.question}</h3>
                            <ul>
                                {q.options.map((opt, i) => (
                                    <li key={i}>{opt}</li>
                                ))}
                            </ul>
                            <p>
                                <strong>Answer:</strong> {q.answer || "Not provided"}
                            </p>
                        </div>
                    ))
                ) : (
                    <p>No questions generated yet. Upload a document and generate a quiz.</p>
                )}
            </div>
        </div>
    );
}

export default App;
