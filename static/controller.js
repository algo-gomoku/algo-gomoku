board_info = {
    sx: 50,
    sy: 50,
    width: 400,
    height: 400,
}
draw_chessboard(board_info.sx, board_info.sy, board_info.width, board_info.height);
draw_piece(1, 1, '●');
update_info('name1', '○', 3.2, 'name2', '●', 4.2);

function get_context() {
    var game_canvas = document.getElementById('game-canvas');
    var context = game_canvas.getContext('2d');

    return context;
}

function draw_chessboard(sx, sy, width, height) {
    var context = get_context();

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

function draw_piece(x, y, piece_char) {
    var context = get_context();

    var unit_width = board_info.width / 19.0;
    var unit_height = board_info.height / 19.0;

    context.beginPath();
    context.arc(board_info.sx + unit_width * (x - 1),
                board_info.sy + unit_width * (y - 1),
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
