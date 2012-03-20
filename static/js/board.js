DATA = {"turn_logs":[], "buildings": [{"owner": null, "worker": null, "class": "CastleBuilding", "repr": "Castle", "name": "Castle"}, {"owner": null, "worker": 'Blue', "class": "GateBuilding", "repr": "Gate", "name": "Gate"}, {"owner": 'Red', "worker": null, "class": "Building", "repr": "3", "name": "Trading Post"}, {"owner": null, "worker": null, "class": "GuildBuilding", "repr": "Prov", "name": "Merchant's Guild"}, {"owner": null, "worker": null, "class": "Building", "repr": "1C->RF", "name": "Joust Field"}, {"owner": null, "worker": null, "class": "StablesBuilding", "repr": "Stables", "name": "Stables"}, {"owner": null, "worker": null, "class": "InnBuilding", "repr": "Inn", "name": "Inn"}, {"owner": null, "worker": null, "class": "MarketBuilding", "repr": "R->4", "name": "Market"}, {"owner": null, "worker": null, "class": "Building", "repr": "S", "name": "Quarry"}, {"owner": null, "worker": null, "class": "CarpenterBuilding", "repr": "Carpenter", "name": "Carpenter"}, {"owner": null, "worker": null, "class": "Building", "repr": "W", "name": "Sawmill"}, {"owner": null, "worker": null, "class": "Building", "repr": "F/W", "name": "Forest"}, {"owner": null, "worker": null, "class": "Building", "repr": "F/C", "name": "Farm"}, {"owner": null, "worker": null, "class": "PeddlerBuilding", "repr": "2->R", "name": "Peddler"}, {"owner": null, "worker": null, "class": "CarpenterBuilding", "repr": "Carpenter", "name": "Carpenter"}, {"owner": null, "worker": null, "class": "NullBuilding", "repr": "", "name": "Null"}, {"owner": null, "worker": null, "class": "NullBuilding", "repr": "", "name": "Null"}, {"owner": null, "worker": null, "class": "NullBuilding", "repr": "", "name": "Null"}, {"owner": null, "worker": null, "class": "NullBuilding", "repr": "", "name": "Null"}, {"owner": null, "worker": null, "class": "NullBuilding", "repr": "", "name": "Null"}, {"owner": null, "worker": null, "class": "NullBuilding", "repr": "", "name": "Null"}, {"owner": null, "worker": null, "class": "NullBuilding", "repr": "", "name": "Null"}, {"owner": null, "worker": null, "class": "Building", "repr": "G", "name": "Gold Mine"}], "players": [{"name": "Blue", "favors": [-1, -1, -1, -1], "workers": 6, "section_batches": [0, 0, 0], "passed": false, "resources": {"stone": 0, "gold": 0, "food": 2, "money": 5, "cloth": 0, "wood": 1, "points": 0}}], "stables_order": [], "section": 0, "provost": 5, "bailiff": 5, "turn": 0, "step": 0, "pass_order": [], "phase": 0, "castle_order": []}
RESOURCES = ['food','wood','stone','cloth','gold']
TRACKS = [
    ["{P1}", "{P2}", "{P3}", "{P4}", "{P5}"],
    ["{$3}", "{$4}", "{$5}", "{$6}", "{$7}"],
    ["{F}", "{W}/{S}", "{C}", "{R}->{R2}", "{G}"],
    ["-", "Carp", "Mason", "Lawyer", "Arch"]
]
PLAYERS = ['Blue', 'Red', 'Green', 'Orange', 'Black']
GAME_ID = null
PLAYER_ID = null
DIALOG = null


