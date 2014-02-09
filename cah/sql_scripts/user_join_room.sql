-- USER JOIN ROOM
-- TAKES INPUT user_id AND room_id

INSERT INTO `players` (`user_id`, `room_id`, `previous_player_id`, `status`, `joined`)
SELECT @user_id, @room_id, user_id, 'active', NOW() 
FROM `players`
WHERE room_id = @room_id
	AND user_id NOT IN
		(
			SELECT previous_player_id
			FROM players
			WHERE room_id = @room_id
		)