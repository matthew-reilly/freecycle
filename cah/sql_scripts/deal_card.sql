-- DEAL ONE CARD
-- TAKES INPUT user_id, room_id, card_type (black/white)

INSERT INTO `hands` (room_id, user_id, card_id, card_status)
SELECT @room_id, @user_id, card_id, 'dealt'
FROM `cards`
WHERE card_type = @card_type
	AND card_id NOT IN
	(
		SELECT card_id 
		FROM `hands` 
		WHERE room_id = @room_id
	)
ORDER BY RAND()
LIMIT 1