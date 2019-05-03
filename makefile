
# temporary debug function for faster testing
debug:
	python3 demo.py

replay:
	python3 replay_manager.py

clean-logs:
	-rm -f dqn_eval_logs/*

clean-replays:
	-rm replays/*
