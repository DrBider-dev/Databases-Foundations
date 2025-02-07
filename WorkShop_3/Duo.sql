CREATE DATABASE IF NOT EXISTS duolingo;
USE duolingo;

-- Table User
CREATE TABLE IF NOT EXISTS User (
	Id INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(50) NOT NULL,
    Nickname VARCHAR(50) NOT NULL,
    joinDate DATE,
    Division INT NOT NULL,
    timesInTop INT,
    Email VARCHAR(75) NOT NULL UNIQUE,
    Password VARCHAR(20) NOT NULL,
    Courses VARCHAR(50) NOT NULL,
    Achievements VARCHAR(50),
    Followed INT NOT NULL,
    Followers INT NOT NULL,
    gemsNumber INT NOT NULL,
    livesNumber INT NOT NULL,
    boostersNumber INT NOT NULL,
    isPremium BOOLEAN NOT NULL
);

-- Table Course
CREATE TABLE IF NOT EXISTS Course (
    Id INT PRIMARY KEY AUTO_INCREMENT,
    Language VARCHAR(60) NOT NULL,
    Stages TEXT NOT NULL,
    Sounds TEXT
);


-- Table Stage
CREATE TABLE IF NOT EXISTS Stage (
    Id INT PRIMARY KEY AUTO_INCREMENT,
    Sections INT NOT NULL,
    Level VARCHAR(2) NOT NULL,
    minimumRequirements VARCHAR(75) NOT NULL
);

-- Table Section
CREATE TABLE IF NOT EXISTS Section (
    Id INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(50) NOT NULL,
    Lessons VARCHAR(50) NOT NULL,
    Guide VARCHAR(50) NOT NULL
);

-- Table Lesson
CREATE TABLE IF NOT EXISTS Lesson (
    Id INT PRIMARY KEY AUTO_INCREMENT,
    Type VARCHAR(11) NOT NULL,
    QuestionsNumber INT NOT NULL,
    EXP INT NOT NULL,
    Time TIME NOT NULL,
    Accuracy FLOAT NOT NULL
);

-- Table Question
CREATE TABLE IF NOT EXISTS Question (
    Id INT PRIMARY KEY AUTO_INCREMENT,
    Content VARCHAR(300) NOT NULL,
    Answer VARCHAR(300) NOT NULL,
    isCorrect BOOLEAN NOT NULL,
    Type VARCHAR(11) NOT NULL
);

-- Table Division
CREATE TABLE IF NOT EXISTS Division (
    Id INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(20) NOT NULL,
    climbingZone INT NOT NULL,
    descentZone INT NOT NULL,
    stayArea INT NOT NULL,
    Users INT NOT NULL
);

-- Table Challenges
CREATE TABLE IF NOT EXISTS Challenges (
    Id INT PRIMARY KEY AUTO_INCREMENT,
    Description VARCHAR(300) NOT NULL,
    Progress INT NOT NULL,
    Goal INT NOT NULL,
    Reward INT NOT NULL
);

-- Table Boosters
CREATE TABLE IF NOT EXISTS Boosters (
    Id INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(25) NOT NULL,
    Cost INT NOT NULL,
    Benefit  NOT NULL,
    maxNumber INT NOT NULL
);

-- Table Achievement
CREATE TABLE IF NOT EXISTS Achievement (
    Id INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(25) NOT NULL,
    Progress INT NOT NULL,
    Goal VARCHAR(50) NOT NULL
);