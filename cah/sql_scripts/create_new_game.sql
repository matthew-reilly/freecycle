-- CREATE NEW GAME
-- TAKES INPUT user_id, room_name (optional), room_password (optional)

INSERT INTO `rooms` (`id`, `room_name`, `room_password`, `user_id`, `room_status`,`create_time`)
VALUES
(NULL, @room_name, @room_password, @user_id, 'init', NOW());

-- IF NONE PROVIDED, UPDATE ROOM NAME TO ROOM(id)
UPDATE `rooms` 
SET `room_name` = concat('room',id) 
WHERE id = last_insert_id() 
	AND `room_name` = '';
	
-- INSERT ROOM OWNER AS FIRST PLAYER
INSERT INTO `players` (`user_id`, `room_id`, `previous_player_id`, `status`, `joined`)
VALUES
(@user_id, last_insert_id(), -1, 'active', NOW());