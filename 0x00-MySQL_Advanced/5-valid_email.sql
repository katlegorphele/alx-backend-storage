-- Active: 1691578679906@@127.0.0.1@5432@hbtn_0d_tvshows

DELIMITER $

CREATE TRIGGER valid_email_trigger BEFORE UPDATE ON users 
FOR EACH ROW 
BEGIN
    IF NEW.email <> OLD.email THEN
        SET NEW.valid_email = 0;
    END IF;
END$

DELIMITER ;