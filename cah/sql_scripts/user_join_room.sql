-- USER JOIN ROOM
-- TAKES INPUT user_id AND room_id

INSERT INTO `players` (`user_id`, `room_id`, `previous_player_id`, `status`, `joined`)
VALUES
(
	@user_id, 
	@room_id, 
	(
		select user_id
		from players 
		where room_id = @room_id 
			and user_id not in 
				(
					select previous_player_id 
					from players 
					where room_id = @room_id
				)
	),
	'active',
	NOW()
)