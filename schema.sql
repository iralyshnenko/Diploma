DROP DATABASE IF EXISTS attendance_journal;
CREATE DATABASE IF NOT EXISTS attendance_journal;

USE attendance_journal;

CREATE TABLE IF NOT EXISTS student_group (
    id SERIAL PRIMARY KEY,
    name VARCHAR(12) NOT NULL
);

CREATE TABLE IF NOT EXISTS teacher (
    id SERIAL PRIMARY KEY,
    login VARCHAR(32) NOT NULL,
    password VARCHAR(32) NOT NULL,
    fio VARCHAR(128) NOT NULL,
    UNIQUE(login)
);

CREATE TABLE IF NOT EXISTS student (
    id SERIAL PRIMARY KEY,
    fio VARCHAR(128) NOT NULL,
    student_group_id BIGINT UNSIGNED NOT NULL,
    FOREIGN KEY (student_group_id)
        REFERENCES student_group(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS subject (
    id SERIAL PRIMARY KEY,
    name VARCHAR(32) NOT NULL,
    teacher_id BIGINT UNSIGNED NOT NULL,
    FOREIGN KEY (teacher_id)
        REFERENCES teacher(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS score (
    id SERIAL PRIMARY KEY,
    international CHAR(1) NOT NULL,
    percentage SMALLINT UNSIGNED NOT NULL,
    student_id BIGINT UNSIGNED NOT NULL,
    subject_id BIGINT UNSIGNED NOT NULL,
    FOREIGN KEY (student_id)
        REFERENCES student(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (subject_id)
        REFERENCES subject(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS attendance (
    id SERIAL PRIMARY KEY,
    attendance_date DATE NOT NULL,
    student_id BIGINT UNSIGNED NOT NULL,
    subject_id BIGINT UNSIGNED NOT NULL,
    UNIQUE(attendance_date, student_id, subject_id),
    FOREIGN KEY (student_id)
        REFERENCES student(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (subject_id)
        REFERENCES subject(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE VIEW student_performance AS
SELECT student.*, attendance.attended_days, AVG(score.percentage) as performance
FROM student, score, (
    SELECT student_id, COUNT(*) as attended_days
    FROM attendance
    GROUP BY student_id
) as attendance
WHERE student.id = score.student_id AND student.id = attendance.student_id
GROUP BY student.id
ORDER BY attendance.attended_days DESC, performance DESC;