IMAGES = {
    "{\\$b}": "/static/img/icons/money/blank.png",
    "{\\$1}": "/static/img/icons/money/1.png",
    "{\\$2}": "/static/img/icons/money/2.png",
    "{\\$3}": "/static/img/icons/money/3.png",
    "{\\$4}": "/static/img/icons/money/4.png",
    "{\\$5}": "/static/img/icons/money/5.png",
    "{\\$6}": "/static/img/icons/money/6.png",
    "{\\$7}": "/static/img/icons/money/7.png",
    "{Pb}": "/static/img/icons/points/blank.png",
    "{P1}": "/static/img/icons/points/1.png",
    "{P2}": "/static/img/icons/points/2.png",
    "{P3}": "/static/img/icons/points/3.png",
    "{P4}": "/static/img/icons/points/4.png",
    "{P5}": "/static/img/icons/points/5.png",
    "{P6}": "/static/img/icons/points/6.png",
    "{P7}": "/static/img/icons/points/7.png",
    "{P8}": "/static/img/icons/points/8.png",
    "{P9}": "/static/img/icons/points/9.png",
    "{P-1}": "/static/img/icons/points/-1.png",
    "{P-2}": "/static/img/icons/points/-2.png",
    "{P-3}": "/static/img/icons/points/-3.png",
    "{P-4}": "/static/img/icons/points/-4.png",
    "{F}": "/static/img/icons/cubes/food.png",
    "{F2}": "/static/img/icons/cubes/food2.png",
    "{W}": "/static/img/icons/cubes/wood.png",
    "{W2}": "/static/img/icons/cubes/wood2.png",
    "{S}": "/static/img/icons/cubes/stone.png",
    "{S2}": "/static/img/icons/cubes/stone2.png",
    "{C}": "/static/img/icons/cubes/cloth.png",
    "{C2}": "/static/img/icons/cubes/cloth2.png",
    "{C3}": "/static/img/icons/cubes/cloth3.png",
    "{G}": "/static/img/icons/cubes/gold.png",
    "{G2}": "/static/img/icons/cubes/gold2.png",
    "{R}": "/static/img/icons/cubes/any.png",
    "{R2}": "/static/img/icons/cubes/any2.png",
    "{R4}": "/static/img/icons/cubes/any4.png",
    "{Fs}": "/static/img/icons/cubes/small/food.png",
    "{Ws}": "/static/img/icons/cubes/small/wood.png",
    "{Ss}": "/static/img/icons/cubes/small/stone.png",
    "{Cs}": "/static/img/icons/cubes/small/cloth.png",
    "{Gs}": "/static/img/icons/cubes/small/gold.png"


}

function substitute_images(s){
    $.each(IMAGES, function(key, value){
        s = s.replace(new RegExp(key, 'g'), '<img class="icon" src="' + value + '">');
    });
    return s;
}

//alert(substitute_images('sdflskdajhfdskj{$1}ad'));

String.prototype.format = function() {
    var formatted = this;
    for (var i = 0; i < arguments.length; i++) {
        var regexp = new RegExp('\\{'+i+'\\}', 'gi');
        formatted = formatted.replace(regexp, arguments[i]);
    }
    return formatted;
};


function init_board(){
    $('.b').each(function(i){
        $(this).text('')
        $(this).append('<div class="span-1 bailiff">&nbsp;</div>');
        $(this).append('<div class="span-1 provost">&nbsp;</div>');
        $(this).append('<div class="span-1 owner last">&nbsp;</div>');
        $(this).append('<div class="span-3 worker last">&nbsp;</div>');
        //$(this).append('<div class="span-1 worker">&nbsp;</div>');
        //$(this).append('<div class="span-1 last">&nbsp;</div>');
        $(this).append('<div class="span-3 label last">&nbsp;</div>'); 
    });
    

    
    for(var i=0; i<TRACKS.length; i++){
        $('#favors').append('<tr id="t' + i + '"></tr>')
        $('#favors').children(':last').append('<td id="t'+i+'c-1">-</td>')
        for(var j=0; j<TRACKS[i].length; j++){
            $('#favors').children(':last').append('<td id="t'+i+'c'+j+'">'+substitute_images(TRACKS[i][j])+'</td>')
        }
    }
    
    for(var i=0; i<DATA.players.length; i++){
        $('#players').append('<tr id="p{0}">'.format(i))
        $('#players').children(':last').append('<td id="p{0}n">-</td>'.format(i))
        $('#players').children(':last').append('<td id="p{0}p">-</td>'.format(i))
        $('#players').children(':last').append('<td id="p{0}m">-</td>'.format(i))
        $('#players').children(':last').append('<td id="p{0}r">-</td>'.format(i))
    }
}

