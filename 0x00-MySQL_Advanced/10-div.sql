-- script that creates a function SafeDiv that divides (and returns) 
-- the second number or returns 0 if the second number is equal to 0.

DELIMITER $

CREATE FUNCTION SAFEDIV(a INT, b INT) 
RETURNS FLOAT DETERMINISTIC
BEGIN
	DECLARE result FLOAT DEFAULT 0;
	IF b = 0 THEN RETURN 0;
	END IF;
	SET result = (a * 1.0) / b;
	RETURN result;
	END$ 


DELIMITER ;