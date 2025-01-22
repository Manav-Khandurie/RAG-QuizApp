import React, { useState } from "react";
import axios from "axios";

function App() {
    const [file, setFile] = useState(null);
    const [quiz, setQuiz] = useState([]);
    const [loading, setLoading] = useState(false);

    const handleUpload = async () => {
        const formData = new FormData();
        formData.append("file", file);

        setLoading(true);
        try {
            const response = await axios.post("http://localhost:8000/upload", formData);
            console.log(response.data);
            alert("Document uploaded successfully!");
        } catch (error) {
            console.error(error);
            alert("Failed to upload document.");
        } finally {
            setLoading(false);
        }
    };

    const handleGenerateQuiz = async () => {
        setLoading(true);
        try {
            const response = await axios.post("http://localhost:8000/generate-quiz", { document_id: 1 });
            setQuiz(response.data.questions);
        } catch (error) {
            console.error(error);
            alert("Failed to generate quiz.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ padding: "20px" }}>
            <h1>Quiz App</h1>
            <div>
                <h2>Upload Document</h2>
                <input type="file" onChange={(e) => setFile(e.target.files[0])} />
                <button onClick={handleUpload} disabled={loading}>
                    {loading ? "Uploading..." : "Upload"}
                </button>
            </div>
            <div>
                <h2>Generate Quiz</h2>
                <button onClick={handleGenerateQuiz} disabled={loading}>
                    {loading ? "Generating..." : "Generate Quiz"}
                </button>
            </div>
            <div>
                <h2>Quiz Questions</h2>
                {quiz.map((q, index) => (
                    <div key={index} style={{ marginBottom: "20px" }}>
                        <h3>{q.question}</h3>
                        <ul>
                            {q.options.map((opt, i) => (
                                <li key={i}>{opt}</li>
                            ))}
                        </ul>
                        <p>Answer: {q.answer}</p>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default App;