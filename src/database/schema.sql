-- LinkedIn Automator Database Schema

CREATE TABLE if not exists projects(
    id integer primary key AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    tech_stack TEXT,
    github_url TEXT,
    key_learnings TEXT,
    last_posted_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Posts table to track uploaded posts

CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic TEXT NOT NULL,
    content TEXT NOT NULL,
    post_format TEXT CHECK(post_format IN (
        'confession', 'hot_take', 'teardown', 
        'question_answer', 'story'
    )),
    image_type TEXT CHECK(image_type IN (
        'excalidraw', 'ai_generated', 'quote_card', 
        'code_screenshot', 'none'
    )),
    image_path TEXT,
    source_url TEXT,
    status TEXT DEFAULT 'draft' CHECK(status IN (
        'draft', 'approved', 'published', 'rejected'
    )),
    project_id INTEGER,
    scheduled_for TIMESTAMP,
    published_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id)
);

CREATE TABLE IF NOT EXISTS topics_covered (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic TEXT NOT NULL,
    category TEXT CHECK(category IN (
        'data_engineering', 'data_analytics', 
        'ai_ml', 'portfolio', 'career', 'tools'
    )),
    post_id INTEGER,
    covered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES posts(id)
);




CREATE TABLE IF NOT EXISTS voice_samples (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    source TEXT DEFAULT 'manual',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

