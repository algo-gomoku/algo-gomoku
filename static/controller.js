// 定义棋盘位置
board_info = {
    sx: 50,
    sy: 50,
    width: 400,
    height: 400,
}


// 获取代表本局棋的id。如果不存在，随机生成一个id。
var id = get_or_generate_id();

// 画棋盘
draw_chessboard(board_info.sx, board_info.sy, board_info.width, board_info.height);

// 定期获取对战信息
var info_url = '/chessboards/' + id + '/';
var interval_id = start_update_interval_ms(1000);

function start_update_interval_ms(interval_ms) {
    return setInterval(update, interval_ms);
}

// TODO: 重构掉这个难看的HACK
var player_info_painted = false;

function update() {
    $.get(info_url).success(function(data) {

        if (!data) {
            return;
        }

        // 画历史棋子
        var chessboard = data.chessboard;
        if (chessboard) {
            for (var i = 0; i < 19; i++) {
                for (var j = 0; j < 19; j++) {
                    if (chessboard[i][j] != ' ') {
                        draw_piece(i, j, chessboard[i][j]);
                    }
                }
            }
        }

        // 画当前棋子
        var next = data.next;
        if (next) {
            draw_piece(next.position.i, next.position.j, next.piece_char);
        }

        // 画玩家信息
        var players = data.players;
        if (players && !player_info_painted) {
            update_info(
                players[0].name, players[0].piece_char, players[0].used_time,
                players[1].name, players[1].piece_char, players[1].used_time
            );
            player_info_painted = true;
        }

        if (data.result != 'ongoing') {
            clearInterval(interval_id);
            draw_result(data.result);
        }
    });
}


function get_or_generate_id() {
    if (window.location.search) {
        var match = window.location.search.match(/\bid=(\d+)/);
        if (match) {
            var id = match[1];
            return id;
        }
    }

    var random_id = parseInt(Math.random() * 1000);
    window.location.search = 'id=' + random_id;
}


function draw_chessboard() {
    var context = get_context();

    sx = board_info.sx;
    sy = board_info.sy;
    width = board_info.width;
    height = board_info.height;

    context.rect(sx, sy, width, height);

    // 画棋盘网格
    context.beginPath();
    var unit_width = width / 19.0;
    var unit_height = height / 19.0;
    for (var i = 0; i < 20; i++) {
        context.moveTo(sx, sy + unit_height * i);
        context.lineTo(sx + width, sy + unit_height * i);
        context.moveTo(sx + unit_width * i, sy);
        context.lineTo(sx + unit_width * i, sy + height);
    }
    context.stroke();
}


function draw_piece(i, j, piece_char) {
    var context = get_context();

    var unit_width = board_info.width / 19.0;
    var unit_height = board_info.height / 19.0;

    context.beginPath();
    context.arc(board_info.sx + unit_width * j,
                board_info.sy + unit_width * i,
                unit_width/3.0, 0, Math.PI*2, true);
    context.fillStyle = piece_char === '●' ? "#FFF" : "#000";
    context.fill();
    context.stroke();
}


function update_info(name1, piece_char1, used_time1, name2, piece_char2, used_time2) {
    var context = get_context();

    context.font = "Bold 20px Arial";
    context.textAlign = "left";
    context.fillStyle = "#000";
    context.fillText("玩家1 (" + name1 + ")", 500, 100);
    context.fillText("棋子", 500, 130);
    context.fillText("总用时", 500, 160);
    context.fillText(used_time1, 580, 160);

    var unit_width = board_info.width / 19.0;
    var unit_height = board_info.height / 19.0;
    context.beginPath();
    context.arc(580 + unit_width/3.0/2, 130 - unit_height/3.0, unit_width/3.0, 0, Math.PI*2, true);
    context.fillStyle = piece_char1 === '●' ? "#FFF" : "#000";
    context.fill();
    context.stroke();

    context.font = "Bold 20px Arial";
    context.textAlign = "left";
    context.fillStyle = "#000";
    context.fillText("玩家2 (" + name2 + ")", 500, 220);
    context.fillText("棋子", 500, 250);
    context.fillText("总用时", 500, 280);
    context.fillText(used_time2, 580, 280);

    var unit_width = board_info.width / 19.0;
    var unit_height = board_info.height / 19.0;
    context.beginPath();
    context.arc(580 + unit_width/3.0/2, 250 - unit_height/3.0, unit_width/3.0, 0, Math.PI*2, true);
    context.fillStyle = piece_char2 === '●' ? "#FFF" : "#000";
    context.fill();
    context.stroke();
}


function draw_result(result_str) {
    context = get_context();
    context.font = "Bold 20px Arial";
    context.textAlign = "left";
    context.fillStyle = "#B00";
    context.fillText(result_str, 150, 250);
}


function get_context() {
    var game_canvas = document.getElementById('game-canvas');
    var context = game_canvas.getContext('2d');

    return context;
}
