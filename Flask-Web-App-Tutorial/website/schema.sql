-- Create User table
CREATE TABLE User (
    userid INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

-- Create Category table
CREATE TABLE Category (
    categoryID INT PRIMARY KEY AUTO_INCREMENT,
    userid INT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    FOREIGN KEY (userid) REFERENCES User(userid) ON DELETE CASCADE
);

-- Create Note table
CREATE TABLE Note (
    noteID INT PRIMARY KEY AUTO_INCREMENT,
    userid INT,
    categoryID INT,
    title VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (userid) REFERENCES User(userid) ON DELETE CASCADE,
    FOREIGN KEY (categoryID) REFERENCES Category(categoryID) ON DELETE SET NULL
);

--View to Get All Notes with User Information:
CREATE VIEW view_notes_with_user AS
SELECT n.noteID, n.userid, n.categoryID, n.title, n.content, n.created_at, n.updated_at,
       u.username AS user_username, u.email AS user_email,
       c.name AS category_name, c.description AS category_description
FROM Note n
JOIN User u ON n.userid = u.userid
LEFT JOIN Category c ON n.categoryID = c.categoryID;

--Stored Procedures:
--Procedure to Create a New Note:
DELIMITER //

CREATE PROCEDURE create_note_procedure(
    IN p_userid INT,
    IN p_categoryID INT,
    IN p_title VARCHAR(100),
    IN p_content TEXT
)
BEGIN
    INSERT INTO Note (userid, categoryID, title, content)
    VALUES (p_userid, p_categoryID, p_title, p_content);
END //

DELIMITER ;

--Procedure to Update a Note:
DELIMITER //

CREATE PROCEDURE update_note_procedure(
    IN p_noteID INT,
    IN p_title VARCHAR(100),
    IN p_content TEXT
)
BEGIN
    UPDATE Note
    SET title = p_title, content = p_content, updated_at = CURRENT_TIMESTAMP
    WHERE noteID = p_noteID;
END //

DELIMITER ;

--Procedure to Delete a Note:
DELIMITER //

CREATE PROCEDURE delete_note_procedure(
    IN p_noteID INT
)
BEGIN
    DELETE FROM Note WHERE noteID = p_noteID;
END //

DELIMITER ;

--Triggers:
--Trigger to Update updated_at on Note Update:
DELIMITER //

CREATE TRIGGER update_note_updated_at
BEFORE UPDATE ON Note
FOR EACH ROW
SET NEW.updated_at = CURRENT_TIMESTAMP;

DELIMITER ;
