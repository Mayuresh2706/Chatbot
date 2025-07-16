CREATE DATABASE AI_Chatbot  
CHARACTER SET utf8mb4  
COLLATE utf8mb4_unicode_ci;


USE AI_Chatbot;

CREATE TABLE Training_Data(
faq_no INT auto_increment PRIMARY KEY,
question TEXT NOT NULL,
answer TEXT NOT NULL
);

