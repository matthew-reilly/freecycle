-- PLAYER REJOIN ROTATION
-- TAKES INPUT user_id, room_id

UPDATE `players` 
SET `status` = 'active'
WHERE `user_id` = @user_id
	AND `room_id` = @room_id