function update_board(){
    /*turn_order = ''
    for(var i=0; i<DATA.players.length; i++){
        turn_order += DATA.players[i].name + '<br>';
    }
    $('#order').html(turn_order)*/

    // Update logs

    $('#log').html('<ul></ul>')
    for(var i=0; i<DATA.turn_logs.length; i++){
        $('#log').find('ul').append('<li>' + substitute_images(DATA.turn_logs[i]) + '</li>')
        if(DATA.turn_logs[i].indexOf('Beginning') == 0){
            $('#log').find('li').last().css({'font-weight':'bold', 'margin-top':'20px'})
        }

    }
    
    // Update buildings
    
    for(var i=0; i<DATA.buildings.length; i++){
        update_building(i);
    }
    
    $('#b0 .worker').html('&nbsp;')
    for(var i=0; i<DATA.castle_order.length; i++){
        $('#b0 .worker').append(piece_image('worker', DATA.castle_order[i]))
    }
    
    $('#b5 .worker').html('&nbsp;')
    for(var i=0; i<DATA.stables_order.length; i++){
        $('#b5 .worker').append(piece_image('worker', DATA.stables_order[i]))
        
    }
    
    if(DATA.bailiff < 11)
        $('#b18 .bailiff').text('D')
    if(DATA.bailiff < 17)
        $('#b24 .bailiff').text('W')
    if(DATA.bailiff < 23)
        $('#b30 .bailiff').text('T')
    
    // Update player status markers
    
    for(var i=0; i<DATA.players.length; i++){
        update_player(i)
    }
    
    // Update bridge
    if(!DATA.pass_order){
        $('#bridge').text('No players have passed.')
    } else{
        $('#bridge').text('Passed: ' + DATA.pass_order)
    }
    
    // Update castle tracker
    $('#castle-tracker').text('')
    for(var i=0; i<DATA.players.length; i++){
        player = DATA.players[i]
        $('#castle-tracker').append(player.name + ': ' + player.section_batches[DATA.section])
    }
    
        
    // Create the red highlight
    
    $('.current').removeClass('current')
    if(DATA.phase == 2)
        $('#b' + (DATA.step + 0)).addClass('current')
    if(DATA.phase == 3)
        $('#bridge').addClass('current')
    if(DATA.phase == 4){
        $('#b' + (DATA.step + 7)).addClass('current')
    }
    if(DATA.phase == 5 || DATA.phase == 6)
        $('#b0').addClass('current')

    console.log(DATA.current_decision)

    if(DATA.over){
        show_game_over()
    }
    else if(DATA.current_decision){
        show_decision()
    }
}

function player_initial(player){
    if(player == 'Black')
        return 'K'
    return player[0]
}

function static_piece_image(type, display){
    if(!display)
        return '&nbsp;'
    return '<img src="/static/img/pieces/' + type + '.png">';
}

function piece_image(type, player){
    if(!player)
        return '&nbsp;'
    return '<img src="/static/img/pieces/' + type + player_initial(player) + '.png">';
}

function update_building(i){
    building = DATA.buildings[i]
    if(i == 6)
        building.owner = DATA.inn_player
    element = $('#b' + i)
    element.removeClass('neutral wood stone residence prestige null fixed')
    element.addClass(building.type)
    element.find('.label').html(substitute_images(building.repr))
    element.find('.provost').html(static_piece_image('provost', DATA.provost == i-7))
    element.find('.bailiff').html(static_piece_image('bailiff', DATA.bailiff == i-7))
    element.find('.owner').html(piece_image('house',building.owner))
    element.find('.worker').html(piece_image('worker',building.worker))
}

function update_player(i){
    player = DATA.players[i]
    $('#p{0}n'.format(i)).text(player.name)
    if(player.name == PLAYER)
        $('#p{0}n'.format(i)).css({'font-weight':'bold'})
    $('#p{0}p'.format(i)).html(substitute_images('{Pb}') + player.resources['points'])
    $('#p{0}m'.format(i)).html(substitute_images('{$b}') + player.resources['money'])
    resources = ' '
    for(var j in RESOURCES){
        resource = RESOURCES[j]
        if(player.resources[resource] > 0)
        {
            for(var k=0; k<player.resources[resource]; k++){
                resources += '{' + resource[0].toUpperCase() + 's}';
            }
            resources += ' '
        }
    }
    $('#p{0}r'.format(i)).html(substitute_images(resources))
    
    // Royal favor board
    $('.rf' + i).remove()
    for(var j=0; j<player.favors.length; j++){
        k = player.favors[j]
        element = $('#t'+j+'c'+k)
        element.append(piece_image('worker', player.name))
        element.children().last().attr('width', 5).addClass('rf'+i)
    }
}

function show_decision_wait(){
    var dialog = DIALOG.html('<div>' + DATA.current_decision.player + ' is making a decision... </div>')
    dialog.dialog({title:'Please wait', closeOnEscape:false});
    dialog.closest('.ui-dialog').find('.ui-dialog-titlebar-close').hide();
    DIALOG = dialog
}

function show_game_over(){
    var dialog = DIALOG.html('<div>The game is over.</div>')
    dialog.dialog({title:'Game Over!', closeOnEscape:false});
    dialog.closest('.ui-dialog').find('.ui-dialog-titlebar-close').hide();
    DIALOG = dialog
}

function show_decision(){
    DECISION = DATA.current_decision
    //if (DECISION.player != PLAYER){
    //    show_decision_wait()
    //}
    if(DATA.current_decision.cls == 'WorkerDecision'){
        show_worker_decision()
    } else if(DATA.current_decision.cls == 'ActionDecision' ||
              DATA.current_decision.cls == 'FavorDecision'){
        show_action_decision()
    } else if(DATA.current_decision.cls == 'FavorTrackDecision'){
        show_favor_track_decision()
    }

    $('.ui-dialog-titlebar').css({'background': DECISION.player});
    //DIALOG.dialog('enable');
    if (DECISION.player != PLAYER){
        DIALOG.find('.btn').addClass('disabled').unbind('click')
        DIALOG.dialog({title:'{0} is making a decision...'.format(DECISION.player)})
        //show_decision_wait()
    }

}


