CREATE DATABASE IF NOT EXISTS ifupan;

USE ifupan;

CREATE TABLE IF NOT EXISTS text_analysis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    input_text TEXT NOT NULL,
    prompt_type VARCHAR(50) NOT NULL,
    result TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS mind_map (
    id INT AUTO_INCREMENT PRIMARY KEY,
    input_text TEXT NOT NULL,
    prompt_type VARCHAR(50) NOT NULL,
    mind_map_file VARCHAR(255),
    pdf_file VARCHAR(255),
    md_file VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS speech_to_text (
    id INT AUTO_INCREMENT PRIMARY KEY,
    audio_file VARCHAR(255) NOT NULL,
    prompt_type VARCHAR(50) NOT NULL,
    transcribed_text TEXT NOT NULL,
    result TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS prompts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Insert sample data into text_analysis table
INSERT INTO text_analysis (input_text, prompt_type, result) VALUES
('今天我完成了一个重要的项目', 'diary', '{"analysis": "您今天完成了一个重要项目，这是一个值得庆祝的成就。建议您反思项目过程中的经验教训，并考虑如何将这些经验应用到未来的工作中。"}'),
('学习了新的编程语言Python', 'study', '{"analysis": "学习新的编程语言是提升技能的好方法。建议您通过实践项目来巩固所学知识，并探索Python在您工作领域的应用。"}'),
('团队会议讨论了新产品launch计划', 'meeting', '{"analysis": "新产品launch是一个重要的里程碑。确保团队成员都清楚自己的职责，并建立定期的进度检查机制。考虑可能的风险并制定应对策略。"}');

-- Insert sample data into mind_map table
INSERT INTO mind_map (input_text, prompt_type, mind_map_file, pdf_file, md_file) VALUES
('项目管理流程', 'study', '/files/mindmaps/project_management.png', '/files/pdfs/project_management.pdf', '/files/markdown/project_management.md'),
('周末旅行计划', 'diary', '/files/mindmaps/weekend_trip.png', '/files/pdfs/weekend_trip.pdf', '/files/markdown/weekend_trip.md'),
('产品发布会议纪要', 'meeting', '/files/mindmaps/product_launch.png', '/files/pdfs/product_launch.pdf', '/files/markdown/product_launch.md');

-- Insert sample data into speech_to_text table
INSERT INTO speech_to_text (audio_file, prompt_type, transcribed_text, result) VALUES
('/audio/meeting_01.mp3', 'meeting', '我们需要在下周五之前完成这个项目的初步设计', '{"analysis": "项目有明确的截止日期，建议立即开始任务分配和进度跟踪。考虑使用项目管理工具来协调团队工作。"}'),
('/audio/diary_01.mp3', 'diary', '今天是我入职新公司的第一天，感觉很兴奋但也有些紧张', '{"analysis": "新的开始总是充满机遇和挑战。建议您积极融入新环境，主动了解公司文化和工作流程。记录下您的观察和感受，这将帮助您更好地适应和成长。"}'),
('/audio/study_01.mp3', 'study', '我正在学习机器学习的基础知识，感觉概念有些抽象', '{"analysis": "机器学习确实有一些抽象的概念。建议您结合实际案例来理解这些概念，可以尝试一些小型项目来实践所学知识。同时，寻找学习伙伴或加入相关社区以帮助您更好地理解和应用这些知识。"}');

-- Insert initial prompts
INSERT INTO prompts (code, name, content) VALUES
('diary', '日记复盘', '日记复盘的提示语...'),
('study', '学习复盘', '# Role: 自动化复盘助手 

## Background: 你是一位专业的复盘分析师，擅长使用STAR、KISS和PDCA模型进行全面的复盘分析。你的任务是帮助用户对事件或项目进行深入、系统的复盘，提升用户的认知水平，并制定改进计划。 

...

## Initialization: 您好，我是您的自动化复盘助手。请描述您想要复盘的事件或项目，包括背景、目标、行动和结果。我会帮您进行全面的复盘分析。'),
('meeting', '会议复盘', '请对以下内容进行全面的复盘分析。包括但不限于：
    1. 主要观点和关键信息
    2. 优点和成功之处
    3. 存在的问题或可改进的地方
    4. 未来的行动建议或改进方向

    请提供一个结构化的复盘分析报告，用markdown代码块展示，只需要markdown代码块。');