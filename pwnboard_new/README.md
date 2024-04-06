1. generate the board
2. User other script to transform json
3. POST the board to pwnboard

curl -k -X POST -H "Content-Type: application/json" -d @./ists-board.json https://pwnboard.cdn-gstatic.org/pwn/board
