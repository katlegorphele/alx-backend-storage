-- script that creates a stored procedure ComputeAverageWeightedScoreForUsers that 
-- computes and store the average weighted score for all students.

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;

DELIMITER $

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
-- begin procedure calculations
BEGIN
    DECLARE usr_id INT;
    DECLARE weight_average FLOAT;
    DECLARE total_weight_for_user INT;
    
    DECLARE done INT DEFAULT FALSE;
    DECLARE cur CURSOR FOR SELECT id FROM users;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN cur;

    read_loop: LOOP
        FETCH cur INTO usr_id;
        IF done THEN
            LEAVE read_loop;
        END IF;

        SELECT SUM(weight) FROM corrections
        JOIN projects ON corrections.project_id = projects.id 
        WHERE corrections.user_id = usr_id INTO total_weight_for_user;

        SELECT (SUM(score * weight)) / total_weight_for_user FROM corrections 
        JOIN projects ON corrections.project_id = projects.id 
        WHERE corrections.user_id = usr_id INTO weight_average;
        UPDATE users 
        SET average_score = weight_average 
        WHERE id = usr_id;
    END LOOP;

    CLOSE cur;
END$

DELIMITER ;