function show_action_decision(){
    var dialog = DIALOG.html('<div></div>')
    for(var i=0; i<DECISION.actions.length; i++){
        dialog.append('<div class="btn" i="'+i+'">');
        dialog.children().last().html(substitute_images(DECISION.actions[i].repr));
        dialog.children().last().click(button_clicked)
    }
    console.log(DECISION);
    var title = 'Select Action';
    if(DECISION.actions.length > 1 && DECISION.actions[1].class == 'BribeProvostAction')
        title = 'Do you want to bribe the provost?';
    dialog.dialog({title:title, closeOnEscape:false});
    dialog.closest('.ui-dialog').find('.ui-dialog-titlebar-close').hide();
    DIALOG = dialog

}

function show_worker_decision(){
    var dialog = DIALOG.html('<div></div>')
    dialog.append('Click a building or pass. <input type="button" class="btn right" i="0" value="Pass"><br>Workers left: {0}<br>Players passed: {1}'.format(DATA.players[PLAYER_ID].workers, DATA.pass_order.length))
    dialog.find('input').click(function(){
        $('.b').removeClass('available')
        submit_decision($(this).attr('i'))
    });
    for(var i=0; i<DECISION.buildings.length; i++){
        building = DECISION.buildings[i]
        if(building != null){
            $('#b' + building.i).addClass('available')
            $('#b' + building.i).attr('i', i)
        }
    }
    dialog.dialog({title:'Worker Placement', closeOnEscape:false, minHeight:50});
    dialog.closest('.ui-dialog').find('.ui-dialog-titlebar-close').hide();
    DIALOG = dialog
}

function show_favor_track_decision(){
    var dialog = DIALOG.html('<div></div>')
    for(var i=0; i<DECISION.tracks.length; i++){
        dialog.append('<div class="btn" i="'+i+'">')
        dialog.children().last().text(DECISION.tracks[i])
        dialog.children().last().click(button_clicked)
    }
    dialog.dialog({title:'Royal Favor', closeOnEscape:false});
    dialog.closest('.ui-dialog').find('.ui-dialog-titlebar-close').hide();
    DIALOG = dialog

}

function button_clicked(){
    submit_decision( $(this).attr('i') )
}

function submit_decision(i){
    $('.ui-dialog-content').text('Submitting... ' + i)
    //dialog = DIALOG
    //DIALOG = null
    $.post('submit', {'id':GAME_ID, 'i':i}, function(data){
        //dialog.dialog('close')
    });
}

function update_received(message){
    //if(DIALOG){
    //    DIALOG.dialog('close')
    //    DIALOG = null
    //}
    DATA = $.parseJSON(message)
    update_board()
    //show_decision()
}

function show_connect_dialog(){
    var dialog = $('<div></div>')
    dialog.append('<form class="form-inline"><label>Game ID:</label><input type="entry" class="span1" id="game-id" value="0"><label>Player:</label><input type="entry" class="span1" id="player" value="0">')
    dialog.append('<label class="checkbox">Create: <input type="checkbox" id="create"></label>')
    dialog.append('<br><input type="button" value="Connect"></form>');
    dialog.children('input[type="button"]').click(perform_connect)
    dialog.dialog({title:'Connect to Server', closeOnEscape:false});
    dialog.closest('.ui-dialog').find('.ui-dialog-titlebar-close').hide();
    DIALOG = dialog    
}

function perform_connect(){
    PLAYER_ID = $('#create').is(':checked') ? 0 : parseInt($('#player').val());
    PLAYER = PLAYERS[PLAYER_ID]
    GAME_ID = $('#game-id').attr('value')
    params = {'id':$('#game-id').attr('value'),
              'player':$('#player').attr('value'),
              'create':($('#create').is(':checked') ? '1' : '0')}
    $('.ui-dialog-content').text('Connecting... ' )
    //dialog = DIALOG
    //DIALOG = null
    $.getJSON('connect', params, function(data) {
        //dialog.dialog('close')
        DATA = data
        init_board()
        update_board()
        updater.update_received = update_received
        updater.id = GAME_ID
        updater.poll();
    });
}



$(document).ready(function(){
    setTimeout(show_connect_dialog, 1000);
    $('.b').click(function(){
        if($(this).hasClass('available')){
            $('.b').removeClass('available')
            submit_decision($(this).attr('i'))
        }
    })
    //DECISION = ACTION_DECISION
    //show_action_decision()
});