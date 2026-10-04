-- ExamAI initial schema for Supabase (PostgreSQL)

CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    role VARCHAR(50) DEFAULT 'student',
    phone_number VARCHAR(20),
    google_id VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS exams (
    exam_id SERIAL PRIMARY KEY,
    exam_name VARCHAR(255) NOT NULL,
    exam_type VARCHAR(100),
    duration INTEGER,
    total_marks INTEGER,
    passing_marks INTEGER,
    created_by INTEGER REFERENCES users(user_id),
    created_at TIMESTAMP DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS exam_patterns (
    pattern_id SERIAL PRIMARY KEY,
    exam_type VARCHAR(100),
    pattern_name VARCHAR(255),
    total_questions INTEGER,
    total_marks INTEGER,
    duration_minutes INTEGER,
    sections TEXT,
    negative_marking DOUBLE PRECISION,
    passing_marks INTEGER,
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS syllabus (
    syllabus_id SERIAL PRIMARY KEY,
    exam_id INTEGER REFERENCES exams(exam_id),
    subject_name VARCHAR(255) NOT NULL,
    topics JSONB,
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS questions (
    question_id SERIAL PRIMARY KEY,
    exam_id INTEGER REFERENCES exams(exam_id),
    subject VARCHAR(255),
    topic VARCHAR(255),
    question_text TEXT NOT NULL,
    question_type VARCHAR(50),
    difficulty_level VARCHAR(50),
    options JSONB,
    correct_answer VARCHAR(255),
    marks INTEGER,
    negative_marks DOUBLE PRECISION DEFAULT 0.0,
    explanation TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS exam_attempts (
    attempt_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    exam_id INTEGER REFERENCES exams(exam_id),
    start_time TIMESTAMP DEFAULT NOW(),
    end_time TIMESTAMP,
    score DOUBLE PRECISION,
    total_questions INTEGER,
    correct_answers INTEGER,
    incorrect_answers INTEGER,
    unanswered INTEGER,
    status VARCHAR(50) DEFAULT 'in_progress'
);

CREATE TABLE IF NOT EXISTS answers (
    answer_id SERIAL PRIMARY KEY,
    attempt_id INTEGER REFERENCES exam_attempts(attempt_id),
    question_id INTEGER REFERENCES questions(question_id),
    user_answer VARCHAR(255),
    is_correct BOOLEAN,
    time_taken INTEGER,
    marked_for_review BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS study_materials (
    material_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    file_url VARCHAR(500),
    material_type VARCHAR(50),
    subject VARCHAR(255),
    topic VARCHAR(255),
    exam_id INTEGER REFERENCES exams(exam_id),
    uploaded_by INTEGER REFERENCES users(user_id),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS subscriptions (
    subscription_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    plan_type VARCHAR(50),
    start_date TIMESTAMP DEFAULT NOW(),
    end_date TIMESTAMP,
    amount DOUBLE PRECISION,
    payment_status VARCHAR(50),
    auto_renew BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    plan_details JSONB,
    discount_applied DOUBLE PRECISION DEFAULT 0.0,
    original_amount DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS payments (
    payment_id SERIAL PRIMARY KEY,
    subscription_id INTEGER REFERENCES subscriptions(subscription_id),
    user_id INTEGER REFERENCES users(user_id),
    amount DOUBLE PRECISION,
    payment_method VARCHAR(50),
    transaction_id VARCHAR(255) UNIQUE,
    status VARCHAR(50),
    payment_date TIMESTAMP DEFAULT NOW(),
    razorpay_order_id VARCHAR(255),
    razorpay_payment_id VARCHAR(255),
    razorpay_signature VARCHAR(500),
    invoice_url VARCHAR(500)
);

CREATE TABLE IF NOT EXISTS reports (
    report_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    exam_id INTEGER REFERENCES exams(exam_id),
    attempt_id INTEGER REFERENCES exam_attempts(attempt_id),
    report_url VARCHAR(500),
    generated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_exam_attempts_user_id ON exam_attempts(user_id);
CREATE INDEX IF NOT EXISTS idx_study_materials_exam_id ON study_materials(exam_id);
