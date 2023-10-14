-- script that creates a stored procedure ComputeAverageWeightedScoreForUser 
-- that computes and store the average weighted score for a student.

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;

DELIMITER $

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN usr_id INT)
-- begin procedure calculations
BEGIN
    DECLARE weight_average FLOAT;
    DECLARE total_weight_for_user INT;
    
    SELECT SUM(weight) FROM corrections
    JOIN projects ON corrections.project_id = projects.id 
    WHERE corrections.user_id = usr_id INTO total_weight_for_user;

    SELECT (SUM(score * weight)) / total_weight_for_user FROM corrections 
    JOIN projects ON corrections.project_id = projects.id 
    WHERE corrections.user_id = usr_id INTO weight_average;
    UPDATE users 
    SET average_score = weight_average 
    WHERE id = usr_id;
END$

DELIMITER ;