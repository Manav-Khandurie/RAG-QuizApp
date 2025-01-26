CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    content TEXT,
    embedding VECTOR(768)  
);

CREATE TABLE quiz_questions (
    id SERIAL PRIMARY KEY,
    document_id INT REFERENCES documents(id) ON DELETE CASCADE,  
    question TEXT,
    options TEXT[],  
    answer TEXT      
);

