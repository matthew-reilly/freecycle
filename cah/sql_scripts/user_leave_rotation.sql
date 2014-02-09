-- PLAYER LEAVE ROTATION
-- TAKES INPUT user_id, room_id

UPDATE `players` 
SET `status` = 'inactive'
WHERE `user_id` = @user_id
	AND `room_id` = @room_id