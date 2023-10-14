-- a trigger scripts that executes when a new row is inserted into the table

DELIMITER $

CREATE TRIGGER decrease_trigger AFTER INSERT ON orders 
FOR EACH ROW 
BEGIN
	UPDATE items
	SET
	    quantity = quantity - NEW.number
	WHERE name = NEW.item_name;
	END;
$

DELIMITER ;